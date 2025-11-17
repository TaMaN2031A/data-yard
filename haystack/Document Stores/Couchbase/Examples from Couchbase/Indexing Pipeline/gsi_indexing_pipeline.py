import json
import logging
import os
import zipfile
from datetime import timedelta
from io import BytesIO
from pathlib import Path

import requests
from couchbase.n1ql import QueryScanConsistency
from haystack import Pipeline
from haystack.components.converters import TextFileToDocument
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.utils import Secret

from couchbase_haystack import (
    CouchbasePasswordAuthenticator,
    CouchbaseQueryDocumentStore,
    CouchbaseQueryOptions,
    QueryVectorSearchType
)

logger = logging.getLogger(__name__)


def fetch_archive_from_http(url: str, output_dir: str):
    if Path(output_dir).is_dir():
        logger.warn(f"'{output_dir}' directory already exists. Skipping data download")
        return

    with requests.get(url, timeout=10, stream=True) as r:
        with zipfile.ZipFile(BytesIO(r.content)) as zf:
            zf.extractall(output_dir)

index_name = "haystack_index_name"
docs_dir = "data/docs"
fetch_archive_from_http(
    url="https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt6.zip",
    output_dir=docs_dir
)

document_store = CouchbaseQueryDocumentStore(
    cluster_connection_string=Secret.from_env_var("CB_CONNECTION_STRING"),
    authenticator=CouchbasePasswordAuthenticator(
        username=Secret.from_env_var("CB_USERNAME"),
        password=Secret.from_env_var("CB_PASSWORD"),
    ),
    bucket="haystack_bucket_name",
    scope="_default",
    collection="_default",
    search_type=QueryVectorSearchType.ANN,
    similarity="L2",
    nprobes=10,
    query_options=CouchbaseQueryOptions(timeout=timedelta(seconds=300), scan_consistency=QueryScanConsistency.REQUEST_PLUS)
)

p = Pipeline()
p.add_component("text_file_converter", TextFileToDocument())
p.add_component("cleaner", DocumentCleaner())
p.add_component("splitter", DocumentSplitter(split_by="sentence", split_length=250, split_overlap=30))
p.add_component("embedder", SentenceTransformersDocumentEmbedder())
p.add_component("writer", DocumentWriter(document_store=document_store))

p.connect("text_file_converter.documents", "cleaner.documents")
p.connect("cleaner.documents", "splitter.documents")
p.connect("splitter.documents", "embedder.documents")
p.connect("embedder.documents", "writer.documents")

file_paths = [docs_dir / Path(name) for name in os.listdir(docs_dir)]
result = p.run({"text_file_converter": {"sources": file_paths}})

cfg = {
    "dimension": 384,
    "train_list": 500,
    "description": "IVF,PQ32x8",
    "similarity": "L2",
}

document_store.scope.query(f"Create Index {index_name} ON _default (embedding vector) Using GSI WITH {json.dumps(cfg)}")

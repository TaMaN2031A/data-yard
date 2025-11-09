from haystack import Pipeline
from haystack.core.serialization import DeserializationCallbacks
from typing import Type, Dict, Any

pipeline_yml = """
components:
    cleaner:
        init_parameters:
            remove_empty_lines: true
            remove_extra_whitespaces: true
            remove_regex: null
            remove_repeated_substrings: false
            remove_substrings: null
        type:
            haystack.components.preprocessors.document_cleaner.DocumentCleaner
    converter:
        init_parameters:
            encoding: utf-8
        type:
            haystack.components.converters.txt.TextFileToDocument
connections:
- receiver: cleaner.documents
  sender: converter.documents
max_loops_allowed: 100
metadata: {}
"""

def component_pre_init_callback(component_name: str, component_cls: Type,
                                init_params: Dict[str, Any]):
    if component_name == "cleaner":
        assert "DocumentCleaner" in component_cls.__name__
        init_params["remove_empty_lines"] = False
        print("Modified 'remove_empty_lines' to False in 'cleaner' component")
    else:
        print(f"Not modifying component {component_name} of class {component_cls}")

pipe = Pipeline.loads(pipeline_yml, callbacks=DeserializationCallbacks(component_pre_init_callback))
print(pipe.to_dict())
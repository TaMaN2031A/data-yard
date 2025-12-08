import os
from getpass import getpass
from typing import List

from haystack import logging, Document, Pipeline
from haystack.components.agents import Agent
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from haystack.tools.from_function import tool
from haystack.components.generators.chat import HuggingFaceAPIChatGenerator
from haystack.utils import Secret
from haystack.utils.hf import HFGenerationAPIType

logger = logging.getLogger(__name__)


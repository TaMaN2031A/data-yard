import logging
from haystack import tracing
from haystack.tracing.logging_tracer import LoggingTracer

logging.basicConfig(format='%(levelname)s - %(name)s -  %(message)s', level=logging.WARNING)
logging.getLogger('haystack').setLevel(logging.DEBUG)

tracing.tracer.is_tracing_enabled = True
tracing.enable_tracing(
    LoggingTracer(
        tags_color_strings={
            "haystack.component.input": "\x1b[1;31m", "haystack.component.name": "\x1b[1;34m"
        }
    )
)
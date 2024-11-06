import time
import logging
from random import randint

from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from prometheus_client import Counter, Histogram, start_http_server

# Set up logging
logging.basicConfig(
    handlers=[
        logging.FileHandler('/app/logs/dummy_data_generator.log'),
        logging.StreamHandler()  # Keep console logging as well
    ],
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set up tracing
resource = Resource(attributes={
    "service.name": "dummy-data-generator",
    "service.version": "1.0.0",
    "deployment.environment": "demo"
})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Configure trace exporter and add a span processor
trace_exporter = OTLPSpanExporter(
    endpoint="otel-collector:4317",  # Remove http:// as it's gRPC
    insecure=True
)
span_processor = BatchSpanProcessor(trace_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Set up metrics with the reader included at initialization
metric_exporter = OTLPMetricExporter(
    endpoint="otel-collector:4317",  # Remove http:// as it's gRPC
    insecure=True
)
metric_reader = PeriodicExportingMetricReader(exporter=metric_exporter)
metrics_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(metrics_provider)
meter = metrics.get_meter(__name__)

# Prometheus Metrics
request_count = Counter("request_count", "Number of requests processed")
processing_time = Histogram("processing_time", "Processing time in seconds")

# Start Prometheus server
start_http_server(8800)

def simulate_log():
    # Simulate log messages
    log_messages = [
        "User logged in",
        "User logged out",
        "Transaction completed",
        "Error processing request",
        "Request timed out"
    ]
    message = log_messages[randint(0, len(log_messages) - 1)]
    logger.info(message)

def simulate_trace():
    # Simulate trace with multiple spans
    with tracer.start_as_current_span("parent-operation") as parent_span:
        parent_span.set_attribute("operation.status", "started")
        parent_span.set_attribute("operation.type", "parent")
        time.sleep(0.1)

        with tracer.start_as_current_span("child-operation-1") as child_span1:
            child_span1.set_attribute("operation.detail", "processing step 1")
            child_span1.set_attribute("operation.type", "child")
            child_span1.set_attribute("step.number", 1)
            time.sleep(randint(1, 3) * 0.1)

        with tracer.start_as_current_span("child-operation-2") as child_span2:
            child_span2.set_attribute("operation.detail", "processing step 2")
            child_span2.set_attribute("operation.type", "child")
            child_span2.set_attribute("step.number", 2)
            time.sleep(randint(1, 3) * 0.1)

def simulate_metrics():
    # Simulate metrics for request count and processing time
    request_count.inc()
    duration = randint(1, 5) * 0.1
    processing_time.observe(duration)

def main():
    try:
        while True:
            simulate_log()
            simulate_trace()
            simulate_metrics()
            time.sleep(1)  # Delay between iterations
    except KeyboardInterrupt:
        print("Stopping simulation")

if __name__ == "__main__":
    main()

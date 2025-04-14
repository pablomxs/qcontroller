# This module is provided as an example of how we can easily integrate
# OpenTelemetry into our API to send telemetry data to an observability platform
# (in this case, we are sending it to New Relic but it can be any other platform
# that supports OpenTelemetry).

import os
import logging
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import set_meter_provider
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

logger = logging.getLogger(__name__)


def setup_otel(app):
    """
    Initializes OpenTelemetry for the FastAPI application.
    """
    load_dotenv()
    logger.info("Setting up OpenTelemetry...")
    setup_tracing(app)
    setup_metrics()
    setup_logging()

def setup_tracing(app):
    """
    Initializes OpenTelemetry for tracing.
    """
    service_name = os.getenv("OTEL_SERVICE_NAME")
    resource = Resource(attributes={
        SERVICE_NAME: service_name
    })
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)
    span_exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"),
        headers=os.getenv("OTEL_EXPORTER_OTLP_HEADERS")
    )
    span_processor = BatchSpanProcessor(span_exporter)
    tracer_provider.add_span_processor(span_processor)
    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()
    logger.info(f"OpenTelemetry tracing initialized for service name: {service_name}")

def setup_metrics():
    """
    Initializes OpenTelemetry for metrics.
    """
    service_name = os.getenv("OTEL_SERVICE_NAME")
    resource = Resource(attributes={
        SERVICE_NAME: service_name
    })
    metric_exporter = OTLPMetricExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"),
        headers=os.getenv("OTEL_EXPORTER_OTLP_HEADERS")
    )
    reader = PeriodicExportingMetricReader(metric_exporter)
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    set_meter_provider(provider)
    logger.info(f"OpenTelemetry metrics initialized for service name: {service_name}")

def setup_logging():
    """
    Initializes OpenTelemetry for logging.
    """
    log_exporter = OTLPLogExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"),
        headers=os.getenv("OTEL_EXPORTER_OTLP_HEADERS")
    )
    log_provider = LoggerProvider()
    log_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    set_logger_provider(log_provider)
    log_handler = LoggingHandler(level=logging.INFO)
    logging.getLogger().addHandler(log_handler)
    logger.info("OpenTelemetry logging initialized")

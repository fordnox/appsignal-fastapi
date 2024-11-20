import os
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Get the OTLP endpoint from the environment variable
OTLP_ENDPOINT = os.getenv("OTLP_ENDPOINT")  # Default to localhost

# Initialize tracer provider and OTLP exporter
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Set up the OTLP exporter
otlp_exporter = OTLPSpanExporter(endpoint=OTLP_ENDPOINT, insecure=True)  # Use insecure=True if no TLS
span_processor = SimpleSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Create FastAPI app
app = FastAPI()

# Instrument the FastAPI app
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
async def root():
    with tracer.start_as_current_span("root_span"):
        return {"message": "Hello, OpenTelemetry with FastAPI and OTLP!"}

@app.get("/greet/{name}")
async def greet(name: str):
    with tracer.start_as_current_span("greet_span"):
        return {"message": f"Hello, {name}!"}

@app.get("/error")
async def error_route():
    with tracer.start_as_current_span("error_span"):
        raise ValueError("An example error!")

# Run the app with: uvicorn app:app --reload

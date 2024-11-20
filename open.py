from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Initialize tracer provider and exporter
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Add a ConsoleSpanExporter to export traces to the console
span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# Create FastAPI app
app = FastAPI()

# Instrument the FastAPI app
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
async def root():
    with tracer.start_as_current_span("root_span"):
        return {"message": "Hello, OpenTelemetry with FastAPI!"}

@app.get("/greet/{name}")
async def greet(name: str):
    with tracer.start_as_current_span("greet_span"):
        return {"message": f"Hello, {name}!"}

@app.get("/error")
async def error_route():
    with tracer.start_as_current_span("error_span"):
        raise ValueError("An example error!")

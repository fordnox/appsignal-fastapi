# app.py
import appsignal
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

appsignal.start()

app = FastAPI()

# ... your app's code goes here ...

FastAPIInstrumentor().instrument_app(app)


@app.get("/")
async def read_item():
    return {"item_id": "ok"}


@app.get("/bug")
async def raise_some_bugs():
    raise Exception("This is a test error")

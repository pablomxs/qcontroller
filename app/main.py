from fastapi import FastAPI
from app.routes_v1 import router
#from app.otel import setup_otel

app = FastAPI(title="QController API",
              version="1.0.0"
)

# Setup OpenTelemetry. This is given as an example of how we can easily integrate
# OpenTelemetry into our API to send telemetry data to an observability platform
# (see app/otel.py for more details).
#setup_otel(app)

app.include_router(router)

from fastapi import FastAPI
from app.endpoints.v1.api_key_auth import router as router_api_key
from app.endpoints.v1.activities import router as router_activities
from app.endpoints.v1.buildings import router as router_buildings
from app.endpoints.v1.organizations import router as router_organizations


app = FastAPI()

app.include_router(router_api_key)
app.include_router(router_activities)
app.include_router(router_buildings)
app.include_router(router_organizations)
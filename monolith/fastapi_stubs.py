from random import random
from typing import Optional

from fastapi import FastAPI, Query, HTTPException

from model import OrderData, ExecuterProfile, ZoneData

app = FastAPI()


@app.get("/order-data")
async def get_order_data(id: Optional[str] = Query(None, description="An optional ID parameter")):
    if id is None:
        raise HTTPException(status_code=400, detail="ID parameter is required and cannot be empty.")

    return OrderData(id, 'some-user-id', 'your-favorite-zone', 100.0)


@app.get("/zone-data")
async def get_zone_data(id: Optional[str] = Query(None, description="An optional ID parameter")):
    if id is None:
        raise HTTPException(status_code=400, detail="ID parameter is required and cannot be empty.")

    return ZoneData(id, 2.0, 'Fancy zone name')


@app.get("/executer-profile")
async def get_executer_profile(id: Optional[str] = Query(None, description="An optional ID parameter")):
    if id is None:
        raise HTTPException(status_code=400, detail="ID parameter is required and cannot be empty.")

    return ExecuterProfile(id, ['top-coin-expert'], 8.5)


@app.get("/toll-roads")
async def get_toll_roads(zone_display_name: Optional[str] = Query(None, description="An optional ID parameter")):
    bonus = 50 if random() > 0.1 else 0
    return {'bonus_amount': bonus}


@app.get("/configs")
async def get_configs():
    return {'coin_coeff_settings': {'maximum': '3', 'fallback': '1'}}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=3629, log_level='info')

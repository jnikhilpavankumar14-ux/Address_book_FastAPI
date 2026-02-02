# Address Book API

## What it does
- Create, update and delete addresses
- Each address has label, latitude, longitude
- Data saved in SQLite
- Input validated (lat -90 to 90, lon -180 to 180)
- Get addresses within X km of a point (GET /addresses/nearby)
- No GUI, use Swagger at /docs

## How to run
- Python 3 required
- Clone or download code, open terminal in project folder
- Create venv: python -m venv .venv
- Activate: Windows use .venv\Scripts\activate, Linux/Mac use source .venv/bin/activate
- Install: pip install -r requirements.txt
- Start: uvicorn app.main:app --reload
- Open browser at http://127.0.0.1:8000/docs to try the API

## Endpoints
- GET /addresses - list (skip, limit optional)
- GET /addresses/nearby - within distance (query: latitude, longitude, distance_km)
- GET /addresses/{id} - get one
- POST /addresses - create (body: label, latitude, longitude)
- PATCH /addresses/{id} - update
- DELETE /addresses/{id} - delete

## Project structure
- app/main.py - app and routes
- app/config.py - DB path
- app/database.py - SQLAlchemy
- app/models.py - Address table
- app/schemas.py - Pydantic
- app/routers/addresses.py - endpoints
- app/utils/distance.py - haversine
- requirements.txt

## Libraries
- FastAPI, uvicorn, SQLAlchemy, Pydantic

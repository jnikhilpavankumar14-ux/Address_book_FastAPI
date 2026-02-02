from datetime import datetime
from pydantic import BaseModel, Field

LATITUDE_RANGE = (-90.0, 90.0)
LONGITUDE_RANGE = (-180.0, 180.0)


class AddressBase(BaseModel):
    label: str = Field(..., min_length=1, max_length=255)
    latitude: float = Field(..., ge=LATITUDE_RANGE[0], le=LATITUDE_RANGE[1])
    longitude: float = Field(..., ge=LONGITUDE_RANGE[0], le=LONGITUDE_RANGE[1])


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    label: str | None = Field(None, min_length=1, max_length=255)
    latitude: float | None = Field(None, ge=LATITUDE_RANGE[0], le=LATITUDE_RANGE[1])
    longitude: float | None = Field(None, ge=LONGITUDE_RANGE[0], le=LONGITUDE_RANGE[1])


class AddressResponse(AddressBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AddressNearbyQuery(BaseModel):
    latitude: float = Field(..., ge=LATITUDE_RANGE[0], le=LATITUDE_RANGE[1])
    longitude: float = Field(..., ge=LONGITUDE_RANGE[0], le=LONGITUDE_RANGE[1])
    distance_km: float = Field(..., gt=0)

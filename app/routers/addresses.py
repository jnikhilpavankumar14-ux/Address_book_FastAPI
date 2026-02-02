import logging
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Address
from app.schemas import AddressCreate, AddressUpdate, AddressResponse
from app.utils.distance import haversine_km

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/addresses", tags=["addresses"])

DEFAULT_SKIP = 0
DEFAULT_LIMIT = 100
MAX_LIMIT = 1000


def get_address_or_404(address_id: int, db: Session) -> Address:
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with id {address_id} not found"
        )
    return address


@router.get("", response_model=list[AddressResponse])
def list_addresses(
    skip: int = Query(DEFAULT_SKIP, ge=0),
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
    db: Session = Depends(get_db),
) -> list[AddressResponse]:
    addresses = db.query(Address).order_by(Address.id).offset(skip).limit(limit).all()
    return addresses


@router.get("/nearby", response_model=list[AddressResponse])
def get_addresses_nearby(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    distance_km: float = Query(..., gt=0),
    db: Session = Depends(get_db),
) -> list[AddressResponse]:
    addresses = db.query(Address).all()
    within = [
        a for a in addresses
        if haversine_km(latitude, longitude, a.latitude, a.longitude) <= distance_km
    ]
    return within


@router.get("/{address_id}", response_model=AddressResponse)
def get_address(address_id: int, db: Session = Depends(get_db)) -> AddressResponse:
    return get_address_or_404(address_id, db)


@router.post("", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(body: AddressCreate, db: Session = Depends(get_db)) -> AddressResponse:
    try:
        address = Address(
            label=body.label,
            latitude=body.latitude,
            longitude=body.longitude,
        )
        db.add(address)
        db.commit()
        db.refresh(address)
        logger.info("Address created: id=%d label='%s'", address.id, address.label)
        return address
    except Exception as e:
        db.rollback()
        logger.error("Failed to create address: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create address"
        )


@router.patch("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int,
    body: AddressUpdate,
    db: Session = Depends(get_db),
) -> AddressResponse:
    address = get_address_or_404(address_id, db)
    update_data = body.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
    try:
        for key, value in update_data.items():
            setattr(address, key, value)
        db.commit()
        db.refresh(address)
        logger.info("Address updated: id=%d fields=%s", address_id, list(update_data.keys()))
        return address
    except Exception as e:
        db.rollback()
        logger.error("Failed to update address id=%d: %s", address_id, str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update address"
        )


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int, db: Session = Depends(get_db)) -> None:
    address = get_address_or_404(address_id, db)
    try:
        db.delete(address)
        db.commit()
        logger.info("Address deleted: id=%d", address_id)
    except Exception as e:
        db.rollback()
        logger.error("Failed to delete address id=%d: %s", address_id, str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete address"
        )

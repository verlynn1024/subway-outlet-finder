from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.db import get_db, Outlet
from app.api.schemas import OutletResponse, OutletCreate, OutletUpdate
from geopy.distance import geodesic

router = APIRouter()

@router.get("/outlets", response_model=List[OutletResponse])
def get_outlets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    city: Optional[str] = None,
    has_delivery: Optional[bool] = None
):
    """Get all outlets with optional filtering"""
    query = db.query(Outlet)
    
    if name:
        query = query.filter(Outlet.name.ilike(f"%{name}%"))
    if city:
        query = query.filter(Outlet.city.ilike(f"%{city}%"))
    if has_delivery is not None:
        query = query.filter(Outlet.has_delivery == has_delivery)
    
    outlets = query.offset(skip).limit(limit).all()
    return outlets

@router.get("/outlets/{outlet_id}", response_model=OutletResponse)
def get_outlet(outlet_id: int, db: Session = Depends(get_db)):
    """Get a specific outlet by ID"""
    outlet = db.query(Outlet).filter(Outlet.id == outlet_id).first()
    if outlet is None:
        raise HTTPException(status_code=404, detail="Outlet not found")
    return outlet

@router.post("/outlets", response_model=OutletResponse)
def create_outlet(outlet: OutletCreate, db: Session = Depends(get_db)):
    """Create a new outlet"""
    db_outlet = Outlet(**outlet.dict())
    db.add(db_outlet)
    db.commit()
    db.refresh(db_outlet)
    return db_outlet

@router.put("/outlets/{outlet_id}", response_model=OutletResponse)
def update_outlet(outlet_id: int, outlet: OutletUpdate, db: Session = Depends(get_db)):
    """Update an existing outlet"""
    db_outlet = db.query(Outlet).filter(Outlet.id == outlet_id).first()
    if db_outlet is None:
        raise HTTPException(status_code=404, detail="Outlet not found")
    
    for key, value in outlet.dict(exclude_unset=True).items():
        setattr(db_outlet, key, value)
    
    db.commit()
    db.refresh(db_outlet)
    return db_outlet

@router.delete("/outlets/{outlet_id}")
def delete_outlet(outlet_id: int, db: Session = Depends(get_db)):
    """Delete an outlet"""
    db_outlet = db.query(Outlet).filter(Outlet.id == outlet_id).first()
    if db_outlet is None:
        raise HTTPException(status_code=404, detail="Outlet not found")
    
    db.delete(db_outlet)
    db.commit()
    return {"message": "Outlet deleted successfully"}

@router.get("/outlets/nearby")
def get_nearby_outlets(
    latitude: float = Query(..., description="Latitude of the reference point"),
    longitude: float = Query(..., description="Longitude of the reference point"),
    radius: float = Query(5.0, description="Search radius in kilometers"),
    db: Session = Depends(get_db)
):
    """Find outlets within a specified radius of a point"""
    outlets = db.query(Outlet).all()
    nearby = []
    
    reference_point = (latitude, longitude)
    
    for outlet in outlets:
        if outlet.latitude and outlet.longitude:
            outlet_point = (outlet.latitude, outlet.longitude)
            distance = geodesic(reference_point, outlet_point).kilometers
            
            if distance <= radius:
                outlet_dict = {
                    "id": outlet.id,
                    "name": outlet.name,
                    "address": outlet.address,
                    "latitude": outlet.latitude,
                    "longitude": outlet.longitude,
                    "distance": round(distance, 2)
                }
                nearby.append(outlet_dict)
    
    return sorted(nearby, key=lambda x: x["distance"])

@router.get("/outlets/catchment-analysis")
def catchment_analysis(db: Session = Depends(get_db)):
    """Perform catchment analysis for all outlets"""
    outlets = db.query(Outlet).all()
    result = []
    
    # For each outlet, find other outlets within 5km
    for outlet in outlets:
        if outlet.latitude and outlet.longitude:
            outlet_point = (outlet.latitude, outlet.longitude)
            overlapping = []
            
            for other in outlets:
                if other.id != outlet.id and other.latitude and other.longitude:
                    other_point = (other.latitude, other.longitude)
                    distance = geodesic(outlet_point, other_point).kilometers
                    
                    if distance <= 5:  # 5km catchment radius
                        overlapping.append({
                            "id": other.id,
                            "name": other.name,
                            "distance": round(distance, 2)
                        })
            
            result.append({
                "id": outlet.id,
                "name": outlet.name,
                "latitude": outlet.latitude,
                "longitude": outlet.longitude,
                "overlapping_catchments": overlapping,
                "total_overlaps": len(overlapping)
            })
    
    return result
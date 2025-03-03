from pydantic import BaseModel, Field
from typing import Optional, List

class OutletBase(BaseModel):
    name: str
    address: str
    city: str
    state: str
    postal_code: str
    phone: Optional[str] = None
    has_delivery: bool = False
    has_dine_in: bool = True
    opening_hours: Optional[str] = None

class OutletCreate(OutletBase):
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class OutletUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    has_delivery: Optional[bool] = None
    has_dine_in: Optional[bool] = None
    opening_hours: Optional[str] = None

class OutletResponse(OutletBase):
    id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    class Config:
        orm_mode = True

class NearbyOutlet(BaseModel):
    id: int
    name: str
    address: str
    latitude: float
    longitude: float
    distance: float

class OverlappingCatchment(BaseModel):
    id: int
    name: str
    distance: float

class CatchmentAnalysis(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    overlapping_catchments: List[OverlappingCatchment]
    total_overlaps: int
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
import time

class TableTypeResponse(BaseModel):
    id: UUID
    name: str
    seats: int
    description: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True) 

class MenuItemResponse(BaseModel):
    id: UUID
    course: str
    name: str
    description: Optional[str] = None
    price: float
    allergens: List[str] = []

    model_config = ConfigDict(from_attributes=True)

class AvailabilityResponse(BaseModel):
    time: str               
    table_type: UUID        
    table_type_name: str   
    seats: int              
    available_seats: int    
    price_per_seat: float   

    model_config = ConfigDict(from_attributes=True)

class TurnAvailabilityResponse(BaseModel):
    name: str
    start_time: time
    end_time: time
    total_capacity: int
    confirmed_reservations: int
    occupancy_percentage: float
    is_closed: bool
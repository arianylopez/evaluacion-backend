from sqlalchemy import Column, String, Integer, Numeric, Date, Time, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    __table_args__ = {'schema': 'content'} 

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    address = Column(String)
    timezone = Column(String(50))
    
    table_types = relationship("TableType", back_populates="restaurant")
    menu_items = relationship("MenuItem", back_populates="restaurant")

class TableType(Base):
    __tablename__ = 'table_type'
    __table_args__ = {'schema': 'content'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('content.restaurant.id'))
    name = Column(String(100))
    seats = Column(Integer)
    description = Column(String)
    price_per_seat = Column(Numeric(10, 2))

    restaurant = relationship("Restaurant", back_populates="table_types")

class MenuItem(Base):
    __tablename__ = 'menu_item'
    __table_args__ = {'schema': 'content'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('content.restaurant.id'))
    date = Column(Date)
    course = Column(String(100))
    name = Column(String(255))
    description = Column(String)
    price = Column(Numeric(10, 2))
    allergens = Column(JSON)

    restaurant = relationship("Restaurant", back_populates="menu_items")

class Reservation(Base):
    __tablename__ = 'reservation'
    __table_args__ = {'schema': 'content'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('content.restaurant.id'))
    table_type_id = Column(UUID(as_uuid=True), ForeignKey('content.table_type.id'))
    date = Column(Date)
    time = Column(Time)
    party_size = Column(Integer)
    status = Column(String(20))

class Turn(Base):
    __tablename__ = 'turn'
    __table_args__ = {'schema': 'content'}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('content.restaurant.id'))
    name = Column(String)
    start_time = Column(Time)
    end_time = Column(Time)

from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Numeric
from unicodedata import numeric

Base = declarative_base()

class CitiesModel(Base):
    __tablename__ = 'cities'
    citi_id = Column(Integer, primary_key=True, autoincrement=True)
    citi_name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    country_id = Column(Integer, ForeignKey('country.country_id'))
    country = relationship('CountryModel', back_populates='cities')
    targets = relationship('TargetsModel', back_populates='city')  # הוספת הקשר ל-TargetsModel

class CountryModel(Base):
    __tablename__ = 'country'
    country_id = Column(Integer, primary_key=True, autoincrement=True)
    country_name = Column(String, nullable=False)
    cities = relationship('CitiesModel', back_populates='country')

class MissionsModel(Base):
    __tablename__ = 'missions'
    mission_id = Column(Integer, primary_key=True, autoincrement=True)
    mission_date = Column(Numeric(10,2), nullable=False)
    airborne_aircraft = Column(Float, nullable=False)
    attacking_aircraft = Column(Float, nullable=False)
    bombing_aircraft = Column(Float, nullable=False)
    aircraft_returned = Column(Float, nullable=False)
    aircraft_failed = Column(Float, nullable=False)
    aircraft_damaged = Column(Float, nullable=False)
    aircraft_lost = Column(Float, nullable=False)
    targets = relationship('TargetsModel', back_populates='mission')

class TargetsModel(Base):
    __tablename__ = 'targets'
    target_id = Column(Integer, primary_key=True, autoincrement=True)
    target_priority = Column(Float, nullable=False)
    target_industry = Column(String, nullable=False)
    mission_id = Column(Integer, ForeignKey('missions.mission_id'))
    mission = relationship('MissionsModel', back_populates='targets')
    target_type_id = Column(Integer, ForeignKey('targets_type.target_type_id'))
    target_type = relationship('Targets_typeModel', back_populates='targets')
    city_id = Column(Integer, ForeignKey('cities.citi_id'))
    city = relationship('CitiesModel', back_populates='targets')

class Targets_typeModel(Base):
    __tablename__ = 'targets_type'
    target_type_id = Column(Integer, primary_key=True, autoincrement=True)
    target_type_name = Column(String, nullable=False)
    targets = relationship('TargetsModel', back_populates='target_type')

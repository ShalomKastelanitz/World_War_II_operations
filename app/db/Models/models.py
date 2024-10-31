from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Numeric,Date
from unicodedata import numeric

Base = declarative_base()
#סידור המודלים לפי השדות בדאטה בייס
class CitiesModel(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    country_id = Column(Integer, ForeignKey('country.country_id'))
    country = relationship('CountryModel', back_populates='cities')
    targets = relationship('TargetsModel', back_populates='city')  # הוספת הקשר ל-TargetsModel

class CountryModel(Base):
    __tablename__ = 'country'
    country_id = Column(Integer, primary_key=True, autoincrement=True)
    country_name = Column(String, nullable=True)
    cities = relationship('CitiesModel', back_populates='country')

class MissionsModel(Base):
    __tablename__ = 'missions'
    mission_id = Column(Integer, primary_key=True, autoincrement=True)
    mission_date = Column(Date, nullable=True)
    airborne_aircraft = Column(Float, nullable=True)
    attacking_aircraft = Column(Float, nullable=True)
    bombing_aircraft = Column(Float, nullable=True)
    aircraft_returned = Column(Float, nullable=True)
    aircraft_failed = Column(Float, nullable=True)
    aircraft_damaged = Column(Float, nullable=True)
    aircraft_lost = Column(Float, nullable=True)
    targets = relationship('TargetsModel', back_populates='mission')

class TargetsModel(Base):
    __tablename__ = 'targets'
    target_id = Column(Integer, primary_key=True, autoincrement=True)
    target_priority = Column(Float, nullable=True)
    target_industry = Column(String, nullable=True)
    mission_id = Column(Integer, ForeignKey('missions.mission_id'))
    mission = relationship('MissionsModel', back_populates='targets')
    target_type_id = Column(Integer, ForeignKey('targets_type.target_type_id'))
    target_type = relationship('Targets_typeModel', back_populates='targets')
    city_id = Column(Integer, ForeignKey('cities.city_id'))
    city = relationship('CitiesModel', back_populates='targets')

class Targets_typeModel(Base):
    __tablename__ = 'targets_type'
    target_type_id = Column(Integer, primary_key=True, autoincrement=True)
    target_type_name = Column(String, nullable=True)
    targets = relationship('TargetsModel', back_populates='target_type')

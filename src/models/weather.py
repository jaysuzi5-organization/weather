"""
Weather Model and Pydantic Schema

This module defines:
- The SQLAlchemy ORM model for persisting current Weather data.
- The Pydantic schema for validating API requests when creating a Weather record.
"""

from sqlalchemy import Column, DateTime, Integer, String, Numeric
from framework.db import Base
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Weather(Base):
    """
    SQLAlchemy ORM model representing a current weather record.

    Attributes:
        collection_time (datetime): Primary key, timestamp when data was collected.
        temperature (int | None): Current temperature in degrees.
        temperature_min (int | None): Minimum temperature.
        temperature_max (int | None): Maximum temperature.
        humidity (int | None): Humidity percentage.
        description (str | None): Weather description (up to 200 characters).
        feels_like (int | None): Feels-like temperature.
        wind_speed (Decimal | None): Wind speed.
        wind_direction (int | None): Wind direction in degrees.
    """

    __tablename__ = "weather_current"

    collection_time = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    temperature = Column(Integer, nullable=True)
    temperature_min = Column(Integer, nullable=True)
    temperature_max = Column(Integer, nullable=True)
    humidity = Column(Integer, nullable=True)
    description = Column(String(200), nullable=True)
    feels_like = Column(Integer, nullable=True)
    wind_speed = Column(Numeric, nullable=True)
    wind_direction = Column(Integer, nullable=True)

    def __repr__(self):
        return (
            f"<WeatherCurrent(collection_time={self.collection_time}, "
            f"temp={self.temperature}, humidity={self.humidity}, desc='{self.description}')>"
        )


class WeatherCreate(BaseModel):
    """
    Pydantic schema for creating a new Weather record.

    Example:
        {
            "collection_time": "2025-09-19T14:00:00Z",
            "temperature": 72,
            "temperature_min": 68,
            "temperature_max": 75,
            "humidity": 55,
            "description": "Clear skies",
            "feels_like": 71,
            "wind_speed": 5.5,
            "wind_direction": 180
        }
    """
    collection_time: datetime
    temperature: Optional[int] = None
    temperature_min: Optional[int] = None
    temperature_max: Optional[int] = None
    humidity: Optional[int] = None
    description: Optional[str] = None
    feels_like: Optional[int] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[int] = None

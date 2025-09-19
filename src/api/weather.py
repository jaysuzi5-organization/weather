from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy import desc
from sqlalchemy.orm import Session
from framework.db import get_db
from models.weather import Weather, WeatherCreate
from datetime import datetime, UTC

router = APIRouter()

def serialize_sqlalchemy_obj(obj):
    """
    Convert a SQLAlchemy ORM model instance into a dictionary.

    Args:
        obj: SQLAlchemy model instance.

    Returns:
        dict: Dictionary containing all column names and their values.
    """
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


@router.get("/api/v1/weather")
def list_weather(
    page: int = Query(1, ge=1, description="Page number to retrieve"),
    limit: int = Query(10, ge=1, le=100, description="Number of records per page"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of Weather records, sorted by latest collection_time first.

    Args:
        page (int): Page number starting from 1.
        limit (int): Maximum number of records to return per page.
        db (Session): SQLAlchemy database session.

    Returns:
        list[dict]: A list of serialized Weather records.
    """
    try:
        offset = (page - 1) * limit
        weather_records = (
            db.query(Weather)
            .order_by(desc(Weather.collection_time))  # sort descending
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [serialize_sqlalchemy_obj(item) for item in weather_records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/api/v1/weather")
def create_record(
    weather_data: WeatherCreate = Body(..., description="Data for the new record"),
    db: Session = Depends(get_db)
):
    """
    Create a new Weather record.

    Args:
        weather_data (WeatherCreate): Data model for the record to create.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The newly created Weather record.
    """
    try:
        data = weather_data.model_dump(exclude_unset=True)
        new_record = Weather(**data)
        new_record.create_date = datetime.now(UTC)
        new_record.update_date = datetime.now(UTC)

        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return serialize_sqlalchemy_obj(new_record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/api/v1/weather/{id}")
def get_weather_by_id(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single Weather record by ID.

    Args:
        id (int): The ID of the record.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The matching Weather record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Weather).filter(Weather.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Weather with id {id} not found")
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/api/v1/weather/{id}")
def update_weather_full(
    id: int,
    weather_data: WeatherCreate = Body(..., description="Updated data for the record"),
    db: Session = Depends(get_db)
):
    """
    Fully update an existing Weather record (all fields required).

    Args:
        id (int): The ID of the record to update.
        weather_data (WeatherCreate): Updated record data (all fields).
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The updated Weather record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Weather).filter(Weather.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Weather with id {id} not found")

        data = weather_data.model_dump(exclude_unset=False)
        for key, value in data.items():
            setattr(record, key, value)

        record.update_date = datetime.now(UTC)
        db.commit()
        db.refresh(record)
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.patch("/api/v1/weather/{id}")
def update_weather_partial(
    id: int,
    weather_data: WeatherCreate = Body(..., description="Partial updated data for the record"),
    db: Session = Depends(get_db)
):
    """
    Partially update an existing Weather record (only provided fields are updated).

    Args:
        id (int): The ID of the record to update.
        Weather_data (WeatherCreate): Partial updated data.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The updated Weather record.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Weather).filter(Weather.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Weather with id {id} not found")

        data = weather_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(record, key, value)

        record.update_date = datetime.now(UTC)
        db.commit()
        db.refresh(record)
        return serialize_sqlalchemy_obj(record)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/api/v1/weather/{id}")
def delete_weather(id: int, db: Session = Depends(get_db)):
    """
    Delete a Weather record by ID.

    Args:
        id (int): The ID of the record to delete.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the record is not found.
    """
    try:
        record = db.query(Weather).filter(Weather.id == id).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Weather with id {id} not found")

        db.delete(record)
        db.commit()
        return {"detail": f"Weather with id {id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List

from api.db.session import get_session
from .models import (
    EventModel,
    EventBucketSchema,
    EventCreateSchema,
    get_utc_now)

from sqlalchemy import func, case
from timescaledb.hyperfunctions import time_bucket
from datetime import datetime, timedelta

router = APIRouter()

DEFAULT_LOOKUP_PAGES = [
        "/", "/about", "/pricing", "/contact",
        "/blog", "/products", "/login", "/signup",
        "/dashboard", "/settings"
    ]

# GET /api/events
@router.get("/", response_model=List[EventBucketSchema])
def read_events(
    duration: str = Query(default="1 day"),
    pages: List[str] = Query(default=None),
    session:Session = Depends(get_session)
    ):

    os_case = case(
        (EventModel.user_agent.ilike("%Windows%"), "Windows"),
        (EventModel.user_agent.ilike("%Linux%"), "Linux"),
        (EventModel.user_agent.ilike("%Macintosh%"), "Mac"),
        (EventModel.user_agent.ilike("%iPhone%"), "iPhone"),
        (EventModel.user_agent.ilike("%Android%"), "Android"),
        else_="Other",
    ).label("operating_system")

    bucket = time_bucket(duration, EventModel.time)
    lookup_pages = pages if isinstance(pages,list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    query = (
        select(
            bucket.label("bucket"),
            os_case,
            EventModel.page.label("page"),
            func.avg(EventModel.duration).label("avg_duration"),
            func.count().label("count"),
        )
        .where(
            EventModel.page.in_(lookup_pages)
        )
        .group_by(
            bucket,
            os_case,
            EventModel.page,
        )
        .order_by(
            bucket,
            os_case,
            EventModel.page,
        )
    )
    results = session.exec(query).fetchall()
    return results

# SEND DATA HERE
# create view
# POST /api/events
@router.post("/", response_model=EventModel)
def create_event(
    payload:EventCreateSchema,
    session:Session = Depends(get_session)):

    data = payload.model_dump()
    obj = EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


# GET /api/events/12
@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id: int, session:Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result

# DELETE /api/events/12
@router.delete("/{event_id}", response_model=EventModel)
def delete_event(event_id: int, session:Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(obj)
    session.commit()
    return obj
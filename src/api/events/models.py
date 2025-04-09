from sqlmodel import SQLModel, Field
from typing import List, Optional
from datetime import datetime, timezone
import sqlmodel
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now

# page visits

class EventModel(TimescaleModel, table=True):
    page: str = Field(index=True)
    user_agent: Optional[str] = Field(default="", index=True)
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0)

    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__= "INTERVAL 3 months"

class EventCreateSchema(SQLModel):
    page: str
    user_agent: Optional[str] = Field(default="", index=True)
    ip_address: Optional[str] = Field(default="", index=True)
    referrer: Optional[str] = Field(default="", index=True)
    session_id: Optional[str] = Field(index=True)
    duration: Optional[int] = Field(default=0)

class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int

class EventBucketSchema(SQLModel):
    page: str
    ua: Optional[str] = ""
    operating_system: Optional[str] = ""
    avg_duration: Optional[float] = 0.00
    bucket: datetime
    count: int
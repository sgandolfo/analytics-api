from fastapi import APIRouter
from .schemas import EventSchema, EventListSchema, EventCreateSchema, EventUpdateSchema

router = APIRouter()

# GET /api/events
@router.get("/")
def read_events() -> EventListSchema:
    return {
        "results": [{"id": 1}, {"id": 2}, {"id": 3}],
        "count": 3
        }

# SEND DATA HERE
# create view
# POST /api/events
@router.post("/")
def create_events(payload:EventCreateSchema) -> EventSchema:
    data = payload.model_dump()
    return {"id": 123, **data}


# GET /api/events/12
@router.get("/{event_id}")
def get_event(event_id: int) -> EventSchema:
    return {
        "id": event_id,
        }

@router.put("/{event_id}")
def update_event(event_id: int, payload:EventUpdateSchema) -> EventSchema:
    data = payload.model_dump()
    print(data)
    return {
        "id": event_id,
        **data
        }
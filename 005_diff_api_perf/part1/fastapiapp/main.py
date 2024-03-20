from datetime import datetime
import os
from typing import List

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request

from pydantic import BaseModel

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker


load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL') or 'nah', pool_size=10, max_overflow=10)
metadata = MetaData()
metadata.reflect(engine, only=['testapp_parent', 'testapp_child'])
Base = automap_base(metadata=metadata)
Base.prepare()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Parent = Base.classes.testapp_parent
Child = Base.classes.testapp_child

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ParentSchema(BaseModel):

    title: str
    created: datetime
    modified: datetime


class ChildSchema(BaseModel):

    title: str
    json_field: dict
    long_text: str
    created: datetime
    modified: datetime
    parent: ParentSchema


class Response(BaseModel):
    count: int
    results: List[ChildSchema]
    previous: str
    next: str


@app.get("/children", response_model=Response)
def read_children(request: Request, page: int = 1, db: Session = Depends(get_db)):
    per_page = 30
    offset = (page - 1) * per_page
    query = db.query(Child, Parent).join(Parent)
    count = query.count()
    if count == 0:
        return {'count': 0, 'results': [], 'previous': None, 'next': None}

    pages = count // per_page
    if count % per_page != 0:
        pages += 1
    payload = []
    for child, parent in query.order_by(Child.id).offset(offset).limit(30):
        child.parent = parent
        payload.append(child)

    base_url = f'{request.url.scheme}://{request.client.host}:{request.scope["server"][1]}'
    next_page = f'{base_url}?page={page + 1}' if page < pages else None
    previous_page = f'{base_url}?page={page - 1}' if page > 1 else None
    return {'count': count, 'results': payload, 'previous': previous_page, 'next': next_page}

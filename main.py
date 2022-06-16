from typing import Optional
from enum import Enum
from pydantic import BaseModel
from pydantic import Field
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query
from fastapi import Path

app = FastAPI()


class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        title="First name",
        description="It's the first name of the person.",
        example="Bryan Antonio",
    )
    last_name: str = Field(..., min_length=1, max_length=50, example="Alvarado")
    age: int = Field(..., gt=0, le=115, example=29)
    hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=False)

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Facundo",
    #             "last_name": "Garcia",
    #             "age": 21,
    #             "hair_color": "blonde",
    #             "is_married": True,
    #         }
    #     }


class Location(BaseModel):
    city: str
    state: str
    country: str


@app.get("/")
def home():
    return {"hello": "world"}


@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is a person name. It's between 1 and 50 charactes.",
    ),
    age: str = Query(
        ..., title="Person Age", description="This is the person age. It's requiered."
    ),
):
    return {name: age}


@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is the person ID. It's requiered.",
    )
):
    return {person_id: "It Exists"}


@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ..., title="Person ID", description="This is the person ID", gt=0
    ),
    person: Person = Body(...),
    # location: Location = Body(...),
):
    # results_dict = person.dict()
    # results_dict.update(location.dict())
    return person

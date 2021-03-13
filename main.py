from typing import Optional, Set, List
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field, HttpUrl


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None,
        title="The description of the item",
        max_length=3000,
        example="A very nice Item",
    )
    price: float = Field(
        ..., gt=0, description="The price must be greater than zero", example=35.4
    )
    tax: Optional[float] = Field(None, example=3.2)
    tags: Set[str] = set()
    images: Optional[List[Image]] = None


class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get", gt=0, le=1000),
    q: Optional[str] = Query(None, alias="item-query"),
    size: float = Query(..., gt=0, lt=10.5),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.post("/items/{item_id}")
async def create_item(
    item_id: int,
    item: Item,
    q: Optional[str] = Query(
        ...,  # interpreted as required
        title="Query string",
        alias="item-query",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        regex="^fixedquery$",
        deprecated=True,
    ),
):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    result = {"item_id": item_id, **item_dict}

    if q:
        result.update({"q": q})
    return result


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    item: Item,
    user: User,
    importance: int = Body(..., gt=0),
    q: Optional[str] = None,
):
    results = {"item_id": item_id, "user": user, "importance": importance}
    if item:
        results.update({"item": item})
    if q:
        results.update({"q": q})
    return results


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

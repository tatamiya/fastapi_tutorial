from typing import Optional
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


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

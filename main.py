from typing import Optional, Set, List
from fastapi import FastAPI, Query, Path, Body, Cookie, Header, status, Form
from pydantic import BaseModel, Field, HttpUrl, EmailStr


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
    tax: Optional[float] = Field(10.5, example=3.2)
    tags: Set[str] = set()
    images: Optional[List[Image]] = None


class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class User(UserBase):
    pass


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get", gt=0, le=1000),
    q: Optional[str] = Query(None, alias="item-query"),
    size: float = Query(..., gt=0, lt=10.5),
    ads_id: Optional[str] = Cookie(None),
    user_agent: Optional[str] = Header(None),
    x_token: Optional[List[str]] = Header(None),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if ads_id:
        results.update({"ads_id", ads_id})
    if user_agent:
        results.update({"User-Agent": user_agent})
    if x_token:
        results.update({"X-Token values": x_token})
    return results


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include=["name", "description"],
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get(
    "/items/{item_id}/public",
    response_model=Item,
    response_model_exclude=["tax"],
    response_model_exclude_unset=True,
)
async def read_item_public_data(item_id: str):
    return items[item_id]


@app.post("/items/{item_id}", response_model=Item, status_code=status.HTTP_201_CREATED)
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
    return item


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


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}

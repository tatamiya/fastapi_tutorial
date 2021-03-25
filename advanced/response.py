from typing import Optional
from fastapi import FastAPI, Response, Cookie

app = FastAPI()


@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}


@app.get("/get-cookie/")
def get_cookie(fakesession: Optional[str] = Cookie(None)):
    return {"fakesession": fakesession}


@app.get("/delete-cookie/")
def delete_cookie(response: Response, fakesession: Optional[str] = Cookie(None)):
    if fakesession:
        response.delete_cookie(key="fakesession")
        return {"message": "Welcome back to the light side, cookies are deleted"}

    return {"message": "You are in the light side"}

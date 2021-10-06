from __future__ import annotations

from typing import List

import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL


@strawberry.type
class User:
    first_name: str
    last_name: str
    age: int
    skills: List[Skill]

    @strawberry.field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@strawberry.type
class Skill:
    language: str
    experience: int


@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(
            first_name="Patrick",
            last_name="Foo",
            age=100,
            skills=[
                Skill(language="Python", experience=5),
                Skill(language="Go", experience=2),
                Skill(language="Rust", experience=1),
            ],
        )


schema = strawberry.Schema(query=Query)

graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

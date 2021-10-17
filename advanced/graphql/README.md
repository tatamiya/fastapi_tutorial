# GraphQL

https://fastapi.tiangolo.com/advanced/graphql/

see also
https://strawberry.rocks/

https://github.com/strawberry-graphql/strawberry/releases/tag/0.84.0

# Example Queries

## search a user by name

```graphql
query{
  user(firstName: "Patrick", lastName: "Foo") {
    fullName
    age
    skills {
      language
      experience
    }
  }
}
```

## search users by skill

```graphql
query{
  searchBySkill(language: "Python") {
    fullName
    age
    skills {
      language
      experience
    }
  }
}
```
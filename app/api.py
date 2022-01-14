import strawberry
from redis_om import HashModel
from slugify import slugify
from strawberry.fastapi import GraphQLRouter


class Post(HashModel):
    title: str
    content: str
    author: str

    @property
    def slug(self):
        return slugify(self.title)


@strawberry.experimental.pydantic.type(model=Post, all_fields=True)
class PostType:
    slug: str


@strawberry.experimental.pydantic.input(model=Post, all_fields=True)
class AddPostInput:
    pass


def get_posts() -> list[Post]:
    pks = Post.all_pks()
    return [Post.get(pk) for pk in pks]


@strawberry.type
class Query:
    posts: list[PostType] = strawberry.field(resolver=get_posts)


@strawberry.type
class Mutation:
    @strawberry.field
    def add_post(self, post: AddPostInput) -> PostType:
        p = Post(title=post.title, author=post.author, content=post.content)
        p.save()
        return p


schema = strawberry.Schema(Query, Mutation)

graphql_app = GraphQLRouter(schema)

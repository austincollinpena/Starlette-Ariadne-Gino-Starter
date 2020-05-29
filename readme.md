**Note**

This is heavily a WIP. The goal is to present it to the community and get feedback.

## Motivation

Build a completely async python graphql server with built in Auth. If you're looking for a very polished implementation of Ariadne, check out [this repo](https://gitlab.com/heathercreech/demmy/-/tree/version-2/server#faq-for-those-using-this-repo-as-a-reference-for-ariadne).

## Components:

1. Starlette Server
2. Ariadne Graphql Server
2. Gino Async wrapper for sqlalchemy
3. Alembic database migration handler
4. Asyncpg database driver

## How To's

**Start The Server**

From the root directory, run ```uvicorn backend.main:app --reload```

**Make Migrations**

This has to be done from the root folder where the ```alembic.ini``` file exists.

Run: ```alembic revision --autogenerate -m "Added initial table"``` to generate the migrations.

And then: ```alembic upgrade head``` to apply them.

Alembic has well know issues with knowing the Python path. This was solved through moving the ```alembic.ini``` file from the ```./backend``` folder to the root folder, and adding the following line to the .ini:

```python
current_dir = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(current_dir)
```

Finally, the last bit of "magic" applied is to ensure that the DB URL specified in the .env file is used during online migrations. This function can be found in ./alembic/env.py 

## How The Apps Work

This starter follows the same conventions as Django where apps are seperated into their own components for organization's sake. Each app inherits types from the utils/graphql folder which are then used to create mutations/queries.

**Adding a new query**

For example, each new added query needs to do the following:

1. Define the new query in a .graphql file with the ```extend type Query``` syntax
2. Import the root query into the file with the resolver 
3. Wrap the resolver around the query:

```graphql
# Graphql typedefs file
extend type Query{
    getUser: Boolean
}
```

```python
# Resolver File
from backend.utils.graphql.query_type import query
@query.field("getUser")
async def resolve_get_user(obj, info):
    return False
```

**Adding a new mutation, type, subscription, or other**

The convention is to define the root class, like the ```type Mutation``` in the ```utils/graphql``` folder, which makes adding new resolvers really easy. 

**How The Graphql Server Knows About Type Defs**

Because there is only one query attached to the server, we need to import all of our schema and resolvers to the root.

To keep things organized, we can see four entry points of interest for our sample app for type defs:
```
/app
__init__.py (Exports the collection of all the type defs)

- /queries
   __init__.py (makes a list of all the query schemas)

- /mutations
   __init__.py (makes a list of all the mutation schemas)

- /types
   __init__.py (makes a list of all the types schemas)
```

Inside of our ```queries/__init__.py``` we load all of the ```.graphql``` files as below. ([docs link](https://ariadnegraphql.org/docs/modularization))

```python
from ariadne import load_schema_from_path
import os
user_query_schema = load_schema_from_path(
    os.path.join(os.getcwd(), "backend/users/queries"))
```
This process is repeated across the ```mutations``` and ```types``` folders.

Then, in the ```/app```'s ```___init__.py```, they are all collected and put in a list.

```python
# TODO: Add the .mutations
from .queries import user_query_schema
from .types import user_type_schema

user_type_defs = [user_query_schema, user_type_schema]
```

Finally, in the ```main.py```, we can put it all together in the following generic format. ([docs link](https://ariadnegraphql.org/docs/intro#making-executable-schema))

```python
schema = make_executable_schema([*list_of_type_defs, *other_list_of_type_defs], query, mutation, subscription)
```

In our example, that looks like this:

```python
from ariadne import make_executable_schema

from backend.utils.graphql.query_type import query as root_query
from backend.utils.graphql.mutation_type import mutation as root_mutation
from backend.utils.graphql import root_graphql_types
from backend.users import user_type_defs

schema = make_executable_schema([*root_graphql_types, *user_type_defs], root_query, root_mutation)
```

**Binding Resolvers**

There are two steps to binding the resolvers, and we've already seen one, the decorator ([more ways here](https://ariadnegraphql.org/docs/resolvers))
```python
from backend.utils.graphql.query_type import query
@query.field("getUser")
async def resolve_get_user(obj, info):
...
```

However, to have this _actually_ get picked up by the Query, we need to export our resolvers from the ```__init__.py``` of each folder containing resolvers like so (of course you could also export each function individually as well).

```python
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
```

## Using Gino

Gino is a wrapper around SQLAlchemy core, allowing for asynchronous actions.

1. Basic CRUD actions are [outline here](https://python-gino.org/docs/en/master/tutorials/tutorial.html#crud-operations). Full [API reference is here](https://python-gino.org/docs/en/master/reference/api/gino.crud.html).
2. Instructions for setting up models [are here](https://python-gino.org/docs/en/master/how-to/schema.html#gino-core)
3. Loading relationships via models loaders [are here](https://python-gino.org/docs/en/master/how-to/loaders.html).

TODO: ondelete=Cascade?

## Authentication

Still a lot to do here! One important note is that there are no refresh JWT's implemented yet. Will likely work based off of the frontend's requirement and [this guide](https://medium.com/@lucasmcgartland/refreshing-token-based-authentication-with-apollo-client-2-0-7d45c20dc703).


## Setting Up The environment

1. Run a pip install
2. Fill out the ```env``` file with variables included for convenience. Just change it from ```env``` to ```.env``` (This of course requires a postgres server up and running)

## Other To Do:

1. Add Redis
2. Add ability to use background tasks
3. Add session based authentication


https://spectrum.chat/ariadne/general/return-cookie-in-response-headers-based-on-response-content~37893ad2-f66a-43ca-9313-201be05e765d
```python
app.middleware("http")
async def cookie_middleware(request: Request, call_next):
# This function also experiments with allowing cookies to be set using data from the resolvers
# that is stored in the request item
response = Response("Internal server error", status_code=500)
try:
    request.state.response_cookies = False
    request.state.response_tokens = None
    response = await call_next(request)
finally:
    if request.state.response_cookies:
        tokens = request.state.response_tokens
        for token in tokens:
            # Parse what kind of token it is
            if token == "accessToken":
                response.set_cookie(
                    key="vidette-Authorization",
                    value=tokens[token].decode("utf-8"),
                    # expires=int(tokens[token][1]),
                    expires=int(10),
                    httponly=True,
                )
            if token == "refreshToken":
                response.set_cookie(
                    key="vidette-Refresh",
                    value=tokens[token].decode("utf-8"),
                    #expires=int(tokens[token][1]),
                    expires=int(10),
                    httponly=True
                )
            if token == "Data":
                response.set_cookie(
                    key="vidette-Data",
                    value=tokens[token].decode("utf-8"),
                    #expires=int(tokens[token][1]),
                    expires=int(10),
                    httponly=True
                )
return response
```

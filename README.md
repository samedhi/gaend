# gaend - **G**oogle **A**pp **E**ngine **End**points

## Synopsis
This project converts a `google.appengine.ext.ndb.Model` into a HTTP endpoints. It provides validation, routing, documentation, and CRUD server endpoints. Its purpose is to act as a "DSL" for Google App Engine, allowing you to quickly write CRUD servers with just a `Model`.

## Full Code Example
```yaml
# app.yaml
runtime: python27
api_version: 1
threadsafe: true

handlers:
- url: /
  script: main.app
```

```python
# main.py
from google.appengine.ext import ndb
from gaend.models import GaendFullMixin

class Alien(ndb.Model, GaendFullMixin):
    proboscis_count = ndb.IntegerProperty(default=1)
    kind = ndb.StringProperty(required=True, choices=["Grey", "Martian", "Hutt"])
    name = ndb.StringProperty(lambda s: len(s) >= 1 and len(s) <= 20)
    full_name = ndb.ComputedProperty(lambda self: self.name + " the " + self.kind)
```

```bash
> gcloud deploy app.yaml
...
Deployed service [modeling-agency] to [https://aliens-are-real.appspot.com]
...
> curl -H "Content-Type: application/json" \
  -d '{"kind": "Martian", "name": "Bob"}' \
  https://aliens-are-real.appspot.com/alien

{"key": "fsdafsdaf",
 "kind": "Martian",
 "proboscis_count": 1,
 "name": "Bob",
 "full_name": "Bob the Martian"}
```

## Motivation

Sometimes your data is actually pretty simple.
* You want to Create, Read, Update, and Destroy entities using REST endpoints.
* You want to do validation every time an entity is written.
* You want to have up to date documentation of your endpoints.

Sometimes, the `ndb.Model` class (`Alien` in the example) contains enough information to do all of the above bullet points. Why spend time writing boilerplate code that can be inferred? Are we programmers or are we programmers? Automate all the things.

## Installation

```bash
> pip install modeling-agency
```

## API Reference

## Test

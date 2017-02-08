.. Gaend documentation master file, created by
   sphinx-quickstart on Mon Feb  6 23:22:52 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Gaend!
===================================================

Gaend converts ``google.appengine.ext.ndb.Model``'s into HTTP endpoints. It provides validation, routing, documentation, and CRUD server endpoints. Its acts as a DSL for Google App Engine, allowing you to quickly write CRUD servers by only declaring ``ndb.Model``'s.

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Full Code Example
=================

app.yaml::

  runtime: python27
  api_version: 1
  threadsafe: true

  handlers:
  - url: /.*
    script: gaend.main.APP

main.py::

  from google.appengine.ext import ndb
  from gaend.models import GaendFullMixin

  class Alien(ndb.Model, GaendFullMixin):
    proboscis_count = ndb.IntegerProperty(default=1)
    kind = ndb.StringProperty(
      required=True, choices=["Grey", "Martian", "Hutt"])
    name = ndb.StringProperty(
      lambda s: len(s) >= 1 and len(s) <= 20)
    full_name = ndb.ComputedProperty(
      lambda self: self.name + " the " + self.kind)

BASH::

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

Motivation
==========

Sometimes your data is actually pretty simple.

#. You want to Create, Read, Update, and Destroy entities using REST endpoints.
#. You want to do validation on every write.
#. You want up to date documentation of your endpoints.

Sometimes, the ``ndb.Model`` class (``Alien`` in the example) contains enough information to do all of the above bullet points. Why spend time writing boilerplate code that can be inferred? Are we programmers or are we programmers? Infer all the things!

Documentation & API
===================

`Gaend Read the Docs <http://gaend.readthedocs.io/en/latest/>`_ contains all documentation for Gaend; including the public API, FAQ's, as well as Cookbook examples.

Installation
============

``> pip install gaend``

Test
====

``> brew install entr``

``> find ./gaend ./tests -name "*.py" -print | entr -drc python runner.py $GOOGLE_CLOUD_SDK``

..
   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

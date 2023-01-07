******
Khanto
******

Project to apply to Seazone position.

Getting started
===============

Prerequisites
-------------

* Python >= 3.8

Installing
----------

1. Create the virtual environment. I recommend using
   `virtualenvwrapper <http://virtualenvwrapper.readthedocs.io/en/latest/index.html>`_.

2. Setup the environment:

   .. code-block:: bash

      $ pip install -r requirements.txt
      $ python manage.py migrate

3. Start the server:

   .. code-block:: bash

      $ python manage.py runserver

The site will be available on <http://localhost:8000>.

REST API
========

REST API documentation will be available on ``/api/v1/docs/`` for version 1 of the API
(currently the only version).

Fixtures
========

Fixtures live in ``fixtures/`` directory.

Commands to load fixtures to the database:

   .. code-block:: bash

      $ python manage.py loaddata fixtures/properties.json
      $ python manage.py loaddata fixtures/listings.json
      $ python manage.py loaddata fixtures/reservations.json


Or to load all fixtures at once:

   .. code-block:: bash

      $ python manage.py loaddata fixtures/*.json

Testing
=======

Tests live in a module called ``tests.py`` inside the package being tested.
For larger tests they can also be inside a ``tests/`` containing modules called ``test_*.py``.

Command to run the tests:

   .. code-block:: bash

      $ python manage.py test

Requirements
============

We use constraints.

Add dependencies to requirements.txt:

   .. code-block:: text

      -c constraints.txt
      Django
      anotherdependency

Then run:

   .. code-block:: bash

      $ pip install -r requirements.txt
      $ pip freeze > constraints.txt

pardot-api-client
==================

A simple Python client for interacting with the Pardot API.


Features
--------

* Supports API version 3
* Supports all API entities: Account, Campaign, Custom Field, Custom Redirect, Dynamic Content, Email, Email Clicks, Form, Identified Company, Lifecycle History, Lifecycle Stage, List, List Membership, Opportunity, Profile, Profile Criteria, Prospect, Prospect Account, Tag, Tag Object, User, Visit, Visitor, Visitor Activity, Visitor Page View, Visitor Referrer
* Supports all API operations: query, assign, unassign, create, batchCreate, read, update, batchUpdate, upsert, batchUpsert, delete
* Supports un-setting of field values
* Handles API session timeouts implicitly
* Supports result set manipulation, eg specifying fields, limit, offset, sort_by, sort_order
* Implicit results pagination
* Implicit chunking for batch operationss
* Transparent API error feedback
* Optional request retries with incremental back-off


Installation
------------

.. code-block:: bash

    $ pip install pardot-api-client


Usage
-----

1. Obtain API authentication credentials from Pardot by following instructions at http://developer.pardot.com/#authentication - you'll need the following: email, password, user_key
2. Review the supported Pardot API documentation at http://developer.pardot.com/#official-pardot-api-documentation
3. Use the Python API client to interact with the API:

    .. code-block:: python

        >>> from pardot.client import APIClient
        >>> client = APIClient(
        ...     'pardot-email',
        ...     'pardot-password',
        ...     'pardot-user_key')
        ...
        >>> # read
        >>> r = client.prospect.read('someone@example.com')
        >>> print(r)
        >>> # update
        >>> r = client.prospect.update('someone@example.com', first_name='John')
        >>> print(r)
        >>> # query
        >>> for r in client.prospect.query(new=True):
        ...    print(r)
        ...


Testing
-------

.. code-block:: bash

    $ python setup.py test

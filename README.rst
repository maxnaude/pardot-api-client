pardot-api-client
==================

A Python client for the Pardot API.

It provides object notation for interacting with resources on the API in clean and simple idiomatic statements like:

.. code-block:: python

    >>> client.prospect.read('someone@example.com')
    >>> client.prospect.update('someone@example.com', first_name='John')


Features
--------

* Supports Python 2 and 3
* Supports API version 3
* Supports all API entities: Account, Campaign, Custom Field, Custom Redirect, Dynamic Content, Email, Email Clicks, Form, Identified Company, Lifecycle History, Lifecycle Stage, List, List Membership, Opportunity, Profile, Profile Criteria, Prospect, Prospect Account, Tag, Tag Object, User, Visit, Visitor, Visitor Activity, Visitor Page View, Visitor Referrer
* Supports most API operations: query, assign, unassign, create, read, update, upsert, delete
* Supports un-setting of field values
* Handles API session timeouts implicitly
* Transparent API error feedback
* Optional request retries with incremental back-off


Planned features
----------------

* Support for API version 4
* Support for API batch operations: batchCreate, batchUpdate, batchUpsert
* Supports result set manipulation, eg specifying fields, limit, offset, sort_by, sort_order
* Implicit results pagination
* Implicit chunking for batch operationss


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


Arguments vs keyword arguments
------------------------------

To keep the client's API simple it makes educated guesses about the identifiers passed in resource operation calls.

To make this work all required parameters (except user_key and api_key, which are automatically added) must be passed as positional arguments and any optional parameters passed as keyword arguments.

For instance, the API documentation states that "assign" operations on "prospect" resources may use either "email" or "id" as identifiers and must supply one of the following parameters:  "user_email" or "user_id" or "group_id".  Any of the forms below could be used to make this call from the client:

.. code-block:: python

    >>> # identify by email
    >>> client.prospect.update('someone@example.com', user_email='someone-else@example.com')
    >>> client.prospect.update('someone@example.com', user_id=2544897)
    >>> client.prospect.update('someone@example.com', group_id=5499876)
    >>> # identify by id
    >>> client.prospect.update(7142577, user_email='someone-else@example.com')
    >>> client.prospect.update(7142577, user_id=2544897)
    >>> client.prospect.update(7142577, group_id=5499876)




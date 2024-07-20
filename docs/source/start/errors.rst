Error Handling
==============

Errors can be correctly handled with ``try...except`` blocks in order to control the behaviour of your application.
Pyrogram errors all live inside the ``errors`` package:

.. code-block:: python

    from pyrogram import errors


-----

RPCError
--------

The father of all errors is named ``RPCError`` and is able to catch all Telegram API related errors.
This error is raised every time a method call against Telegram's API was unsuccessful.

.. code-block:: python

    from pyrogram.errors import RPCError

.. warning::

    Avoid catching this error everywhere, especially when no feedback is given (i.e. by logging/printing the full error
    traceback), because it makes it impossible to understand what went wrong.

Error Categories
----------------

The ``RPCError`` packs together all the possible errors Telegram could raise, but to make things tidier, Pyrogram
provides categories of errors, which are named after the common HTTP errors and are subclass-ed from the ``RPCError``:

.. code-block:: python

    from pyrogram.errors import BadRequest, Forbidden, ...

-   :doc:`303 - SeeOther <../api/errors/see-other>`
-   :doc:`400 - BadRequest <../api/errors/bad-request>`
-   :doc:`401 - Unauthorized <../api/errors/unauthorized>`
-   :doc:`403 - Forbidden <../api/errors/forbidden>`
-   :doc:`406 - NotAcceptable <../api/errors/not-acceptable>`
-   :doc:`420 - Flood <../api/errors/flood>`
-   :doc:`500 - InternalServerError <../api/errors/internal-server-error>`

Single Errors
-------------

For a fine-grained control over every single error, Pyrogram does also expose errors that deal each with a specific
issue. For example:

.. code-block:: python

    from pyrogram.errors import FloodWait

These errors subclass directly from the category of errors they belong to, which in turn subclass from the father
``RPCError``, thus building a class of error hierarchy such as this:

- RPCError
    - BadRequest
        - ``MessageEmpty``
        - ``UsernameOccupied``
        - ``...``
    - InternalServerError
        - ``RpcCallFail``
        - ``InterDcCallError``
        - ``...``
    - ``...``

.. _Errors: api/errors

Unknown Errors
--------------

In case Pyrogram does not know anything about a specific error yet, it raises a generic error from its known category,
for example, an unknown error with error code ``400``, will be raised as a ``BadRequest``. This way you can catch the
whole category of errors and be sure to also handle these unknown errors.

.. admonition :: RPC Errors
    :class: tip
    
    There isn't any official list of all possible RPC errors, so the list of known errors is provided on a best-effort basis. When new methods are available, the list may be lacking since we simply don't know what errors can raise from them. Pyrogram creates an `unknown_errors.txt` file in the root directory from where the `Client` is run.

.. admonition :: `... <https://t.me/pyrogramchat/607757>`__

    If you want the file to be created in a different location, set the ``PYROGRAM_LOG_UNKNOWN_ERRORS_FILENAME`` to an absolute file path of your choice.


Errors with Values
------------------

Exception objects may also contain some informative values. For example, ``FloodWait`` holds the amount of seconds you
have to wait before you can try again, some other errors contain the DC number on which the request must be repeated on.
The value is stored in the ``value`` attribute of the exception object:

.. code-block:: python

    import asyncio
    from pyrogram.errors import FloodWait

    ...
        try:
            ...  # Your code
        except FloodWait as e:
            await asyncio.sleep(e.value)  # Wait N seconds before continuing
    ...
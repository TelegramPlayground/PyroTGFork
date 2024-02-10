RPC Errors
==========

All Pyrogram API errors live inside the ``errors`` sub-package: ``pyrogram.errors``.
The errors ids listed here are shown as *UPPER_SNAKE_CASE*, but the actual exception names to import from Pyrogram
follow the usual *PascalCase* convention.

.. code-block:: python

    from pyrogram.errors import FloodWait

    try:
        ...
    except FloodWait as e:
        ...

.. hlist::
    :columns: 1

    - :doc:`see-other`
    - :doc:`bad-request`
    - :doc:`unauthorized`
    - :doc:`forbidden`
    - :doc:`not-acceptable`
    - :doc:`flood`
    - :doc:`internal-server-error`

.. toctree::
    :hidden:

    see-other
    bad-request
    unauthorized
    forbidden
    not-acceptable
    flood
    internal-server-error

.. admonition :: RPC Errors
    :class: tip
    
    There isn't any official list of all possible RPC errors, so the list of known errors is provided on a best-effort basis. When new methods are available, the list may be lacking since we simply don't know what errors can raise from them. Pyrogram creates an `unknown_errors.txt` file in the root directory from where the `Client` is run.

.. admonition :: PLEASE DO NOT DO THIS

    .. tip::

        If you do not want this file to be created, set the `PYROGRAM_DONOT_LOG_UNKNOWN_ERRORS` environment variable before running the Pyrogram `Client`.

    .. tip::

        If you want the file to be created in a different location, set the `PYROGRAM_LOG_UNKNOWN_ERRORS_FILENAME` to a file path of your choice.

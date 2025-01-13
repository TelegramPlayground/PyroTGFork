Install Guide
=============

Being a modern Python framework, Pyrogram requires an up to date version of Python to be installed in your system.
We recommend using the latest versions of both Python 3 and pip.


-----

Install Pyrogram
----------------

Bleeding Edge
-------------

You can install the development version from the git appropriate branch using this command:

    .. code-block:: text

        $ pip uninstall -y pyrogram && pip install pyrotgfork

-   or, with :doc:`TgCrypto <../topics/speedups>` as extra requirement (recommended):

    .. code-block:: text

        $ pip install pyrotgfork[fast]

Verifying
---------

To verify that Pyrogram is correctly installed, open a Python shell and import it.
If no error shows up you are good to go.

.. parsed-literal::

    >>> from pyrogram import __version__
    >>> __version__
    '2.0.106-TL-158'

.. _`Github repo`: http://github.com/TelegramPlayGround/pyrogram

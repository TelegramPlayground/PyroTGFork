Available Methods
=================

This page is about Pyrogram methods. All the methods listed here are bound to a :class:`~pyrogram.Client` instance,
except for :meth:`~pyrogram.idle()` and :meth:`~pyrogram.compose()`, which are special functions that can be found in
the main package directly.

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")

    with app:
        app.send_message(chat_id="me", text="hi")

-----

.. currentmodule:: pyrogram.Client

Utilities
---------

.. autosummary::
    :nosignatures:

    {utilities}

.. toctree::
    :hidden:

    {utilities}

.. currentmodule:: pyrogram

.. autosummary::
    :nosignatures:

    idle
    compose

.. toctree::
    :hidden:

    idle
    compose

.. currentmodule:: pyrogram.Client

Authorization
-------------

.. autosummary::
    :nosignatures:

    {authorization}

.. toctree::
    :hidden:

    {authorization}

Messages
--------

.. autosummary::
    :nosignatures:

    {messages}

.. toctree::
    :hidden:

    {messages}

Chats
-----

.. autosummary::
    :nosignatures:

    {chats}

.. toctree::
    :hidden:

    {chats}

Invite Links
------------

.. autosummary::
    :nosignatures:

    {invite_links}

.. toctree::
    :hidden:

    {invite_links}

Chat Forum Topics
-----

.. autosummary::
    :nosignatures:

    {chat_topics}

.. toctree::
    :hidden:

    {chat_topics}

Users
-----

.. autosummary::
    :nosignatures:

    {users}

.. toctree::
    :hidden:

    {users}

Contacts
--------

.. autosummary::
    :nosignatures:

    {contacts}

.. toctree::
    :hidden:

    {contacts}

Password
--------

.. autosummary::
    :nosignatures:

    {password}

.. toctree::
    :hidden:

    {password}

Bots
----

.. autosummary::
    :nosignatures:

    {bots}

.. toctree::
    :hidden:

    {bots}

Stickers
--------

.. autosummary::
    :nosignatures:

    {stickers}

.. toctree::
    :hidden:

    {stickers}

Stories
--------

.. autosummary::
    :nosignatures:

    {stories}

.. toctree::
    :hidden:

    {stories}

Payments
---------

.. autosummary::
    :nosignatures:

    {payments}

.. toctree::
    :hidden:

    {payments}

Phone
--------

.. autosummary::
    :nosignatures:

    {phone}

.. toctree::
    :hidden:

    {phone}

Advanced
--------

Methods used only when dealing with the raw Telegram API.
Learn more about how to use the raw API at :doc:`Advanced Usage <../../topics/advanced-usage>`.

.. autosummary::
    :nosignatures:

    {advanced}

.. toctree::
    :hidden:

    {advanced}

raw_updates
===========

This example shows how to handle raw updates.

.. include:: /_includes/usable-by/users-bots.rst

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")


    @app.on_raw_update()
    async def raw(client, update, users, chats):
        print(update)


    app.run()  # Automatically start() and idle()

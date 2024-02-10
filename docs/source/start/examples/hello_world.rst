hello_world
===========

This example demonstrates a basic API usage

.. include:: /_includes/usable-by/users.rst

.. code-block:: python

    from pyrogram import Client

    # Create a new Client instance
    app = Client("my_account")


    async def main():
        async with app:
            # Send a message, Markdown is enabled by default
            await app.send_message(chat_id="me", text="Hi there! I'm using **Pyrogram**")


    app.run(main())

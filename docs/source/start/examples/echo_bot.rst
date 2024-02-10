echo_bot
========

This simple echo bot replies to every private text message.

It uses the :meth:`~pyrogram.Client.on_message` decorator to register a :obj:`~pyrogram.handlers.MessageHandler` and applies two filters on it:
``filters.text`` and ``filters.private`` to make sure it will reply to private text messages only.

.. include:: /_includes/usable-by/users-bots.rst

.. code-block:: python

    from pyrogram import Client, filters

    app = Client("my_account")


    @app.on_message(filters.text & filters.private)
    async def echo(client, message):
        await message.reply(message.text)


    app.run()  # Automatically start() and idle()

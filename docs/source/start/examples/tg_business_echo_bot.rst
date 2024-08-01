business_echo_bot
==================

This simple echo bot replies to every private business message.

It uses the :meth:`~pyrogram.Client.on_message` decorator to register a :obj:`~pyrogram.handlers.MessageHandler` and applies two filters on it:
``filters.tg_business`` and ``filters.private`` to make sure it will reply to private business messages only.

.. include:: /_includes/usable-by/bots.rst

.. code-block:: python

    from pyrogram import Client, filters

    app = Client("my_account")


    @app.on_message(filters.tg_business & filters.private)
    async def echo(client, message):
        await message.copy(message.chat.id)


    app.run()  # Automatically start() and idle()


You can explore more :doc:`advanced usages <../../topics/advanced-usage>` by directly working with the **raw Telegram API**.

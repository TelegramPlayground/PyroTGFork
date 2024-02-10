callback_queries
================

This example shows how to handle callback queries, i.e.: queries coming from inline button presses.
It uses the :meth:`~pyrogram.Client.on_callback_query` decorator to register a :obj:`~pyrogram.handlers.CallbackQueryHandler`.

.. include:: /_includes/usable-by/bots.rst

.. code-block:: python

    from pyrogram import Client

    app = Client("my_bot", bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")


    @app.on_callback_query()
    async def answer(client, callback_query):
        await callback_query.answer(
            f"Button contains: '{callback_query.data}'",
            show_alert=True)


    app.run()  # Automatically start() and idle()
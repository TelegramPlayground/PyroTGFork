send_voice
===========

.. include:: /_includes/usable-by/users-bots.rst

.. code-block:: python

    from pyrogram import Client, filters

    app = Client("my_account")

    @app.on_message(filters.audio)
    async def re_upload_as_voice(client, message):
        # Downlaod the Voice
        o = await message.download()
        # Re Upload the Audio as Telegram Voice Message
        await message.reply_voice(o, waveform=b'\xff\xbf\xf7\xde\xff\xcf\xbd\xbd\xf7\xfb\xff\xff\xff\xde{\xff?\xf7\xf6\xde\xef\xff\xff\xff{\xef\xfd\xff\xdc\xdb{\xbf\xff\xff\xff\xef\xbd\xf7\xffso\xef\xfd\xfe\xff')

    app.run()  # Automatically start() and idle()

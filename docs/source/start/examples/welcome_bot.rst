welcome_bot
===========

This example uses the ``emoji`` module to easily add emoji in your text messages and ``filters``
to make it only work for specific messages in a specific chat.

.. include:: /_includes/usable-by/bots.rst

.. code-block:: python

    from pyrogram import Client, emoji, filters

    # Target chat. Can also be a list of multiple chat ids/usernames
    TARGET = -100123456789
    # Welcome message template
    MESSAGE = "{} Welcome to [Pyrogram](https://telegramplayground.github.io/pyrogram/)'s group chat {}!"

    app = Client("my_account")


    # Filter in only new_chat_members updates generated in TARGET chat
    @app.on_chat_member_updated(filters.chat(TARGET))
    async def welcome(client, chat_member_updated):
        if chat_member_updated.old_chat_member:
            return # it's not a new join
        # Build the new members list (with mentions) by using their first_name
        new_member = chat_member_updated.new_chat_member.user.mention
        added_by = message.from_user.id  # is equal to new_member if user wasn't added
        # Build the welcome message by using an emoji and the list we built above
        text = MESSAGE.format(emoji.SPARKLES, new_member)
        # send a message to the chat
        await client.send_message(
            chat_id=chat_member_updated.chat.id,
            text=text
        )

    app.run()  # Automatically start() and idle()

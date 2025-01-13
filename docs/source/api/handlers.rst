Update Handlers
===============

Handlers are used to instruct Pyrogram about which kind of updates you'd like to handle with your callback functions.
For a much more convenient way of registering callback functions have a look at :doc:`Decorators <decorators>` instead.

.. code-block:: python

    from pyrogram import Client
    from pyrogram.handlers import MessageHandler

    app = Client("my_account")


    def dump(client, message):
        print(message)


    app.add_handler(MessageHandler(dump))

    app.run()


-----

.. currentmodule:: pyrogram.handlers

Index
-----

.. hlist::
    :columns: 3

    - :class:`MessageHandler`
    - :class:`EditedMessageHandler`
    - :class:`BusinessBotConnectionHandler`
    - :class:`MessageReactionUpdatedHandler`
    - :class:`MessageReactionCountUpdatedHandler`
    - :class:`InlineQueryHandler`
    - :class:`ChosenInlineResultHandler`
    - :class:`CallbackQueryHandler`
    - :class:`ShippingQueryHandler`
    - :class:`PreCheckoutQueryHandler`
    - :class:`PurchasedPaidMediaHandler`
    - :class:`PollHandler`

    - :class:`ChatMemberUpdatedHandler`
    - :class:`ChatJoinRequestHandler`


    - :class:`DeletedMessagesHandler`
    - :class:`UserStatusHandler`
    - :class:`DisconnectHandler`
    - :class:`StoryHandler`
    - :class:`RawUpdateHandler`

-----

Details
-------

.. Handlers
.. autoclass:: MessageHandler()
.. autoclass:: EditedMessageHandler()
.. autoclass:: BusinessBotConnectionHandler()
.. autoclass:: MessageReactionUpdatedHandler()
.. autoclass:: MessageReactionCountUpdatedHandler()
.. autoclass:: InlineQueryHandler()
.. autoclass:: ChosenInlineResultHandler()
.. autoclass:: CallbackQueryHandler()
.. autoclass:: ShippingQueryHandler()
.. autoclass:: PreCheckoutQueryHandler()
.. autoclass:: PurchasedPaidMediaHandler()
.. autoclass:: PollHandler()

.. autoclass:: ChatMemberUpdatedHandler()
.. autoclass:: ChatJoinRequestHandler()


.. autoclass:: DeletedMessagesHandler()
.. autoclass:: UserStatusHandler()
.. autoclass:: DisconnectHandler()
.. autoclass:: StoryHandler()
.. autoclass:: RawUpdateHandler()

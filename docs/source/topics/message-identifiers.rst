Message identifiers
===========================

This is an in-depth explanation (`copied <https://docs.telethon.dev/en/v2/concepts/messages.html#message-identifiers>`_) for how the :obj:`pyrogram.types.Message` ``id`` works.

.. note::

    You can safely skip this section if you're not interested.

Every account, whether it's an user account or bot account, has its own message counter.
This counter starts at 1, and is incremented by 1 every time a new message is received.
In private conversations or small groups, each account will receive a copy each message.
The message identifier will be based on the message counter of the receiving account.

In megagroups and broadcast channels, the message counter instead belongs to the channel itself.
It also starts at 1 and is incremented by 1 for every message sent to the group or channel.
This means every account will see the same message identifier for a given mesasge in a group or channel.

This design has the following implications:

* The message identifier alone is enough to uniquely identify a message only if it's not from a megagroup or channel.
  This is why :obj:`~pyrogram.handlers.DeletedMessagesHandler` does not need to (and doesn't always) include chat information.
* Messages cannot be deleted for one-side only in megagroups or channels.
  Because every account shares the same identifier for the message, it cannot be deleted only for some.
* Links to messages only work for everyone inside megagroups or channels.
  In private conversations and small groups, each account will have their own counter, and the identifiers won't match.

Let's look at a concrete example.

* You are logged in as User-A.
* Both User-B and User-C are your mutual contacts.
* You have share a small group called Group-S with User-B.
* You also share a megagroup called Group-M with User-C.


.. figure:: https://te.legra.ph/file/110b577d4511bb978cc96.png
    :align: center


Every account and channel has just been created.
This means everyone has a message counter of one.

First, User-A will sent a welcome message to both User-B and User-C::

..
    User-A → User-B: Hey, welcome!

    User-A → User-C: ¡Bienvenido!

* For User-A, "Hey, welcome!" will have the message identifier 1. The message with "¡Bienvenido!" will have an ID of 2.
* For User-B, "Hey, welcome" will have ID 1.
* For User-B, "¡Bienvenido!" will have ID 1.

.. csv-table:: Message identifiers
   :header: "Message", "User-A", "User-B", "User-C", "Group-S", "Group-M"

   "Hey, welcome!", 1, 1, "", "", ""
   "¡Bienvenido!", 2, "", 1, "", ""

Next, User-B and User-C will respond to User-A::

..
    User-B → User-A: Thanks!

    User-C → User-A: Gracias :)

.. csv-table:: Message identifiers
   :header: "Message", "User-A", "User-B", "User-C", "Group-S", "Group-M"

   "Hey, welcome!", 1, 1, "", "", ""
   "¡Bienvenido!", 2, "", 1, "", ""
   "Thanks!", 3, 2, "", "", ""
   "Gracias :)", 4, "", 2, "", ""

Notice how for each message, the counter goes up by one, and they are independent.

Let's see what happens when User-B sends a message to Group-S::

..
    User-B → Group-S: Nice group

.. csv-table:: Message identifiers
   :header: "Message", "User-A", "User-B", "User-C", "Group-S", "Group-M"

   "Hey, welcome!", 1, 1, "", "", ""
   "¡Bienvenido!", 2, "", 1, "", ""
   "Thanks!", 3, 2, "", "", ""
   "Gracias :)", 4, "", 2, "", ""
   "Nice group", 5, 3, "", "", ""

While the message was sent to a different chat, the group itself doesn't have a counter.
The message identifiers are still unique for each account.
The chat where the message was sent can be completely ignored.

Megagroups behave differently::

..
    User-C → Group-M: Buen grupo

.. csv-table:: Message identifiers
   :header: "Message", "User-A", "User-B", "User-C", "Group-S", "Group-M"

   "Hey, welcome!", 1, 1, "", "", ""
   "¡Bienvenido!", 2, "", 1, "", ""
   "Thanks!", 3, 2, "", "", ""
   "Gracias :)", 4, "", 2, "", ""
   "Nice group", 5, 3, "", "", ""
   "Buen grupo", "", "", "", "", 1

The group has its own message counter.
Each user won't get a copy of the message with their own identifier, but rather everyone sees the same message.

For scheduled messages, the ``message_id`` is equal to the ID of the message in the schedule queue for the current chat (each PM, chat, supergroup and channel has its own schedule queue and ID sequence). This counter is distinct from the message counter of the normal messages. Since December 1, 2024, scheduled messages can also have messages automatically scheduled by server, to generate alternative qualities for videos in **big** channels. You can distinguish the messages manually scheduled by the user and that automatically scheduled by the server using the :obj:`~pyrogram.raw.types.Message.video_processing_pending` parameter. `Read More <https://core.telegram.org/api/scheduled-messages>`__

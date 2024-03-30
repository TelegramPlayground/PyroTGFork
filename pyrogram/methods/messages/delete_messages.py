#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union, Iterable

import pyrogram
from pyrogram import raw


class DeleteMessages:
    async def delete_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]],
        revoke: bool = True,
        is_scheduled: bool = False
    ) -> int:
        """Delete messages, including service messages, with the following limitations:

        - **For BOTS Only**: A message can only be deleted if it was sent less than 48 hours ago.
        - Service messages about a supergroup, channel, or forum topic creation can't be deleted.
        - A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.
        - :obj:`~pyrogram.Client` can delete outgoing messages in private chats, groups, and supergroups.
        - :obj:`~pyrogram.Client` can delete incoming messages in private chats.
        - :obj:`~pyrogram.Client` granted can_post_messages permissions can delete outgoing messages in channels.
        - If the :obj:`~pyrogram.Client` is an administrator of a group, it can delete any message there.
        - If the :obj:`~pyrogram.Client` has can_delete_messages permission in a supergroup or a channel, it can delete any message there.

        Use this method to delete multiple messages simultaneously.
        If some of the specified messages can't be found, they are skipped.

        .. include:: /_includes/usable-by/users-bots.rst

        Please be aware about using the correct :doc:`Message Identifiers <../../topics/message-identifiers>`, specifically when using the ``is_scheduled`` parameter.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_ids (``int`` | Iterable of ``int``):
                An iterable of message identifiers to delete (integers) or a single message id.

            revoke (``bool``, *optional*):
                Deletes messages on both parts.
                This is only for private cloud chats and normal groups, messages on
                channels and supergroups are always revoked (i.e.: deleted for everyone).
                Defaults to True.

            is_scheduled (``bool``, *optional*):
                True, if the specified ``message_ids`` refers to a scheduled message. Defaults to False.

        Returns:
            ``int``: Amount of affected messages

        Example:
            .. code-block:: python

                # Delete one message
                await app.delete_messages(chat_id, message_id)

                # Delete multiple messages at once
                await app.delete_messages(chat_id, list_of_message_ids)

                # Delete messages only on your side (without revoking)
                await app.delete_messages(chat_id, message_id, revoke=False)
        """
        peer = await self.resolve_peer(chat_id)
        message_ids = list(message_ids) if not isinstance(message_ids, int) else [message_ids]

        if is_scheduled:
            r = await self.invoke(
                raw.functions.messages.DeleteScheduledMessages(
                    peer=peer,
                    id=message_ids
                )
            )
            for i in r.updates:
                if isinstance(i, raw.types.UpdateDeleteScheduledMessages):
                    return len(i.messages)
        else:
            if isinstance(peer, raw.types.InputPeerChannel):
                r = await self.invoke(
                    raw.functions.channels.DeleteMessages(
                        channel=peer,
                        id=message_ids
                    )
                )
            else:
                r = await self.invoke(
                    raw.functions.messages.DeleteMessages(
                        id=message_ids,
                        revoke=revoke
                    )
                )

            return r.pts_count

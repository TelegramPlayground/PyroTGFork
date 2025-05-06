#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present <https://github.com/TelegramPlayGround>
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

from datetime import datetime
import logging
from typing import Optional, Union

import pyrogram
from pyrogram import raw, utils

log = logging.getLogger(__name__)


class DeleteChatHistory:
    async def delete_chat_history(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        max_id: Optional[int] = 0,
        # TODO
        revoke: Optional[bool] = None,
        just_clear: Optional[bool] = None,
        min_date: Optional[datetime] = None,
        max_date: Optional[datetime] = None
    ) -> int:
        """Deletes all messages in the chat. For group chats this will release the usernames and remove all members.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            max_id (``int``, *optional*):
                Maximum ID of message to delete.
                Defaults to 0.

            revoke (``bool``, *optional*):
                Pass True to delete messages for all chat members.
                Always True if using in :obj:`~pyrogram.enums.ChatType.CHANNEL` and :obj:`~pyrogram.enums.ChatType.SUPERGROUP` chats.

            just_clear (``bool``, *optional*):
                Pass True to clear history for the current user, without actually removing chat.
                For :obj:`~pyrogram.enums.ChatType.PRIVATE` and :obj:`~pyrogram.enums.ChatType.GROUP` chats only.

            min_date (:py:obj:`~datetime.datetime`, *optional*):
                The minimum date of the messages to delete.
                Delete all messages newer than this time.
                For :obj:`~pyrogram.enums.ChatType.PRIVATE` and :obj:`~pyrogram.enums.ChatType.GROUP` chats only.

            max_date (:py:obj:`~datetime.datetime`, *optional*):
                The maximum date of the messages to delete.
                Delete all messages older than this time.
                For :obj:`~pyrogram.enums.ChatType.PRIVATE` and :obj:`~pyrogram.enums.ChatType.GROUP` chats only.

        Returns:
            ``int``: Amount of affected messages

        Example:
            .. code-block:: python

                # Delete all messages in channel
                await app.delete_chat_history(chat_id, revoke=True)

        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.DeleteHistory(
                    channel=raw.types.InputChannel(
                        channel_id=peer.channel_id,
                        access_hash=peer.access_hash
                    ),
                    max_id=max_id,
                    for_everyone=revoke
                )
            )
        else:
            r = await self.invoke(
                raw.functions.messages.DeleteHistory(
                    peer=peer,
                    max_id=max_id,
                    just_clear=just_clear,
                    revoke=revoke,
                    min_date=utils.datetime_to_timestamp(min_date),
                    max_date=utils.datetime_to_timestamp(max_date)
                )
            )

        return len(r.updates[0].messages) if isinstance(peer, raw.types.InputPeerChannel) else r.pts_count

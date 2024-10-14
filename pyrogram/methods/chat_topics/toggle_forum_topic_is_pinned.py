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

import pyrogram
from pyrogram import raw
from typing import Union


class ToggleForumTopicIsPinned:
    async def toggle_forum_topic_is_pinned(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_thread_id: int,
        is_pinned: bool
    ) -> bool:
        """Changes the pinned state of a forum topic; requires can_manage_topics right in the supergroup. There can be up to ``pinned_forum_topic_count_max`` pinned forum topics.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_thread_id (``int``):
                Unique identifier for the target message thread of the forum topic.

            is_pinned (``bool``):
                Pass True to pin the topic; pass False to unpin it.

        Returns:
            ``bool``: On success, True is returned.

        Raises:
            RPCError: In case of invalid arguments.

        Example:
            .. code-block:: python

                await app.toggle_forum_topic_is_pinned(chat_id, topic_id, True)
        """
        await self.invoke(
            raw.functions.channels.UpdatePinnedForumTopic(
                channel=await self.resolve_peer(chat_id),
                topic_id=message_thread_id,
                pinned=is_pinned
            )
        )

        return True

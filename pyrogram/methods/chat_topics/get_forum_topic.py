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

import logging
from typing import Union, List, Iterable

import pyrogram
from pyrogram import raw
from pyrogram import types

log = logging.getLogger(__name__)


class GetForumTopic:
    async def get_forum_topic(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_thread_ids: Union[int, Iterable[int]]
    ) -> Union["types.ForumTopic", List["types.ForumTopic"]]:
        """Get one or more topic from a chat by using topic identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_thread_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single message thread identifier or an iterable of message thread identifiers (as integers) to get the information of the topic themselves.

        Returns:
            :obj:`~pyrogram.types.ForumTopic` | List of :obj:`~pyrogram.types.ForumTopic`: In case *message_thread_ids* was not
            a list, a single topic is returned, otherwise a list of topics is returned.

        Example:
            .. code-block:: python

                # Get one topic
                await app.get_forum_topic(chat_id, 12345)

                # Get more than one topic (list of topics)
                await app.get_forum_topic(chat_id, [12345, 12346])

        Raises:
            ValueError: In case of invalid arguments.
        """
        is_iterable = not isinstance(message_thread_ids, int)
        ids = list(message_thread_ids) if is_iterable else [message_thread_ids]

        r = await self.invoke(
            raw.functions.channels.GetForumTopicsByID(
                channel=await self.resolve_peer(chat_id),
                topics=ids
            )
        )
        # TODO order_by_create_date:flags.0?true count:int pts:int

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        messages = {}
        for message in getattr(r, "messages", []):
            messages[message.id] = await types.Message._parse(
                self, message, users, chats, replies=0
            )

        topics = types.List()
        for i in getattr(r, "topics"):
            topics.append(
                types.ForumTopic._parse(
                    self, i, messages, users, chats
                )
            )

        return topics if is_iterable else topics[0] if topics else None

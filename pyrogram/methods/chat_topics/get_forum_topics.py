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

from asyncio import sleep
from datetime import datetime
from typing import Union, AsyncGenerator

import pyrogram
from pyrogram import types, raw, utils


class GetForumTopics:
    async def get_forum_topics(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        query: str = "",
        offset_date: datetime = utils.zero_datetime(),
        offset_message_id: int = 0,
        offset_message_thread_id: int = 0,
        limit: int = 0
    ) -> AsyncGenerator["types.ForumTopic", None]:
        """Get one or more topic from a chat.
        Returns found forum topics in a forum chat.
        This is a temporary method for getting information about topic list from the server

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            query (``str``, *optional*):
                Query to search for in the forum topic's name

            offset_date (:py:obj:`~datetime.datetime`, *optional*):
                The date starting from which the results need to be fetched. Use 0 or any date in the future to get results from the last topic

            offset_message_id (``int``, *optional*):
                The message identifier of the last message in the last found topic, or 0 for the first request

            offset_message_thread_id (``int``, *optional*):
                The message thread identifier of the last found topic, or 0 for the first request

            limit (``int``, *optional*):
                The maximum number of forum topics to be returned; up to 100.
                For optimal performance, the number of returned forum topics is chosen by Telegram Server and can be smaller than the specified limit
                By default, no limit is applied and all topics are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.ForumTopic` objects.

        Example:
            .. code-block:: python

                # Iterate through all topics
                async for topic in app.get_forum_topics(chat_id):
                    print(topic)
        """
        current = 0
        total = limit or (1 << 31) - 1
        limit = min(100, total)

        offset_date = utils.datetime_to_timestamp(offset_date)

        while True:
            r = await self.invoke(
                raw.functions.channels.GetForumTopics(
                    channel=await self.resolve_peer(chat_id),
                    offset_date=offset_date,
                    offset_id=offset_message_id,
                    offset_topic=offset_message_thread_id,
                    limit=limit
                )
            )

            users = {i.id: i for i in r.users}
            chats = {i.id: i for i in r.chats}
            messages = {}

            for message in getattr(r, "messages", []):
                if isinstance(message, raw.types.MessageEmpty):
                    continue

                messages[message.id] = await types.Message._parse(
                    self,
                    message,
                    users,
                    chats,
                    replies=self.fetch_replies
                )

            topics = []

            for topic in getattr(r, "topics", []):
                topics.append(
                    types.ForumTopic._parse(
                        self, topic, messages, users, chats
                    )
                )

            if not topics:
                return

            last = topics[-1]

            offset_message_id = last.last_message.id
            # TODO: fix inconsistency
            offset_date = utils.datetime_to_timestamp(
                last.last_message.date
            )
            offset_message_thread_id = last.message_thread_id

            for topic in topics:
                await sleep(0)
                yield topic

                current += 1

                if current >= total:
                    return

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

from asyncio import sleep
from typing import AsyncGenerator, Union

import pyrogram
from pyrogram import raw, types


class GetChatArchivedStories:
    async def get_chat_archived_stories(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        from_story_id: int = 0,
        limit: int = 0,
    ) -> AsyncGenerator["types.Story", None]:
        """Get all archived stories from a chat by using chat identifier.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            from_story_id (``int``, *optional*):
                Identifier of the story starting from which stories must be returned; use 0 to get results from the last story.

            limit (``int``, *optional*):
                The maximum number of stories to be returned..
                By default, no limit is applied and optimal number of stories chosen by Telegram Server is returned which can be smaller than the specified limit.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Story` objects.

        Example:
            .. code-block:: python

                # Get archived stories from specific chat
                async for story in app.get_chat_archived_stories(chat_id):
                    print(story)
        """
        current = 0
        total = abs(limit) or (1 << 31)
        limit = min(100, total)

        while True:
            peer = await self.resolve_peer(chat_id)
            r = await self.invoke(
                raw.functions.stories.GetStoriesArchive(
                    peer=peer,
                    offset_id=from_story_id,
                    limit=limit
                )
            )

            stories = r.stories

            if not stories:
                return

            last = stories[-1]
            from_story_id = last.id

            users = {i.id: i for i in r.users}
            chats = {i.id: i for i in r.chats}

            for story in stories:
                await sleep(0)
                yield await types.Story._parse(
                    self,
                    users,
                    chats,
                    None, None, None,
                    # TODO
                    story,
                    None, #
                    # TODO
                )

                current += 1

                if current >= total:
                    return

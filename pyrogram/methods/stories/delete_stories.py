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

from typing import Union, Iterable

import pyrogram
from pyrogram import raw, types, utils


class DeleteStories:
    async def delete_stories(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        story_ids: Union[int, Iterable[int]],
    ) -> list[int]:
        """Deletes a previously sent story.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".

            story_ids (``int`` | Iterable of ``int``, *optional*):
                Unique identifier (int) or list of unique identifiers (list of int) for the target stories.

        Returns:
            List of ``int``: List of deleted stories IDs.

        Example:
            .. code-block:: python

                # Delete a single story
                app.delete_stories(chat_id, 1)

                # Delete multiple stories
                app.delete_stories(chat_id, [1, 2])

        """
        is_iterable = utils.is_list_like(story_ids)
        ids = list(story_ids) if is_iterable else [story_ids]
        r = await self.invoke(
            raw.functions.stories.DeleteStories(
                peer=await self.resolve_peer(chat_id),
                id=ids
            )
        )
        return types.List(r)


    async def delete_business_story(
        self: "pyrogram.Client",
        business_connection_id: str,
        story_id: int,
    ) -> list[int]:
        """Deletes a story previously posted by the bot on behalf of a managed business account.
        
        Requires the can_manage_stories business bot right.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            business_connection_id (``str``):
                Unique identifier of the business connection.
            
            story_id (``int``):
                Unique identifier of the story to delete.
        
        Returns:
            List of ``int``: List of deleted stories IDs.

        """
        if not business_connection_id:
            raise ValueError("business_connection_id is required")

        business_connection = self.business_user_connection_cache[business_connection_id]
        if business_connection is None:
            business_connection = await self.get_business_connection(business_connection_id)
        return await self.delete_stories(
            chat_id=business_connection.user_chat_id,
            story_ids=story_id
        )

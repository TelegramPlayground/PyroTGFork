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
from pyrogram import raw, types, utils


class GetStories:
    async def get_stories(
        self: "pyrogram.Client",
        story_sender_chat_id: Union[int, str],
        story_ids: Union[int, Iterable[int]],
    ) -> Union["types.Story", list["types.Story"]] :
        """Get one or more stories from a chat by using stories identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            story_sender_chat_id (``int`` | ``str``):
                Identifier of the chat that posted the story.

            story_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single story identifier or an iterable of story ids (as integers) to get the content of the
                story themselves.

        Returns:
            :obj:`~pyrogram.types.Story` | List of :obj:`~pyrogram.types.Story`: In case *story_ids* was not
            a list, a single story is returned, otherwise a list of stories is returned.

        Example:
            .. code-block:: python

                # Get stories by id
                stories = await app.get_stories(
                    story_sender_chat_id,
                    [1, 2, 3]
                )

                for story in stories:
                    print(story)
        """

        is_iterable = utils.is_list_like(story_ids)
        ids = list(story_ids) if is_iterable else [story_ids]

        peer = await self.resolve_peer(story_sender_chat_id)
        r = await self.invoke(
            raw.functions.stories.GetStoriesByID(
                peer=peer,
                id=ids
            )
        )

        stories = []

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        for story in r.stories:
            stories.append(
                await types.Story._parse(
                    self,
                    users,
                    chats,
                    None, None, None,
                    # TODO
                    story,
                    None, #
                    # TODO
                )
            )

        return types.List(stories) if is_iterable else stories[0] if stories else None

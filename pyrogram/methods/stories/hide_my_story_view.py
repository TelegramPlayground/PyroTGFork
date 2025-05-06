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

from typing import Optional, Union

import pyrogram
from pyrogram import raw, types


class HideMyStoryView:
    async def hide_my_story_view(
        self: "pyrogram.Client",
        past: Optional[bool] = True,
        future: Optional[bool] = True,
    ) -> Union["types.StoryStealthMode", bool]:
        """Activates stealth mode for stories, which hides all views of stories from the current user in the last "stories_stealth_past_period" seconds and for the next "stories_stealth_future_period" seconds; for Telegram Premium users only.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            past (``bool``, *optional*):
                Pass True to erase views from any stories opened in the past stories_stealth_past_period seconds, as specified by the client configuration.

            future (``bool``, *optional*):
                Pass True to hide future story views for the next stories_stealth_future_period seconds, as specified by the client configuration.

        Returns:
            :obj:`~pyrogram.types.StoryStealthMode`: On success, the information about stealth mode session is returned.

        Example:
            .. code-block:: python

                # Erase and hide story views in the past stories_stealth_past_period and the next stories_stealth_future_period seconds
                await app.hide_my_story_view()

        Raises:
            RPCError: In case of Telegram RPCError.

        """

        r = await self.invoke(
            raw.functions.stories.ActivateStealthMode(
                past=past,
                future=future
            )
        )
        for i in r.updates:
            if isinstance(i, raw.types.UpdateStoriesStealthMode):
                return types.StoryStealthMode._parse(i.stealth_mode)
        return False

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

from typing import Optional

import pyrogram
from pyrogram import types, raw

from .story_area_type import StoryAreaType


class StoryAreaTypeSuggestedReaction(StoryAreaType):
    """This object describes a story area pointing to a suggested reaction. Currently, a story can have up to 5 suggested reaction areas.

    Parameters:
        reaction_type (:obj:`~pyrogram.types.ReactionType`):
            Type of the reaction.

        is_dark (``bool``, *optional*):
            Pass True if the reaction area has a dark background.

        is_flipped (``bool``, *optional*):
            Pass True if reaction area corner is flipped.

    """

    def __init__(
        self,
        reaction_type: "types.ReactionType" = None,
        is_dark: Optional[bool] = None,
        is_flipped: Optional[bool] = None,
    ):
        super().__init__()

        self.reaction_type = reaction_type
        self.is_dark = is_dark
        self.is_flipped = is_flipped

    async def write(
        self,
        client: "pyrogram.Client",
        coordinates: "raw.types.MediaAreaCoordinates"
    ):
        return raw.types.MediaAreaSuggestedReaction(
            dark=self.is_dark,
            flipped=self.is_flipped,
            coordinates=coordinates,
            reaction=self.reaction_type.write(client)
        )

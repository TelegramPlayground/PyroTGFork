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

import pyrogram
from pyrogram import raw

from .story_area_type import StoryAreaType


class StoryAreaTypeUniqueGift(StoryAreaType):
    """This object describes a story area pointing to a unique gift. Currently, a story can have at most 1 unique gift area.

    Parameters:
        name (``str``):
            Unique name of the gift.

    """

    def __init__(
        self,
        name: str = None,
    ):
        super().__init__()

        self.name = name

    async def write(
        self,
        client: "pyrogram.Client",
        coordinates: "raw.types.MediaAreaCoordinates"
    ):
        return raw.types.MediaAreaStarGift(
            coordinates=coordinates,
            slug=self.name
        )

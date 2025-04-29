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


class StoryAreaTypeWeather(StoryAreaType):
    """This object describes a story area containing weather information. Currently, a story can have up to 3 weather areas.

    Parameters:
        temperature (``float``):
            Temperature, in degree Celsius.

        emoji (``str``):
            Emoji representing the weather.

        background_color (``int``):
            A color of the area background in the ARGB format.

    """

    def __init__(
        self,
        temperature: float = None,
        emoji: str = None,
        background_color: int = None,
    ):
        super().__init__()

        self.temperature = temperature
        self.emoji = emoji
        self.background_color = background_color

    async def write(
        self,
        client: "pyrogram.Client",
        coordinates: "raw.types.MediaAreaCoordinates"
    ):
        return raw.types.MediaAreaWeather(
            coordinates=coordinates,
            emoji=self.emoji,
            temperature_c=self.temperature,
            color=self.background_color
        )

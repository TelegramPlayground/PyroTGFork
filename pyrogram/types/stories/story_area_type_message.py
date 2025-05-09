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

from typing import Union

import pyrogram
from pyrogram import raw

from .story_area_type import StoryAreaType


class StoryAreaTypeMessage(StoryAreaType):
    """This object describes an area pointing to a message. Currently, a story can have up to 1 message area.

    Parameters:
        chat_id (``int`` | ``str``):
            Unique identifier (int) or username (str) of the target chat.
        
        message_id (``int``):
            Identifier of the message.

    """

    def __init__(
        self,
        chat_id: Union[int, str] = None,
        message_id: int = None,
    ):
        super().__init__()

        self.chat_id = chat_id
        self.message_id = message_id

    async def write(
        self,
        client: "pyrogram.Client",
        coordinates: "raw.types.MediaAreaCoordinates"
    ):
        return raw.types.InputMediaAreaChannelPost(
            coordinates=coordinates,
            channel=await client.resolve_peer(self.chat_id),
            msg_id=self.message_id
        )

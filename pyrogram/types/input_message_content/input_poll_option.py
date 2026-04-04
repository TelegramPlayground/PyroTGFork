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

from typing import Union

import pyrogram
from pyrogram import raw, utils, types
from pyrogram.file_id import FileType

from ..object import Object


class InputPollOption(Object):
    """This object contains information about one answer option in a poll to send.

    Parameters:
        text (:obj:`~pyrogram.types.FormattedText`):
            Option text, 1-100 characters after entity parsing.
            Only custom emoji entities are allowed to be added and only by Premium users.

        animation (``str``, *optional*):
            Pass a file_id as string to send a photo that exists on the Telegram servers.

        photo (``str``, *optional*):
            Pass a file_id as string to send a photo that exists on the Telegram servers.

        sticker (``str``, *optional*):
            Pass a file_id as string to send a photo that exists on the Telegram servers.

        video (``str``, *optional*):
            Pass a file_id as string to send a photo that exists on the Telegram servers.

    """

    def __init__(
        self,
        *,
        text: "types.FormattedText",
        animation: str = None,
        # messageLocation
        photo: str = None,
        sticker: str = None,
        # messageVenue
        video: str = None,
    ):
        super().__init__()

        self.text = text
        self.animation = animation
        # TODO
        self.photo = photo
        self.sticker = sticker
        self.video = video

    async def write(
        self,
        client: "pyrogram.Client",
        idx: int,
    ) -> "raw.types.PollAnswer":
        if isinstance(self.text, str):
            self.text = types.FormattedText(text=self.text)

        media = None
        if self.animation:
            media = utils.get_input_media_from_file_id(self.animation, FileType.ANIMATION)
        elif self.photo:
            media = utils.get_input_media_from_file_id(self.photo, FileType.PHOTO)
        elif self.sticker:
            media = utils.get_input_media_from_file_id(self.sticker, FileType.STICKER)
        elif self.video:
            media = utils.get_input_media_from_file_id(self.video, FileType.VIDEO)
        return raw.types.PollAnswer(
            text=await self.text.write(client),
            media=media,
            option=bytes(idx),
            # added_by:flags.1?Peer
            # date:flags.1?int
        )

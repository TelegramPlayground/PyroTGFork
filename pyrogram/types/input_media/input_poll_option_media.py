#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present <https://github.com/KurimuzonAkuma>
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

import io

from typing import TYPE_CHECKING, Callable, Optional, Union

from ..object import Object

if TYPE_CHECKING:
    from pyrogram import raw, types


class InputPollOptionMedia(Object):
    """Content of a media message to be sent.

    It should be one of:

    - :obj:`~pyrogram.types.InputMediaAnimation`
    - :obj:`~pyrogram.types.InputMediaLivePhoto`
    - :obj:`~pyrogram.types.InputMediaLocation`
    - :obj:`~pyrogram.types.InputMediaPhoto`
    - :obj:`~pyrogram.types.InputMediaVenue`
    - :obj:`~pyrogram.types.InputMediaVideo`

    """

    def __init__(
        self,
        media: Optional[Union[str, "io.BytesIO"]] = None,
        caption: str = "",
        parse_mode: Optional[str] = None,
        caption_entities: Optional[list["types.MessageEntity"]] = None,
    ):
        super().__init__()

        self.media = media
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities

    async def write(
        self,
        client: "pyrogram.Client",
        chat_id: Optional[Union[int, str]] = None,
        business_connection_id: Optional[str] = None,
        progress: Optional[Callable] = None,
        progress_args: tuple = (),
    ) -> tuple["raw.base.InputMedia", bool]:
        raise NotImplementedError

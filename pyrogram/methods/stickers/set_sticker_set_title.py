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

import logging

import pyrogram
from pyrogram import raw

log = logging.getLogger(__name__)


class SetStickerSetTitle:
    async def set_sticker_set_title(
        self: "pyrogram.Client",
        name: str,
        title: str
    ) -> bool:
        """Use this method to set the title of a created sticker set.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            name (``str``):
                Sticker set name.
            
            title (``str``):
                Sticker set title, 1-64 characters.

        Returns:
            ``bool``: True on success.

        Raises:
            RPCError: In case of Telegram RPCError.

        """
        r = await self.invoke(
            raw.functions.stickers.RenameStickerSet(
                stickerset=raw.types.InputStickerSetShortName(
                    short_name=name
                ),
                title=title
            )
        )
        return r

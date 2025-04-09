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
import os

import pyrogram
from pyrogram import enums, raw, types, utils

log = logging.getLogger(__name__)


class UploadStickerFile:
    async def upload_sticker_file(
        self: "pyrogram.Client",
        user_id: int,
        sticker: str,
        sticker_format: "enums.StickerFormat"
    ) -> bool:
        """Use this method to upload a file with a sticker for later use in the :meth:`~pyrogram.Client.create_new_sticker_set`, :meth:`~pyrogram.Client.add_sticker_to_set`, or :meth:`~pyrogram.Client.replace_sticker_in_set` methods (the file can be used multiple times).

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            user_id (``int``):
                User identifier of sticker file owner; ignored for regular users.
            
            sticker (``str``):
                A file with the sticker in .WEBP, .PNG, .TGS, or .WEBM format.
                File to upload; must fit in a 512x512 square. For WEBP stickers the file must be in WEBP or PNG format, which will be converted to WEBP server-side.
                See https://core.telegram.org/animated_stickers#technical-requirements for technical requirements
            
            sticker_format (:obj:`~pyrogram.enums.StickerFormat`):
                Format of the sticker.

        Returns:
            :obj:`~pyrogram.raw.types.InputDocument`: Returns the uploaded :obj:`~pyrogram.types.File` on success. TODO

        Raises:
            RPCError: In case of Telegram RPCError.
            ValueError: In case of invalid arguments.

        """
        mime_type = None
        if sticker_format == enums.StickerFormat.STATIC:
            mime_type = "image/png"
        elif sticker_format == enums.StickerFormat.ANIMATED:
            mime_type = "application/x-tgsticker"
        elif sticker_format == enums.StickerFormat.VIDEO:
            mime_type = "video/webm"
        else:
            raise ValueError("Invalid sticker_format")
        peer = None
        if self.me.is_bot:
            peer = await self.resolve_peer(user_id)
        else:
            peer = await self.resolve_peer("me")
        file = await self.save_file(sticker)
        media = raw.types.InputMediaUploadedDocument(
            mime_type=mime_type,
            file=file,
            attributes=[
                raw.types.DocumentAttributeFilename(
                    file_name=os.path.basename(sticker)
                ),
            ]
        )
        uploaded_media = await self.invoke(
            raw.functions.messages.UploadMedia(
                peer=peer,
                media=media
            )
        )
        return utils.get_input_document(uploaded_media)

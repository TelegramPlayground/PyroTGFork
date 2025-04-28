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
from pyrogram import enums, raw, types
from pyrogram.file_id import FileId, FileType, FileUniqueId, FileUniqueType

log = logging.getLogger(__name__)


class UploadStickerFile:
    async def upload_sticker_file(
        self: "pyrogram.Client",
        user_id: int,
        sticker: str,
        sticker_format: "enums.StickerFormat"
    ) -> "types.File":
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
            :obj:`~pyrogram.types.File`: Returns the uploaded file on success.

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
        media = await self.invoke(
            raw.functions.messages.UploadMedia(
                peer=peer,
                media=media
            )
        )
        media = raw.types.InputMediaDocument(
            id=raw.types.InputDocument(
                id=media.document.id,
                access_hash=media.document.access_hash,
                file_reference=media.document.file_reference
            )
        )
        sticker = media.document
        document_attributes = sticker.attributes
        sticker_attributes = (
            document_attributes[raw.types.DocumentAttributeSticker]
            if raw.types.DocumentAttributeSticker in document_attributes
            else document_attributes[raw.types.DocumentAttributeCustomEmoji]
        )
        file_name = getattr(document_attributes.get(raw.types.DocumentAttributeFilename, None), "file_name", None)
        return types.File(
            file_id=FileId(
                file_type=FileType.STICKER,
                dc_id=sticker.dc_id,
                media_id=sticker.id,
                access_hash=sticker.access_hash,
                file_reference=sticker.file_reference
            ).encode(),
            file_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=sticker.id
            ).encode(),
            file_name=file_name,
            file_size=sticker.size,
        )

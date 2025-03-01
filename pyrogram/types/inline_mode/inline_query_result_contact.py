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

import logging

import pyrogram
from pyrogram import raw, types
from .inline_query_result import InlineQueryResult

log = logging.getLogger(__name__)


class InlineQueryResultContact(InlineQueryResult):
    """Contact with a phone number.
    
    By default, this contact will be sent by the user.
    Alternatively, you can use *input_message_content* to send a message with the specified content instead of the
    contact.
    
    Parameters:
        phone_number (``str``):
            Contact's phone number.

        first_name (``str``):
            Contact's first name.

        last_name (``str``, *optional*):
            Contact's last name.

        vcard (``str``, *optional*):
            Additional data about the contact in the form of a `vCard <https://en.wikipedia.org/wiki/VCard>`_, 0-2048 bytes.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.
            
        input_message_content (:obj:`~pyrogram.types.InputMessageContent`, *optional*):
            Content of the message to be sent instead of the contact.

        thumbnail_url (``str``, *optional*):
            Url of the thumbnail for the result.

        thumbnail_width (``int``, *optional*):
            Thumbnail width.

        thumbnail_height (``int``, *optional*):
            Thumbnail height.
    """

    def __init__(
        self,
        phone_number: str,
        first_name: str,
        last_name: str = "",
        vcard: str = "",
        id: str = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None,
        thumbnail_url: str = None,
        thumbnail_width: int = 0,
        thumbnail_height: int = 0,
        thumb_url: str = None,
        thumb_width: int = None,
        thumb_height: int = None
    ):
        if thumb_url and thumbnail_url:
            raise ValueError(
                "Parameters `thumb_url` and `thumbnail_url` are mutually "
                "exclusive."
            )
        
        if thumb_url is not None:
            log.warning(
                "This property is deprecated. "
                "Please use thumbnail_url instead"
            )
            thumbnail_url = thumb_url
        
        if thumb_width and thumbnail_width:
            raise ValueError(
                "Parameters `thumb_width` and `thumbnail_width` are mutually "
                "exclusive."
            )
        
        if thumb_width is not None:
            log.warning(
                "This property is deprecated. "
                "Please use thumbnail_width instead"
            )
            thumbnail_width = thumb_width
        
        if thumb_height and thumbnail_height:
            raise ValueError(
                "Parameters `thumb_height` and `thumbnail_height` are mutually "
                "exclusive."
            )
        
        if thumb_height is not None:
            log.warning(
                "This property is deprecated. "
                "Please use thumbnail_height instead"
            )
            thumbnail_height = thumb_height

        super().__init__("contact", id, input_message_content, reply_markup)

        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.vcard = vcard
        self.thumbnail_url = thumbnail_url
        self.thumbnail_width = thumbnail_width
        self.thumbnail_height = thumbnail_height

    async def write(self, client: "pyrogram.Client"):
        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.first_name,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaContact(
                    phone_number=self.phone_number,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    vcard=self.vcard,
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None,
                )
            ),
            thumb=raw.types.InputWebDocument(
                url=self.thumbnail_url,
                size=0,
                mime_type="image/jpg",
                attributes=[
                    raw.types.DocumentAttributeImageSize(
                        w=self.thumbnail_width,
                        h=self.thumbnail_height
                    )
                ]
            ) if self.thumbnail_url else None
        )

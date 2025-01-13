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

import pyrogram
from pyrogram import raw, types

from ..object import Object
from .message import Str

class SponsoredMessage(Object):
    """Describes a sponsored message.

    Parameters:
        random_id (``bytes``):
            Message identifier; unique for the chat to which the sponsored message belongs among both ordinary and sponsored messages.

        url (``str``):
            ad url

        title (``str``):
            Title of the sponsored message.
        
        content (``str``):
            sponsored message.

        button_text (``str``):
            Text for the message action button.

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            special entities that appear in the text.

        photo (:obj:`~pyrogram.types.Photo`, *optional*):
            sponsored message photo

        is_recommended (``bool``, *optional*):
            True, if the message needs to be labeled as "recommended" instead of "sponsored".

        can_be_reported (``bool``, *optional*):
            True, if the message can be reported to Telegram moderators through :meth:`~pyrogram.Client.report_chat_sponsored_message`.

        color (:obj:`~pyrogram.types.ChatColor`, *optional*):
            Identifier of the accent color for title, button text and message background.

        sponsor_info (``str``, *optional*):
            Information about the sponsor of the message.

        additional_info (``str``, *optional*):
            If non-empty, additional information about the sponsored message to be shown along with the message.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        random_id: bytes,
        url: str,
        title: str,
        content: str,
        button_text: str,
        entities: list["types.MessageEntity"] = None,
        photo: "types.Photo" = None,
        is_recommended: bool = None,
        can_be_reported: bool = None,
        color: "types.ChatColor" = None,
        sponsor_info: str = None,
        additional_info: str = None
    ):
        super().__init__(client)

        self.random_id = random_id
        self.url = url
        self.title = title
        self.content = content
        self.button_text = button_text
        self.entities = entities
        self.photo = photo
        self.is_recommended = is_recommended
        self.can_be_reported = can_be_reported
        self.color = color
        self.sponsor_info = sponsor_info
        self.additional_info = additional_info

    @staticmethod
    def _parse(client, sponsored_message: "raw.types.SponsoredMessage"):
        entities = [
            types.MessageEntity._parse(client, entity, users)
            for entity in getattr(sponsored_message, "entities", [])
        ]
        entities = types.List(
            filter(lambda x: x is not None, entities)
        )
        return SponsoredMessage(
            random_id=sponsored_message.random_id,
            url=sponsored_message.url,
            title=sponsored_message.title,
            content=Str(sponsored_message.message).init(entities),
            button_text=sponsored_message.button_text,
            photo=types.Photo._parse(client, sponsored_message.photo) if sponsored_message.photo else None,
            is_recommended=sponsored_message.recommended,
            can_be_reported=sponsored_message.can_report,
            entities=entities,
            color=types.ChatColor._parse(sponsored_message.color) if sponsored_message.color else None,
            sponsor_info=getattr(sponsored_message, "sponsor_info", None),
            additional_info=getattr(sponsored_message, "additional_info", None),
            client=client
        )

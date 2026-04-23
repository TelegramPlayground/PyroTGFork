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

import os

import pyrogram
from pyrogram import enums, raw, types, utils

from ..object import Object
from .message import Str


class FormattedText(Object):
    """A text with some entities.

    Parameters:
        text (``str``):
            The text.
            If the message contains entities (bold, italic, ...) you can access *text.markdown* or
            *text.html* to get the marked up message text. In case there are no entities, the fields
            will contain the same text as *text*.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            Parse mode of the text.
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            Entities contained in the text.
            Entities can be nested, but must not mutually intersect with each other.
            :obj:`~pyrogram.enums.MessageEntityType.PRE`, :obj:`~pyrogram.enums.MessageEntityType.CODE` and :obj:`~pyrogram.enums.MessageEntityType.DATE_TIME` entities can't contain other entities.
            :obj:`~pyrogram.enums.MessageEntityType.BLOCKQUOTE` entities can't contain other :obj:`~pyrogram.enums.MessageEntityType.BLOCKQUOTE` entities.
            :obj:`~pyrogram.enums.MessageEntityType.BOLD`, :obj:`~pyrogram.enums.MessageEntityType.ITALIC`, :obj:`~pyrogram.enums.MessageEntityType.UNDERLINE`, :obj:`~pyrogram.enums.MessageEntityType.STRIKETHROUGH`, and :obj:`~pyrogram.enums.MessageEntityType.SPOILER` entities can contain and can be part of any other entities.
            All other entities can't contain each other.

    """

    def __init__(
        self,
        *,
        text: Str,
        parse_mode: "enums.ParseMode" = None,
        entities: list["types.MessageEntity"] = None
    ):
        self.text = text
        self.parse_mode = parse_mode
        self.entities = entities

    def __custom__(self):
        if bool(os.environ.get("PYROGRAM_PRE_BOT_API_7_3", None)):
            return self.text
        return None

    def __str__(self) -> str:
        _custom_p_check = self.__custom__()
        if _custom_p_check is not None:
            return self.text
        return super().__str__()

    @staticmethod
    def _parse(
        client,
        result: "raw.types.TextWithEntities"
    ) -> "FormattedText":
        if not result.text:
            return None
        entities = [
            types.MessageEntity._parse(
                client,
                entity,
                {}  # there isn't a TEXT_MENTION entity available yet
            )
            for entity in result.entities
        ]
        entities = types.List(filter(lambda x: x is not None, entities))
        return FormattedText(
            text=Str(result.text).init(entities) or None, entities=entities or None
        )

    async def write(
        self,
        client: "pyrogram.Client",
        VBL = []
    ) -> "raw.types.TextWithEntities":
        message, entities = (
            await utils.parse_text_entities(
                client,
                self.text,
                self.parse_mode,
                self.entities
            )
        ).values()

        return raw.types.TextWithEntities(
            text=message,
            entities=entities or VBL
        )

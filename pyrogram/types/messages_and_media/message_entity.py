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

from typing import Optional

import pyrogram
from pyrogram import raw, enums, types
from pyrogram.parser import utils as parserutils
from ..object import Object


class MessageEntity(Object):
    """One special entity in a text message.
    
    For example, hashtags, usernames, URLs, etc.

    Parameters:
        type (:obj:`~pyrogram.enums.MessageEntityType`):
            Type of the entity.

        offset (``int``):
            Offset in UTF-16 code units to the start of the entity.

        length (``int``):
            Length of the entity in UTF-16 code units.

        url (``str``, *optional*):
            For :obj:`~pyrogram.enums.MessageEntityType.TEXT_LINK` only, url that will be opened after user taps on the text.

        user (:obj:`~pyrogram.types.User`, *optional*):
            For :obj:`~pyrogram.enums.MessageEntityType.TEXT_MENTION` only, the mentioned user.

        language (``str``, *optional*):
            For :obj:`~pyrogram.enums.MessageEntityType.PRE` only, the programming language of the entity text.

        custom_emoji_id (``str``, *optional*):
            For :obj:`~pyrogram.enums.MessageEntityType.CUSTOM_EMOJI` only, unique identifier of the custom emoji.
            Use :meth:`~pyrogram.Client.get_custom_emoji_stickers` to get full information about the sticker.

        unix_time (``int``, *optional*):
            For :obj:`~pyrogram.enums.MessageEntityType.DATE_TIME` only, the Unix time associated with the entity.

        date_time_format (``str``, *optional*):
            For :obj:`~pyrogram.enums.MessageEntityType.DATE_TIME` only, the string that defines the formatting of the date and time.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        type: "enums.MessageEntityType",
        offset: int,
        length: int,
        url: str = None,
        user: "types.User" = None,
        language: str = None,
        custom_emoji_id: str = None,
        unix_time: int = None,
        date_time_format: str = None,
    ):
        super().__init__(client)

        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user
        self.language = language
        self.custom_emoji_id = custom_emoji_id
        self.unix_time = unix_time
        self.date_time_format = date_time_format

    @staticmethod
    def _parse(client, entity: "raw.base.MessageEntity", users: dict) -> Optional["MessageEntity"]:
        user_id = None
        unix_time = None
        date_time_format = None

        # Special case for InputMessageEntityMentionName -> MessageEntityType.TEXT_MENTION
        # This happens in case of UpdateShortSentMessage inside send_message() where entities are parsed from the input
        if isinstance(entity, raw.types.InputMessageEntityMentionName):
            entity_type = enums.MessageEntityType.TEXT_MENTION
            user_id = entity.user_id.user_id

        elif isinstance(entity, raw.types.MessageEntityBlockquote):
            if entity.collapsed:
                entity_type = enums.MessageEntityType.EXPANDABLE_BLOCKQUOTE
            else:
                entity_type = enums.MessageEntityType.BLOCKQUOTE

        elif isinstance(entity, raw.types.MessageEntityFormattedDate):
            entity_type = enums.MessageEntityType.DATE_TIME
            unix_time = entity.date
            date_time_format = ""
            if entity.relative:
                date_time_format = "r"
            else:
                if entity.day_of_week:
                    date_time_format += "w"
                if entity.short_date or entity.long_date:
                    if entity.short_date:
                        date_time_format += "d"
                    if entity.long_date:
                        date_time_format += "D"
                if entity.short_time or entity.long_time:
                    if entity.short_time:
                        date_time_format += "t"
                    if entity.long_time:
                        date_time_format += "T"

        else:
            try:
                entity_type = enums.MessageEntityType(entity.__class__)
            except ValueError:
                entity_type = enums.MessageEntityType.UNKNOWN
            user_id = getattr(entity, "user_id", None)

        custom_emoji_id = getattr(entity, "document_id", None)

        return MessageEntity(
            type=entity_type,
            offset=entity.offset,
            length=entity.length,
            url=getattr(entity, "url", None),
            user=types.User._parse(client, users.get(user_id, None)),
            language=getattr(entity, "language", None),
            custom_emoji_id=str(custom_emoji_id) if custom_emoji_id else None,
            unix_time=unix_time,
            date_time_format=date_time_format,
            client=client
        )

    async def write(self):
        args = self.__dict__.copy()

        for arg in ("_client", "type", "user"):
            args.pop(arg)

        unix_time = args.pop("unix_time")
        date_time_format = args.pop("date_time_format")

        if self.user:
            args["user_id"] = await self._client.resolve_peer(self.user.id)

        if not self.url:
            args.pop("url")

        if self.language is None:
            args.pop("language")

        args.pop("custom_emoji_id")
        if self.custom_emoji_id is not None:
            args["document_id"] = int(self.custom_emoji_id)

        if self.type == enums.MessageEntityType.EXPANDABLE_BLOCKQUOTE:
            args["collapsed"] = True

        entity = self.type.value

        if entity is raw.types.MessageEntityMentionName:
            entity = raw.types.InputMessageEntityMentionName
        elif self.type in (
            enums.MessageEntityType.BLOCKQUOTE,
            enums.MessageEntityType.EXPANDABLE_BLOCKQUOTE,
        ):
            entity = raw.types.MessageEntityBlockquote
        elif self.type == enums.MessageEntityType.DATE_TIME:
            entity = raw.types.MessageEntityFormattedDate
            args["date"] = unix_time
            args = parserutils.parse_date_time_format_tl(args, date_time_format)

        return entity(**args)

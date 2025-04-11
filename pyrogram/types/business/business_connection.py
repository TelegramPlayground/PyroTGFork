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
from datetime import datetime
from typing import Optional

import pyrogram
from pyrogram import raw, types, utils

from ..object import Object


log = logging.getLogger(__name__)


class BusinessConnection(Object):
    """Describes the connection of the bot with a business account.

    Parameters:
        id (``str``):
            Unique identifier of the business connection
        
        user (:obj:`~pyrogram.types.User`):
            Business account user that created the business connection

        user_chat_id (``int``):
            Identifier of a private chat with the user who created the business connection. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier.

        date (:py:obj:`~datetime.datetime`):
            Date the connection was established in Unix time

        rights (:obj:`~pyrogram.types.BusinessBotRights`, *optional*):
            Rights of the business bot.

        is_enabled (``bool``):
            True, if the connection is active

    """

    def __init__(
        self,
        *,
        id: str = None,
        user: "types.User" = None,
        user_chat_id: int = None,
        date: datetime,
        rights: Optional["types.BusinessBotRights"] = None,
        is_enabled: bool = None,
        _raw: "raw.types.UpdateBotBusinessConnect" = None,
    ):
        super().__init__()

        self.id = id
        self.user = user
        self.user_chat_id = user_chat_id
        self.date = date
        self.rights = rights
        self.is_enabled = is_enabled
        self._raw = _raw


    @staticmethod
    def _parse(
        client,
        business_connect_update: "raw.types.UpdateBotBusinessConnect",
        users: dict,
        chats: dict
    ) -> "BusinessConnection":
        return BusinessConnection(
            _raw=business_connect_update,
            id=business_connect_update.connection.connection_id,
            user=types.User._parse(
                client,
                users[
                    business_connect_update.connection.user_id
                ]
            ),
            user_chat_id=business_connect_update.connection.user_id,
            date=utils.timestamp_to_datetime(business_connect_update.connection.date),
            rights=types.BusinessBotRights._parse(
                client,
                business_connect_update.connection.rights
            ),
            is_enabled=not bool(getattr(business_connect_update.connection, "disabled", None))
        )


    @property
    def can_reply(self) -> str:
        log.warning(
            "This property is deprecated. "
            "Please use rights instead"
        )
        if self.rights:
            return self.rights.can_reply
        return False

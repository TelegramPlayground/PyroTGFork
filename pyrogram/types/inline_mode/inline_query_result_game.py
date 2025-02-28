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
from pyrogram import raw, types
from .inline_query_result import InlineQueryResult

log = logging.getLogger(__name__)


class InlineQueryResultGame(InlineQueryResult):
    """Represents a :obj:`~pyrogram.types.Game`.

    Parameters:
        game_short_name (``str``):
            Short name of the game.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.

    """

    def __init__(
        self,
        game_short_name: str,
        id: str = None,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ):
        super().__init__("game", id, None, reply_markup)

        self.game_short_name = game_short_name

    async def write(self, client: "pyrogram.Client"):
        return raw.types.InputBotInlineResultGame(
            id=self.id,
            short_name=self.game_short_name,
            title=self.first_name,
            send_message=raw.types.InputBotInlineMessageGame(
                reply_markup=await self.reply_markup.write(client) if self.reply_markup else None,
            )
        )

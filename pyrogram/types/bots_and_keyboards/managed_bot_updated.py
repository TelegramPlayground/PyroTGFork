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

from pyrogram import raw, types
from ..object import Object
from ..update import Update


class ManagedBotUpdated(Object, Update):
    """This object contains information about the creation or token update of a bot that is managed by the current bot.

    Parameters:
        user (:obj:`~pyrogram.types.User`, *optional*):
            User that created the bot.
        
        bot (:obj:`~pyrogram.types.User`, *optional*):
            Information about the bot. The bot's token can be fetched using the method :meth:`~pyrogram.Client.get_managed_bot_token`.

    """

    def __init__(
        self,
        *,
        user: "types.User",
        bot: "types.User",
    ):
        super().__init__()

        self.user = user
        self.bot = bot

    @staticmethod
    def _parse(
        client,
        update: "raw.types.UpdateManagedBot",
        users: dict,
    ) -> "ManagedBotUpdated":
        return ManagedBotUpdated(
            user=types.User._parse(client, users[update.user_id]),
            bot=types.User._parse(client, users[update.bot_id]),
        )

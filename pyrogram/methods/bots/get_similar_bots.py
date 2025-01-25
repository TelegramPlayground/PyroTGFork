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

from typing import Union

import pyrogram
from pyrogram import raw, types


class GetSimilarBots:
    async def get_similar_bots(
        self: "pyrogram.Client",
        user_id: Union[int, str]
    ) -> list["types.User"]:
        """Returns a list of bots similar to the given bot.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target bot.

        Returns:
            List of :obj:`~pyrogram.types.User`: On success.

        Example:
            .. code-block:: python

                bots = await app.get_similar_bots()
        """

        botss = await self.invoke(raw.functions.bots.GetBotRecommendations(
            bot=await self.resolve_peer(user_id)
        ))
        return types.List([
            types.User._parse(self, b)
            for b in botss.users
        ])

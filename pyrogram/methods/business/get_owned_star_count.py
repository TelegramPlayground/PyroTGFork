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

from typing import Optional, Union

import pyrogram
from pyrogram import raw, types


class GetOwnedStarCount:
    async def get_owned_star_count(
        self: "pyrogram.Client",
        user_id: Optional[Union[int, str]] = None,
    ) -> "types.StarAmount":
        """Get the number of Telegram Stars count owned by the current account or the specified bot.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            user_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the bot for which the star count should be returned instead of the current user.
                The bot should have ``can_be_edited`` property set to True.
                Pass ``None`` to return the count of the current user.

        Returns:
            :obj:`~pyrogram.types.StarAmount`: On success, the current stars balance is returned.

        Example:
            .. code-block:: python

                # Get stars balance
                app.get_stars_balance()

                # Get stars balance of a bot owned by the current user
                app.get_stars_balance(user_id="pyrogrambot")

        """
        if user_id is None:
            peer = raw.types.InputPeerSelf()
        else:
            peer = await self.resolve_peer(user_id)

        r = await self.invoke(
            raw.functions.payments.GetStarsStatus(
                peer=peer
            )
        )

        return types.StarAmount._parse(self, r)

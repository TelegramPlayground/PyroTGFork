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


from typing import Union

import pyrogram
from pyrogram import raw


class ToggleGiftIsSaved:
    async def toggle_gift_is_saved(
        self: "pyrogram.Client",
        message_id: int,
        is_saved: bool
    ) -> bool:
        """Toggles whether a gift is shown on the current user's profile page.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            message_id (``int``):
                Unique message identifier of the message with the gift in the chat with the user.

            is_saved (``bool``):
                Pass True to display the gift on the user's profile page; pass False to remove it from the profile page.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Hide gift
                app.toggle_gift_is_saved(message_id=123, is_saved=False)
        """

        return await self.invoke(
            raw.functions.payments.SaveStarGift(
                msg_id=message_id,
                unsave=not is_saved
            )
        )

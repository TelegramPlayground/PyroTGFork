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
from pyrogram import raw
from pyrogram.utils import compute_password_check


class DeleteAccount:
    async def delete_account(
        self: "pyrogram.Client", reason: str = "", password: str = None
    ) -> bool:
        """Deletes the account of the current user, deleting all information associated with the user from the server.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            reason (``str``, *optional*):
                The reason why the account was deleted.

            password (``str``, *optional*):
                The 2-step verification password of the current user. If the current user isn't authorized, then an empty string can be passed and account deletion can be canceled within one week.

        Returns:
            `bool`: True On success.

        Example:
            .. code-block:: python

                await app.delete_account(reason, password)
        """
        r = await self.invoke(
            raw.functions.account.DeleteAccount(
                reason=reason,
                password=compute_password_check(
                    await self.invoke(raw.functions.account.GetPassword()), password
                )
                if password
                else None,
            )
        )

        return bool(r)

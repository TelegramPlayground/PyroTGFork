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


class TerminateSession:
    async def terminate_session(
        self: "pyrogram.Client",
        session_id: int
    ) -> bool:
        """Terminates a session of the current user.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            session_id (``int``):
                Session identifier.

        Returns:
            ``bool``: On success, in case the session is destroyed, True is returned. Otherwise, False is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.

        """
        return await self.invoke(
            raw.functions.account.ResetAuthorization(hash=session_id)
        )

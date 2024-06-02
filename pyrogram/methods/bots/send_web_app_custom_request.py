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
from pyrogram import raw, types


class SendWebAppCustomRequest:
    async def send_web_app_custom_request(
        self: "pyrogram.Client",
        bot_user_id: Union[int, str],
        method: str,
        parameters: str
    ) -> str:
        """Sends a custom request from a Web App.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            bot_user_id (``int`` | ``str``):
                Unique identifier of the inline bot you want to get results from. You can specify
                a @username (str) or a bot ID (int).

            method (``str``):
                The method name.
            
            parameters (``str``):
                JSON-serialized method parameters.

        Returns:
            ``str``: On success, a JSON-serialized result is returned.
        """

        r = await self.invoke(
            raw.functions.bots.InvokeWebViewCustomMethod(
                bot=await self.resolve_peer(bot_user_id),
                custom_method=method,
                params=raw.types.DataJSON(
                    data=parameters
                )
            )
        )

        return r.data

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

from typing import Optional, Union

import pyrogram
from pyrogram import raw


class GetOption:
    @staticmethod
    def _parse_tggob_json(obj):
        """Recursively parses Telegram's raw JSON types into native Python types."""
        if isinstance(obj, raw.types.JsonString):
            return obj.value
        elif isinstance(obj, raw.types.JsonNumber):
            return obj.value
        elif isinstance(obj, raw.types.JsonBool):
            return obj.value
        elif isinstance(obj, raw.types.JsonNull):
            return None
        elif isinstance(obj, raw.types.JsonArray):
            # Recursively parse every item in the array to a Python list
            return [GetOption._parse_tggob_json(item) for item in obj.value]
        elif isinstance(obj, raw.types.JsonObject):
            # Recursively parse every key-value pair to a Python dict
            return {item.key: GetOption._parse_tggob_json(item.value) for item in obj.value}
        # Fallback for base values
        return obj

    async def get_option(
        self: "pyrogram.Client",
        name: str,
    ) -> Optional[Union[bool, int, str, list, dict]]:
        """Returns the value of an option by its name.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            name (``str``):
                The name of the option.

        Returns:
            ``bool`` | ``int`` | ``str`` | ``list`` | ``dict``: On success, the value of the option is returned.

        """
        app_config = await self.invoke(
            raw.functions.help.GetAppConfig(
                hash=0
            )
        )
        option = next(
            (x for x in app_config.config.value if x.key == name), 
            None
        )
        if not option:
            return option
        return self._parse_tggob_json(option.value)

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
from pyrogram import raw, types

from ..object import Object


class ChatHasProtectedContentToggled(Object):
    """Describes a service message about a chat ``has_protected_content`` setting was changed or request to change it was rejected.

    Parameters:
        request_message_id (``int``):
            Identifier of the message with the request to change the setting; can be an identifier of a deleted message or 0.

        old_has_protected_content (``bool``):
            Previous value of the setting.

        new_has_protected_content (``bool``):
            New value of the setting.

    """

    def __init__(
        self, *,
        request_message_id: int = None,
        old_has_protected_content: bool = None,
        new_has_protected_content: bool = None,
    ):
        super().__init__()

        self.request_message_id = request_message_id
        self.old_has_protected_content = old_has_protected_content
        self.new_has_protected_content = new_has_protected_content

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        message: "raw.types.MessageService",
    ) -> "ChatHasProtectedContentToggled":
        action: "raw.types.MessageActionNoForwardsToggle" = message.action
        if isinstance(action, raw.types.MessageActionNoForwardsToggle):
            return ChatHasProtectedContentToggled(
                request_message_id=message.id,
                old_has_protected_content=action.prev_value,
                new_has_protected_content=action.new_value,
            )

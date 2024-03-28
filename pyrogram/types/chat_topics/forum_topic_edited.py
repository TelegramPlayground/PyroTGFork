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

from typing import Optional, List, Union

import pyrogram
from pyrogram import raw, types, utils, enums
from ..object import Object


class ForumTopicEdited(Object):
    """This object represents a service message about an edited forum topic.

    Parameters:
        name (``str``, *optional*):
            New name of the topic, if it was edited

        icon_custom_emoji_id (``str``, *optional*):
            New identifier of the custom emoji shown as the topic icon, if it was edited; an empty string if the icon was removed

    """

    def __init__(
        self,
        *,
        name: str = None,
        icon_custom_emoji_id: str = None
    ):
        super().__init__()

        self.name = name
        self.icon_custom_emoji_id = icon_custom_emoji_id


    @staticmethod
    def _parse(
        topic_edit_action: "raw.types.MessageActionTopicEdit"
    ) -> "ForumTopicEdited":
        return ForumTopicEdited(
            name=getattr(topic_edit_action, "title", None),
            icon_custom_emoji_id=getattr(topic_edit_action, "icon_emoji_id", None)
        )

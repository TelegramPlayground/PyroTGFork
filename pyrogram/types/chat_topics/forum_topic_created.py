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


class ForumTopicCreated(Object):
    """This object represents a service message about a new forum topic created in the chat.

    Parameters:
        name (``str``):
            Name of the topic

        icon_color  (``int``):
            Color of the topic icon in RGB format

        icon_custom_emoji_id (``str``, *optional*):
            Unique identifier of the custom emoji shown as the topic icon

    """

    def __init__(
        self,
        *,
        name: str,
        icon_color: int,
        icon_custom_emoji_id: str = None
    ):
        super().__init__()

        self.name = name
        self.icon_color = icon_color
        self.icon_custom_emoji_id = icon_custom_emoji_id


    @staticmethod
    def _parse(
        topic_create_action: "raw.types.MessageActionTopicCreate"
    ) -> "ForumTopicCreated":
        return ForumTopicCreated(
            name=topic_create_action.title,
            icon_color=topic_create_action.icon_color,  # TODO
            icon_custom_emoji_id=getattr(topic_create_action, "", None)
        )

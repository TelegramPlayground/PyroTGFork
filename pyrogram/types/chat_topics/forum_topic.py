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

from datetime import datetime
from typing import Optional, List, Union

import pyrogram
from pyrogram import raw, types, utils, enums
from ..object import Object


class ForumTopic(Object):
    """This object represents a forum topic.

    Parameters:
        message_thread_id (``int``):
            Unique identifier of the forum topic

        name (``str``):
            Name of the topic

        icon_color  (``int``):
            Color of the topic icon in RGB format

        icon_custom_emoji_id (``str``, *optional*):
            Unique identifier of the custom emoji shown as the topic icon

        creation_date (:py:obj:`~datetime.datetime`, *optional*):
            Point in time (Unix timestamp) when the topic was created

        creator (:obj:`~pyrogram.types.Chat`, *optional*):
            Identifier of the creator of the topic
        
        outgoing (``bool``, *optional*):
            True, if the topic was created by the current user

        is_closed (``bool``, *optional*):
            True, if the topic is closed

        is_hidden (``bool``, *optional*):
            True, if the topic is hidden above the topic list and closed; for General topic only
        
        is_deleted (``bool``, *optional*):
            True, if the topic is delete

        is_pinned (``bool``, *optional*):
            True, if the topic is pinned
    """

    def __init__(
        self,
        *,
        message_thread_id: int,
        name: str,
        icon_color: int,
        icon_custom_emoji_id: str = None,
        creation_date: datetime = None,
        creator: "types.Chat" = None,
        outgoing: bool = None,
        is_closed: bool = None,
        is_hidden: bool = None,
        is_deleted: bool = None,
        is_pinned: bool = None
    ):
        super().__init__()

        self.message_thread_id = message_thread_id
        self.name = name
        self.icon_color = icon_color
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.creation_date = creation_date
        self.creator = creator
        self.outgoing = outgoing
        # self.is_general = is_general
        self.is_closed = is_closed
        self.is_hidden = is_hidden
        self.is_deleted = is_deleted
        self.is_pinned = is_pinned


    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        forum_topic: "raw.types.ForumTopic",
        messages: dict,
        users: dict,
        chats: dict
    ) -> "ForumTopic":
        if isinstance(forum_topic, raw.types.ForumTopicDeleted):
            return ForumTopic(
                message_thread_id=forum_topic.id,
                name=None,
                icon_color=None,
                is_deleted=True
            )

        creator = None
        peer = getattr(forum_topic, "from_id", None)
        if peer:
            peer_id = utils.get_raw_peer_id(peer)
            if isinstance(peer, raw.types.PeerUser):
                creator = types.Chat._parse_user_chat(
                    client, users[peer_id]
                )
            else:
                creator = types.Chat._parse_channel_chat(
                    client, chats[peer_id]
                )

        return ForumTopic(
            message_thread_id=forum_topic.id,
            name=forum_topic.title,
            icon_color=forum_topic.icon_color,  # TODO
            icon_custom_emoji_id=getattr(forum_topic, "icon_emoji_id", None),
            creation_date=utils.timestamp_to_datetime(forum_topic.date),
            creator=creator,
            outgoing=getattr(forum_topic, "my", None),
            is_closed=getattr(forum_topic, "closed", None),
            is_hidden=getattr(forum_topic, "hidden", None),
            is_pinned=getattr(forum_topic, "pinned", None),
        )

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

        last_message (:obj:`~pyrogram.types.Message`, *optional*):
            Last message in the topic; may be None if unknown
        
        is_pinned (``bool``, *optional*):
            True, if the topic is pinned

        unread_count (``int``, *optional*):
            Number of unread messages in the topic

        last_read_inbox_message_id (``int``, *optional*):
            Identifier of the last read incoming message

        last_read_outbox_message_id (``int``, *optional*):
            Identifier of the last read outgoing message

        unread_mention_count (``int``, *optional*):
            Number of unread messages with a mention/reply in the topic

        unread_reaction_count (``int``, *optional*):
            Number of messages with unread reactions in the topic

        is_reduced_version (``bool``, *optional*):
            True, if this is a reduced version of the full topic information.
            If needed, full information can be fetched using :meth:`~pyrogram.Client.get_forum_topic`.

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
        last_message: "types.Message" = None,
        is_pinned: bool = None,
        unread_count: int = None,
        last_read_inbox_message_id: int = None,
        last_read_outbox_message_id: int = None,
        unread_mention_count: int = None,
        unread_reaction_count: int = None,

        is_reduced_version: bool = None
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
        self.last_message = last_message
        self.is_pinned = is_pinned
        self.unread_count = unread_count
        self.last_read_inbox_message_id = last_read_inbox_message_id
        self.last_read_outbox_message_id = last_read_outbox_message_id
        self.unread_mention_count = unread_mention_count
        self.unread_reaction_count = unread_reaction_count

        self.is_reduced_version = is_reduced_version


    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        forum_topic: "raw.types.ForumTopic",
        messages: dict, # friendly
        users: dict, # raw
        chats: dict, # raw 
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

        last_message = None
        top_message_id = getattr(forum_topic, "top_message", None)
        if top_message_id:
            last_message = messages.get(top_message_id, None)

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
            last_message=last_message,
            is_pinned=getattr(forum_topic, "pinned", None),
            unread_count=getattr(forum_topic, "unread_count", None),
            last_read_inbox_message_id=getattr(forum_topic, "read_inbox_max_id", None),
            last_read_outbox_message_id=getattr(forum_topic, "read_outbox_max_id", None),
            unread_mention_count=getattr(forum_topic, "unread_mentions_count", None),
            unread_reaction_count=getattr(forum_topic, "unread_reactions_count", None),
            # TODO: notify_settings: PeerNotifySettings, draft: DraftMessage
            is_reduced_version=getattr(forum_topic, "short", None)
        )

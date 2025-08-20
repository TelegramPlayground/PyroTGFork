#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present <https://github.com/TelegramPlayground>
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

from typing import Optional

import pyrogram
from pyrogram import raw, types, utils

from ..object import Object


class DirectMessagesTopic(Object):
    """Describes a topic of a direct messages chat administered by the current user.

    Parameters:
        topic_id (``int``):
            Unique identifier of the topic inside the chat.

        user (:obj:`~pyrogram.types.User`, *optional*):
            Information about the user that created the topic. Currently, it is always present.

        can_send_unpaid_messages (``bool``, *optional*):
            True, if the other party can send unpaid messages even if the chat has paid messages enabled.

        is_marked_as_unread (``bool``, *optional*):
            True, if the forum topic is marked as unread.

        unread_count (``int``, *optional*):
            Number of unread messages in the chat.

        last_read_inbox_message_id (``int``, *optional*):
            Identifier of the last read incoming message.

        last_read_outbox_message_id (``int``, *optional*):
            Identifier of the last read outgoing message.

        unread_reactions_count (``int``, *optional*):
            Number of messages with unread reactions in the chat.

        last_message (:obj:`~pyrogram.types.Message`, *optional*):
            Last message in the topic.

    """

    def __init__(
        self,
        *,
        topic_id: int,
        user: Optional["types.User"] = None,
        can_send_unpaid_messages: Optional[bool] = None,
        is_marked_as_unread: Optional[bool] = None,
        unread_count: Optional[int] = None,
        last_read_inbox_message_id: Optional[int] = None,
        last_read_outbox_message_id: Optional[int] = None,
        unread_reactions_count: Optional[int] = None,
        last_message: Optional["types.Message"] = None
    ):
        super().__init__()

        self.topic_id = topic_id
        self.user = user
        self.can_send_unpaid_messages = can_send_unpaid_messages
        self.is_marked_as_unread = is_marked_as_unread
        self.unread_count = unread_count
        self.last_read_inbox_message_id = last_read_inbox_message_id
        self.last_read_outbox_message_id = last_read_outbox_message_id
        self.unread_reactions_count = unread_reactions_count
        self.last_message = last_message

    @staticmethod
    def _parse_dialog(
        client: "pyrogram.Client",
        topic: "raw.types.MonoForumDialog",
        messages: dict = {},
        users: dict[int, "raw.base.User"] = {},
        chats: dict[int, "raw.base.Chat"] = {},
    ) -> "DirectMessagesTopic":
        if not topic:
            return None
        user_chat_id = utils.get_raw_peer_id(topic.peer)
        if not user_chat_id:
            return None
        return DirectMessagesTopic(
            topic_id=user_chat_id,
            user=types.User._parse(client, users.get(user_chat_id)),
            can_send_unpaid_messages=topic.nopaid_messages_exception,
            is_marked_as_unread=topic.unread_mark,
            unread_count=topic.unread_count,
            last_read_inbox_message_id=topic.read_inbox_max_id,
            last_read_outbox_message_id=topic.read_outbox_max_id,
            unread_reactions_count=topic.unread_reactions_count,
            last_message=messages.get(topic.top_message)
        )

    @staticmethod
    def _parse_message(
        client: "pyrogram.Client",
        message: "raw.types.Message",
        users: dict[int, "raw.base.User"] = {},
        chats: dict[int, "raw.base.Chat"] = {},
    ) -> "DirectMessagesTopic":
        user_chat_id = utils.get_raw_peer_id(message.saved_peer_id)
        if not user_chat_id:
            return None
        return DirectMessagesTopic(
            topic_id=user_chat_id,
            user=types.User._parse(client, users.get(user_chat_id)),
        )

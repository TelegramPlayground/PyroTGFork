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

from enum import auto

from .auto_name import AutoName


class MessageServiceType(AutoName):
    """Message service type enumeration used in :obj:`~pyrogram.types.Message`."""

    NEW_CHAT_MEMBERS = auto()
    "New members join"

    LEFT_CHAT_MEMBERS = auto()
    "Left chat members"

    NEW_CHAT_TITLE = auto()
    "New chat title"

    NEW_CHAT_PHOTO = auto()
    "New chat photo"

    DELETE_CHAT_PHOTO = auto()
    "Deleted chat photo"

    GROUP_CHAT_CREATED = auto()
    "Group chat created"

    SUPERGROUP_CHAT_CREATED = auto()
    "Supergroup chat created"

    CHANNEL_CHAT_CREATED = auto()
    "Channel chat created"

    MIGRATE_TO_CHAT_ID = auto()
    "Migrated to chat id"

    MIGRATE_FROM_CHAT_ID = auto()
    "Migrated from chat id"

    PINNED_MESSAGE = auto()
    "Pinned message"

    GAME_HIGH_SCORE = auto()
    "Game high score"

    GIVEAWAY_CREATED = auto()
    "Giveaway Created"

    GIVEAWAY_COMPLETED = auto()
    "Giveaway Completed"

    GIFT_CODE = auto()
    "Gift code"

    GIFTED_PREMIUM = auto()
    "Gifted Premium"

    GIFTED_STARS = auto()
    "Gifted Stars"

    VIDEO_CHAT_STARTED = auto()
    "Video chat started"

    VIDEO_CHAT_ENDED = auto()
    "Video chat ended"

    VIDEO_CHAT_SCHEDULED = auto()
    "Video chat scheduled"

    VIDEO_CHAT_PARTICIPANTS_INVITED = auto()
    "Video chat participants invited"

    WEB_APP_DATA = auto()
    "Web app data"

    USERS_SHARED = auto()
    "Users Shared"

    CHAT_SHARED = auto()
    "Chat Shared"

    MESSAGE_AUTO_DELETE_TIMER_CHANGED = auto()
    "Message Auto Delete Timer changed"

    CHAT_BOOST_ADDED = auto()
    "Chat Boost Added"

    CUSTOM_ACTION = auto()
    "Custom action"

    FORUM_TOPIC_CREATED = auto()
    "a new forum topic created in the chat"

    FORUM_TOPIC_CLOSED = auto()
    "a new forum topic closed in the chat"

    FORUM_TOPIC_REOPENED = auto()
    "a new forum topic reopened in the chat"

    FORUM_TOPIC_EDITED = auto()
    "a new forum topic renamed in the chat"

    GENERAL_FORUM_TOPIC_HIDDEN = auto()
    "a forum general topic hidden in the chat"

    GENERAL_FORUM_TOPIC_UNHIDDEN = auto()
    "a forum general topic unhidden in the chat"

    SUCCESSFUL_PAYMENT = auto()
    "Successful payment"

    REFUNDED_PAYMENT = auto()
    "Refunded payment"

    CONTACT_REGISTERED = auto()
    "A contact has registered with Telegram"

    SCREENSHOT_TAKEN = auto()
    "A screenshot of a message in the chat has been taken"

    CONNECTED_WEBSITE = auto()
    "The user connected a website by logging in using Telegram Login Widget on it"

    WRITE_ACCESS_ALLOWED = auto()
    "The user accepted webapp bot's request to send messages"

    RECEIVED_GIFT = auto()
    "Owner Received gift"

    UNKNOWN = auto()
    "This service message is unsupported by the current version of Pyrogram"

#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
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

from pyrogram import types
from ..object import Object


class KeyboardButtonRequestChat(Object):
    """This object defines the criteria used to request a suitable chat.
    Information about the selected chat will be shared with the bot when the corresponding button is pressed.
    The bot will be granted requested rights in the сhat if appropriate.
    `More about requesting chats. <https://core.telegram.org/bots/features#chat-and-user-selection>`_

    Parameters:
        request_id (``int``):
            Signed 32-bit identifier of the request, which will be received back in the :obj:`~pyrogram.types.ChatShared` object. Must be unique within the message

        chat_is_channel (``bool``):
            Pass True to request a channel chat, pass False to request a group or a supergroup chat.

        chat_is_forum (``bool``, *optional*):
            Pass True to request a forum supergroup, pass False to request a non-forum chat. If not specified, no additional restrictions are applied.

        chat_has_username (``bool``, *optional*):
            Pass True to request a supergroup or a channel with a username, pass False to request a chat without a username. If not specified, no additional restrictions are applied.

        chat_is_created (``bool``, *optional*):
            Pass True to request a chat owned by the user. Otherwise, no additional restrictions are applied.

        user_administrator_rights (:obj:`~pyrogram.types.ChatPrivileges`, *optional*):
            A object listing the required administrator rights of the user in the chat. The rights must be a superset of bot_administrator_rights. If not specified, no additional restrictions are applied.

        bot_administrator_rights (:obj:`~pyrogram.types.ChatPrivileges`, *optional*):
            A object listing the required administrator rights of the bot in the chat. The rights must be a subset of user_administrator_rights. If not specified, no additional restrictions are applied.

        bot_is_member (``bool``, *optional*):
            Pass True to request a chat with the bot as a member. Otherwise, no additional restrictions are applied.

        request_title (``bool``, *optional*):
            Pass True to request the chat's title

        request_username (``bool``, *optional*):
            Pass True to request the chat's username

        request_photo (``bool``, *optional*):
            Pass True to request the chat's photo

    """
    def __init__(
        self,
        request_id: int,
        chat_is_channel: bool,
        chat_is_forum: bool = None,
        chat_has_username: bool = None,
        chat_is_created: bool = None,
        user_administrator_rights: "types.ChatPrivileges" = None,
        bot_administrator_rights: "types.ChatPrivileges" = None,
        bot_is_member: bool = None,
        request_title: bool = None,
        request_username: bool = None,
        request_photo: bool = None
    ):
        self.request_id = request_id
        self.chat_is_channel = chat_is_channel
        self.chat_is_forum = chat_is_forum
        self.chat_has_username = chat_has_username
        self.chat_is_created = chat_is_created
        self.user_administrator_rights = user_administrator_rights
        self.bot_administrator_rights = bot_administrator_rights
        self.bot_is_member = bot_is_member
        self.request_title = request_title
        self.request_username = request_username
        self.request_photo = request_photo

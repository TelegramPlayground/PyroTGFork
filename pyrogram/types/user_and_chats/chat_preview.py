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

from typing import List

import pyrogram
from pyrogram import raw, types, enums
from ..object import Object


class ChatPreview(Object):
    """A chat preview.

    Parameters:
        title (``str``):
            Title of the chat.

        type (``str``):
            Type of chat, can be either, "group", "supergroup" or "channel".

        members_count (``int``):
            Chat members count.

        photo (:obj:`~pyrogram.types.Photo`, *optional*):
            Chat photo.

        members (List of :obj:`~pyrogram.types.User`, *optional*):
            Preview of some of the chat members.
        
        description (``str``, *optional*):
            Description, for groups, supergroups and channel chats.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        accent_color_id (``int``, *optional*):
            Identifier of the accent color for the chat name and backgrounds of the chat photo, reply header, and link preview. See `accent colors <https://core.telegram.org/bots/api#accent-colors>`_ for more details. Returned only in :meth:`~pyrogram.Client.get_chat`. Always returned in :meth:`~pyrogram.Client.get_chat`.

        is_verified (``bool``, *optional*):
            True, if this chat has been verified by Telegram. Supergroups, channels and bots only.

        is_scam (``bool``, *optional*):
            True, if this chat has been flagged for scam.

        is_fake (``bool``, *optional*):
            True, if this chat has been flagged for impersonation.
        
        is_public (``bool``, *optional*):
            True, if this chat is public.

        join_by_request (``bool``, *optional*):
            True, if all users directly joining the supergroup need to be approved by supergroup administrators.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        title: str,
        type: str,
        members_count: int,
        photo: "types.Photo" = None,
        members: List["types.User"] = None,
        description: str = None,
        accent_color_id: int = None,
        is_verified: bool = None,
        is_scam: bool = None,
        is_fake: bool = None,
        is_public: bool = None,
        join_by_request: bool = None
    ):
        super().__init__(client)

        self.title = title
        self.type = type
        self.members_count = members_count
        self.photo = photo
        self.members = members
        self.description = description
        self.accent_color_id = accent_color_id
        self.is_verified = is_verified
        self.is_scam = is_scam
        self.is_fake = is_fake
        self.is_public = is_public
        self.join_by_request = join_by_request

    @staticmethod
    def _parse(client, chat_invite: "raw.types.ChatInvite") -> "ChatPreview":
        return ChatPreview(
            title=chat_invite.title,
            type=(
                enums.ChatType.GROUP if not chat_invite.channel else
                enums.ChatType.CHANNEL if chat_invite.broadcast else
                enums.ChatType.SUPERGROUP
            ),
            members_count=chat_invite.participants_count,
            photo=types.Photo._parse(client, chat_invite.photo),
            members=[
                types.User._parse(client, user)
                for user in chat_invite.participants
            ] or None,
            description=getattr(chat_invite, "about", None),
            accent_color_id=getattr(chat_invite, "color", None),
            is_verified=getattr(chat_invite, "verified", None),
            is_scam=getattr(chat_invite, "scam", None),
            is_fake=getattr(chat_invite, "fake", None),
            is_public=getattr(chat_invite, "public", None),
            join_by_request=getattr(chat_invite, "request_needed", None),
            client=client
        )

    # TODO: Maybe just merge this object into Chat itself by adding the "members" field.
    #  get_chat can be used as well instead of get_chat_preview

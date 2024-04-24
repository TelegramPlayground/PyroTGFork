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
from typing import Union, List, Optional, AsyncGenerator, BinaryIO

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from pyrogram import utils
from pyrogram.errors import MessageIdsEmpty
from ..object import Object


class Chat(Object):
    """A chat.

    Parameters:
        id (``int``, *optional*):
            Unique identifier for this chat.

        type (:obj:`~pyrogram.enums.ChatType`, *optional*):
            Type of chat.

        title (``str``, *optional*):
            Title, for supergroups, channels and basic group chats.

        username (``str``, *optional*):
            Username, for private chats, bots, supergroups and channels if available.
        
        first_name (``str``, *optional*):
            First name of the other party in a private chat, for private chats and bots.

        last_name (``str``, *optional*):
            Last name of the other party in a private chat, for private chats.

        is_forum (``bool``, *optional*):
            True, if the supergroup chat is a forum

        photo (:obj:`~pyrogram.types.ChatPhoto`, *optional*):
            Chat photo. Suitable for downloads only.

        active_usernames (List of :obj:`~pyrogram.types.Username`, *optional*):
            If non-empty, the list of all `active chat usernames <https://telegram.org/blog/topics-in-groups-collectible-usernames#collectible-usernames>`_; for private chats, supergroups and channels.

        birthdate (:obj:`~pyrogram.types.Birthdate`, *optional*):
            For private chats, the date of birth of the user.

        business_intro (:obj:`~pyrogram.types.BusinessIntro`, *optional*):
            For private chats with business accounts, the intro of the business.

        business_location (:obj:`~pyrogram.types.BusinessLocation`, *optional*):
            For private chats with business accounts, the location of the business.

        business_opening_hours (:obj:`~pyrogram.types.BusinessOpeningHours`, *optional*):
            For private chats with business accounts, the opening hours of the business.

        personal_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            For private chats, the personal channel of the user.

        personal_chat_message (:obj:`~pyrogram.types.Message`, *optional*):
            **TEMPORARY**: For private chats, the personal message_id in the ``personal_chat``.

        available_reactions (:obj:`~pyrogram.types.ChatReactions`, *optional*):
            Available reactions in the chat.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        accent_color (:obj:`~pyrogram.types.ChatColor`, *optional*):
            Chat accent color.

        profile_color (:obj:`~pyrogram.types.ChatColor`, *optional*):
            Chat profile color.

        emoji_status (:obj:`~pyrogram.types.EmojiStatus`, *optional*):
            Emoji status.

        bio (``str``, *optional*):
            Bio of the other party in a private chat.
            Returned only in :meth:`~pyrogram.Client.get_chat`.
        
        join_by_request (``bool``, *optional*):
            True, if all users directly joining the supergroup need to be approved by supergroup administrators.

        description (``str``, *optional*):
            Description, for groups, supergroups and channel chats.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        invite_link (``str``, *optional*):
            Chat invite link, for groups, supergroups and channels.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        pinned_message (:obj:`~pyrogram.types.Message`, *optional*):
            Pinned message, for groups, supergroups channels and own chat.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        permissions (:obj:`~pyrogram.types.ChatPermissions` *optional*):
            Default chat member permissions, for groups and supergroups.

        slowmode_next_send_date (:py:obj:`~datetime.datetime`, *optional*):
            Indicates when the user will be allowed to send another message in the chat. For supergroups only.

        slow_mode_delay (``int``, *optional*):
            For supergroups, the minimum allowed delay between consecutive messages sent by each unpriviledged user; in seconds.

        unrestrict_boost_count (``int``, *optional*):
            For supergroups, the minimum number of boosts that a non-administrator user needs to add in order to ignore slow mode and chat permissions.

        message_auto_delete_time (``int``, *optional*):
            The time after which all messages sent to the chat will be automatically deleted; in seconds.

        has_aggressive_anti_spam_enabled (``bool``, *optional*):
            True, if aggressive anti-spam checks are enabled in the supergroup. The field is only available to chat administrators.

        has_hidden_members (``bool``, *optional*):
            True, if non-administrators can only get the list of bots and administrators in the chat.

        has_protected_content (``bool``, *optional*):
            True, if messages from the chat can't be forwarded to other chats.

        has_visible_history (``bool``, *optional*):
            True, if new chat members will have access to old messages; available only to chat administrators.

        sticker_set_name (``str``, *optional*):
            For supergroups, name of group sticker set.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        can_set_sticker_set (``bool``, *optional*):
            True, if the group sticker set can be changed by you.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        custom_emoji_sticker_set_name (``str``, *optional*):
            For supergroups, the name of the group's custom emoji sticker set. Custom emoji from this set can be used by all users and bots in the group.

        linked_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            The linked discussion group (in case of channels) or the linked channel (in case of supergroups).
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        is_verified (``bool``, *optional*):
            True, if this chat has been verified by Telegram. Supergroups, channels and bots only.

        is_restricted (``bool``, *optional*):
            True, if this chat has been restricted. Supergroups, channels and bots only.
            See *restriction_reason* for details.

        is_creator (``bool``, *optional*):
            True, if this chat owner is the current user. Supergroups, channels and groups only.

        is_scam (``bool``, *optional*):
            True, if this chat has been flagged for scam.

        is_fake (``bool``, *optional*):
            True, if this chat has been flagged for impersonation.

        is_support (``bool``, *optional*):
            True, if this chat is part of the Telegram support team. Users and bots only.

        is_public (``bool``, *optional*):
            True, if this chat is public.

        dc_id (``int``, *optional*):
            The chat assigned DC (data center). Available only in case the chat has a photo.
            Note that this information is approximate; it is based on where Telegram stores the current chat photo.
            It is accurate only in case the owner has set the chat photo, otherwise the dc_id will be the one assigned
            to the administrator who set the current chat photo.

        members (List of :obj:`~pyrogram.types.User`, *optional*):
            Preview of some of the chat members.

        members_count (``int``, *optional*):
            Chat members count, for groups, supergroups and channels only.
            Returned only in :meth:`~pyrogram.Client.get_chat`.

        restrictions (List of :obj:`~pyrogram.types.Restriction`, *optional*):
            The list of reasons why this chat might be unavailable to some users.
            This field is available only in case *is_restricted* is True.

        distance (``int``, *optional*):
            Distance in meters of this group chat from your location.
            Returned only in :meth:`~pyrogram.Client.get_nearby_chats`.

        send_as_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            The default "send_as" chat.
            Returned only in :meth:`~pyrogram.Client.get_chat`.
        
        is_peak_preview (``bool``, *optional*):
            True, if this is a peak preview.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int = None,
        type: "enums.ChatType" = None,
        is_verified: bool = None,
        is_restricted: bool = None,
        is_creator: bool = None,
        is_scam: bool = None,
        is_fake: bool = None,
        is_support: bool = None,
        is_public: bool = None,
        title: str = None,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        photo: "types.ChatPhoto" = None,
        active_usernames: List["types.Username"] = None,
        birthdate: "types.Birthdate" = None,
        business_intro: "types.BusinessIntro" = None,
        business_location: "types.BusinessLocation" = None,
        business_opening_hours: "types.BusinessOpeningHours" = None,
        bio: str = None,
        join_by_request: bool = None,
        description: str = None,
        dc_id: int = None,
        has_protected_content: bool = None,
        invite_link: str = None,
        pinned_message=None,
        sticker_set_name: str = None,
        custom_emoji_sticker_set_name: str = None,
        can_set_sticker_set: bool = None,
        members: List["types.User"] = None,
        members_count: int = None,
        restrictions: List["types.Restriction"] = None,
        permissions: "types.ChatPermissions" = None,
        distance: int = None,
        linked_chat: "types.Chat" = None,
        send_as_chat: "types.Chat" = None,
        personal_chat: "types.Chat" = None,
        personal_chat_message: "types.Message" = None,
        available_reactions: Optional["types.ChatReactions"] = None,
        accent_color: "types.ChatColor" = None,
        profile_color: "types.ChatColor" = None,
        emoji_status: "types.EmojiStatus" = None,
        has_visible_history: bool = None,
        has_hidden_members: bool = None,
        has_aggressive_anti_spam_enabled: bool = None,
        message_auto_delete_time: int = None,
        slow_mode_delay: int = None,
        slowmode_next_send_date: datetime = None,
        unrestrict_boost_count: int = None,
        is_forum: bool = None,
        is_peak_preview: bool = None,
        _raw: Union[
            "raw.types.ChatInvite",
            "raw.types.Channel",
            "raw.types.Chat",
            "raw.types.User",
            "raw.types.messages.ChatFull",
            "raw.types.users.UserFull"
        ] = None
    ):
        super().__init__(client)

        self.id = id
        self.type = type
        self.is_verified = is_verified
        self.is_restricted = is_restricted
        self.is_creator = is_creator
        self.is_scam = is_scam
        self.is_fake = is_fake
        self.is_support = is_support
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.photo = photo
        self.bio = bio
        self.description = description
        self.dc_id = dc_id
        self.has_protected_content = has_protected_content
        self.invite_link = invite_link
        self.pinned_message = pinned_message
        self.sticker_set_name = sticker_set_name
        self.custom_emoji_sticker_set_name = custom_emoji_sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set
        self.members = members
        self.members_count = members_count
        self.restrictions = restrictions
        self.permissions = permissions
        self.distance = distance
        self.linked_chat = linked_chat
        self.send_as_chat = send_as_chat
        self.available_reactions = available_reactions
        self.accent_color = accent_color
        self.profile_color = profile_color
        self.emoji_status = emoji_status
        self.has_visible_history = has_visible_history
        self.has_hidden_members = has_hidden_members
        self.has_aggressive_anti_spam_enabled = has_aggressive_anti_spam_enabled
        self.message_auto_delete_time = message_auto_delete_time
        self.slow_mode_delay = slow_mode_delay
        self.slowmode_next_send_date = slowmode_next_send_date
        self.is_forum = is_forum
        self.unrestrict_boost_count = unrestrict_boost_count
        self.is_public = is_public
        self.join_by_request = join_by_request
        self.is_peak_preview = is_peak_preview
        self.personal_chat = personal_chat
        self.personal_chat_message = personal_chat_message
        self.birthdate = birthdate
        self.business_intro = business_intro
        self.business_location = business_location
        self.business_opening_hours = business_opening_hours
        self.active_usernames = active_usernames
        self._raw = _raw

    @staticmethod
    def _parse_user_chat(client, user: raw.types.User) -> "Chat":
        peer_id = user.id

        active_usernames = types.List(
            [
                types.Username._parse(u)
                for u in getattr(user, "usernames", [])
            ]
        ) or None
        _tmp_username = None
        if (
            active_usernames and
            len(active_usernames) > 0
        ):
            _tmp_username = active_usernames[0].username

        return Chat(
            id=peer_id,
            type=enums.ChatType.BOT if user.bot else enums.ChatType.PRIVATE,
            is_verified=getattr(user, "verified", None),
            is_restricted=getattr(user, "restricted", None),
            is_scam=getattr(user, "scam", None),
            is_fake=getattr(user, "fake", None),
            is_support=getattr(user, "support", None),
            username=user.username or _tmp_username,
            first_name=user.first_name,
            last_name=user.last_name,
            photo=types.ChatPhoto._parse(client, user.photo, peer_id, user.access_hash),
            restrictions=types.List([types.Restriction._parse(r) for r in user.restriction_reason]) or None,
            dc_id=getattr(getattr(user, "photo", None), "dc_id", None),
            client=client,
            active_usernames=active_usernames,
            accent_color=types.ChatColor._parse(getattr(user, "color", None)),
            profile_color=types.ChatColor._parse_profile_color(getattr(user, "profile_color", None)),
            emoji_status=types.EmojiStatus._parse(client, user.emoji_status),
            _raw=user
        )

    @staticmethod
    def _parse_chat_chat(client, chat: raw.types.Chat) -> "Chat":
        peer_id = -chat.id

        return Chat(
            id=peer_id,
            type=enums.ChatType.GROUP,
            title=chat.title,
            is_creator=getattr(chat, "creator", None),
            photo=types.ChatPhoto._parse(client, getattr(chat, "photo", None), peer_id, 0),
            permissions=types.ChatPermissions._parse(getattr(chat, "default_banned_rights", None)),
            members_count=getattr(chat, "participants_count", 0),
            dc_id=getattr(getattr(chat, "photo", None), "dc_id", None),
            has_protected_content=getattr(chat, "noforwards", None),
            client=client,
            _raw=chat
        )

    @staticmethod
    def _parse_channel_chat(client, channel: raw.types.Channel) -> "Chat":
        peer_id = utils.get_channel_id(channel.id)

        if isinstance(channel, raw.types.ChatForbidden):
            return Chat(
                id=peer_id,
                type=enums.ChatType.GROUP,
                title=channel.title,
                client=client,
                _raw=channel
            )

        if isinstance(channel, raw.types.ChannelForbidden):
            return Chat(
                id=peer_id,
                type=enums.ChatType.SUPERGROUP if channel.megagroup else enums.ChatType.CHANNEL,
                title=channel.title,
                client=client,
                _raw=channel
            )

        active_usernames = types.List(
            [
                types.Username._parse(u)
                for u in getattr(channel, "usernames", [])
            ]
        ) or None
        _tmp_username = None
        if (
            active_usernames and
            len(active_usernames) > 0
        ):
            _tmp_username = active_usernames[0].username

        return Chat(
            id=peer_id,
            type=enums.ChatType.SUPERGROUP if channel.megagroup else enums.ChatType.CHANNEL,
            is_verified=channel.verified,
            is_restricted=channel.restricted,
            is_creator=channel.creator,
            is_scam=channel.scam,
            is_fake=channel.fake,
            title=channel.title,
            username=channel.username or _tmp_username,
            photo=types.ChatPhoto._parse(
                client,
                getattr(channel, "photo", None),
                peer_id,
                getattr(channel, "access_hash", 0)
            ),
            restrictions=types.List(
                [
                    types.Restriction._parse(r)
                    for r in getattr(channel, "restriction_reason", None)
                ]
            ) or None,
            permissions=types.ChatPermissions._parse(getattr(channel, "default_banned_rights", None)),
            members_count=getattr(channel, "participants_count", 0),
            dc_id=getattr(getattr(channel, "photo", None), "dc_id", None),
            has_protected_content=getattr(channel, "noforwards", None),
            is_forum=getattr(channel, "forum", None),
            client=client,
            active_usernames=active_usernames,
            accent_color=types.ChatColor._parse(getattr(channel, "color", None)),
            profile_color=types.ChatColor._parse_profile_color(getattr(channel, "profile_color", None)),
            emoji_status=types.EmojiStatus._parse(client, channel.emoji_status),
            _raw=channel
        )

    @staticmethod
    def _parse(
        client,
        message: Union[raw.types.Message, raw.types.MessageService],
        users: dict,
        chats: dict,
        is_chat: bool
    ) -> "Chat":
        from_id = utils.get_raw_peer_id(message.from_id)
        peer_id = utils.get_raw_peer_id(message.peer_id)
        chat_id = (peer_id or from_id) if is_chat else (from_id or peer_id)

        if isinstance(message.peer_id, raw.types.PeerUser):
            return Chat._parse_user_chat(client, users[chat_id])

        if isinstance(message.peer_id, raw.types.PeerChat):
            return Chat._parse_chat_chat(client, chats[chat_id])

        return Chat._parse_channel_chat(client, chats[chat_id])

    @staticmethod
    def _parse_dialog(client, peer, users: dict, chats: dict):
        if isinstance(peer, raw.types.PeerUser):
            return Chat._parse_user_chat(client, users[peer.user_id])
        elif isinstance(peer, raw.types.PeerChat):
            return Chat._parse_chat_chat(client, chats[peer.chat_id])
        else:
            return Chat._parse_channel_chat(client, chats[peer.channel_id])

    @staticmethod
    async def _parse_full(client, chat_full: Union[raw.types.messages.ChatFull, raw.types.users.UserFull]) -> "Chat":
        users = {u.id: u for u in chat_full.users}
        chats = {c.id: c for c in chat_full.chats}

        personal_chat = None
        personal_chat_message = None

        if isinstance(chat_full, raw.types.users.UserFull):
            full_user = chat_full.full_user

            parsed_chat = Chat._parse_user_chat(client, users[full_user.id])
            parsed_chat.bio = full_user.about

            if getattr(full_user, "personal_channel_id", None):
                personal_chat = Chat._parse_channel_chat(
                    client,
                    chats[full_user.personal_channel_id]
                )
            # TODO:?|
            if getattr(full_user, "personal_channel_message", None):
                personal_chat_message = types.Message(
                    client=client,
                    id=full_user.personal_channel_message
                )

            if full_user.pinned_msg_id:
                try:
                    parsed_chat.pinned_message = await client.get_messages(
                        chat_id=parsed_chat.id,
                        message_ids=full_user.pinned_msg_id
                    )
                except MessageIdsEmpty:
                    parsed_chat.pinned_message = types.Message(
                        id=full_user.pinned_msg_id,
                        empty=True,
                        client=client
                    )

            if getattr(full_user, "birthday", None):
                parsed_chat.birthdate = types.Birthdate._parse(
                    full_user.birthday
                )
            
            if getattr(full_user, "business_intro", None):
                parsed_chat.business_intro = await types.BusinessIntro._parse(
                    client,
                    full_user.business_intro
                )
            if getattr(full_user, "business_location", None):
                parsed_chat.business_location = types.BusinessLocation._parse(
                    client,
                    full_user.business_location
                )
            if getattr(full_user, "business_work_hours", None):
                parsed_chat.business_opening_hours = types.BusinessOpeningHours._parse(
                    client,
                    full_user.business_work_hours
                )

        else:
            full_chat = chat_full.full_chat
            chat_raw = chats[full_chat.id]

            if isinstance(full_chat, raw.types.ChatFull):
                parsed_chat = Chat._parse_chat_chat(client, chat_raw)
                parsed_chat.description = full_chat.about or None

                if isinstance(full_chat.participants, raw.types.ChatParticipants):
                    parsed_chat.members_count = len(full_chat.participants.participants)
            else:
                parsed_chat = Chat._parse_channel_chat(client, chat_raw)
                parsed_chat.members_count = full_chat.participants_count
                parsed_chat.description = full_chat.about or None
                # TODO: Add StickerSet type
                parsed_chat.can_set_sticker_set = full_chat.can_set_stickers
                parsed_chat.sticker_set_name = getattr(full_chat.stickerset, "short_name", None)

                linked_chat_raw = chats.get(full_chat.linked_chat_id, None)

                if linked_chat_raw:
                    parsed_chat.linked_chat = Chat._parse_channel_chat(client, linked_chat_raw)

                default_send_as = full_chat.default_send_as

                if default_send_as:
                    if isinstance(default_send_as, raw.types.PeerUser):
                        send_as_raw = users[default_send_as.user_id]
                    else:
                        send_as_raw = chats[default_send_as.channel_id]

                    parsed_chat.send_as_chat = Chat._parse_chat(client, send_as_raw)

                parsed_chat.members_count = getattr(full_chat, "participants_count", 0)                
                parsed_chat.has_visible_history = not getattr(full_chat, "hidden_prehistory", False)
                parsed_chat.has_hidden_members = not getattr(full_chat, "participants_hidden", True)
                parsed_chat.has_aggressive_anti_spam_enabled = getattr(full_chat, "antispam", False)

                parsed_chat.slow_mode_delay = getattr(full_chat, "slowmode_seconds")
                parsed_chat.slowmode_next_send_date = utils.timestamp_to_datetime(
                    getattr(full_chat, "slowmode_next_send_date")
                )

                parsed_chat.unrestrict_boost_count = getattr(full_chat, "boosts_unrestrict", None)
                # TODO: Add EmojieStickerSet type
                parsed_chat.custom_emoji_sticker_set_name = getattr(full_chat.emojiset, "short_name", None)

            parsed_chat.message_auto_delete_time = getattr(full_chat, "ttl_period")

            if full_chat.pinned_msg_id:
                try:
                    parsed_chat.pinned_message = await client.get_messages(
                        chat_id=parsed_chat.id,
                        message_ids=full_chat.pinned_msg_id
                    )
                except MessageIdsEmpty:
                    parsed_chat.pinned_message = types.Message(
                        id=full_chat.pinned_msg_id,
                        empty=True,
                        client=client
                    )

            if isinstance(full_chat.exported_invite, raw.types.ChatInviteExported):
                parsed_chat.invite_link = full_chat.exported_invite.link

            parsed_chat.available_reactions = types.ChatReactions._parse(
                client,
                full_chat.available_reactions,
                reactions_limit=getattr(full_chat, "reactions_limit", None)
            )

        parsed_chat.personal_chat = personal_chat
        parsed_chat.personal_chat_message = personal_chat_message
        parsed_chat._raw = chat_full

        return parsed_chat

    @staticmethod
    def _parse_chat(client, chat: Union[raw.types.Chat, raw.types.User, raw.types.Channel]) -> "Chat":
        if isinstance(chat, raw.types.Chat):
            return Chat._parse_chat_chat(client, chat)
        elif isinstance(chat, raw.types.User):
            return Chat._parse_user_chat(client, chat)
        else:
            return Chat._parse_channel_chat(client, chat)

    @staticmethod
    def _parse_chat_preview(client, chat_invite: "raw.types.ChatInvite") -> "Chat":
        return Chat(
            _raw=chat_invite,
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
            is_verified=getattr(chat_invite, "verified", None),
            is_scam=getattr(chat_invite, "scam", None),
            is_fake=getattr(chat_invite, "fake", None),
            is_public=getattr(chat_invite, "public", None),
            join_by_request=getattr(chat_invite, "request_needed", None),
            is_peak_preview=True,
            client=client
        )

    async def archive(self):
        """Bound method *archive* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.archive_chats(-100123456789)

        Example:
            .. code-block:: python

                await chat.archive()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.archive_chats(self.id)

    async def unarchive(self):
        """Bound method *unarchive* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.unarchive_chats(-100123456789)

        Example:
            .. code-block:: python

                await chat.unarchive()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.unarchive_chats(self.id)

    # TODO: Remove notes about "All Members Are Admins" for basic groups, the attribute doesn't exist anymore
    async def set_title(self, title: str) -> bool:
        """Bound method *set_title* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.set_chat_title(
                chat_id=chat_id,
                title=title
            )

        Example:
            .. code-block:: python

                await chat.set_title("Lounge")

        Note:
            In regular groups (non-supergroups), this method will only work if the "All Members Are Admins"
            setting is off.

        Parameters:
            title (``str``):
                New chat title, 1-255 characters.

        Returns:
            ``bool``: True on success.

        Raises:
            RPCError: In case of Telegram RPC error.
            ValueError: In case a chat_id belongs to user.
        """

        return await self._client.set_chat_title(
            chat_id=self.id,
            title=title
        )

    async def set_description(self, description: str) -> bool:
        """Bound method *set_description* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.set_chat_description(
                chat_id=chat_id,
                description=description
            )

        Example:
            .. code-block:: python

                await chat.set_chat_description("Don't spam!")

        Parameters:
            description (``str``):
                New chat description, 0-255 characters.

        Returns:
            ``bool``: True on success.

        Raises:
            RPCError: In case of Telegram RPC error.
            ValueError: If a chat_id doesn't belong to a supergroup or a channel.
        """

        return await self._client.set_chat_description(
            chat_id=self.id,
            description=description
        )

    async def set_photo(
        self,
        *,
        photo: Union[str, BinaryIO] = None,
        video: Union[str, BinaryIO] = None,
        video_start_ts: float = None,
    ) -> bool:
        """Bound method *set_photo* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.set_chat_photo(
                chat_id=chat_id,
                photo=photo
            )

        Example:
            .. code-block:: python

                # Set chat photo using a local file
                await chat.set_photo(photo="photo.jpg")

                # Set chat photo using an existing Photo file_id
                await chat.set_photo(photo=photo.file_id)


                # Set chat video using a local file
                await chat.set_photo(video="video.mp4")

                # Set chat photo using an existing Video file_id
                await chat.set_photo(video=video.file_id)

        Parameters:
            photo (``str`` | ``BinaryIO``, *optional*):
                New chat photo. You can pass a :obj:`~pyrogram.types.Photo` file_id, a file path to upload a new photo
                from your local machine or a binary file-like object with its attribute
                ".name" set for in-memory uploads.

            video (``str`` | ``BinaryIO``, *optional*):
                New chat video. You can pass a :obj:`~pyrogram.types.Video` file_id, a file path to upload a new video
                from your local machine or a binary file-like object with its attribute
                ".name" set for in-memory uploads.

            video_start_ts (``float``, *optional*):
                The timestamp in seconds of the video frame to use as photo profile preview.

        Returns:
            ``bool``: True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
            ValueError: if a chat_id belongs to user.
        """

        return await self._client.set_chat_photo(
            chat_id=self.id,
            photo=photo,
            video=video,
            video_start_ts=video_start_ts
        )

    async def set_ttl(self, ttl_seconds: int) -> "types.Message":
        """Bound method *set_ttl* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.set_chat_ttl(
                chat_id=chat_id,
                ttl_seconds=ttl_seconds
            )

        Example:
            .. code-block:: python

                await chat.set_ttl(86400)

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the generated service message is returned.
        """
        return await self._client.set_chat_ttl(
            chat_id=self.id,
            ttl_seconds=ttl_seconds
        )

    async def ban_member(
        self,
        user_id: Union[int, str],
        until_date: datetime = utils.zero_datetime()
    ) -> Union["types.Message", bool]:
        """Bound method *ban_member* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.ban_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )

        Example:
            .. code-block:: python

                await chat.ban_member(123456789)

        Note:
            In regular groups (non-supergroups), this method will only work if the "All Members Are Admins" setting is
            off in the target group. Otherwise members may only be removed by the group's creator or by the member
            that added them.

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            until_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the user will be unbanned.
                If user is banned for more than 366 days or less than 30 seconds from the current time they are
                considered to be banned forever. Defaults to epoch (ban forever).

        Returns:
            :obj:`~pyrogram.types.Message` | ``bool``: On success, a service message will be returned (when applicable), otherwise, in
            case a message object couldn't be returned, True is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.ban_chat_member(
            chat_id=self.id,
            user_id=user_id,
            until_date=until_date
        )

    async def unban_member(
        self,
        user_id: Union[int, str]
    ) -> bool:
        """Bound method *unban_member* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.unban_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )

        Example:
            .. code-block:: python

                await chat.unban_member(123456789)

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            ``bool``: True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.unban_chat_member(
            chat_id=self.id,
            user_id=user_id,
        )

    async def restrict_member(
        self,
        user_id: Union[int, str],
        permissions: "types.ChatPermissions",
        use_independent_chat_permissions: bool = False,
        until_date: datetime = utils.zero_datetime(),
    ) -> "types.Chat":
        """Bound method *unban_member* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions()
            )

        Example:
            .. code-block:: python

                await chat.restrict_member(user_id, ChatPermissions())

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            permissions (:obj:`~pyrogram.types.ChatPermissions`):
                New user permissions.

            use_independent_chat_permissions (``bool``, *optional*):
                Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages and can_add_web_page_previews permissions will imply the can_send_messages, can_send_audios, can_send_documents, can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls permission will imply the can_send_messages permission.

            until_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the user will be unbanned.
                If user is banned for more than 366 days or less than 30 seconds from the current time they are
                considered to be banned forever. Defaults to epoch (ban forever).

        Returns:
            :obj:`~pyrogram.types.Chat`: On success, a chat object is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.restrict_chat_member(
            chat_id=self.id,
            user_id=user_id,
            permissions=permissions,
            use_independent_chat_permissions=use_independent_chat_permissions,
            until_date=until_date,
        )

    # Set None as privileges default due to issues with partially initialized module, because at the time Chat
    # is being initialized, ChatPrivileges would be required here, but was not initialized yet.
    async def promote_member(
        self,
        user_id: Union[int, str],
        privileges: "types.ChatPrivileges" = None
    ) -> bool:
        """Bound method *promote_member* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.promote_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )

        Example:

            .. code-block:: python

                await chat.promote_member(123456789)

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            privileges (:obj:`~pyrogram.types.ChatPrivileges`, *optional*):
                New user privileges.

        Returns:
            ``bool``: True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.promote_chat_member(
            chat_id=self.id,
            user_id=user_id,
            privileges=privileges
        )

    async def join(self):
        """Bound method *join* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.join_chat(123456789)

        Example:
            .. code-block:: python

                await chat.join()

        Note:
            This only works for public groups, channels that have set a username or linked chats.

        Returns:
            :obj:`~pyrogram.types.Chat`: On success, a chat object is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.join_chat(self.username or self.id)

    async def leave(self):
        """Bound method *leave* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.leave_chat(123456789)

        Example:
            .. code-block:: python

                await chat.leave()

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.leave_chat(self.id)

    async def export_invite_link(self):
        """Bound method *export_invite_link* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            client.export_chat_invite_link(123456789)

        Example:
            .. code-block:: python

                chat.export_invite_link()

        Returns:
            ``str``: On success, the exported invite link is returned.

        Raises:
            ValueError: In case the chat_id belongs to a user.
        """

        return await self._client.export_chat_invite_link(self.id)

    async def get_member(
        self,
        user_id: Union[int, str],
    ) -> "types.ChatMember":
        """Bound method *get_member* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.get_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )

        Example:
            .. code-block:: python

                await chat.get_member(user_id)

        Returns:
            :obj:`~pyrogram.types.ChatMember`: On success, a chat member is returned.
        """

        return await self._client.get_chat_member(
            self.id,
            user_id=user_id
        )

    def get_members(
        self,
        query: str = "",
        limit: int = 0,
        filter: "enums.ChatMembersFilter" = enums.ChatMembersFilter.SEARCH
    ) -> Optional[AsyncGenerator["types.ChatMember", None]]:
        """Bound method *get_members* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            async for member in client.get_chat_members(chat_id):
                print(member)

        Example:
            .. code-block:: python

                async for member in chat.get_members():
                    print(member)

        Parameters:
            query (``str``, *optional*):
                Query string to filter members based on their display names and usernames.
                Only applicable to supergroups and channels. Defaults to "" (empty string).
                A query string is applicable only for :obj:`~pyrogram.enums.ChatMembersFilter.SEARCH`,
                :obj:`~pyrogram.enums.ChatMembersFilter.BANNED` and :obj:`~pyrogram.enums.ChatMembersFilter.RESTRICTED`
                filters only.

            limit (``int``, *optional*):
                Limits the number of members to be retrieved.

            filter (:obj:`~pyrogram.enums.ChatMembersFilter`, *optional*):
                Filter used to select the kind of members you want to retrieve. Only applicable for supergroups
                and channels.

        Returns:
            ``Generator``: On success, a generator yielding :obj:`~pyrogram.types.ChatMember` objects is returned.
        """

        return self._client.get_chat_members(
            self.id,
            query=query,
            limit=limit,
            filter=filter
        )

    async def add_members(
        self,
        user_ids: Union[Union[int, str], List[Union[int, str]]],
        forward_limit: int = 100
    ) -> bool:
        """Bound method *add_members* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.add_chat_members(chat_id, user_id)

        Example:
            .. code-block:: python

                await chat.add_members(user_id)

        Returns:
            ``bool``: On success, True is returned.
        """

        return await self._client.add_chat_members(
            self.id,
            user_ids=user_ids,
            forward_limit=forward_limit
        )

    async def mark_unread(self, ) -> bool:
        """Bound method *mark_unread* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.mark_unread(chat_id)

        Example:
            .. code-block:: python

                await chat.mark_unread()

        Returns:
            ``bool``: On success, True is returned.
        """

        return await self._client.mark_chat_unread(self.id)

    async def set_protected_content(self, enabled: bool) -> bool:
        """Bound method *set_protected_content* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            await client.set_chat_protected_content(chat_id, enabled)

        Parameters:
            enabled (``bool``):
                Pass True to enable the protected content setting, False to disable.

        Example:
            .. code-block:: python

                await chat.set_protected_content(enabled)

        Returns:
            ``bool``: On success, True is returned.
        """

        return await self._client.set_chat_protected_content(
            self.id,
            enabled=enabled
        )

    async def unpin_all_messages(self) -> bool:
        """Bound method *unpin_all_messages* of :obj:`~pyrogram.types.Chat`.

        Use as a shortcut for:

        .. code-block:: python

            client.unpin_all_chat_messages(chat_id)

        Example:
            .. code-block:: python

                chat.unpin_all_messages()

        Returns:
            ``bool``: On success, True is returned.
        """

        return await self._client.unpin_all_chat_messages(self.id)

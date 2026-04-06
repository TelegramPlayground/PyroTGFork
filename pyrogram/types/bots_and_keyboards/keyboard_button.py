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

from typing import Optional

from pyrogram import raw, types, enums
from ..object import Object


class KeyboardButton(Object):
    """One button of the reply keyboard.

    At most one of the fields other than ``text``, ``icon_custom_emoji_id``, and ``style`` must be used to specify the type of the button.

    For simple text buttons String can be used instead of this object to specify text of the button.

    Parameters:
        text (``str``):
            Text of the button. If none of the optional fields are used, it will be sent as a message when
            the button is pressed.

        icon_custom_emoji_id (``int``, *optional*):
            Unique identifier of the custom emoji shown before the text of the button. Can only be used by bots that purchased additional usernames on Fragment or in the messages directly sent by the bot to private, group and supergroup chats if the owner of the bot has a Telegram Premium subscription..

        style (:obj:`~pyrogram.enums.ButtonStyle`, *optional*):
            Style of the button.
            If omitted, then an app-specific style is used.

        request_users (:obj:`~pyrogram.types.KeyboardButtonRequestUsers`, *optional*):
            If specified, pressing the button will open a list of suitable users. Identifiers of selected users will be sent to the bot in a “users_shared” service message.
            Available in private chats only.

        request_chat (:obj:`~pyrogram.types.KeyboardButtonRequestChat`, *optional*):
            If specified, pressing the button will open a list of suitable chats. Tapping on a chat will send its identifier to the bot in a “chat_shared” service message.
            Available in private chats only.

        request_managed_bot (:obj:`~pyrogram.types.KeyboardButtonRequestManagedBot`, *optional*):
            If specified, pressing the button will ask the user to create and share a bot that will be managed by the current bot.
            Available for bots that enabled management of other bots in the @BotFather Mini App.
            Available in private chats only.

        request_contact (``bool``, *optional*):
            If True, the user's phone number will be sent as a contact when the button is pressed.
            Available in private chats only.

        request_location (``bool``, *optional*):
            If True, the user's current location will be sent when the button is pressed.
            Available in private chats only.

        request_poll (:obj:`~pyrogram.types.KeyboardButtonPollType`, *optional*):
            If specified, the user will be asked to create a poll and send it to the bot when the button is pressed.
            Available in private chats only

        web_app (:obj:`~pyrogram.types.WebAppInfo`, *optional*):
            If specified, the described `Web App <https://core.telegram.org/bots/webapps>`_ will be launched when the
            button is pressed. The Web App will be able to send a “web_app_data” service message. Available in private
            chats only.

    """

    def __init__(
        self,
        text: str, *,
        request_contact: bool = None,
        request_location: bool = None,
        request_poll: "types.KeyboardButtonPollType" = None,
        web_app: "types.WebAppInfo" = None,
        request_users: "types.KeyboardButtonRequestUsers" = None,
        request_chat: "types.KeyboardButtonRequestChat" = None,
        request_managed_bot: "types.KeyboardButtonRequestManagedBot" = None,
        icon_custom_emoji_id: Optional[int] = None,
        style: "enums.ButtonStyle" = enums.ButtonStyle.DEFAULT
    ):
        super().__init__()

        self.text = str(text)
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_poll = request_poll
        self.web_app = web_app
        self.request_users = request_users
        self.request_chat = request_chat
        self.request_managed_bot = request_managed_bot
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.style = style

    @staticmethod
    def read(b):
        raw_style: "raw.types.KeyboardButtonStyle" = b.style
        button_style = enums.ButtonStyle.DEFAULT
        icon_custom_emoji_id = None

        if raw_style is not None:
            if raw_style.bg_primary:
                button_style = enums.ButtonStyle.PRIMARY
            elif raw_style.bg_danger:
                button_style = enums.ButtonStyle.DANGER
            elif raw_style.bg_success:
                button_style = enums.ButtonStyle.SUCCESS
            if raw_style.icon:
                icon_custom_emoji_id = raw_style.icon

        if isinstance(b, raw.types.KeyboardButton):
            return KeyboardButton(
                text=b.text,
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButtonRequestPhone):
            return KeyboardButton(
                text=b.text,
                request_contact=True,
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButtonRequestGeoLocation):
            return KeyboardButton(
                text=b.text,
                request_location=True,
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButtonRequestPoll):
            return KeyboardButton(
                text=b.text,
                request_poll=types.KeyboardButtonPollType(
                    type=enums.PollType.QUIZ if b.quiz else enums.PollType.REGULAR
                ),
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButtonSimpleWebView):
            return KeyboardButton(
                text=b.text,
                web_app=types.WebAppInfo(
                    url=b.url
                ),
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )
        # TODO
        if (
            isinstance(b, raw.types.KeyboardButtonRequestPeer) or
            isinstance(b, raw.types.InputKeyboardButtonRequestPeer)
        ):
            isFakeChannel = isinstance(b.peer_type, raw.types.RequestPeerTypeBroadcast)
            isFakeChat = isinstance(b.peer_type, raw.types.RequestPeerTypeChat)

            _nr = getattr(b, "name_requested", None)
            _ur = getattr(b, "username_requested", None)
            _pr = getattr(b, "photo_requested", None)

            if isFakeChannel or isFakeChat:
                user_administrator_rights = types.ChatPrivileges._parse(
                    getattr(
                        b.peer_type,
                        "user_admin_rights",
                        None
                    )
                )
                bot_administrator_rights = types.ChatPrivileges._parse(
                    getattr(
                        b.peer_type,
                        "bot_admin_rights",
                        None
                    )
                )
                return KeyboardButton(
                    text=b.text,
                    request_chat=types.KeyboardButtonRequestChat(
                        request_id=b.button_id,
                        chat_is_channel=isFakeChannel,
                        chat_is_forum=getattr(b.peer_type, "forum", None),
                        chat_has_username=getattr(b.peer_type, "has_username", None),
                        chat_is_created=getattr(b.peer_type, "creator", None),
                        user_administrator_rights=user_administrator_rights,
                        bot_administrator_rights=bot_administrator_rights,
                        bot_is_member=getattr(b.peer_type, "bot_participant", None),
                        request_title=_nr,
                        request_username=_ur,
                        request_photo=_pr
                    ),
                    style=button_style,
                    icon_custom_emoji_id=icon_custom_emoji_id
                )

            if isinstance(b.peer_type, raw.types.RequestPeerTypeUser):
                return KeyboardButton(
                    text=b.text,
                    request_users=types.KeyboardButtonRequestUsers(
                        request_id=b.button_id,
                        user_is_bot=getattr(b.peer_type, "bot", None),
                        user_is_premium=getattr(b.peer_type, "premium", None),
                        max_quantity=b.max_quantity,
                        request_name=_nr,
                        request_username=_ur,
                        request_photo=_pr
                    ),
                    style=button_style,
                    icon_custom_emoji_id=icon_custom_emoji_id
                )

            if isinstance(b.peer_type, raw.types.RequestPeerTypeCreateBot):
                return KeyboardButton(
                    text=b.text,
                    style=button_style,
                    icon_custom_emoji_id=icon_custom_emoji_id,
                    request_managed_bot=types.KeyboardButtonRequestManagedBot(
                        request_id=b.button_id,
                        suggested_name=b.peer_type.suggested_name,
                        suggested_username=b.peer_type.suggested_username,
                    )
                )

    def write(self):
        if isinstance(self, str):
            return raw.types.KeyboardButton(
                text=self
            )

        raw_style = raw.types.KeyboardButtonStyle(
            bg_primary=self.style == enums.ButtonStyle.PRIMARY,
            bg_danger=self.style == enums.ButtonStyle.DANGER,
            bg_success=self.style == enums.ButtonStyle.SUCCESS,
            icon=self.icon_custom_emoji_id
        )

        if self.request_contact:
            return raw.types.KeyboardButtonRequestPhone(
                text=self.text,
                style=raw_style
            )
        elif self.request_location:
            return raw.types.KeyboardButtonRequestGeoLocation(
                text=self.text,
                style=raw_style
            )
        elif self.request_poll:
            return raw.types.KeyboardButtonRequestPoll(
                text=self.text,
                quiz=True if self.request_poll.type == enums.PollType.QUIZ else False,
                style=raw_style
            )
        elif self.web_app:
            return raw.types.KeyboardButtonSimpleWebView(
                text=self.text,
                url=self.web_app.url,
                style=raw_style
            )
        elif self.request_users:
            return raw.types.InputKeyboardButtonRequestPeer(
                name_requested=self.request_users.request_name,
                username_requested=self.request_users.request_username,
                photo_requested=self.request_users.request_photo,
                text=self.text,
                button_id=self.request_users.request_id,
                peer_type=raw.types.RequestPeerTypeUser(
                    bot=self.request_users.user_is_bot,
                    premium=self.request_users.user_is_premium
                ),
                max_quantity=self.request_users.max_quantity,
                style=raw_style
            )

        elif self.request_chat:
            user_admin_rights = self.request_chat.user_administrator_rights.write() if self.request_chat.user_administrator_rights else None
            bot_admin_rights = self.request_chat.bot_administrator_rights.write() if self.request_chat.bot_administrator_rights else None
            if self.request_chat.chat_is_channel:
                return raw.types.InputKeyboardButtonRequestPeer(
                    name_requested=self.request_chat.request_title,
                    username_requested=self.request_chat.request_username,
                    photo_requested=self.request_chat.request_photo,
                    text=self.text,
                    button_id=self.request_chat.request_id,
                    peer_type=raw.types.RequestPeerTypeBroadcast(
                        creator=self.request_chat.chat_is_created,
                        has_username=self.request_chat.chat_has_username,
                        user_admin_rights=user_admin_rights,
                        bot_admin_rights=bot_admin_rights
                    ),
                    max_quantity=1,
                    style=raw_style
                )
            else:
                return raw.types.InputKeyboardButtonRequestPeer(
                    name_requested=self.request_chat.request_title,
                    username_requested=self.request_chat.request_username,
                    photo_requested=self.request_chat.request_photo,
                    text=self.text,
                    button_id=self.request_chat.request_id,
                    peer_type=raw.types.RequestPeerTypeChat(
                        creator=self.request_chat.chat_is_created,
                        bot_participant=self.request_chat.bot_is_member,
                        has_username=self.request_chat.chat_has_username,
                        forum=self.request_chat.chat_is_forum,
                        user_admin_rights=user_admin_rights,
                        bot_admin_rights=bot_admin_rights
                    ),
                    max_quantity=1,
                    style=raw_style
                )
        elif self.request_managed_bot:
            return raw.types.InputKeyboardButtonRequestPeer(
                max_quantity=1, 
                style=raw_style,
                text=self.text,
                button_id=self.request_managed_bot.request_id,
                peer_type=raw.types.RequestPeerTypeCreateBot(
                    bot_managed=True,
                    suggested_name=self.request_managed_bot.suggested_name,
                    suggested_username=self.request_managed_bot.suggested_username,
                ),
            )
        else:
            return raw.types.KeyboardButton(
                text=self.text,
                style=raw_style
            )

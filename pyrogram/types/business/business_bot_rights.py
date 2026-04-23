#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present <https://github.com/TelegramPlayGround>
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
from pyrogram import raw

from ..object import Object


class BusinessBotRights(Object):
    """Represents the rights of a business bot.

    Parameters:
        can_reply (``bool``, *optional*):
            True, if the bot can send and edit messages in the private chats that had incoming messages in the last 24 hours.

        can_read_messages (``bool``, *optional*):
            True, if the bot can mark incoming private messages as read.

        can_delete_sent_messages (``bool``, *optional*):
            True, if the bot can delete messages sent by the bot.

        can_delete_all_messages (``bool``, *optional*):
            True, if the bot can delete all private messages in managed chats.

        can_edit_name (``bool``, *optional*):
            True, if the bot can edit the first and last name of the business account.

        can_edit_bio (``bool``, *optional*):
            True, if the bot can edit the bio of the business account.

        can_edit_profile_photo (``bool``, *optional*):
            True, if the bot can edit the profile photo of the business account.

        can_edit_username (``bool``, *optional*):
            True, if the bot can edit the username of the business account.

        can_change_gift_settings (``bool``, *optional*):
            True, if the bot can change the privacy settings pertaining to gifts for the business account.

        can_view_gifts_and_stars (``bool``, *optional*):
            True, if the bot can view gifts and the amount of Telegram Stars owned by the business account.

        can_convert_gifts_to_stars (``bool``, *optional*):
            True, if the bot can convert regular gifts owned by the business account to Telegram Stars.
        
        can_transfer_and_upgrade_gifts (``bool``, *optional*):
            True, if the bot can transfer and upgrade gifts owned by the business account.

        can_transfer_stars (``bool``, *optional*):
            True, if the bot can transfer Telegram Stars received by the business account to its own account, or use them to upgrade and transfer gifts.

        can_manage_stories (``bool``, *optional*):
            True, if the bot can post, edit and delete stories on behalf of the business account.

    """

    def __init__(
        self,
        *,
        can_reply: Optional[bool] = None,
        can_read_messages: Optional[bool] = None,
        can_delete_sent_messages: Optional[bool] = None,
        can_delete_all_messages: Optional[bool] = None,
        can_edit_name: Optional[bool] = None,
        can_edit_bio: Optional[bool] = None,
        can_edit_profile_photo: Optional[bool] = None,
        can_edit_username: Optional[bool] = None,
        can_change_gift_settings: Optional[bool] = None,
        can_view_gifts_and_stars: Optional[bool] = None,
        can_convert_gifts_to_stars: Optional[bool] = None,
        can_transfer_and_upgrade_gifts: Optional[bool] = None,
        can_transfer_stars: Optional[bool] = None,
        can_manage_stories: Optional[bool] = None,
    ):
        super().__init__()

        self.can_reply = can_reply
        self.can_read_messages = can_read_messages
        self.can_delete_sent_messages = can_delete_sent_messages
        self.can_delete_all_messages = can_delete_all_messages
        self.can_edit_name = can_edit_name
        self.can_edit_bio = can_edit_bio
        self.can_edit_profile_photo = can_edit_profile_photo
        self.can_edit_username = can_edit_username
        self.can_change_gift_settings = can_change_gift_settings
        self.can_view_gifts_and_stars = can_view_gifts_and_stars
        self.can_convert_gifts_to_stars = can_convert_gifts_to_stars
        self.can_transfer_and_upgrade_gifts = can_transfer_and_upgrade_gifts
        self.can_transfer_stars = can_transfer_stars
        self.can_manage_stories = can_manage_stories


    @staticmethod
    def _parse(
        client,
        business_bot_rights: "raw.types.BusinessBotRights"
    ) -> "BusinessBotRights":
        if not business_bot_rights:
            return None
        return BusinessBotRights(
            can_reply=business_bot_rights.reply,
            can_read_messages=business_bot_rights.read_messages,
            can_delete_sent_messages=business_bot_rights.delete_sent_messages,
            can_delete_all_messages=business_bot_rights.delete_received_messages,
            can_edit_name=business_bot_rights.edit_name,
            can_edit_bio=business_bot_rights.edit_bio,
            can_edit_profile_photo=business_bot_rights.edit_profile_photo,
            can_edit_username=business_bot_rights.edit_username,
            can_change_gift_settings=business_bot_rights.change_gift_settings,
            can_view_gifts_and_stars=business_bot_rights.view_gifts,
            can_convert_gifts_to_stars=business_bot_rights.sell_gifts,
            can_transfer_and_upgrade_gifts=business_bot_rights.transfer_and_upgrade_gifts,
            can_transfer_stars=business_bot_rights.transfer_stars,
            can_manage_stories=business_bot_rights.manage_stories,
        )

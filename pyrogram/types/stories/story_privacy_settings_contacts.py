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


from typing import Union

import pyrogram
from pyrogram import raw

from .story_privacy_settings import StoryPrivacySettings


class StoryPrivacySettingsContacts(StoryPrivacySettings):
    """The story can be viewed by all contacts except chosen users.

    Parameters:
        except_user_ids (List of ``int`` | ``str``, *optional*):
            User identifiers of the contacts that can't see the story; always unknown and empty for non-owned stories.

    """

    def __init__(self, *, except_user_ids: list[Union[int, str]]=None):
        super().__init__()

        self.except_user_ids = except_user_ids

    async def write(self, client: "pyrogram.Client"):
        privacy_rules = []
        privacy_rules.append(raw.types.InputPrivacyValueAllowContacts())
        users = [await client.resolve_peer(user_id) for user_id in (self.except_user_ids or [])]
        if users:
            privacy_rules.append(raw.types.InputPrivacyValueDisallowUsers(users=users))
        return privacy_rules

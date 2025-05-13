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
from pyrogram import errors, raw, types


class CanPostStory:
    async def can_post_story(
        self: "pyrogram.Client",
        chat_id: Union[int, str]
    ) -> "types.CanPostStoryResult":
        """Checks whether the current user can post a story on behalf of a chat.

        .. include:: /_includes/usable-by/users.rst

        Requires can_post_stories right for supergroup and channel chats.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns:
            :obj:`~pyrogram.types.CanPostStoryResult`: On success.

        Example:
            .. code-block:: python

                # Check if you can send story to chat id
                await app.can_post_story(chat_id)

        """
        try:
            r = await self.invoke(
                raw.functions.stories.CanSendStory(
                    peer=await self.resolve_peer(chat_id),
                )
            )
        except errors.PremiumAccountRequired:
            return types.CanPostStoryResultPremiumNeeded()
        except errors.BoostsRequired:
            return types.CanPostStoryResultBoostNeeded()
        except errors.StoriesTooMuch:
            return types.CanPostStoryResultActiveStoryLimitExceeded()
        except errors.StorySendFloodWeekly as ex:
            return types.CanPostStoryResultWeeklyLimitExceeded(
                retry_after=ex.value
            )
        except errors.StorySendFloodMonthly as ex:
            return types.CanPostStoryResultMonthlyLimitExceeded(
                retry_after=ex.value
            )
        return types.CanPostStoryResultOk(story_count=r.count_remains)

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


import pyrogram
from pyrogram import types

from .story_origin import StoryOrigin


class StoryOriginPublicStory(StoryOrigin):
    """The original story was a public story that was posted by a known chat.

    Parameters:
        chat (:obj:`~pyrogram.types.Chat`):
            Identifier of the chat that posted original story.
        
        story_id (``int``):
            Story identifier of the original story.

    """

    def __init__(
        self,
        *,
        chat: "types.Chat" = None,
        story_id: int = None
    ):
        super().__init__()

        self.chat = chat
        self.story_id = story_id

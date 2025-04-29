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


from ..object import Object


class StoryAreaType(Object):
    """This object describes the type of a clickable area on a story.

    Currently, it can be one of:

    .. include:: /_includes/usable-by/users-bots.rst

    - :obj:`~pyrogram.types.StoryAreaTypeLocation`
    - :obj:`~pyrogram.types.StoryAreaTypeSuggestedReaction`
    - :obj:`~pyrogram.types.StoryAreaTypeLink`
    - :obj:`~pyrogram.types.StoryAreaTypeWeather`
    - :obj:`~pyrogram.types.StoryAreaTypeUniqueGift`

    .. include:: /_includes/usable-by/users.rst

    - :obj:`~pyrogram.types.StoryAreaTypeMessage`
    - :obj:`~pyrogram.types.StoryAreaTypeFoundVenue`

    """

    def __init__(self):
        super().__init__()

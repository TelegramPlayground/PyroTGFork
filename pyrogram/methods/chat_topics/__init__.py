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

from .get_forum_topic_icon_stickers import GetForumTopicIconStickers
from .create_forum_topic import CreateForumTopic
from .edit_forum_topic import EditForumTopic
from .close_forum_topic import CloseForumTopic
from .reopen_forum_topic import ReopenForumTopic
from .hide_forum_topic import HideForumTopic
from .unhide_forum_topic import UnhideForumTopic
from .delete_forum_topic import DeleteForumTopic
from .get_forum_topics import GetForumTopics
from .get_forum_topic import GetForumTopic


class ChatTopics(
    CloseForumTopic,
    CreateForumTopic,
    DeleteForumTopic,
    EditForumTopic,
    GetForumTopic,
    GetForumTopicIconStickers,
    GetForumTopics,
    HideForumTopic,
    ReopenForumTopic,
    UnhideForumTopic,
):
    pass

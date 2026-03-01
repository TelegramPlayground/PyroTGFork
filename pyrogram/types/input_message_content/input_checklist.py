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
from pyrogram import types, enums
from ..object import Object


class InputChecklist(Object):
    """Describes a checklist to create.

    Parameters:
        title  (``str``):
            Title of the checklist; 1-255 characters after entities parsing.
        
        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        title_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            List of special entities that appear in the poll option text, which can be specified instead of *text_parse_mode*.
            Currently, only bold, italic, underline, strikethrough, spoiler, and custom_emoji entities are allowed.

        tasks (List of :obj:`~pyrogram.types.InputChecklistTask`):
            List of 1-30 tasks in the checklist.

        others_can_add_tasks  (``bool``, *optional*):
            Pass True if other users can add tasks to the checklist.

        others_can_mark_tasks_as_done (``bool``, *optional*):
            Pass True if other users can mark tasks as done or not done in the checklist.

    """

    def __init__(
        self,
        title: str = None,
        parse_mode: "enums.ParseMode" = None,
        title_entities: list["types.MessageEntity"] = None,
        tasks: list["types.InputChecklistTask"] = None,
        others_can_add_tasks: bool = None,
        others_can_mark_tasks_as_done: bool = None,
    ):
        super().__init__()

        self.title = title
        self.parse_mode = parse_mode
        self.title_entities = title_entities
        self.tasks = tasks
        self.others_can_add_tasks = others_can_add_tasks
        self.others_can_mark_tasks_as_done = others_can_mark_tasks_as_done

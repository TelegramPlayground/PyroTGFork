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

from typing import Dict, Optional

import pyrogram
from pyrogram import raw, types, utils

from ..object import Object
from .message import Str


class Checklist(Object):
    """Describes a checklist.

    Parameters:
        title (``str``):
            Title of the checklist.

        title_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            Special entities that appear in the checklist title.
            May contain only Bold, Italic, Underline, Strikethrough, Spoiler, and CustomEmoji entities.

        tasks (List of :obj:`~pyrogram.types.ChecklistTask`, *optional*):
            List of tasks in the checklist.

        others_can_add_tasks (``bool``, *optional*):
            True, if users other than the creator of the list can add tasks to the list.

        others_can_mark_tasks_as_done (``bool``, *optional*):
            True, if users other than the creator of the list can mark tasks as done or not done.

    """

    def __init__(
        self,
        *,
        title: str,
        title_entities: Optional[list["types.MessageEntity"]] = None,
        tasks: Optional[list["types.ChecklistTask"]] = None,
        others_can_add_tasks: Optional[bool] = None,
        others_can_mark_tasks_as_done: Optional[bool] = None,
    ):
        super().__init__()

        self.title = title
        self.title_entities = title_entities
        self.tasks = tasks
        self.others_can_add_tasks = others_can_add_tasks
        self.others_can_mark_tasks_as_done = others_can_mark_tasks_as_done

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        checklist: "raw.types.MessageMediaToDo",
        users: Dict[int, "raw.base.User"],
    ) -> "Checklist":
        completions = {i.id: i for i in getattr(checklist, "completions", [])}

        checklist_tasks = []

        for task in checklist.todo.list:
            checklist_tasks.append(
                types.ChecklistTask._parse(
                    client,
                    task,
                    completions.get(task.id),
                    users
                )
            )

        title_entities = [
            types.MessageEntity._parse(client, entity, users)
            for entity in checklist.todo.title.entities
        ]
        title_entities = types.List(filter(lambda x: x is not None, title_entities))
        title = Str(checklist.todo.title.text).init(title_entities) or None

        return Checklist(
            title=title,
            title_entities=title_entities,
            tasks=checklist_tasks,
            others_can_add_tasks=checklist.todo.others_can_append,
            others_can_mark_tasks_as_done=checklist.todo.others_can_complete,
        )

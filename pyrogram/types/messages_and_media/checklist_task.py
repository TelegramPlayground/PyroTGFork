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

from datetime import datetime
from typing import Dict, Optional

import pyrogram
from pyrogram import raw, types, utils

from ..object import Object
from .message import Str


class ChecklistTask(Object):
    """Describes a task in a checklist.

    Parameters:
        id (``int``):
            Unique identifier of the task.

        text (``str``):
            Text of the task.

        text_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            Special entities that appear in the task text.
            May contain only Bold, Italic, Underline, Strikethrough, Spoiler, CustomEmoji, Url, EmailAddress, Mention, Hashtag, Cashtag and PhoneNumber entities.

        completed_by_user (:obj:`~pyrogram.types.User`, *optional*):
            The user that completed the task.
            None if the task isn't completed.

        completion_date (:py:obj:`~datetime.datetime`, *optional*):
            Date when the task was completed.
            None if the task isn't completed.

    """

    def __init__(
        self,
        *,
        id: int,
        text: str,
        text_entities: Optional[list["types.MessageEntity"]] = None,
        completed_by_user: Optional["types.User"] = None,
        completion_date: Optional[datetime] = None,
    ):
        super().__init__()

        self.id = id
        self.text = text
        self.text_entities = text_entities
        self.completed_by_user = completed_by_user
        self.completion_date = completion_date

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        item: "raw.types.TodoItem",
        completion: "raw.types.TodoCompletion",
        users: Dict[int, "raw.base.User"],
    ) -> "ChecklistTask":
        text_entities = [
            types.MessageEntity._parse(client, entity, users)
            for entity in item.title.entities
        ]
        text_entities = types.List(filter(lambda x: x is not None, text_entities))
        text = Str(item.title.text).init(text_entities) or None

        return ChecklistTask(
            id=item.id,
            text=text,
            text_entities=text_entities,
            completed_by_user=types.User._parse(client, users.get(getattr(completion, "completed_by", None))),
            completion_date=utils.timestamp_to_datetime(getattr(completion, "date", None))
        )

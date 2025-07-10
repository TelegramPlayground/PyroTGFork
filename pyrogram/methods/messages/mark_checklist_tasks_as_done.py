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
from pyrogram import raw, types


class MarkChecklistTasksAsDone:
    async def mark_checklist_tasks_as_done(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        *,
        done_task_ids: list[int] = None,
        not_done_task_ids: list[int] = None,
    ) -> Union["types.Message", bool]:
        """Add tasks of a checklist in a message as done or not done.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Identifier of the message containing the checklist.

            done_task_ids (List of ``int``):
                Identifiers of tasks that were marked as done.

            not_done_task_ids (List of ``int``):
                Identifiers of tasks that were marked as not done.

        Returns:
            :obj:`~pyrogram.types.Message` | ``bool``: On success, an edited message or a service message will be returned (when applicable),
            otherwise, in case a message object couldn't be returned, True is returned.

        Example:
            .. code-block:: python

                await app.mark_checklist_tasks_as_done(
                    chat_id,
                    message_id,
                    done_task_ids=[1, 2, 3]
                )

        """
        r = await self.invoke(
            raw.functions.messages.ToggleTodoCompleted(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                completed=done_task_ids or [],
                incompleted=not_done_task_ids or [],
            )
        )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage, raw.types.UpdateEditChannelMessage, raw.types.UpdateNewChannelMessage)):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    replies=self.fetch_replies
                )

        return True

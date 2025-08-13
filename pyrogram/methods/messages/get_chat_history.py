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

import logging
from asyncio import sleep
from datetime import datetime
from typing import AsyncGenerator, Optional, Union 

import pyrogram
from pyrogram import raw, types, utils

log = logging.getLogger(__name__)


async def get_chunk(
    *,
    client: "pyrogram.Client",
    chat_id: Union[int, str],
    limit: int = 0,
    offset: int = 0,
    min_id: int = 0,
    max_id: int = 0,
    offset_id: int = 0,
    from_date: datetime = utils.zero_datetime(),
    reverse: bool = False,
    is_scheduled: bool = False
) -> list[types.Message]:
    if is_scheduled:
        r = await client.invoke(
            raw.functions.messages.GetScheduledHistory(
                peer=await client.resolve_peer(chat_id),
                hash=0
            ),
            sleep_threshold=60
        )
        messages = await utils.parse_messages(
            client,
            r,
            is_scheduled=True,
            replies=0
        )
        if reverse:
            messages.reverse()
        return messages
    else:
        if (min_id or max_id) and not offset_id:
            if max_id:
                offset_id = max_id + 1
            elif min_id:
                offset_id = 0
        if min_id and max_id and not offset_id:
            offset_id = max_id + 1
        history: raw.base.messages.Messages = await client.invoke(
            raw.functions.messages.GetHistory(
                peer=await client.resolve_peer(chat_id),
                offset_id=offset_id,
                offset_date=utils.datetime_to_timestamp(from_date),
                add_offset=offset,
                limit=limit,
                max_id=max_id,
                min_id=min_id,
                hash=0
            ),
            sleep_threshold=60
        )
        messages = await utils.parse_messages(
            client,
            history,
            is_scheduled=False,
            replies=0
        )
        if reverse:
            messages.reverse()
        return messages


class GetChatHistory:
    async def get_chat_history(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        limit: int = 0,
        *,
        offset: int = 0,
        offset_id: int = None,
        min_id: int = 0,
        max_id: int = 0,
        offset_date: datetime = utils.zero_datetime(),
        reverse: bool = False,
        is_scheduled: bool = False
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Get messages from a chat history.

        The messages are returned in reverse chronological order by default.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, no limit is applied and all messages are returned.

            offset (``int``, *optional*):
                Sequential number of the first message to be returned.
                Negative values are also accepted and become useful in case you set offset_id or offset_date.

            offset_id (``int``, *optional*):
                Identifier of the first message to be returned.
                This parameter is deprecated and should not be used.
                Use ``min_id`` / ``max_id`` instead for proper filtering.

            min_id (``int``, *optional*):
                If a positive value was transferred, the method will return only messages with IDs more than min_id.
                Defaults to 0.

            max_id (``int``, *optional*):
                If a positive value was transferred, the method will return only messages with IDs less than max_id.
                Defaults to 0.

            offset_date (:py:obj:`~datetime.datetime`, *optional*):
                Pass a date as offset to retrieve only older messages starting from that date.

            reverse (``bool``, *optional*):
                Pass True to retrieve the messages in reversed order (from older to most recent). Defaults to False.

            is_scheduled (``bool``, *optional*):
                Whether to get scheduled messages. Defaults to False.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Message` objects.

        Example:
            .. code-block:: python

                async for message in app.get_chat_history(chat_id):
                    print(message.text)
        """
        if offset_id is not None:
            log.warning(
                "`offset_id` is deprecated and will be removed in future updates. Use `min_id` or `max_id` instead."
            )

        current: int = 0
        total: int = limit or (1 << 31) - 1
        limit: int = min(100, total)

        if reverse:
            offset_id = min_id if min_id else 1
            offset = offset - limit
        else:
            offset_id = max_id if max_id else 0

        while True:
            messages = await get_chunk(
                client=self,
                chat_id=chat_id,
                limit=limit,
                offset=offset,
                offset_id=offset_id,
                min_id=min_id,
                max_id=max_id,
                from_date=offset_date,
                reverse=reverse,
                is_scheduled=is_scheduled
            )

            if not messages:
                return

            offset_id = messages[-1].id + (1 if reverse else 0)

            for message in messages:
                await sleep(0)
                yield message

                current += 1

                if current >= total:
                    return

            if is_scheduled:
                break

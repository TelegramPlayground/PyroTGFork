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

from typing import AsyncGenerator, Optional

from pyrogram import types, raw, utils
from pyrogram.errors import ChannelPrivate, PeerIdInvalid


class GetDialogs:
    async def get_dialogs(
        self: "pyrogram.Client",
        limit: int = 0,
        pinned_only: bool = False,
        chat_list: int = 0
    ) -> Optional[AsyncGenerator["types.Dialog", None]]:

        current = 0
        total = limit or (1 << 31) - 1
        request_limit = min(100, total)

        offset_date = 0
        offset_id = 0
        offset_peer = raw.types.InputPeerEmpty()

        seen_dialog_ids = set()

        while True:
            r = await self.invoke(
                raw.functions.messages.GetDialogs(
                    offset_date=offset_date,
                    offset_id=offset_id,
                    offset_peer=offset_peer,
                    limit=request_limit,
                    hash=0,
                    exclude_pinned=not pinned_only,
                    folder_id=chat_list
                ),
                sleep_threshold=60
            )

            users = {i.id: i for i in r.users}
            chats = {i.id: i for i in r.chats}

            messages = {}

            for message in r.messages:
                if isinstance(message, raw.types.MessageEmpty):
                    continue

                chat_id = utils.get_peer_id(message.peer_id)
                try:
                    messages[chat_id] = await types.Message._parse(self, message, users, chats)
                except (ChannelPrivate, PeerIdInvalid):
                    continue

            dialogs = []

            for dialog in r.dialogs:
                if not isinstance(dialog, raw.types.Dialog):
                    continue

                parsed = types.Dialog._parse(self, dialog, messages, users, chats)
                if parsed.chat.id in seen_dialog_ids:
                    continue
                seen_dialog_ids.add(parsed.chat.id)

                dialogs.append(parsed)

            if not dialogs:
                return

            last = dialogs[-1]

            if last.top_message is None:
                return

            offset_id = last.top_message.id
            offset_date = utils.datetime_to_timestamp(last.top_message.date)
            offset_peer = await self.resolve_peer(last.chat.id)

            for dialog in dialogs:
                yield dialog
                current += 1
                if current >= total:
                    return

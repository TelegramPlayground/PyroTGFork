#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present <https://github.com/KurimuzonAkuma>
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

from asyncio import sleep
from typing import AsyncGenerator, Optional, Union

import pyrogram
from pyrogram import raw, types


class GetChatAudios:
    async def get_chat_audios(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        offset: Optional[int] = 0,
        limit: Optional[int] = 0,
    ) -> Optional[
        AsyncGenerator["types.Audio", None]
    ]:
        """Get a user profile audios sequentially.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            offset (``int``, *optional*):
                Sequential number of the first audio to be returned. By default, all audios are returned.

            limit (``int``, *optional*):
                Limits the number of audios to be retrieved.
                By default, no limit is applied and all profile audios are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Audio` objects.

        Example:
            .. code-block:: python

                async for audio in app.get_chat_audios("me"):
                    print(audio)

        """
        peer_id = await self.resolve_peer(chat_id)

        current = 0
        total = limit or (1 << 31)
        limit = min(100, total)

        while True:
            r = await self.invoke(
                raw.functions.users.GetSavedMusic(
                    id=peer_id,
                    offset=offset,
                    limit=limit,
                    hash=0
                )
            )

            audios = []

            for doc in r.documents:
                attributes = {type(i): i for i in doc.attributes}

                audios.append(
                    types.Audio._parse(
                        self,
                        doc,
                        attributes[raw.types.DocumentAttributeAudio],
                        getattr(
                            attributes.get(raw.types.DocumentAttributeFilename, None),
                            "file_name",
                            None,
                        ),
                    )
                )

            if not audios:
                return

            offset += len(audios)

            for audio in audios:
                await sleep(0)

                yield audio

                current += 1

                if current >= total:
                    return

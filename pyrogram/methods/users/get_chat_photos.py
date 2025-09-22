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

from asyncio import sleep
from typing import Union, AsyncGenerator
import pyrogram
from pyrogram import types, raw, utils


class GetChatPhotos:
    async def get_chat_photos(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        limit: int = 0,
    ) -> AsyncGenerator[Union["types.Photo", "types.Animation"], None]:
        """Get a chat or a user profile photos sequentially, without duplicates."""

        total = limit or (1 << 31)
        chunk_limit = min(100, total)

        peer_id = await self.resolve_peer(chat_id)
        seen: set[str] = set()  # зберігаємо file_unique_id

        if isinstance(peer_id, raw.types.InputPeerChannel):
            r = await self.invoke(raw.functions.channels.GetFullChannel(channel=peer_id))

            _animation = types.Animation._parse_chat_animation(self, r.full_chat.chat_photo)
            _photo = types.Photo._parse(self, r.full_chat.chat_photo)
            chat_icons = [_animation or _photo]

            if not (self.me and self.me.is_bot):
                r = await utils.parse_messages(
                    self,
                    await self.invoke(
                        raw.functions.messages.Search(
                            peer=peer_id,
                            q="",
                            filter=raw.types.InputMessagesFilterChatPhotos(),
                            min_date=0,
                            max_date=0,
                            offset_id=0,
                            add_offset=0,
                            limit=chunk_limit,
                            max_id=0,
                            min_id=0,
                            hash=0,
                        )
                    ),
                )
                for m in r:
                    if isinstance(m.new_chat_photo, (types.Animation, types.Photo)):
                        chat_icons.append(m.new_chat_photo)

            current = 0
            for icon in chat_icons:
                await sleep(0)
                if not icon:
                    continue

                if icon.file_unique_id in seen:
                    continue
                seen.add(icon.file_unique_id)

                yield icon
                current += 1

                if current >= total:
                    return

        else:
            current = 0
            offset = 0

            while True:
                r = await self.invoke(
                    raw.functions.photos.GetUserPhotos(
                        user_id=peer_id, offset=offset, max_id=0, limit=chunk_limit
                    )
                )

                photos = [
                    types.Animation._parse_chat_animation(self, p) or types.Photo._parse(self, p)
                    for p in r.photos
                ]

                if not photos:
                    return

                offset += len(photos)

                for photo in photos:
                    await sleep(0)
                    if not photo:
                        continue

                    if photo.file_unique_id in seen:
                        continue
                    seen.add(photo.file_unique_id)

                    yield photo
                    current += 1

                    if current >= total:
                        return

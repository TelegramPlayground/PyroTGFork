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
from typing import Union, AsyncGenerator, Optional

import pyrogram
from pyrogram import types, raw


class GetChatPhotos:
    async def get_chat_photos(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        limit: int = 0,
    ) -> Optional[
        Union[
            AsyncGenerator["types.Photo", None],
            AsyncGenerator["types.Animation", None],
        ]
    ]:
        """Get a chat or a user profile photos sequentially.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            limit (``int``, *optional*):
                Limits the number of profile photos to be retrieved.
                By default, no limit is applied and all profile photos are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Photo` | :obj:`~pyrogram.types.Animation` objects.

        Example:
            .. code-block:: python

                async for photo in app.get_chat_photos("me"):
                    print(photo)
        """
        total = limit or (1 << 31)
        limit = min(100, total)

        peer_id = await self.resolve_peer(chat_id)

        if isinstance(peer_id, raw.types.InputPeerChannel):
            r = await self.invoke(raw.functions.channels.GetFullChannel(channel=peer_id))

            _animation = types.Animation._parse_chat_animation(self, r.full_chat.chat_photo)
            _photo = types.Photo._parse(self, r.full_chat.chat_photo)
            chat_icons = [_animation or _photo]

            if not (self.me and self.me.is_bot):
                r = await self.invoke(
                    raw.functions.messages.Search(
                        peer=peer_id,
                        q="",
                        filter=raw.types.InputMessagesFilterChatPhotos(),
                        min_date=0,
                        max_date=0,
                        offset_id=0,
                        add_offset=0,
                        limit=limit,
                        max_id=0,
                        min_id=0,
                        hash=0,
                    )
                )
                if _icon := chat_icons[0]:
                    _first_file_id = _icon.file_id if _animation else _icon.sizes[0].file_id
                else:
                    _first_file_id = None

                for m in getattr(r, "messages", []):
                    if not isinstance(getattr(m, "action", None), raw.types.MessageActionChatEditPhoto):
                        continue

                    _c_animation = types.Animation._parse_chat_animation(self, m.action.photo)
                    _c_photo = types.Photo._parse(self, m.action.photo)

                    _current_file_id = (_c_animation and _c_animation.file_id) or (_c_photo and _c_photo.sizes[0].file_id)

                    if (_c_animation or _c_photo) and _first_file_id != _current_file_id:
                        chat_icons.append(_c_animation or _c_photo)

            current = 0

            for icon in chat_icons:
                await sleep(0)

                if not icon:
                    continue

                yield icon

                current += 1

                if current >= limit:
                    return
        else:
            current = 0
            offset = 0

            while True:
                r = await self.invoke(
                    raw.functions.photos.GetUserPhotos(
                        user_id=peer_id, offset=offset, max_id=0, limit=limit
                    )
                )

                photos = []
                for photo in r.photos:
                    photos.append(
                        types.Animation._parse_chat_animation(self, photo)
                        or types.Photo._parse(self, photo)
                    )

                if not photos:
                    return

                offset += len(photos)

                for photo in photos:
                    await sleep(0)

                    if not photo:
                        continue

                    yield photo

                    current += 1

                    if current >= total:
                        return

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

import pyrogram
from pyrogram import raw, utils
from pyrogram.file_id import FileType


class AddProfileAudio:
    async def add_profile_audio(
        self: "pyrogram.Client",
        audio: str,
    ):
        """Adds an audio file to the beginning of the profile audio files of the current user.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            audio (``str``):
                Audio file to add.
                Pass a file_id as string to add an audio file that exists on the Telegram servers.
                The file must have been uploaded to the server using :meth:`~pyrogram.Client.send_audio`.

        Returns:
            ``bool``: On success, True is returned.
        
        Raises:
            :doc:`RPCError <../../start/errors>`: In case of a Telegram RPC error.

        Example:
            .. code-block:: python

                # Adds an audio file to a profile
                await app.add_profile_audio(file_id)

        """
        return await self.invoke(
            raw.functions.account.SaveMusic(
                id=(utils.get_input_media_from_file_id(audio, FileType.AUDIO)).id
            )
        )

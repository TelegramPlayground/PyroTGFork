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

from typing import Union, List, Iterable

import pyrogram
from pyrogram import types, raw


class GetFolders:
    async def get_folders(
        self: "pyrogram.Client",
        folder_ids: Union[int, Iterable[int]] = None,
    ) -> Union["types.Folder", List["types.Folder"]]:
        """Get one or more folders by using folder identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            folder_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single folder identifier or an iterable of folder ids (as integers) to get the content of the
                folders themselves.
                By default all folders are returned.

        Returns:
            :obj:`~pyrogram.types.Folder` | List of :obj:`~pyrogram.types.Folder`: In case *folder_ids* was not
            a list, a single folder is returned, otherwise a list of folders is returned.

        Example:
            .. code-block:: python

                # Get one folder
                await app.get_folders(12345)

                # Get more than one folders (list of folders)
                await app.get_folders([12345, 12346])

                # Get all folders
                await app.get_folders()
        """
        is_iterable = hasattr(folder_ids, "__iter__")
        ids = list(folder_ids) if is_iterable else [folder_ids]

        raw_folders = await self.invoke(raw.functions.messages.GetDialogFilters())
        dialog_peers = []

        for folder in raw_folders:
            if isinstance(folder, (raw.types.DialogFilter, raw.types.DialogFilterChatlist)):
                peers = folder.pinned_peers + folder.include_peers + getattr(folder, "exclude_peers", [])
                input_peers = [raw.types.InputDialogPeer(peer=peer) for peer in peers] + [raw.types.InputDialogPeerFolder(folder_id=folder.id)]

                dialog_peers.extend(input_peers)

        r = await self.invoke(raw.functions.messages.GetPeerDialogs(peers=dialog_peers))

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        folders = types.List([])

        for folder in raw_folders:
            if isinstance(folder, (raw.types.DialogFilter, raw.types.DialogFilterChatlist)):
                folders.append(types.Folder._parse(self, folder, users, chats))

        if not folders:
            return None

        if folder_ids:
            folders = types.List([folder for folder in folders if folder.id in ids])
            if is_iterable:
                return folders or None
            else:
                return folders[0] if folders else None

        return folders

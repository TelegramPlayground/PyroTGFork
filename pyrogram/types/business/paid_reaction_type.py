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

from ..object import Object

import pyrogram
from pyrogram import raw, types


class PaidReactionType(Object):
    """This object describes the type of paid message reaction.
    
    It can be one of:

    - :obj:`~pyrogram.types.PaidReactionTypeRegular`
    - :obj:`~pyrogram.types.PaidReactionTypeAnonymous`
    - :obj:`~pyrogram.types.PaidReactionTypeChat`

    """

    def __init__(self):
        super().__init__()
    
    async def write(
        self,
        client: "pyrogram.Client",
    ):
        if isinstance(self, PaidReactionTypeChat):
            return self._raw(
                peer=await client.resolve_peer(self.chat_id)
            )
        else:
            return self._raw()



class PaidReactionTypeRegular(PaidReactionType):
    """A paid reaction on behalf of the current user.

    """
    def __init__(self):
        super().__init__()

        self._raw = raw.types.PaidReactionPrivacyDefault


class PaidReactionTypeAnonymous(PaidReactionType):
    """An anonymous paid reaction.
    
    """
    def __init__(self):
        super().__init__()

        self._raw = raw.types.PaidReactionPrivacyAnonymous


class PaidReactionTypeChat(PaidReactionType):
    """A paid reaction on behalf of an owned chat.

    It is intended to be used with :obj:`~pyrogram.Client.`.

    Parameters:
        chat_id (``int``):
            Unique identifier (int) or username (str) of the target chat.
    
    """

    def __init__(self, chat_id: int):
        super().__init__()

        self.chat_id = chat_id
        self._raw = raw.types.PaidReactionPrivacyPeer

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

import pyrogram
from pyrogram import raw
from pyrogram import types

log = logging.getLogger(__name__)


class GetMessageEffects:
    async def get_message_effects(
        self: "pyrogram.Client"
    ) -> list["types.MessageEffect"]:
        """Returns information about all available message effects.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            List of :obj:`~pyrogram.types.MessageEffect`: A list of message effects is returned.

        Example:
            .. code-block:: python

                # Get all message effects
                await app.get_message_effects()

        """
        r = await self.invoke(
            raw.functions.messages.GetAvailableEffects(
                hash=0
            )
        )
        documents = {d.id: d for d in r.documents}
        outlst = []
        for effect in r.effects:
            effect_animation_document = documents.get(effect.effect_sticker_id, None)
            static_icon_document = documents.get(effect.static_icon_id, None) if getattr(effect, "static_icon_id", None) else None
            select_animation_document = documents.get(effect.effect_animation_id, None) if getattr(effect, "effect_animation_id", None) else None
            outlst.append(
                await types.MessageEffect._parse(
                    self,
                    effect,
                    effect_animation_document,
                    static_icon_document,
                    select_animation_document
                )
            )
        return types.List(outlst)

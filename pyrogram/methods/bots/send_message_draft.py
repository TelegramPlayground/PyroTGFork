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

from typing import Union, Optional

import pyrogram
from pyrogram import raw, utils, enums, types


class SendMessageDraft:
    async def send_message_draft(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        draft_id: int,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: list["types.MessageEntity"] = None,
        message_thread_id: int = None,
    ) -> bool:
        """Sends a draft for a being generated text message.

        Use this method to stream a partial message to a user while the message is being generated. This method shows a live text preview as it is being composed. To achieve a smooth
        AI-streaming effect, call this method repeatedly with progressively longer text, passing a consistent *draft_id* for all frames of the same stream.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier of the target chat.

            draft_id (``int``):
                Unique identifier of the message draft; must be non-zero. Changes of drafts with the same identifier are animated.

            text (``str``):
                Text of the message to be sent, 1-4096 characters after entities parsing.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                Mode for parsing entities in the message text. By default, texts are parsed using Markdown and HTML styles.

            entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in the text, which can be specified instead of **parse_mode**.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread.

        Returns:
            ``bool``: On success, True is returned.

        Raises:
            ValueError: If the text is empty or the chat type is not a private chat.
            :obj:`~pyrogram.errors.RPCError`: In case of a Telegram RPC error.

        """

        if not chat_id:
            raise ValueError("chat_id is required")

        if not text:
            raise ValueError("text cannot be empty")

        peer = await self.resolve_peer(chat_id)

        if not isinstance(peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
            raise ValueError("Streaming text is only supported in private chats (user-to-bot)")

        message, entities = (
            await utils.parse_text_entities(self, text, parse_mode, entities)
        ).values()

        if not message:
            raise ValueError("text cannot be empty after parsing")

        return await self.invoke(
            raw.functions.messages.SetTyping(
                peer=peer,
                action=raw.types.SendMessageTextDraftAction(
                    random_id=draft_id,
                    text=raw.types.TextWithEntities(
                        text=message,
                        entities=entities or []
                    )
                ),
                top_msg_id=message_thread_id
            )
        )

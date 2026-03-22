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


class SendStreamText:
    async def send_stream_text(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: list["types.MessageEntity"] = None,
        random_id: int = None,
        message_thread_id: int = None,
        reply_parameters: "types.ReplyParameters" = None,
        business_connection_id: str = None
    ) -> bool:
        """Send a streaming text action to a chat.

        This method shows a live text preview as it is being composed. To achieve a smooth
        AI-streaming effect, call this method repeatedly with progressively longer text,
        passing a consistent *random_id* for all frames of the same stream.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier of the target chat.

            text (``str``):
                The text content to stream.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using Markdown and HTML styles.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the text.

            random_id (``int``, *optional*):
                Long random identifier. Use the same identifier for multiple calls to update
                the same streaming draft. If not provided, a new one is generated.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread or forum topic.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Reply parameters, primarily used to determine the thread/topic ID.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the action will be sent.

        Returns:
            ``bool``: On success, True is returned.

        Raises:
            ValueError: If the text is empty or the chat type is not a private chat.
        """
        if not chat_id:
            raise ValueError("chat_id is required")

        if not text:
            raise ValueError("text cannot be empty")

        peer = await self.resolve_peer(chat_id)

        if not isinstance(peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
            raise ValueError("Streaming text is only supported in private chats (user-to-user or user-to-bot)")

        message, entities = (
            await utils.parse_text_entities(self, text, parse_mode, entities)
        ).values()

        if not message:
            raise ValueError("text cannot be empty after parsing")

        top_msg_id = message_thread_id
        if reply_parameters:
            reply_to = await utils._get_reply_message_parameters(
                self,
                message_thread_id,
                reply_parameters
            )
            top_msg_id = getattr(reply_to, "top_msg_id", message_thread_id)

        rpc = raw.functions.messages.SetTyping(
            peer=peer,
            action=raw.types.SendMessageTextDraftAction(
                random_id=random_id or self.rnd_id(),
                text=raw.types.TextWithEntities(
                    text=message,
                    entities=entities or []
                )
            ),
            top_msg_id=top_msg_id
        )

        if business_connection_id:
            return await self.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    query=rpc,
                    connection_id=business_connection_id
                )
            )
        else:
            return await self.invoke(rpc)

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
from datetime import datetime
from typing import Union, List, Optional

import pyrogram
from pyrogram import raw, utils, enums, types, errors
from .inline_session import get_session

log = logging.getLogger(__name__)


class SendMessage:
    async def send_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str] = None,
        text: str = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        link_preview_options: "types.LinkPreviewOptions" = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        message_thread_id: int = None,
        business_connection_id: str = None,
        reply_parameters: "types.ReplyParameters" = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        schedule_date: datetime = None,
        disable_web_page_preview: bool = None,
        reply_to_message_id: int = None
    ) -> "types.Message":
        """Send text messages.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            text (``str``):
                Text of the message to be sent.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            link_preview_options (:obj:`~pyrogram.types.LinkPreviewOptions`, *optional*):
                Link preview generation options for the message

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            message_thread_id (``int``, *optional*):
                If the message is in a thread, ID of the original message.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent text message is returned.

        Example:
            .. code-block:: python

                # Simple example
                await app.send_message(chat_id="me", text="Message sent with **Pyrogram**!")

                # Disable web page previews
                await app.send_message(
                    chat_id="me", text="https://docs.pyrogram.org",
                    link_preview_options=types.LinkPreviewOptions(
                        is_disabled=True
                    )
                )

                # Reply to a message using its id
                await app.send_message(chat_id="me", text="this is a reply", reply_parameters=types.ReplyParameters(message_id=123))

            .. code-block:: python

                # For bots only, send messages with keyboards attached

                from pyrogram.types import (
                    ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)

                # Send a normal keyboard
                await app.send_message(
                    chat_id=chat_id, text="Look at that button!",
                    reply_markup=ReplyKeyboardMarkup([["Nice!"]]))

                # Send an inline keyboard
                await app.send_message(
                    chat_id=chat_id, text="These are inline buttons",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("Data", callback_data="callback_data")],
                            [InlineKeyboardButton("Docs", url="https://docs.pyrogram.org")]
                        ]))
        """
        if disable_web_page_preview and link_preview_options:
            raise ValueError(
                "Parameters `disable_web_page_preview` and `link_preview_options` are mutually "
                "exclusive."
            )

        if disable_web_page_preview is not None:
            log.warning(
                "This property is deprecated. "
                "Please use link_preview_options instead"
            )
            link_preview_options = types.LinkPreviewOptions(is_disabled=disable_web_page_preview)

        if reply_to_message_id and reply_parameters:
            raise ValueError(
                "Parameters `reply_to_message_id` and `reply_parameters` are mutually "
                "exclusive."
            )
        
        if reply_to_message_id is not None:
            log.warning(
                "This property is deprecated. "
                "Please use reply_parameters instead"
            )
            reply_parameters = types.ReplyParameters(message_id=reply_to_message_id)

        reply_to = await utils._get_reply_message_parameters(
            self,
            message_thread_id,
            reply_parameters
        )
        message, entities = (await utils.parse_text_entities(self, text, parse_mode, entities)).values()

        session = None
        business_connection = None
        if business_connection_id:
            business_connection = self.business_user_connection_cache[business_connection_id]
            if not business_connection:
                business_connection = await self.get_business_connection(business_connection_id)
            session = await get_session(
                self,
                business_connection._raw.connection.dc_id
            )

        if (
            link_preview_options and
            link_preview_options.url
        ):
            try:
                rpc = raw.functions.messages.SendMedia(
                    peer=await self.resolve_peer(chat_id),
                    silent=disable_notification or None,
                    reply_to=reply_to,
                    random_id=self.rnd_id(),
                    schedule_date=utils.datetime_to_timestamp(schedule_date),
                    reply_markup=await reply_markup.write(self) if reply_markup else None,
                    message=message,
                    media=raw.types.InputMediaWebPage(
                        url=link_preview_options.url,
                        force_large_media=link_preview_options.prefer_large_media,
                        force_small_media=link_preview_options.prefer_small_media
                    ),
                    invert_media=link_preview_options.show_above_text,
                    entities=entities,
                    noforwards=protect_content
                )
                if business_connection_id:
                    r = await session.invoke(
                        raw.functions.InvokeWithBusinessConnection(
                            query=rpc,
                            connection_id=business_connection_id
                        )
                    )
                    # await session.stop()
                else:
                    r = await self.invoke(rpc)
            except errors.WebpageNotFound:
                if not message:
                    raise ValueError(
                        "Bad Request: text is empty"
                    ) from None

                xe = [
                    raw.types.MessageEntityTextUrl(
                        offset=0,
                        length=1,
                        url=link_preview_options.url
                    )
                ]
                if entities:
                    entities = xe + entities
                else:
                    entities = xe
                rpc = raw.functions.messages.SendMessage(
                    peer=await self.resolve_peer(chat_id),
                    no_webpage=link_preview_options.is_disabled if link_preview_options else None,
                    silent=disable_notification or None,
                    # TODO
                    # TODO
                    noforwards=protect_content,
                    # TODO
                    invert_media=link_preview_options.show_above_text if link_preview_options else None,
                    reply_to=reply_to,
                    schedule_date=utils.datetime_to_timestamp(schedule_date),
                    reply_markup=await reply_markup.write(self) if reply_markup else None,
                    # TODO
                    random_id=self.rnd_id(),
                    message=message,
                    entities=entities,
                    # TODO
                )
                if business_connection_id:
                    r = await session.invoke(
                        raw.functions.InvokeWithBusinessConnection(
                            query=rpc,
                            connection_id=business_connection_id
                        )
                    )
                    # await session.stop()
                else:
                    r = await self.invoke(rpc)

        elif message:
            rpc = raw.functions.messages.SendMessage(
                peer=await self.resolve_peer(chat_id),
                no_webpage=link_preview_options.is_disabled if link_preview_options else None,
                silent=disable_notification or None,
                # TODO
                # TODO
                noforwards=protect_content,
                # TODO
                invert_media=link_preview_options.show_above_text if link_preview_options else None,
                reply_to=reply_to,
                schedule_date=utils.datetime_to_timestamp(schedule_date),
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                # TODO
                random_id=self.rnd_id(),
                message=message,
                entities=entities,
                # TODO
            )
            if business_connection_id:
                r = await session.invoke(
                    raw.functions.InvokeWithBusinessConnection(
                        query=rpc,
                        connection_id=business_connection_id
                    )
                )
                # await session.stop()
            else:
                r = await self.invoke(rpc)

        else:
            raise ValueError("Invalid Arguments passed")

        if isinstance(r, raw.types.UpdateShortSentMessage):
            peer = await self.resolve_peer(chat_id)

            peer_id = (
                peer.user_id
                if isinstance(peer, raw.types.InputPeerUser)
                else -peer.chat_id
            )

            return types.Message(
                id=r.id,
                chat=types.Chat(
                    id=peer_id,
                    type=enums.ChatType.PRIVATE,
                    client=self
                ),
                text=message,
                date=utils.timestamp_to_datetime(r.date),
                outgoing=r.out,
                reply_markup=reply_markup,
                entities=[
                    types.MessageEntity._parse(None, entity, {})
                    for entity in entities
                ] if entities else None,
                client=self
            )

        for i in r.updates:
            if isinstance(
                i,
                (
                    raw.types.UpdateNewMessage,
                    raw.types.UpdateNewChannelMessage,
                    raw.types.UpdateNewScheduledMessage
                )
            ):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage),
                    replies=0
                )
            elif isinstance(
                i,
                (
                    raw.types.UpdateBotNewBusinessMessage
                )
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    business_connection_id=getattr(i, "connection_id", business_connection_id),
                    raw_reply_to_message=i.reply_to_message
                )

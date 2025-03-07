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
from typing import Union, Optional

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
        entities: list["types.MessageEntity"] = None,
        link_preview_options: "types.LinkPreviewOptions" = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        allow_paid_broadcast: bool = None,
        paid_message_star_count: int = None,
        message_thread_id: int = None,
        business_connection_id: str = None,
        send_as: Union[int, str] = None,
        message_effect_id: int = None,
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
                Pass True if the content of the message must be protected from forwarding and saving; for bots only.
            
            allow_paid_broadcast (``bool``, *optional*):
                Pass True to allow the message to ignore regular broadcast limits for a small fee; for bots only

            paid_message_star_count (``int``, *optional*):
                The number of Telegram Stars the user agreed to pay to send the messages.

            message_thread_id (``int``, *optional*):
                If the message is in a thread, ID of the original message.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            send_as (``int`` | ``str``):
                Unique identifier (int) or username (str) of the chat or channel to send the message as.
                You can use this to send the message on behalf of a chat or channel where you have appropriate permissions.
                Use the :meth:`~pyrogram.Client.get_send_as_chats` to return the list of message sender identifiers, which can be used to send messages in the chat, 
                This setting applies to the current message and will remain effective for future messages unless explicitly changed.
                To set this behavior permanently for all messages, use :meth:`~pyrogram.Client.set_send_as_chat`.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

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
                    chat_id="me", text="https://github.com/TelegramPlayground/pyrogram",
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
                            [
                                InlineKeyboardButton("Data", callback_data="callback_data")
                            ],
                            [
                                InlineKeyboardButton("Docs", url="https://telegramplayground.github.io/pyrogram/")
                            ]
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

        link_preview_options = link_preview_options or self.link_preview_options

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

        peer = await self.resolve_peer(chat_id)

        if (
            link_preview_options and
            link_preview_options.url
        ):
            try:
                rpc = raw.functions.messages.SendMedia(
                    peer=peer,
                    silent=disable_notification or None,
                    reply_to=reply_to,
                    random_id=self.rnd_id(),
                    send_as=await self.resolve_peer(send_as) if send_as else None,
                    schedule_date=utils.datetime_to_timestamp(schedule_date),
                    reply_markup=await reply_markup.write(self) if reply_markup else None,
                    message=message,
                    media=raw.types.InputMediaWebPage(
                        url=link_preview_options.url,
                        force_large_media=link_preview_options.prefer_large_media,
                        force_small_media=link_preview_options.prefer_small_media,
                        optional=True
                    ),
                    invert_media=link_preview_options.show_above_text,
                    entities=entities,
                    noforwards=protect_content,
                    allow_paid_floodskip=allow_paid_broadcast,
                    allow_paid_stars=paid_message_star_count,
                    effect=message_effect_id
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
            except errors.MessageEmpty:
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
                    peer=peer,
                    no_webpage=link_preview_options.is_disabled if link_preview_options else None,
                    silent=disable_notification or None,
                    # TODO
                    # TODO
                    noforwards=protect_content,
                    allow_paid_floodskip=allow_paid_broadcast,
                    allow_paid_stars=paid_message_star_count,
                    # TODO
                    invert_media=link_preview_options.show_above_text if link_preview_options else None,
                    reply_to=reply_to,
                    schedule_date=utils.datetime_to_timestamp(schedule_date),
                    reply_markup=await reply_markup.write(self) if reply_markup else None,
                    random_id=self.rnd_id(),
                    send_as=await self.resolve_peer(send_as) if send_as else None,
                    message=message,
                    entities=entities,
                    # TODO
                    effect=message_effect_id
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
                peer=peer,
                no_webpage=link_preview_options.is_disabled if link_preview_options else None,
                silent=disable_notification or None,
                # TODO
                # TODO
                noforwards=protect_content,
                allow_paid_floodskip=allow_paid_broadcast,
                allow_paid_stars=paid_message_star_count,
                # TODO
                invert_media=link_preview_options.show_above_text if link_preview_options else None,
                reply_to=reply_to,
                schedule_date=utils.datetime_to_timestamp(schedule_date),
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                random_id=self.rnd_id(),
                send_as=await self.resolve_peer(send_as) if send_as else None,
                message=message,
                entities=entities,
                # TODO
                effect=message_effect_id
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
            peer_id = (
                peer.user_id
                if isinstance(peer, raw.types.InputPeerUser)
                else -peer.chat_id
            )

            return types.Message(
                id=r.id,
                outgoing=r.out,
                date=utils.timestamp_to_datetime(r.date),
                entities=[
                    types.MessageEntity._parse(None, entity, {})
                    for entity in r.entities
                ] if r.entities else None,
                message_auto_delete_timer_changed=types.MessageAutoDeleteTimerChanged(
                    message_auto_delete_time=getattr(r, "ttl_period", None)
                ),
                chat=types.Chat(
                    id=peer_id,
                    type=enums.ChatType.PRIVATE,
                    client=self
                ),
                text=message,
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
                    replies=self.fetch_replies
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
                    raw_reply_to_message=i.reply_to_message,
                    replies=0
                )

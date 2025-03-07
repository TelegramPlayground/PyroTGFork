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
from typing import Iterable, Optional, Union

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.messages_and_media.message import Str

log = logging.getLogger(__name__)


class GetMessages:
    async def get_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str] = None,
        message_ids: Union[int, Iterable[int]] = None,
        replies: int = 1,
        is_scheduled: bool = False,
        link: str = None,
    ) -> Union[
        "types.Message",
        list["types.Message"],
        "types.DraftMessage"
    ]:
        """Get one or more messages from a chat by using message identifiers. You can retrieve up to 200 messages at once.

        .. include:: /_includes/usable-by/users-bots.rst

        You must use exactly one of ``message_ids`` OR (``chat_id``, ``message_ids``) OR ``link``.

        Parameters:
            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single message identifier or an iterable of message ids (as integers) to get the content of the
                message themselves.

            replies (``int``, *optional*):
                The number of subsequent replies to get for each message.
                Pass 0 for no reply at all or -1 for unlimited replies.
                Defaults to 1.
                Is ignored if ``is_scheduled`` parameter is set.

            is_scheduled (``bool``, *optional*):
                Whether to get scheduled messages. Defaults to False.
                Only supported if both ``chat_id`` and ``message_ids`` are passed. Other parameters are ignored when this is set.

            link (``str``):
                A link of the message, usually can be copied using ``Copy Link`` functionality OR obtained using :obj:`~pyrogram.raw.types.Message.link` OR  :obj:`~pyrogram.raw.functions.channels.ExportMessageLink`

        Returns:
            :obj:`~pyrogram.types.Message` | List of :obj:`~pyrogram.types.Message` | :obj:`~pyrogram.types.DraftMessage`: In case *message_ids* was not
            a list, a single message is returned, otherwise a list of messages is returned.

        Example:
            .. code-block:: python

                # Get one message
                await app.get_messages(chat_id=chat_id, message_ids=12345)

                # Get more than one message (list of messages)
                await app.get_messages(chat_id=chat_id, message_ids=[12345, 12346])

                # Get message by ignoring any replied-to message
                await app.get_messages(chat_id=chat_id, message_ids=message_id, replies=0)

                # Get message with all chained replied-to messages
                await app.get_messages(chat_id=chat_id, message_ids=message_id, replies=-1)

        Raises:
            ValueError: In case of invalid arguments.
        """

        if message_ids:
            is_iterable = utils.is_list_like(message_ids)
            ids = list(message_ids) if is_iterable else [message_ids]

            if replies < 0:
                replies = (1 << 31) - 1

            peer = await self.resolve_peer(chat_id) if chat_id else None

            if chat_id and is_scheduled:
                rpc = raw.functions.messages.GetScheduledMessages(
                    peer=peer,
                    id=ids
                )
            else:
                ids = [raw.types.InputMessageID(id=i) for i in ids]
                if chat_id and isinstance(peer, raw.types.InputPeerChannel):
                    rpc = raw.functions.channels.GetMessages(channel=peer, id=ids)
                else:
                    rpc = raw.functions.messages.GetMessages(id=ids)

            r = await self.invoke(rpc, sleep_threshold=-1)

            messages = await utils.parse_messages(
                self,
                r,
                is_scheduled=is_scheduled,
                replies=replies
            )

            return messages if is_iterable else messages[0] if messages else None

        if link:
            linkps = link.split("/")
            raw_chat_id, message_thread_id, message_id = None, None, None
            if (
                len(linkps) == 7 and
                linkps[3] == "c"
            ):
                # https://t.me/c/1192302355/322/487
                raw_chat_id = utils.get_channel_id(
                    int(linkps[4])
                )
                message_thread_id = int(linkps[5])
                message_id = int(linkps[6])
            elif len(linkps) == 6:
                if linkps[3] == "c":
                    # https://t.me/c/1387666944/609282
                    raw_chat_id = utils.get_channel_id(
                        int(linkps[4])
                    )
                    message_id = int(linkps[5])
                else:
                    # https://t.me/TheForum/322/487
                    raw_chat_id = linkps[3]
                    message_thread_id = int(linkps[4])
                    message_id = int(linkps[5])

            elif (
                not (self.me and self.me.is_bot) and
                len(linkps) == 5 and
                linkps[3] == "m"
            ):
                r = await self.invoke(
                    raw.functions.account.ResolveBusinessChatLink(
                        slug=linkps[4]
                    )
                )
                users = {i.id: i for i in r.users}
                chats = {i.id: i for i in r.chats}
                entities = [
                    types.MessageEntity._parse(
                        self, entity, users
                    )
                    for entity in getattr(r, "entities", [])
                ]
                entities = types.List(
                    filter(lambda x: x is not None, entities)
                )
                chat = None
                cat_id = utils.get_raw_peer_id(r.peer)
                if isinstance(r.peer, raw.types.PeerUser):
                    chat = types.Chat._parse_user_chat(self, users[cat_id])
                # elif isinstance(r.peer, raw.types.PeerChat):
                #     chat = types.Chat._parse_chat_chat(self, chats[cat_id])
                # else:
                #     chat = types.Chat._parse_channel_chat(
                #         self, chats[cat_id]
                #     )
                return types.DraftMessage(
                    text=Str(r.message).init(entities) or None,
                    entities=entities or None,
                    chat=chat,
                    _raw=r,
                )

            elif len(linkps) == 5:
                # https://t.me/pyrogramchat/609282
                raw_chat_id = linkps[3]
                if raw_chat_id == "m":
                    raise ValueError(
                        "Invalid ClientType used to parse this message link"
                    )
                message_id = int(linkps[4])

            return await self.get_messages(
                chat_id=raw_chat_id,
                message_ids=message_id
            )

        raise ValueError("No valid argument supplied. https://telegramplayground.github.io/pyrogram/api/methods/get_messages")


    async def get_chat_pinned_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        replies: int = 1
    ) -> Optional["types.Message"]:
        """Returns information about a newest pinned message in the chat.
        Use :meth:`~pyrogram.Client.search_messages` to return all the pinned messages.

        .. include:: /_includes/usable-by/users-bots.rst
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            replies (``int``, *optional*):
                The number of subsequent replies to get for each message.
                Pass 0 for no reply at all or -1 for unlimited replies.
                Defaults to 1.

        """

        peer = await self.resolve_peer(chat_id)
        if not isinstance(peer, raw.types.InputPeerChannel):
            raise ValueError("chat_id must belong to a supergroup or channel.")
        rpc = raw.functions.channels.GetMessages(channel=peer, id=[raw.types.InputMessagePinned()])
        r = await self.invoke(rpc, sleep_threshold=-1)
        if replies < 0:
            replies = (1 << 31) - 1
        messages = await utils.parse_messages(
            self,
            r,
            is_scheduled=False,
            replies=replies
        )
        return messages[0] if messages else None


    async def get_callback_query_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        callback_query_id: int,
        replies: int = 1
    ) -> Optional["types.Message"]:
        """Returns information about a message with the callback button that originated a callback query.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Message identifier.

            callback_query_id (``int``):
                Identifier of the callback query.

            replies (``int``, *optional*):
                The number of subsequent replies to get for each message.
                Pass 0 for no reply at all or -1 for unlimited replies.
                Defaults to 1.

        """

        peer = await self.resolve_peer(chat_id)
        ids = [raw.types.InputMessageCallbackQuery(id=message_id, query_id=callback_query_id)]
        if isinstance(peer, raw.types.InputPeerChannel):
            rpc = raw.functions.channels.GetMessages(channel=peer, id=ids)
        else:
            rpc = raw.functions.messages.GetMessages(id=ids)
        r = await self.invoke(rpc, sleep_threshold=-1)
        if replies < 0:
            replies = (1 << 31) - 1
        messages = await utils.parse_messages(
            self,
            r,
            is_scheduled=False,
            replies=replies
        )
        return messages[0] if messages else None


    async def get_replied_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]],
        replies: int = 1
    ) -> Optional["types.Message"]:
        """Returns information about a non-bundled message that is replied by a given message.

        .. include:: /_includes/usable-by/users-bots.rst

        Also, returns the pinned message, the game message, the invoice message,
        the message with a previously set same background, the giveaway message, and the topic creation message for messages of the types
        messagePinMessage, messageGameScore, messagePaymentSuccessful, messageChatSetBackground, messageGiveawayCompleted and topic messages
        without non-bundled replied message respectively.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_ids (``int`` | Iterable of ``int``):
                Pass a single message identifier or an iterable of message ids (as integers) to get the content of
                the previous message you replied to using this message.

            replies (``int``, *optional*):
                The number of subsequent replies to get for each message.
                Pass 0 for no reply at all or -1 for unlimited replies.
                Defaults to 1.

        Example:
            .. code-block:: python

                # Get the replied-to message of a message
                await app.get_replied_message(chat_id=chat_id, message_ids=message_id)

        """

        peer = await self.resolve_peer(chat_id)
        is_iterable = utils.is_list_like(message_ids)
        ids = list(message_ids) if is_iterable else [message_ids]
        ids = [raw.types.InputMessageReplyTo(id=i) for i in ids]
        if isinstance(peer, raw.types.InputPeerChannel):
            rpc = raw.functions.channels.GetMessages(channel=peer, id=ids)
        else:
            rpc = raw.functions.messages.GetMessages(id=ids)
        r = await self.invoke(rpc, sleep_threshold=-1)
        if replies < 0:
            replies = (1 << 31) - 1
        messages = await utils.parse_messages(
            self,
            r,
            is_scheduled=False,
            replies=replies
        )
        return messages if is_iterable else messages[0] if messages else None

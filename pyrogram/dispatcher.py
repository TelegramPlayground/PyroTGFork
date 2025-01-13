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

import asyncio
import inspect
import logging
from collections import OrderedDict

import pyrogram
from pyrogram import errors, utils, raw
from pyrogram.handlers import (
    MessageHandler, EditedMessageHandler,
    BusinessBotConnectionHandler,
    MessageReactionUpdatedHandler,
    MessageReactionCountUpdatedHandler,
    InlineQueryHandler,
    ChosenInlineResultHandler,
    CallbackQueryHandler,
    ShippingQueryHandler,
    PreCheckoutQueryHandler,
    PurchasedPaidMediaHandler,
    PollHandler,


    ChatMemberUpdatedHandler,
    ChatJoinRequestHandler,


    DeletedMessagesHandler,
    UserStatusHandler,
    StoryHandler,
    RawUpdateHandler
)
from pyrogram.raw.types import (
    UpdateNewMessage, UpdateNewChannelMessage, UpdateNewScheduledMessage,
    UpdateEditMessage, UpdateEditChannelMessage,
    UpdateDeleteMessages, UpdateDeleteChannelMessages,
    UpdateBotCallbackQuery, UpdateInlineBotCallbackQuery,
    UpdateUserStatus, UpdateBotInlineQuery,
    UpdateMessagePoll, UpdateMessagePollVote,
    UpdateBotInlineSend, UpdateChatParticipant, UpdateChannelParticipant, UpdateBotStopped,
    UpdateBotChatInviteRequester,
    UpdateBotMessageReaction,
    UpdateBotMessageReactions,
    UpdateBotNewBusinessMessage,
    UpdateBotEditBusinessMessage,
    UpdateBotDeleteBusinessMessage,
    UpdateBotPrecheckoutQuery,
    UpdateBotShippingQuery,
    UpdateStory,
    UpdateBusinessBotCallbackQuery,
    UpdateBotBusinessConnect,
    UpdateBotPurchasedPaidMedia,
)

log = logging.getLogger(__name__)


class Dispatcher:
    NEW_MESSAGE_UPDATES = (UpdateNewMessage, UpdateNewChannelMessage, UpdateNewScheduledMessage, UpdateBotNewBusinessMessage)
    EDIT_MESSAGE_UPDATES = (UpdateEditMessage, UpdateEditChannelMessage, UpdateBotEditBusinessMessage)
    DELETE_MESSAGES_UPDATES = (UpdateDeleteMessages, UpdateDeleteChannelMessages, UpdateBotDeleteBusinessMessage)
    CALLBACK_QUERY_UPDATES = (UpdateBotCallbackQuery, UpdateInlineBotCallbackQuery, UpdateBusinessBotCallbackQuery)
    CHAT_MEMBER_UPDATES = (UpdateChatParticipant, UpdateChannelParticipant, UpdateBotStopped,)
    USER_STATUS_UPDATES = (UpdateUserStatus,)
    BOT_INLINE_QUERY_UPDATES = (UpdateBotInlineQuery,)
    POLL_UPDATES = (UpdateMessagePoll,)
    POLL_ANSWER_UPDATES = (UpdateMessagePollVote,)
    CHOSEN_INLINE_RESULT_UPDATES = (UpdateBotInlineSend,)
    CHAT_JOIN_REQUEST_UPDATES = (UpdateBotChatInviteRequester,)
    MESSAGE_BOT_NA_REACTION_UPDATES = (UpdateBotMessageReaction,)
    MESSAGE_BOT_A_REACTION_UPDATES = (UpdateBotMessageReactions,)
    PRE_CHECKOUT_QUERY_UPDATES = (UpdateBotPrecheckoutQuery,)
    SHIPPING_QUERY_UPDATES = (UpdateBotShippingQuery,)
    NEW_STORY_UPDATES = (UpdateStory,)
    BOT_BUSINESS_CONNECT_UPDATES = (UpdateBotBusinessConnect,)
    PURCHASED_PAID_MEDIA_UPDATES = (UpdateBotPurchasedPaidMedia,)

    def __init__(self, client: "pyrogram.Client"):
        self.client = client
        self.loop = asyncio.get_event_loop()

        self.handler_worker_tasks = []
        self.locks_list = []

        self.updates_queue = asyncio.Queue()
        self.groups = OrderedDict()

        async def message_parser(update, users, chats):
            business_connection_id = getattr(update, "connection_id", None)
            return (
                await pyrogram.types.Message._parse(
                    self.client,
                    update.message,
                    users,
                    chats,
                    is_scheduled=isinstance(update, UpdateNewScheduledMessage),
                    business_connection_id=business_connection_id,
                    raw_reply_to_message=getattr(update, "reply_to_message", None),
                    replies=0 if business_connection_id else self.client.fetch_replies
                ),
                MessageHandler
            )

        async def edited_message_parser(update, users, chats):
            # Edited messages are parsed the same way as new messages, but the handler is different
            parsed, _ = await message_parser(update, users, chats)

            return (
                parsed,
                EditedMessageHandler
            )

        async def deleted_messages_parser(update, users, chats):
            return (
                await utils.parse_deleted_messages(self.client, update, users, chats),
                DeletedMessagesHandler
            )

        async def callback_query_parser(update, users, chats):
            return (
                await pyrogram.types.CallbackQuery._parse(self.client, update, users, chats),
                CallbackQueryHandler
            )

        async def user_status_parser(update, users, chats):
            return (
                pyrogram.types.User._parse_user_status(self.client, update),
                UserStatusHandler
            )

        async def inline_query_parser(update, users, chats):
            return (
                pyrogram.types.InlineQuery._parse(self.client, update, users),
                InlineQueryHandler
            )

        async def poll_parser(update, users, chats):
            return (
                pyrogram.types.Poll._parse_update(
                    self.client, update, users, chats
                ),
                PollHandler
            )
        
        async def poll_answer_parser(update, users, chats):
            return (
                pyrogram.types.PollAnswer._parse_update(
                    self.client, update, users, chats
                ),
                PollHandler
            )

        async def chosen_inline_result_parser(update, users, chats):
            return (
                pyrogram.types.ChosenInlineResult._parse(self.client, update, users),
                ChosenInlineResultHandler
            )

        async def chat_member_updated_parser(update, users, chats):
            return (
                pyrogram.types.ChatMemberUpdated._parse(self.client, update, users, chats),
                ChatMemberUpdatedHandler
            )

        async def chat_join_request_parser(update, users, chats):
            return (
                pyrogram.types.ChatJoinRequest._parse(self.client, update, users, chats),
                ChatJoinRequestHandler
            )

        
        async def message_bot_na_reaction_parser(update, users, chats):
            return (
                pyrogram.types.MessageReactionUpdated._parse(self.client, update, users, chats),
                MessageReactionUpdatedHandler
            )

        async def message_bot_a_reaction_parser(update, users, chats):
            return (
                pyrogram.types.MessageReactionCountUpdated._parse(self.client, update, users, chats),
                MessageReactionCountUpdatedHandler
            )

        async def shipping_query_parser(update, users, chats):
            return (
                await pyrogram.types.ShippingQuery._parse(self.client, update, users),
                ShippingQueryHandler
            )

        async def pre_checkout_query_parser(update, users, chats):
            return (
                await pyrogram.types.PreCheckoutQuery._parse(self.client, update, users),
                PreCheckoutQueryHandler
            )

        async def story_parser(update, users, chats):
            return (
                await pyrogram.types.Story._parse(
                    self.client,
                    users,
                    chats,
                    None, None,
                    update,
                    None, None
                ),
                StoryHandler
            )

        async def bot_business_connect_parser(update, users, chats):
            return (
                pyrogram.types.BusinessConnection._parse(self.client, update, users, chats),
                BusinessBotConnectionHandler
            )

        async def purchased_paid_media_parser(update, users, chats):
            return (
                pyrogram.types.PaidMediaPurchased._parse(self.client, update, users),
                PurchasedPaidMediaHandler
            )

        self.update_parsers = {
            Dispatcher.NEW_MESSAGE_UPDATES: message_parser,
            Dispatcher.EDIT_MESSAGE_UPDATES: edited_message_parser,
            Dispatcher.DELETE_MESSAGES_UPDATES: deleted_messages_parser,
            Dispatcher.CALLBACK_QUERY_UPDATES: callback_query_parser,
            Dispatcher.USER_STATUS_UPDATES: user_status_parser,
            Dispatcher.BOT_INLINE_QUERY_UPDATES: inline_query_parser,
            Dispatcher.POLL_UPDATES: poll_parser,
            Dispatcher.POLL_ANSWER_UPDATES: poll_answer_parser,
            Dispatcher.CHOSEN_INLINE_RESULT_UPDATES: chosen_inline_result_parser,
            Dispatcher.CHAT_MEMBER_UPDATES: chat_member_updated_parser,
            Dispatcher.CHAT_JOIN_REQUEST_UPDATES: chat_join_request_parser,
            Dispatcher.MESSAGE_BOT_NA_REACTION_UPDATES: message_bot_na_reaction_parser,
            Dispatcher.MESSAGE_BOT_A_REACTION_UPDATES: message_bot_a_reaction_parser,
            Dispatcher.SHIPPING_QUERY_UPDATES: shipping_query_parser,
            Dispatcher.PRE_CHECKOUT_QUERY_UPDATES: pre_checkout_query_parser,
            Dispatcher.NEW_STORY_UPDATES: story_parser,
            Dispatcher.BOT_BUSINESS_CONNECT_UPDATES: bot_business_connect_parser,
            Dispatcher.PURCHASED_PAID_MEDIA_UPDATES: purchased_paid_media_parser,
        }

        self.update_parsers = {key: value for key_tuple, value in self.update_parsers.items() for key in key_tuple}


    async def start(self):
        if not self.client.no_updates:
            for i in range(self.client.workers):
                self.locks_list.append(asyncio.Lock())

                self.handler_worker_tasks.append(
                    self.loop.create_task(self.handler_worker(self.locks_list[-1]))
                )

            log.info("Started %s HandlerTasks", self.client.workers)

            if not self.client.skip_updates:
                await self.client.recover_gaps()

    async def stop(self):
        if not self.client.no_updates:
            for i in range(self.client.workers):
                self.updates_queue.put_nowait(None)

            for i in self.handler_worker_tasks:
                await i

            self.handler_worker_tasks.clear()
            self.groups.clear()

            log.info("Stopped %s HandlerTasks", self.client.workers)

    def add_handler(self, handler, group: int):
        async def fn():
            for lock in self.locks_list:
                await lock.acquire()

            try:
                if group not in self.groups:
                    self.groups[group] = []
                    self.groups = OrderedDict(sorted(self.groups.items()))

                self.groups[group].append(handler)
            finally:
                for lock in self.locks_list:
                    lock.release()

        self.loop.create_task(fn())

    def remove_handler(self, handler, group: int):
        async def fn():
            for lock in self.locks_list:
                await lock.acquire()

            try:
                if group not in self.groups:
                    raise ValueError(f"Group {group} does not exist. Handler was not removed.")

                self.groups[group].remove(handler)
            finally:
                for lock in self.locks_list:
                    lock.release()

        self.loop.create_task(fn())

    async def handler_worker(self, lock):
        while True:
            packet = await self.updates_queue.get()

            if packet is None:
                break

            try:
                update, users, chats = packet
                parser = self.update_parsers.get(type(update), None)

                parsed_update, handler_type = (
                    await parser(update, users, chats)
                    if parser is not None
                    else (None, type(None))
                )

                async with lock:
                    for group in self.groups.values():
                        for handler in group:
                            args = None

                            if isinstance(handler, handler_type):
                                try:
                                    if await handler.check(self.client, parsed_update):
                                        args = (parsed_update,)
                                except Exception as e:
                                    log.exception(e)
                                    continue

                            elif isinstance(handler, RawUpdateHandler):
                                try:
                                    if await handler.check(self.client, update):
                                        args = (update, users, chats)
                                except Exception as e:
                                    log.exception(e)
                                    continue

                            if args is None:
                                continue

                            try:
                                if inspect.iscoroutinefunction(handler.callback):
                                    await handler.callback(self.client, *args)
                                else:
                                    await self.loop.run_in_executor(
                                        self.client.executor,
                                        handler.callback,
                                        self.client,
                                        *args
                                    )
                            except pyrogram.StopPropagation:
                                raise
                            except pyrogram.ContinuePropagation:
                                continue
                            except Exception as e:
                                log.exception(e)

                            break
            except pyrogram.StopPropagation:
                pass
            except Exception as e:
                log.exception(e)
            finally:
                self.updates_queue.task_done()

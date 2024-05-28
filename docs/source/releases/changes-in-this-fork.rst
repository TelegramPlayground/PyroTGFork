Changes in this Fork
=========

This page lists all the documented changes of this fork,
in reverse chronological order. You should read this when upgrading
to this fork to know where your code can break, and where
it can take advantage of new goodies!

`For a more detailed description, please check the commits. <https://github.com/TelegramPlayGround/pyrogram/commits/unknown_errors/>`_

If you found any issue or have any suggestions, feel free to make `an issue <https://github.com/TelegramPlayGround/pyrogram/issues>`_ on github.

+------------------------+
| Scheme layer used: 181 |
+------------------------+


- `View new and changed raw API methods <https://telegramplayground.github.io/TG-APIs/TL/diff/?from=178&to=181>`__.

+------------------------+
| Scheme layer used: 179 |
+------------------------+

- Add ``invoice`` to :obj:`~pyrogram.types.Message` and :obj:`~pyrogram.types.ExternalReplyInfo`.
- Add ``link_preview_options`` to :obj:`~pyrogram.Client`.
- Support for the updated Channel ID format. `#28 <https://github.com/TelegramPlayGround/pyrogram/pull/28>`_
- Improvements to :meth:`~pyrogram.Client.save_file` and :meth:`~pyrogram.Client.get_file` to handle the new `FLOOD_PREMIUM_WAIT <https://t.me/swiftgram/72>`_ errors.
- Added ``has_animation``, ``is_personal``, ``minithumbnail`` parameters to :obj:`~pyrogram.types.ChatPhoto`.
- Changed return type of :meth:`~pyrogram.Client.get_chat_photos` to return :obj:`~pyrogram.types.Photo` or :obj:`~pyrogram.types.Animation`.
- Added :meth:`~pyrogram.Client.get_chat_sponsored_messages` and the type :obj:`~pyrogram.types.SponsoredMessage`, by stealing unauthored changes from `KurimuzonAkuma/pyrogram#55 <https://github.com/KurimuzonAkuma/pyrogram/pull/55>`_.
- Added :meth:`~pyrogram.Client.load_group_call_participants` and the type :obj:`~pyrogram.types.GroupCallParticipant`, by stealing unauthored changes from `6df467f <https://github.com/KurimuzonAkuma/pyrogram/commit/6df467f89c0f6fa513a3f56ff1b517574fd3d164>`_.
- Added :meth:`~pyrogram.Client.view_messages` and the bound methods :meth:`~pyrogram.types.Message.read` and :meth:`~pyrogram.types.Message.view`.
- Added the field ``question_entities`` to the class :obj:`~pyrogram.types.Poll`.
- Added the field ``text_entities`` to the class :obj:`~pyrogram.types.PollOption`.
- Added the parameters ``question_parse_mode`` and ``question_entities`` to the method :meth:`~pyrogram.Client.send_poll`.
- Added the class :obj:`~pyrogram.types.InputPollOption` and changed the type of the parameter ``options`` in the method :meth:`~pyrogram.Client.send_poll` to Array of :obj:`~pyrogram.types.InputPollOption`.
- Added the field ``max_reaction_count`` to the class :obj:`~pyrogram.types.Chat`.
- Added the field ``via_join_request`` to the class :obj:`~pyrogram.types.ChatMemberUpdated`.
- Added the class :obj:`~pyrogram.types.TextQuote` and the field ``quote`` of type :obj:`~pyrogram.types.TextQuote` to the class :obj:`~pyrogram.types.Message`, which contains the part of the replied message text or caption that is quoted in the current message.
- Added ``full_name`` to :obj:`~pyrogram.types.Chat` and :obj:`~pyrogram.types.User` only for :obj:`~pyrogram.enums.ChatType.PRIVATE`.
- Added ``revoke_messages`` parameter to :meth:`~pyrogram.Client.ban_chat_member` and :meth:`~pyrogram.types.Chat.ban_member`.
- Added :meth:`~pyrogram.Client.get_collectible_item_info`.
- Added ``reverse`` parameter to :meth:`~pyrogram.Client.get_chat_history`. (`855e69e <https://github.com/pyrogram/pyrogram/blob/855e69e3f881c8140781c1d5e42e3098b2134dd2/pyrogram/methods/messages/get_history.py>`_, `a086b49 <https://github.com/dyanashek/pyrogram/commit/a086b492039687dd1b807969f9202061ce5305da>`_)
- `View new and changed raw API methods <https://telegramplayground.github.io/TG-APIs/TL/diff/?from=176&to=178>`__.

+------------------------+
| Scheme layer used: 178 |
+------------------------+

- Added :meth:`~pyrogram.Client.search_chats`.
- Added :meth:`~pyrogram.Client.get_bot_name`, :meth:`~pyrogram.Client.get_bot_info_description`, :meth:`~pyrogram.Client.get_bot_info_short_description`, :meth:`~pyrogram.Client.set_bot_name`, :meth:`~pyrogram.Client.set_bot_info_description`, :meth:`~pyrogram.Client.set_bot_info_short_description`.
- Added :meth:`~pyrogram.Client.edit_cached_media` and :meth:`~pyrogram.types.Message.edit_cached_media`.
- Steal `d51eef3 <https://github.com/PyrogramMod/PyrogramMod/commit/d51eef31dc28724405ff473e45ca21b7d835d8b4>`_ without attribution.
- Added ``max_reaction_count`` to :obj:`~pyrogram.types.ChatReactions`.
- Added ``personal_chat_message`` to :obj:`~pyrogram.types.Chat`.
- Added ``only_in_channels`` parameter to :meth:`~pyrogram.Client.search_global` and :meth:`~pyrogram.Client.search_global_count`.

+------------------------+
| Scheme layer used: 177 |
+------------------------+

- Added ``emoji_message_interaction`` parameter to :meth:`~pyrogram.Client.send_chat_action` and :meth:`~pyrogram.types.Message.reply_chat_action`.
- **BOTS ONLY**: Updated :obj:`~pyrogram.handlers.ChatMemberUpdatedHandler` to handle updates when the bot is blocked or unblocked by a user.
- Added missing parameters in :meth:`~pyrogram.Client.create_group`, :meth:`~pyrogram.Client.create_supergroup`, :meth:`~pyrogram.Client.create_channel`.
- Try to return the service message (when applicable) in the methods :meth:`~pyrogram.Client.add_chat_members`, :meth:`~pyrogram.Client.promote_chat_member`
- Add :obj:`~pyrogram.enums.ChatAction.TRIGGER_EMOJI_ANIMATION` and :obj:`~pyrogram.enums.ChatAction.WATCH_EMOJI_ANIMATION` in :meth:`~pyrogram.Client.send_chat_action` and :meth:`~pyrogram.types.Message.reply_chat_action`.
- Attempted to revert the Backward Incompatible changes in the commits `fb118f95d <https://github.com/TelegramPlayGround/pyrogram/commit/fb118f9>`_ and `848bc8644 <https://github.com/TelegramPlayGround/pyrogram/commit/848bc86>`_.
- Added ``callback_data_with_password`` to :obj:`~pyrogram.types.InlineKeyboardButton` and added support in :meth:`~pyrogram.types.Message.click` for such buttons.
- PR from upstream: `1391 <https://github.com/pyrogram/pyrogram/pull/1391>`_ without attribution.
- Added ``gifted_premium`` service message to :obj:`~pyrogram.types.Message`.
- Added :meth:`~pyrogram.Client.get_stickers`.
- Added ``filters.users_shared`` and ``filters.chat_shared``.
- Added the field ``origin`` of type :obj:`~pyrogram.types.MessageOrigin` in the class :obj:`~pyrogram.types.ExternalReplyInfo`.
- Added the class :obj:`~pyrogram.types.MessageOrigin` and replaced the fields ``forward_from``, ``forward_from_chat``, ``forward_from_message_id``, ``forward_signature``, ``forward_sender_name``, and ``forward_date`` with the field ``forward_origin`` of type :obj:`~pyrogram.types.MessageOrigin` in the class :obj:`~pyrogram.types.Message`.
- Added ``accent_color``, ``profile_color``, ``emoji_status``, ``is_close_friend`` to :obj:`~pyrogram.types.Chat` and :obj:`~pyrogram.types.User`.
- Added the method :meth:`~pyrogram.Client.get_created_chats`.
- Added the class :obj:`~pyrogram.types.ForumTopic` and the methods :meth:`~pyrogram.Client.get_forum_topics`, :meth:`~pyrogram.Client.get_forum_topic`.
- Install the version, from PyPI, using ``pip uninstall -y pyrogram && pip install pyrotgfork==2.1.17``.
- Added the classes :obj:`~pyrogram.types.BusinessOpeningHours` and :obj:`~pyrogram.types.BusinessOpeningHoursInterval` and the field       ``business_opening_hours`` to the class :obj:`~pyrogram.types.Chat`.
- Added the class :obj:`~pyrogram.types.BusinessLocation` and the field ``business_location`` to the class :obj:`~pyrogram.types.Chat`.
- Added the class :obj:`~pyrogram.types.BusinessIntro` and the field ``business_intro`` to the class :obj:`~pyrogram.types.Chat`.
- Added the parameter ``business_connection_id`` to the methods :meth:`~pyrogram.Client.send_message`, :meth:`~pyrogram.Client.send_photo`, :meth:`~pyrogram.Client.send_video`, :meth:`~pyrogram.Client.send_animation`, :meth:`~pyrogram.Client.send_audio`, :meth:`~pyrogram.Client.send_document`, :meth:`~pyrogram.Client.send_sticker`, :meth:`~pyrogram.Client.send_video_note`, :meth:`~pyrogram.Client.send_voice`, :meth:`~pyrogram.Client.send_location`, :meth:`~pyrogram.Client.send_venue`, :meth:`~pyrogram.Client.send_contact`, :meth:`~pyrogram.Client.send_poll`, :meth:`~pyrogram.Client.send_game`, :meth:`~pyrogram.Client.send_media_group`, :meth:`~pyrogram.Client.send_dice`, :meth:`~pyrogram.Client.send_chat_action`, :meth:`~pyrogram.Client.send_cached_media` and :meth:`~pyrogram.Client.copy_message` and the corresponding reply_* methods.
- Added :meth:`~pyrogram.Client.get_business_connection`.
- Added ``active_usernames`` to :obj:`~pyrogram.types.Chat` and :obj:`~pyrogram.types.User`.
- Added :obj:`~pyrogram.types.BusinessConnection`.
- Added support for ``https://t.me/m/blah`` links in the ``link`` parameter of :meth:`~pyrogram.Client.get_messages`
- Added the parameter ``message_thread_id`` to the :meth:`~pyrogram.Client.search_messages` and :meth:`~pyrogram.Client.search_messages_count`.
- Added the parameter ``chat_list`` to :meth:`~pyrogram.Client.search_global` and :meth:`~pyrogram.Client.search_global_count`.
- PR from upstream: `1411 <https://github.com/pyrogram/pyrogram/pull/1411>`_ without attribution.
- **BOTS ONLY**: Handled the parameter ``business_connection_id`` to the update handlers :obj:`~pyrogram.handlers.MessageHandler`, :obj:`~pyrogram.handlers.EditedMessageHandler`, :obj:`~pyrogram.handlers.DeletedMessagesHandler`.
- Added the field ``business_connection_id`` to the class :obj:`~pyrogram.types.Message`.
- Bug fix for the ``users_shared``, ``chat_shared`` logic in :obj:`~pyrogram.types.Message`.
- Added :meth:`~pyrogram.Client.set_birthdate` and :meth:`~pyrogram.Client.set_personal_chat`, for user accounts only.
- Added the field ``birthdate`` to the class :obj:`~pyrogram.types.Chat`.
- Added the field ``is_from_offline`` to the class :obj:`~pyrogram.types.Message`.
- Added the field ``sender_business_bot`` to the class :obj:`~pyrogram.types.Message`.
- Added the fields ``users_shared``, ``chat_shared`` to the class :obj:`~pyrogram.types.Message`.
- Added the field ``personal_chat`` to the class :obj:`~pyrogram.types.Chat`.
- Added the field ``can_connect_to_business`` to the class :obj:`~pyrogram.types.User`.
- Rearrange :meth:`~pyrogram.Client.send_sticker` parameter names.
- Added the fields ``request_title``, ``request_username``, and ``request_photo`` to the class :obj:`~pyrogram.types.KeyboardButtonRequestChat`.
- Added the fields ``request_name``, ``request_username``, and ``request_photo`` to the class :obj:`~pyrogram.types.KeyboardButtonRequestUsers`.

+------------------------+
| Scheme layer used: 176 |
+------------------------+

- Add ``message_thread_id`` parameter to :meth:`~pyrogram.Client.unpin_all_chat_messages`.
- Add :meth:`~pyrogram.Client.create_forum_topic`, :meth:`~pyrogram.Client.edit_forum_topic`, :meth:`~pyrogram.Client.close_forum_topic`, :meth:`~pyrogram.Client.reopen_forum_topic`, :meth:`~pyrogram.Client.hide_forum_topic`, :meth:`~pyrogram.Client.unhide_forum_topic`, :meth:`~pyrogram.Client.delete_forum_topic`, :meth:`~pyrogram.Client.get_forum_topic_icon_stickers`.
- Add ``AioSQLiteStorage``, by stealing the following commits:
    - `fded06e <https://github.com/KurimuzonAkuma/pyrogram/commit/fded06e7bdf8bb591fb5857d0f126986ccf357c8>`_
- Add ``skip_updates`` parameter to :obj:`~pyrogram.Client` class, by stealing the following commits:
    - `c16c83a <https://github.com/KurimuzonAkuma/pyrogram/commit/c16c83abc307e4646df0eba34aad6de42517c8bb>`_
    - `55aa162 <https://github.com/KurimuzonAkuma/pyrogram/commit/55aa162a38831d79604d4c10df1a046c8a1c3ea6>`_
- Add ``public``, ``for_my_bot`` to :meth:`~pyrogram.Client.delete_profile_photos`.
- Make ``photo_ids`` parameter as optional in :meth:`~pyrogram.Client.delete_profile_photos`.
- Add ``supergroup_chat_created`` to :obj:`~pyrogram.types.Message`.
- Add ``forum_topic_created``, ``forum_topic_closed``, ``forum_topic_edited``, ``forum_topic_reopened``, ``general_forum_topic_hidden``, ``general_forum_topic_unhidden`` to :obj:`~pyrogram.types.Message`.
- Add ``custom_action`` to :obj:`~pyrogram.types.Message`.
- Add ``public``, ``for_my_bot``, ``photo_frame_start_timestamp`` to :meth:`~pyrogram.Client.set_profile_photo`.
- Add ``inline_need_location``, ``can_be_edited`` to :obj:`~pyrogram.types.User`.
- Add ``giveaway``, ``giveaway_created``, ``giveaway_completed`` and ``giveaway_winners`` in :obj:`~pyrogram.types.Message` and :obj:`~pyrogram.types.ExternalReplyInfo`.
- Bug fix for :meth:`~pyrogram.Client.send_message` with the ``message_thread_id`` parameter.
- Added ``request_users`` and ``request_chat`` to :obj:`~pyrogram.types.KeyboardButton`.
- **NOTE**: using the ``scheduled`` parameter, please be aware about using the correct :doc:`Message Identifiers <../../topics/message-identifiers>`.
    - Add ``is_scheduled`` parameter to :meth:`~pyrogram.Client.delete_messages`.
    - Add ``schedule_date`` parameter to :meth:`~pyrogram.Client.edit_message_caption`, :meth:`~pyrogram.Client.edit_message_media`, :meth:`~pyrogram.Client.edit_message_text`.
    - Added ``is_scheduled`` to :meth:`~pyrogram.Client.get_messages`.
    - Added ``is_scheduled`` to :meth:`~pyrogram.Client.get_chat_history`.
- Added new parameter ``client_platform`` to :obj:`~pyrogram.Client`.
- PR from upstream: `1403 <https://github.com/pyrogram/pyrogram/pull/1403>`_.
- Added ``story`` to :obj:`~pyrogram.types.ExternalReplyInfo`.
- Added ``story_id`` to :obj:`~pyrogram.types.ReplyParameters`.
- Added support for clicking (:obj:`~pyrogram.types.WebAppInfo`, :obj:`~pyrogram.types.LoginUrl`, ``user_id``, ``switch_inline_query_chosen_chat``) buttons in :meth:`~pyrogram.types.Message.click`.
- Rewrote :meth:`~pyrogram.Client.download_media` to support Story, and also made it future proof.
- `Fix bug in clicking UpdateBotCallbackQuery buttons <https://t.me/pyrogramchat/610636>`_

+-------------+
|  PmOItrOAe  |
+-------------+

- Renamed ``placeholder`` to ``input_field_placeholder`` in :obj:`~pyrogram.types.ForceReply`.
- Add ``link`` parameter in :meth:`~pyrogram.Client.get_messages`
- `fix(filters): add type hints in filters.py <https://github.com/TelegramPlayGround/pyrogram/pull/8>`_
- Documentation Builder Fixes
- `faster-pyrogram <https://github.com/cavallium/faster-pyrogram>`_ is not polished or documented for anyone else's use. We don't have the capacity to support `faster-pyrogram <https://github.com/TelegramPlayGround/pyrogram/pull/6>`_ as an independent open-source project, nor any desire for it to become an alternative to Pyrogram. Our goal in making this code available is a unified faster Pyrogram. `... <https://github.com/cavallium/faster-pyrogram/blob/b781909/README.md#L28>`_
    - Lock-free and asynchronous implementation of the sqlite session.
    - The possibility of turning off journaling and vacuum when starting a session.
    - Improved implementation of rle_encode.
    - Implementation of _parse_channel_chat without getattr, in some scenarios.
    - Cache of FileId and UniqueFileId instances and of their string-coded versions.
    - Use of tcp abridged instead of tcp obfuscated as the default protocol.

+-----------------------------+
|   Leaked Scheme Layers (2)  |
+-----------------------------+

- `Add ttl_seconds attribute to Voice and VideoNote class <https://github.com/KurimuzonAkuma/pyrogram/commit/7556d3e3864215386f018692947cdf52a82cb420>`_
- `#713 <https://github.com/pyrogram/pyrogram/pull/713>`_
- Removed :obj:`~pyrogram.types.ChatPreview` class, and merged the parameters with the :obj:`~pyrogram.types.Chat` class.
- Added ``description``, ``accent_color_id``, ``is_verified``, ``is_scam``, ``is_fake``, ``is_public``, ``join_by_request`` attributes to the class :obj:`~pyrogram.types.ChatPreview`.
- Added ``force_full`` parameter to :meth:`~pyrogram.Client.get_chat`.
- Bug Fix for :meth:`~pyrogram.Client.get_chat` and :meth:`~pyrogram.Client.join_chat` when ``https://t.me/username`` was passed.
- Added missing attributes to the class :obj:`~pyrogram.types.Story` when it is available.
- Added the field ``reply_to_story`` to the class :obj:`~pyrogram.types.Message`.
- Added the field ``user_chat_id`` to the class :obj:`~pyrogram.types.ChatJoinRequest`.
- Added the field ``switch_inline_query_chosen_chat`` of the type :obj:`~pyrogram.types.SwitchInlineQueryChosenChat` to the class :obj:`~pyrogram.types.InlineKeyboardButton`, which allows bots to switch to inline mode in a chosen chat of the given type.
- Add support for ``pay`` in :obj:`~pyrogram.types.InlineKeyboardButton`
- `#1345 <https://github.com/pyrogram/pyrogram/issues/1345>`_
- `Add undocumented things <https://github.com/TelegramPlayGround/pyrogram/commit/8a72939d98f343eae1e07981f95769efaa741e4e>`_
- `Add missing enums.SentCodeType <https://github.com/KurimuzonAkuma/pyrogram/commit/40ddcbca6062f13958f4ca2c9852f8d1c4d62f3c>`_
- Renamed ``placeholder`` to ``input_field_placeholder`` in :obj:`~pyrogram.types.ReplyKeyboardMarkup`
- `#693 <https://github.com/KurimuzonAkuma/pyrogram/pull/693>`_
- Revert `e678c05 <https://github.com/TelegramPlayGround/pyrogram/commit/e678c054d4aa0bbbb7d583eb426ca8753a4c9354>`_ and stole squashed unauthored changes from `bcd18d5 <https://github.com/Masterolic/pyrogram/commit/bcd18d5e04f18f949389a03f309816d6f0f9eabe>`_

+------------------------+
| Scheme layer used: 174 |
+------------------------+

- Added the field ``story`` to the class :obj:`~pyrogram.types.Message` for messages with forwarded stories. Currently, it holds no information.
- Added the class :obj:`~pyrogram.types.ChatBoostAdded` and the field ``boost_added`` to the class :obj:`~pyrogram.types.Message` for service messages about a user boosting a chat.
- Added the field ``custom_emoji_sticker_set_name`` to the class :obj:`~pyrogram.types.Chat`.
- Added the field ``unrestrict_boost_count`` to the class :obj:`~pyrogram.types.Chat`.
- Added the field ``sender_boost_count`` to the class :obj:`~pyrogram.types.Message`.

+------------------------+
| Scheme layer used: 173 |
+------------------------+

- Fix ConnectionResetError when only ping task (`#24 <https://github.com/KurimuzonAkuma/pyrogram/pull/24>`_)
- Added ``is_topic_message`` to the :obj:`~pyrogram.types.Message` object.
- Added ``has_visible_history``, ``has_hidden_members``, ``has_aggressive_anti_spam_enabled``, ``message_auto_delete_time``, ``slow_mode_delay``, ``slowmode_next_send_date``, ``is_forum`` to the :obj:`~pyrogram.types.Chat` object.
- Added ``add_to_recent``, ``story_id`` parameters in :meth:`~pyrogram.Client.set_reaction`.
- Bug fix in parsing ``Vector<Bool>`` (Thanks to `@AmarnathCJD <https://github.com/AmarnathCJD/>`_ and `@roj1512 <https://github.com/roj1512>`_).
- Documentation Fix of ``max_concurrent_transmissions`` type hint.
- Bug Fix in the ``get_file`` method. (Thanks to `@ALiwoto <https://github.com/ALiwoto>`_).
- Added missing attributes to :obj:`~pyrogram.types.ChatPermissions` and :obj:`~pyrogram.types.ChatPrivileges`.
- `Bug Fix for MIN_CHAT_ID <https://t.me/pyrogramchat/593090>`_.
- Added new parameter ``no_joined_notifications`` to :obj:`~pyrogram.Client`.
- Fix history TTL Service Message Parse.
- Added environment variables ``PYROGRAM_DONOT_LOG_UNKNOWN_ERRORS``. Thanks to `... <https://t.me/pyrogramchat/607757>`_.
- Renamed ``force_document`` to ``disable_content_type_detection`` in :meth:`~pyrogram.Client.send_document` and :meth:`~pyrogram.types.Message.reply_document`.
- Added missing attributes ``added_to_attachment_menu``, ``can_be_added_to_attachment_menu``, ``can_join_groups``, ``can_read_all_group_messages``, ``supports_inline_queries``, ``restricts_new_chats`` to the :obj:`~pyrogram.types.User`.
- Migrate project to ``pyproject.toml`` from ``setup.py``.
- PRs from upstream: `1366 <https://github.com/pyrogram/pyrogram/pull/1366>`_, `1305 <https://github.com/pyrogram/pyrogram/pull/1305>`_, `1288 <https://github.com/pyrogram/pyrogram/pull/1288>`_, `1262 <https://github.com/pyrogram/pyrogram/pull/1262>`_, `1253 <https://github.com/pyrogram/pyrogram/pull/1253>`_, `1234 <https://github.com/pyrogram/pyrogram/pull/1234>`_, `1210 <https://github.com/pyrogram/pyrogram/pull/1210>`_, `1201 <https://github.com/pyrogram/pyrogram/pull/1201>`_, `1197 <https://github.com/pyrogram/pyrogram/pull/1197>`_, `1143 <https://github.com/pyrogram/pyrogram/pull/1143>`_, `1059 <https://github.com/pyrogram/pyrogram/pull/1059>`_.
- Bug fix for :meth:`~pyrogram.Client.send_audio` and :meth:`~pyrogram.Client.send_voice`. (Thanks to `... <https://t.me/c/1220993104/1360174>`_).
- Add `waveform` parameter to :meth:`~pyrogram.Client.send_voice`.
- Added `view_once` parameter to :meth:`~pyrogram.Client.send_photo`, :meth:`~pyrogram.Client.send_video`, :meth:`~pyrogram.Client.send_video_note`, :meth:`~pyrogram.Client.send_voice`.
- Add missing parameters to :obj:`~pyrogram.types.Message.reply_photo`, :obj:`~pyrogram.types.Message.reply_video`, :obj:`~pyrogram.types.Message.reply_video_note`, :obj:`~pyrogram.types.Message.reply_voice`.

+------------------------+
| Scheme layer used: 170 |
+------------------------+

- Stole documentation from `PyrogramMod <https://github.com/PyrogramMod/PyrogramMod>`_.
- Renamed ``send_reaction`` to :meth:`~pyrogram.Client.set_reaction`.
- Added support for :meth:`~pyrogram.Client.send_photo`, :meth:`~pyrogram.Client.send_video`, :meth:`~pyrogram.Client.send_animation`, :meth:`~pyrogram.Client.send_voice` messages that could be played once.
- Added ``_raw`` to the :obj:`~pyrogram.types.Chat` object.
- Added the field ``via_chat_folder_invite_link`` to the class :obj:`~pyrogram.types.ChatMemberUpdated`.
- **BOTS ONLY**: Added updates about a reaction change on a message with non-anonymous reactions, represented by the class :obj:`~pyrogram.handlers.MessageReactionUpdatedHandler` and the field ``message_reaction`` in the class Update.
- **BOTS ONLY**: Added updates about reaction changes on a message with anonymous reactions, represented by the class :obj:`~pyrogram.handlers.MessageReactionCountUpdatedHandler` and the field ``message_reaction_count`` in the class Update.
- Replaced the parameter ``disable_web_page_preview`` with :obj:`~pyrogram.types.LinkPreviewOptions` in the methods :meth:`~pyrogram.Client.send_message` and :meth:`~pyrogram.Client.edit_message_text`.
- Replaced the field ``disable_web_page_preview`` with :obj:`~pyrogram.types.LinkPreviewOptions` in the class :obj:`~pyrogram.types.InputTextMessageContent`.
- Added missing parameters to :meth:`~pyrogram.Client.forward_messages`.
- Added the class :obj:`~pyrogram.types.ReplyParameters` and replaced parameters ``reply_to_message_id`` in the methods :meth:`~pyrogram.Client.copy_message`, :meth:`~pyrogram.Client.forward_messages`, :meth:`~pyrogram.Client.send_message`, :meth:`~pyrogram.Client.send_photo`, :meth:`~pyrogram.Client.send_video`, :meth:`~pyrogram.Client.send_animation`, :meth:`~pyrogram.Client.send_audio`, :meth:`~pyrogram.Client.send_document`, :meth:`~pyrogram.Client.send_sticker`, :meth:`~pyrogram.Client.send_video_note`, :meth:`~pyrogram.Client.send_voice`, :meth:`~pyrogram.Client.send_location`, :meth:`~pyrogram.Client.send_venue`, :meth:`~pyrogram.Client.send_contact`, :meth:`~pyrogram.Client.send_poll`, :meth:`~pyrogram.Client.send_dice`, :meth:`~pyrogram.Client.send_game`, :meth:`~pyrogram.Client.send_media_group`, :meth:`~pyrogram.Client.copy_media_group`, :meth:`~pyrogram.Client.send_inline_bot_result`, :meth:`~pyrogram.Client.send_cached_media`, and the corresponding reply_* methods with the field ``reply_parameters`` of type :obj:`~pyrogram.types.ReplyParameters`.
- Bug fixes for sending ``ttl_seconds`` and ``has_spoiler``.

+------------------------+
| Scheme layer used: 169 |
+------------------------+

- Changed condition in :meth:`~pyrogram.Client.join_chat` and :meth:`~pyrogram.Client.get_chat`.
- Added ``nosound_video`` parameter to :obj:`~pyrogram.types.InputMediaVideo`.
- Added ``has_spoiler`` parameter to :meth:`~pyrogram.Client.copy_message`.
- Improved :meth:`~pyrogram.Client.get_chat_history`: add ``min_id`` and ``max_id`` params.
- Improved ``set_reaction`` for Telegram Premium Users.
- `Prevent connection to dc every time in get_file <https://github.com/TelegramPlayGround/pyrogram/commit/f2581fd7ab84ada7685645a6f80475fbea5e743a>`_
- Added ``_raw`` to the :obj:`~pyrogram.types.Chat`, :obj:`~pyrogram.types.Dialog`, and :obj:`~pyrogram.types.User` objects.
- Fix downloading media to ``WORKDIR`` when ``WORKDIR`` was not specified.
- `Update multiple fragment chat usernames <https://github.com/TelegramPlayGround/pyrogram/commit/39aea4831ee18e5263bf6755306f0ca49f075bda>`_
- `Custom Storage Engines <https://github.com/TelegramPlayGround/pyrogram/commit/cd937fff623759dcac8f437a8c524684868590a4>`_
- Documentation fix for ``user.mention`` in :obj:`~pyrogram.types.User`.

+------------------------+
| Scheme layer used: 167 |
+------------------------+

- Fixed the TL flags being Python reserved keywords: ``from`` and ``self``.

+------------------------+
| Scheme layer used: 164 |
+------------------------+

- Added ``_raw`` to the :obj:`~pyrogram.types.Message` object.

+------------------------+
| Scheme layer used: 161 |
+------------------------+

- Added ``my_stories_from`` to the :meth:`~pyrogram.Client.block_user` and :meth:`~pyrogram.Client.unblock_user` methods.

+------------------------+
| Scheme layer used: 160 |
+------------------------+

- Added ``message_thread_id`` to the methods :meth:`~pyrogram.Client.copy_message`, :meth:`~pyrogram.Client.forward_messages`, :meth:`~pyrogram.Client.send_message`, :meth:`~pyrogram.Client.send_photo`, :meth:`~pyrogram.Client.send_video`, :meth:`~pyrogram.Client.send_animation`, :meth:`~pyrogram.Client.send_audio`, :meth:`~pyrogram.Client.send_document`, :meth:`~pyrogram.Client.send_sticker`, :meth:`~pyrogram.Client.send_video_note`, :meth:`~pyrogram.Client.send_voice`, :meth:`~pyrogram.Client.send_location`, :meth:`~pyrogram.Client.send_venue`, :meth:`~pyrogram.Client.send_contact`, :meth:`~pyrogram.Client.send_poll`, :meth:`~pyrogram.Client.send_dice`, :meth:`~pyrogram.Client.send_game`, :meth:`~pyrogram.Client.send_media_group`, :meth:`~pyrogram.Client.copy_media_group`, :meth:`~pyrogram.Client.send_inline_bot_result`, :meth:`~pyrogram.Client.send_cached_media`.

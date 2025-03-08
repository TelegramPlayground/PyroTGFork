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

from .answer_pre_checkout_query import AnswerPreCheckoutQuery
from .answer_shipping_query import AnswerShippingQuery
from .create_invoice_link import CreateInvoiceLink
from .get_business_connection import GetBusinessConnection
from .get_collectible_item_info import GetCollectibleItemInfo
from .refund_star_payment import RefundStarPayment
from .send_invoice import SendInvoice
from .get_payment_form import GetPaymentForm
from .send_payment_form import SendPaymentForm
from .get_available_gifts import GetAvailableGifts
from .get_owned_star_count import GetOwnedStarCount
from .get_received_gifts import GetReceivedGifts
from .sell_gift import SellGift
from .send_gift import SendGift
from .toggle_gift_is_saved import ToggleGiftIsSaved


class TelegramBusiness(
    AnswerPreCheckoutQuery,
    AnswerShippingQuery,
    CreateInvoiceLink,
    GetBusinessConnection,
    GetCollectibleItemInfo,
    RefundStarPayment,
    SendInvoice,
    GetPaymentForm,
    SendPaymentForm,
    GetAvailableGifts,
    GetOwnedStarCount,
    GetReceivedGifts,
    SellGift,
    SendGift,
    ToggleGiftIsSaved,
):
    pass

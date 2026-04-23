from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_pay_keyboard(payout_id: str):
    print(payout_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="✅ Оплачено",
            callback_data=f"paid:{payout_id}"
        )]
    ])


def get_attach_keyboard(payout_id: str):
    print(payout_id)

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📎 Прикрепить чек",
            callback_data=f"attach:{payout_id}"
        )]
    ])

def get_edit_keyboard(payout_id: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔄 Изменить чек",
            callback_data=f"edit_receipt:{payout_id}"
        )]
    ])
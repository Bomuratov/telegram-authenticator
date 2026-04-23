from schemas.courier_payout import CourierPayout


def create_courier_payout_text(payload: CourierPayout):
    caption = "💸 <b>Запрос на вывод средств</b>\n\n"

    body = (
        f"👤 <b>Курьер:</b> #{payload.courier_id}A\n"
        f"💰 <b>Сумма вывода:</b> {payload.requested_amount} {payload.currency}\n\n"
        f"📊 <b>Баланс до:</b> {payload.balance_before} {payload.currency}\n"
        f"📉 <b>Баланс после:</b> {payload.balance_after} {payload.currency}\n\n"
        f"🧑‍💼 <b>Инициатор:</b> #{payload.initiator_id}A\n"
    )

    return caption + body



from schemas.notifications import ReviewSchema


TYPE_CONFIG = {
    "courier": {
        "title": "Отзыв о курьере",
        "icon": "🚗",
        "label": "Курьер",
    },
    "vendor": {
        "title": "Отзыв о заведении",
        "icon": "🍽",
        "label": "Заведение",
    },
}

LOW_RATING_THRESHOLD = 3


def render_stars(rating: int | None) -> str:
    if not rating:
        return "—"
    return "⭐" * rating + f" ({rating}/5)"


def format_tags(tags: list[str] | None) -> str:
    if not tags:
        return "—"
    return ", ".join(tags)


def format_comment(comment: str | None) -> str:
    if not comment:
        return "Без комментария"
    return comment.strip()


def format_date(dt) -> str:
    if not dt:
        return "—"
    return dt.strftime("%d.%m.%Y %H:%M")


def build_alert_block(rating: int | None) -> str:
    if not rating:
        return ""

    if rating < LOW_RATING_THRESHOLD:
        return "🚨 <b>НИЗКИЙ РЕЙТИНГ!</b>\n" "Требует внимания\n\n"

    return ""


def build_caption(payload: ReviewSchema) -> str:
    config = TYPE_CONFIG.get(
        payload.type,
        {
            "title": "📦 Отзыв",
            "icon": "📦",
            "label": payload.type,
        },
    )

    # базовые данные
    order = payload.orderId or "—"
    user = payload.userId or "—"
    date = format_date(payload.created_at)

    rating = render_stars(payload.rating)
    tags = format_tags(payload.tags)
    comment = format_comment(payload.comment)

    alert_block = build_alert_block(payload.rating)
    # 👉 динамический блок (разный для типов)
    subject_block = (
        f"{config['icon']} <b>{config['label']}:</b>\n"
        f"⭐ <b>Оценка:</b> {rating}\n"
        f"🏷 <b>Теги:</b> {tags}"
    )

    return (
        f"{alert_block}"
        f"📩 <b>{config['title']}</b>\n\n"
        f"📦 <b>Заказ:</b> #{order}\n"
        f"👤 <b>User ID:</b> {user}\n"
        f"🕒 <b>Дата:</b> {date}\n\n"
        f"{subject_block}\n"
        f"<b>━━━━━━━━━━━━━━━</b>\n"
        f"💬 <b>Комментарий:</b>\n{comment}"
    )

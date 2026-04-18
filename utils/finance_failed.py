

def create_failed_text(payload):
    linear = "—————————————————————————"
    caption = f"<b>🚨 ALERT!! #{payload.order_id}A\n\n<code>{payload.title}</code></b>\n"
    error = f"\n<b>ОШИБКА:</b>\n<code>{payload.error}</code>\n"
    trace = f"\n<b>TRACE:</b> <pre language='python'>{payload.trace}</pre>\n"
    data = f"\n<b>DATA:</b><pre language='json'>{payload.data}</pre>\n"
    text = caption+linear+error+linear+trace+linear+data
    return text
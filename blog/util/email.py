async def send_eamil(app, message):
    await app.smtp.send_message(message)

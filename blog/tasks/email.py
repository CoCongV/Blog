import aiosmtplib


async def open_smtp_connection(app, loop):
    host = getattr(app.config, 'EMAIL_HOST')
    port = getattr(app.config, 'EMAIL_PORT')
    smtp = aiosmtplib.SMTP(hostname=host, port=port, loop=loop, use_tls=True)
    await smtp.connect()
    app.smtp = smtp


async def close_redis_connection(app, loop):
    app.smtp.close()

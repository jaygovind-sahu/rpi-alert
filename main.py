import os
import smtplib
import ssl

from time import mktime
from datetime import datetime

import feedparser


def send_email(message):
    print(message)
    context = ssl.create_default_context()
    with smtplib.SMTP(
            os.environ['RPIALERT_SMTP_SERVER'],
            int(os.environ['RPIALERT_SMTP_PORT'])
    ) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(os.environ['RPIALERT_SENDER_EMAIL'], os.environ['RPIALERT_SENDER_PW'])
        server.sendmail(
            os.environ['RPIALERT_SENDER_EMAIL'],
            os.environ['RPIALERT_RECIPIENT_EMAIL'],
            message
        )


def format_message(alerts):
    message = ''
    for alert in alerts:
        a_message, a_link, a_published_at = alert
        message += f'\n{a_message} @ {a_published_at}\n{a_link}\n'
    return message


def main():
    feed = feedparser.parse("https://rpilocator.com/feed/")
    alerts = []
    for entry in feed['entries']:
        summary = entry['summary']
        if summary.strip().lower().startswith('stock alert (za)'):
            link = entry['link']
            published_at = datetime.fromtimestamp(mktime(entry['published_parsed']))
            staleness = (datetime.now() - published_at).total_seconds()
            if abs(staleness) < int(os.environ['RPIALERT_FRESHNESS_THRESHOLD']):
                alerts.append((summary, link, published_at))
    if alerts:
        send_email(format_message(alerts))


if __name__ == "__main__":
    main()

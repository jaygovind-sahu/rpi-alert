import os
import smtplib
import ssl

from pytz import timezone
from time import mktime
from datetime import datetime

import feedparser


def send_email(message):
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
    feed = feedparser.parse("https://rpilocator.com/feed/?country=US")
    alerts = []
    for entry in feed['entries']:
        summary = entry['summary']
        link = entry['link']
        gmt = timezone('GMT')
        rtz = timezone(os.environ['RPIALERT_RECIPIENT_TZ'])
        published_gmt = gmt.localize(datetime.fromtimestamp(mktime(entry['published_parsed'])))
        published_est = published_gmt.astimezone(rtz)
        staleness = (datetime.now(rtz) - published_est).total_seconds()
        if staleness < int(os.environ['RPIALERT_FRESHNESS_THRESHOLD']):
            alerts.append((summary, link, published_est))
    if alerts:
        message = format_message(alerts)
        send_email(message)


if __name__ == "__main__":
    main()

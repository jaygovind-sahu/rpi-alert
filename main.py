"""
Use the RPI Locator (https://rpilocator.com/) RSS feed to get new
Raspberry PI stock alerts.
"""

import os
import smtplib
import ssl
from datetime import datetime
from typing import List

import feedparser
from pytz import timezone

# Change this URL as needed
RPILOCATOR_FEED_URL = 'https://rpilocator.com/feed/?country=US'


def send_email(message: str) -> None:
    """
    Send email with given message. Below environment variables must be set:

    * RPIALERT_SMTP_SERVER
    * RPIALERT_SMTP_PORT
    * RPIALERT_SENDER_EMAIL
    * RPIALERT_SENDER_PW
    * RPIALERT_RECIPIENT_EMAIL

    :param message: the input message
    :return:
    """
    context = ssl.create_default_context()
    with smtplib.SMTP(
            os.environ['RPIALERT_SMTP_SERVER'],
            int(os.environ['RPIALERT_SMTP_PORT'])
    ) as server:
        server.starttls(context=context)
        server.login(os.environ['RPIALERT_SENDER_EMAIL'], os.environ['RPIALERT_SENDER_PW'])
        server.sendmail(
            os.environ['RPIALERT_SENDER_EMAIL'],
            os.environ['RPIALERT_RECIPIENT_EMAIL'],
            message
        )


def format_message(alerts: List[tuple]) -> str:
    """
    Build a message string from list of alerts.

    :param alerts: list of alerts
    :return:
    """
    message = ''
    for alert in alerts:
        a_message, a_link, a_published_at = alert
        message += f'\n{a_message} @ {a_published_at}\n{a_link}\n'
    return message


def main() -> None:
    """
    The main function:

    1. Get the entries from RPI Locator RSS feed
    2. Determine the freshness (or staleness) of each entry
    3. Consider fresh entries as alerts
    4. Build a message
    5. Send the message as email

    :return:
    """
    feed = feedparser.parse(RPILOCATOR_FEED_URL)
    alerts = []
    for entry in feed['entries']:
        summary = entry['summary']
        link = entry['link']
        gmt = timezone('GMT')
        rtz = timezone(os.environ['RPIALERT_RECIPIENT_TZ'])
        published_gmt = gmt.localize(datetime.strptime(entry['published'], '%a, %d %b %Y %X %Z'))
        published_rtz = published_gmt.astimezone(rtz)
        monitored_rtz = datetime.now(rtz)
        staleness = (monitored_rtz - published_rtz).total_seconds()
        if staleness < int(os.environ['RPIALERT_FRESHNESS_THRESHOLD']):
            alerts.append((summary, link, published_rtz))
    if alerts:
        message = format_message(alerts)
        send_email(message)


if __name__ == "__main__":
    main()

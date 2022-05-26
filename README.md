# RPI Alert

Reads an RSS feed and sends email if any RPI is available in the US.

### Environment

```shell
export RPIALERT_SMTP_PORT=587
export RPIALERT_SMTP_SERVER="smtp.gmail.com"
export RPIALERT_SENDER_EMAIL="your@gmail.com"
export RPIALERT_SENDER_PW="yourpassword"
export RPIALERT_RECIPIENT_EMAIL="another@email.id"
export RPIALERT_RECIPIENT_TZ="US/Eastern"
export RPIALERT_FRESHNESS_THRESHOLD=660
```

### Install

Either `git clone` or download:

```shell
wget -O main.py https://raw.githubusercontent.com/jaygovind-sahu/rpi-alert/main/main.py
```

#### Cron

```shell
*/10 * * * * sudo -E python3 /path/to/rpi-alert/main.py
```

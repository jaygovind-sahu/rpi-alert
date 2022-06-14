# RPI Alert

Use the RPI Locator (https://rpilocator.com/) RSS feed to get new Raspberry PI stock alerts.

### Environment

```shell
export RPIALERT_SMTP_PORT=587
export RPIALERT_SMTP_SERVER="smtp.gmail.com"
export RPIALERT_SENDER_EMAIL="your@gmail.com"
export RPIALERT_SENDER_PW="yourpassword"
export RPIALERT_RECIPIENT_EMAIL="another@email.id"
export RPIALERT_RECIPIENT_TZ="US/Eastern"
export RPIALERT_FRESHNESS_THRESHOLD=66
```

You can use GMail SMTP configuration to send emails. It is recommended to use a 
Google "app password" instead of login password.

`RPIALERT_FRESHNESS_THRESHOLD` should be configured based on cron schedule. If 
you are running the script every minute, it should check all entries which are 
posted in last ~60 seconds. Example shows 66 seconds - just to have some overlap.

If you prefer to receive a text message instead of email, you can follow [this](https://www.digitaltrends.com/mobile/how-to-send-a-text-from-your-email-account/) 
guide to put the appropriate email address in `RPIALERT_RECIPIENT_EMAIL`.

### Install

`git clone` / download / copy:

```shell
wget -O main.py https://raw.githubusercontent.com/jaygovind-sahu/rpi-alert/main/main.py
```

```shell
scp main.py pi@pi-hole.local:/home/pi/rpi-alert/
```

### Cron

To run the script every minute:
```shell
* * * * * sudo -E python3 /home/pi/rpi-alert/main.py
```

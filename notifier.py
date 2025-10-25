import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from zoneinfo import ZoneInfo


def format_timestamp():
    dk = ZoneInfo("Europe/Copenhagen")
    return datetime.now(dk).strftime("%d-%m-%Y %H:%M dansk tid")


def build_message(ticker, headline, risk, extra_note):
    return (
        f"🟥 [{format_timestamp()}] ⚠️ EARLY HEADS-UP\n"
        f"Ticker: {ticker}\n"
        f"Headline: {headline}\n"
        f"Risiko: {risk}\n"
        f"Note: {extra_note}\n"
    )


def send_alert(ticker, headline, risk, extra_note):
    alert_to = os.environ.get("ALERT_TO")
    alert_from = os.environ.get("ALERT_FROM")
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")

    body = build_message(ticker, headline, risk, extra_note)
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = f"AKTIE HEADS-UP: {ticker}"
    msg["From"] = alert_from
    msg["To"] = alert_to

with smtplib.SMTP(smtp_host, smtp_port) as server:
    server.connect(smtp_host, smtp_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(smtp_user, smtp_pass)
    server.send_message(msg)


    print(f"[ALERT SENT] {ticker}")

from datetime import date
from common.ipo_listing import get_ipo_list,build_email_body
from common.mailer import Mailer

import os
from dotenv import load_dotenv
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
print(SENDER_EMAIL)
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

recipients_list = [
        "krishnakaranam14@gmail.com"
    ]

if __name__ == "__main__":

    ipo_threshold = 200000

    ipo_list = get_ipo_list()
    filtered_ipos = [
        {
            "date": x["date"],
            "name": x["name"],
            "symbol": x["symbol"],
            "totalSharesValue": x["totalSharesValue"]
        }
        for x in ipo_list.get("ipoCalendar", [])
        if x.get("totalSharesValue") and x["totalSharesValue"] >= ipo_threshold
    ]
    email_body = build_email_body(filtered_ipos)

    mailer = Mailer(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        sender_email=SENDER_EMAIL,
        sender_password=SENDER_PASSWORD
    )

    mailer.send_email(
        recipients = recipients_list,
        subject=f"IPO Alert | {date.today()}",
        body=email_body
    )
    

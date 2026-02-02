import finnhub
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()



def get_ipo_list(from_date = None,to_date = None):
    """
    Get ipo list for a given from_date and to_date. 
    Default is today (in UTC)
    """
    if not from_date:
        from_date = str(datetime.today().date())
    if not to_date:
        to_date = str(datetime.today().date())

    FINNHUB_API_KEY = os.getenv("FINHUB_APIKEY")
    finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
    
    ipo_list = finnhub_client.ipo_calendar(_from=from_date, to=to_date)

    return ipo_list

def build_email_body(filtered_ipos):

    """
    this function formats the email body into a table of filtered ipos
    """

    if not filtered_ipos:
        body = (
            "Hello,\n\n"
            "There are no IPOs matching the criteria (Total Shares Value >= 200,000) "
            "for the selected date.\n\n"
            "Regards,\n"
            "IPO Alert System"
        )
    else:
        table_rows = ""
        for ipo in filtered_ipos:
            table_rows += f"""
            <tr>
                <td>{ipo['date']}</td>
                <td>{ipo['name']}</td>
                <td>{ipo['symbol']}</td>
                <td>{ipo['totalSharesValue']}</td>
            </tr>
            """

        body = f"""
        <html>
        <body>
            <p>Hello,</p>
            <p>Please find below the IPOs matching the criteria:</p>

            <table border="1" cellpadding="6" cellspacing="0">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Name</th>
                        <th>Symbol</th>
                        <th>Total Shares Value</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>

            <p>Regards,<br>IPO Alert System</p>
        </body>
        </html>
        """
    
    return body

    

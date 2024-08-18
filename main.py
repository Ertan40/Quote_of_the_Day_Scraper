from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText


def fetch_data():
    url = 'https://www.quoteoftheday.nu/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    raise Exception(f"Not able to fetch data due to an error: {response.status_code}")


def collect_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())  # Print formatted HTML for better readability
    div_quote = soup.find('div', class_='carousel-item active')
    if div_quote:
        quote_text = div_quote.get_text(strip=True)
        return quote_text  # Return the quote so to be used later
        # print(f"Quote of the Day: {quote_text}")
    else:
        print("Quote not found.")
        return None


def send_email(quote_text):
    if not quote_text:
        print("No quote to send.")
        return

    try:
        quote, author = quote_text.rsplit('.', 1)
        author = author.strip()  # Clean up leading/trailing whitespace
    except ValueError:
        print("Quote text format is invalid.")
        return

    # Create email message
    message_content = f"""\
    Dear team,

    Please find below the Quote of the Day:

    "{quote}". {author}

    Best regards,
    Ertan Donmez
    """
    # message = MIMEText(f"Quote of the Day: {quote_text}")
    message = MIMEText(message_content)
    message['Subject'] = 'Quote of the Day'
    message['From'] = 'sugarangel028@gmail.com'
    message['To'] = 'ertan.donmez@sitel.com'
    # message['To'] = 'ertandonmez1@gmail.com'

    try:
        # Connect to Gmail's SMTP server with SSL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            # Instead of using your regular Gmail password, you should create an App Password
            # from your Google account (under Security settings > App Passwords)
            server.login('your_email', 'your_app_password')  # Use your Gmail App Password here
            server.send_message(message)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    # Fetch data from the website
    html_data = fetch_data()

    # Collect the quote from the fetched HTML
    quote_of_the_day = collect_data(html_data)
    # print(f"{quote_of_the_day}")
    quote, author = quote_of_the_day.split('.')
    print(f"Quote of the day: '{quote}'. {author}")

    # Send the email if the quote was successfully extracted
    if quote_of_the_day:
        send_email(quote_of_the_day)

## Output:
# Quote of the day: 'You cannot find peace by avoiding life'. Virginia Woolf
# Email sent successfully!
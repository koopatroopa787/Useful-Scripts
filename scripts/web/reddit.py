import smtplib
import requests

def send_email(subject, body):
    from_addr = 'your_email@example.com'
    to_addr = 'your_email@example.com'
    msg = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_password')
        server.sendmail(from_addr, to_addr, msg)

def get_reddit_posts(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/new.json"
    headers = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    data = response.json()
    return [post['data']['title'] for post in data['data']['children']]

posts = get_reddit_posts('python')
send_email('Latest Reddit Posts', '\n'.join(posts))
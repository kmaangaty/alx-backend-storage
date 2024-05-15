import requests
import redis


def get_page(url: str) -> str:
    """
    Function to get page content and cache it with expiration

    Parameters:
        url (str): The URL of the page to fetch

    Returns:
        str: The content of the fetched page
    """
    redis_conn = redis.Redis()
    count_key = f"count:{url}"
    page_key = f"page:{url}"
    count = redis_conn.incr(count_key)
    if count == 1:
        page_content = requests.get(url).text
        redis_conn.setex(page_key, 10, page_content)
        return page_content
    else:
        return redis_conn.get(page_key).decode()

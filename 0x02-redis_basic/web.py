#!/usr/bin/env python3
"""
Module for web caching and tracking.
"""
import requests
import redis
from functools import wraps

redis_conn = redis.Redis()


def cache_and_track_access(method):
    """
    Decorator for counting how many times a URL is accessed
    and caching the response.
    """
    @wraps(method)
    def wrapper(url):
        """
        Wrapper function for caching and tracking URL accesses.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the URL.
        """
        cached_key = "cached:" + url
        cached_data = redis_conn.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")
        count_key = "count:" + url
        html_content = method(url)
        redis_conn.incr(count_key)
        redis_conn.set(cached_key, html_content)
        redis_conn.expire(cached_key, 10)

        return html_content

    return wrapper


@cache_and_track_access
def get_page(url: str) -> str:
    """
    Function to fetch the HTML content of a URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text

#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import requests
import redis
import time


def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a URL and cache the
    result with an expiration time of 10 seconds.
    Args:
        url (str): The URL to fetch HTML content from.
    Returns:
        str: The HTML content of the URL.
    """
    # Initialize Redis client
    r = redis.Redis()

    # Increment access count for the URL
    r.incr(f"count:{url}")

    # Check if the content is already cached
    cached_content = r.get(url)
    if cached_content:
        return cached_content.decode('utf-8')

    # Fetch HTML content from the URL
    response = requests.get(url)
    html_content = response.text

    # Cache the HTML content with expiration time of 10 seconds
    r.setex(url, 10, html_content)

    return html_content


# Test the function
if __name__ == "__main__":
    # Test URLs
    base_url = "http://slowwly.robertomurray.co.uk"
    urls = [f"{base_url}/delay/10000/url/http://www.example.com",
            f"{base_url}/delay/5000/url/http://www.example.com",
            f"{base_url}/delay/2000/url/http://www.example.com"
            ]

    # Fetch HTML content for each URL
    for url in urls:
        print(get_page(url))

    # Wait for caching to expire
    time.sleep(10)

    # Fetch HTML content again for each URL
    for url in urls:
        print(get_page(url))

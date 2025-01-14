import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def scrape_links(url, hostname, visited):
    """
    Scrape links from a given URL and recursively scrape links from the same hostname.

    Args:
        url (str): The URL to scrape.
        hostname (str): The base hostname for filtering.
        visited (set): Set of visited URLs to avoid duplicates.

    Returns:
        set: A set of all unique links found on the website.
    """
    try:
        # Send an HTTP request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all anchor tags with href attributes
        links = set()
        for a_tag in soup.find_all('a', href=True):
            # Create the full URL
            full_url = urljoin(url, a_tag['href'])

            # Parse the URL and check the hostname
            if urlparse(full_url).hostname == hostname:
                if full_url not in visited:
                    links.add(full_url)

        return links

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while scraping {url}: {e}")
        return set()

def crawl_website(start_url):
    """
    Crawl a website starting from the given URL, scraping all links within the same hostname.

    Args:
        start_url (str): The starting URL.

    Returns:
        set: A set of all unique links found on the website.
    """
    visited = set()
    to_visit = {start_url}
    hostname = urlparse(start_url).hostname

    while to_visit:
        current_url = to_visit.pop()
        print(f"Scraping: {current_url}")
        visited.add(current_url)

        # Get links from the current URL
        links = scrape_links(current_url, hostname, visited)

        # Add new links to the queue for further crawling
        to_visit.update(links - visited)

    return visited

if __name__ == "__main__":
    # Input the starting website URL
    website_url = input("Enter the starting website URL (e.g., https://example.com): ").strip()

    # Start crawling the website
    all_links = crawl_website(website_url)

    # Print the results
    print(f"\nTotal links found: {len(all_links)}")
    for link in sorted(all_links):
        print(link)

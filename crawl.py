import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag

class WebCrawler:
    """
    A web crawler that scrapes all links from a website, ensuring no duplicates
    by removing fragments and crawling only links within the same hostname.
    """

    def __init__(self, start_url):
        """
        Initialize the WebCrawler with a starting URL.

        Args:
            start_url (str): The starting URL for the crawl.
        """
        self.start_url = start_url
        self.hostname = urlparse(start_url).hostname
        self.visited = set()
        self.to_visit = {start_url}

    def scrape_links(self, url):
        """
        Scrape all unique links from the given URL.

        Args:
            url (str): The URL to scrape.

        Returns:
            set: A set of unique links within the same hostname.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            links = set()
            for a_tag in soup.find_all('a', href=True):
                # Create the full URL and remove fragments
                full_url = urljoin(url, a_tag['href'])
                clean_url, _ = urldefrag(full_url)

                # Add to links if it's within the same hostname and not visited
                if urlparse(clean_url).hostname == self.hostname and clean_url not in self.visited:
                    links.add(clean_url)

            return links

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while scraping {url}: {e}")
            return set()

    def crawl(self):
        """
        Start crawling the website from the start URL.

        Returns:
            set: A set of all unique links found on the website.
        """
        while self.to_visit:
            current_url = self.to_visit.pop()
            print(f"Scraping: {current_url}")
            self.visited.add(current_url)

            # Scrape links from the current URL
            links = self.scrape_links(current_url)

            # Add new links to the queue
            self.to_visit.update(links - self.visited)

        return self.visited

if __name__ == "__main__":
    # Input the starting website URL
    website_url = input("Enter the starting website URL (e.g., https://example.com): ").strip()

    # Initialize the WebCrawler and start crawling
    crawler = WebCrawler(website_url)
    all_links = crawler.crawl()

    # Print the results
    print(f"\nTotal links found: {len(all_links)}")
    for link in sorted(all_links):
        print(link)

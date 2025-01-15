import os
import requests
from bs4 import BeautifulSoup


class TextExtractor:
    """
    A class to extract and save text data from a list of URLs.
    """

    def __init__(self, urls, output_dir="extracted_text"):
        """
        Initialize the TextExtractor with a list of URLs.

        Args:
            urls (list): A list of URLs to extract text from.
            output_dir (str): Directory where the extracted text files will be saved.
        """
        self.urls = urls
        self.output_dir = output_dir
        self.data = []

    def create_output_dir(self):
        """
        Create the output directory if it doesn't already exist.
        """
        os.makedirs(self.output_dir, exist_ok=True)

    def extract_text(self, url):
        """
        Extract the text content from a single URL.

        Args:
            url (str): The URL to extract text from.

        Returns:
            str: The extracted text.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the text content
            text = soup.get_text(separator="\n", strip=True)
            return text

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while extracting text from {url}: {e}")
            return ""

    def save_text(self, text, metadata):
        """
        Save the extracted text to a file named after the URL.

        Args:
            url (str): The URL (used to generate the file name).
            text (str): The text content to save.
        """
        # Generate a safe file name based on the URL
        file_name = metadata['url'].replace("https://", "").replace("http://", "").replace("/", "_")
        self.data.append({
            "metadata": metadata,
            "content": text
        })        

        print(f"Saved content from {metadata['url']}")

    def extract(self):
        """
        Extract and save text data for all URLs in the list.
        """
        for url in self.urls:
            print(f"Extracting text from {url}...")
            text = self.extract_text(url)
            if text:
                self.save_text(text, {
                    "url": url
                })
        return self.data


if __name__ == "__main__":
    # Example list of URLs (replace with your own list from the crawler)
    urls = [
        "https://tryintent.com/docs/transformers",
        "https://tryintent.com/docs/helpers",
        "https://tryintent.com/docs/providers",
        # Add more URLs as needed
    ]

    # Initialize and run the TextExtractor
    extractor = TextExtractor(urls)
    extractor.run()

import requests
from bs4 import BeautifulSoup

class GithubDocLoader:
    def load(self, url: str) -> dict:
        response= requests.get(url)
        response.raise_for_status()

        soup= BeautifulSoup(response.text,"lxml")

        main_content= soup.find("main",{"id":"main-content"})

        if not main_content:
            raise ValueError("Main Content not found")
        
        content= main_content.get_text(separator= "\n", strip=True)

        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else ""

        return {
            "content": content,
            "source": url,
            "title": title,
            "doc_type": "web"
        }
    


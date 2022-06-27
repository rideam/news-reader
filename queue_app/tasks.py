from urllib import request
from bs4 import BeautifulSoup
# import lxml

def scrape_url(url):
    try:
        r = request.urlopen(url)

        if "cnn" in url:
            tag_text = "div"
            class_text = "zn-body__paragraph"
        else:
            tag_text="p"
            class_text = None

        soup = BeautifulSoup(r.read().decode(), "lxml")
        title = soup.title.text
        paragraphs = [p.text for p in soup.find_all(tag_text, class_text)]
        return paragraphs, title
    except Exception as e:
        print(e)
        paragraphs = ["The url you submitted is invalid or cannot be scraped."]
        title = "Failed to access url"
        return paragraphs, title

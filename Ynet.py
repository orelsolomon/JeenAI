import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd
from gensim.summarization import summarize


def get_ynet_links(url):
    def extract_internal_links(url):
        r = requests.get(url)
        links = set()
        links.add(url)
        if r.status_code == 200:  # 200 is success, 404 or 500 unsuccessful
            soup = BeautifulSoup(r.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                link_url = urljoin(url, href)
                if urlparse(link_url).scheme in ['http', 'https']:
                    links.add(link_url)
        return links

    links = extract_internal_links(url)
    return list(links)


def get_page_title(url):
    r = requests.get(url)
    if r.status_code == 200:  # 200 is success, 404 or 500 unsuccessful
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.title.string


def get_page_summarize(url):
    r = requests.get(url)
    if r.status_code == 200:  # 200 is success, 404 or 500 unsuccessful
        soup = BeautifulSoup(r.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
    if len(text) > 50:
        summary = summarize(text)
    else:
        summary = text
    return summary


def create_Excel(file):
    df_urls = pd.read_excel(file)
    page_name, page_url, page_summary = [], [], []

    for url in df_urls['URL']:
        page_name.append(get_page_title(url))
        page_url.append(url)
        page_summary.append(get_page_summarize(url))

    df_result = pd.DataFrame({'Page Name': page_name, 'Page URL': page_url, 'Summary': page_summary})
    df_result.to_excel(file, index=False)


def export_to_excel(urls, file):
    df = pd.DataFrame(urls, columns=['URL'])
    df.to_excel(file, index=False)


# Main
ynet_url = 'https://www.ynet.co.il/home/0,7340,L-8,00.html'
ynet_links = get_ynet_links(ynet_url)
file = 'data.xlsx'
export_to_excel(ynet_links, file)

create_Excel(file)
print("process success")

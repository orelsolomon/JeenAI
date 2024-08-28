import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd


def get_ynet_links(url):
    def extract_internal_links(url):
        r = requests.get(url)
        links = set()
        if r.status_code == 200:  # 200 is success, 404 or 500 unsuccessful
            soup = BeautifulSoup(r.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                if urlparse(full_url).scheme in ['http', 'https']:
                    links.add(full_url)
        return links

    links = extract_internal_links(url)
    return list(links)


def get_page_title(url):
    r = requests.get(url)
    if r.status_code == 200:  # 200 is success, 404 or 500 unsuccessful
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.title.string


def create_Excel(file):
    df_urls = pd.read_excel(file)

    page_names, page_urls = [], []

    for url in df_urls['URL']:
        page_names.append(get_page_title(url))
        page_urls.append(url)

    df_result = pd.DataFrame({'Page Name': page_names, 'Page URL': page_urls})
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

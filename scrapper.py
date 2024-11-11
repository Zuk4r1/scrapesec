# scrapper.py
import requests
from bs4 import BeautifulSoup
import yaml
import logging
from urllib.parse import urljoin, urlparse

BANNER = """
Herramienta desarrollada por Zuk4r1

--------------------------------------------------------------------
 ______      _    _      _  __         _         _____       _____  
|___  /     | |  | |    | |/ /       / \       |  __ \     |_   _| 
   / /      | |  | |    | ' /       / _ \      | |__) |      | |   
  / /       | |  | |    |  <       / ___ \     |  _  /       | |   
 / /__      | |__| |    | . \     /_/   \_\    | | \ \      _| |_  
/_____|      \____/     |_|\_\               |_|  \_\    |_____|  

--------------------------------------------------------------------

"""

class Scrapper:
    def __init__(self, url, config):
        self.url = url
        self.config = config
        self.headers = {"User-Agent": config["scraping"].get("user_agent", "ScrapperBot/1.0")}
        self.timeout = config["scraping"].get("timeout", 5)
        self.max_links = config["scan_parameters"].get("max_links", 50)
        self.logger = self.setup_logger()

    @staticmethod
    def setup_logger():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        return logging.getLogger("Scrapper")

    @staticmethod
    def load_config(config_path="config/config.yml"):
        with open(config_path, "r") as file:
            return yaml.safe_load(file)

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.scheme) and bool(parsed.netloc)

    def fetch_page(self):
        """Obtiene el contenido HTML de la página objetivo."""
        try:
            self.logger.info(f"Fetching page: {self.url}")
            response = requests.get(self.url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Error al obtener la página: {e}")
            return None

    def parse_links(self, html):
        """Extrae y retorna una lista de enlaces únicos válidos en la página objetivo."""
        soup = BeautifulSoup(html, "html.parser")
        links = set()
        for a in soup.find_all('a', href=True):
            link = urljoin(self.url, a['href'])
            if self.is_valid_url(link):
                links.add(link)
        links = list(links)[:self.max_links]  # Limitar a max_links
        self.logger.info(f"Found {len(links)} unique links.")
        return links

if __name__ == "__main__":
    print(BANNER)  # Imprimir el banner al iniciar
    config = Scrapper.load_config()
    url = config.get("scanner", {}).get("url", "http://example.com")

    # Ejecutar el scrapper
    scrapper = Scrapper(url, config)
    page_content = scrapper.fetch_page()
    if page_content:
        links = scrapper.parse_links(page_content)
        print("Enlaces encontrados:", links)

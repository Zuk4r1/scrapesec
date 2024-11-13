import requests
from bs4 import BeautifulSoup
import yaml
import logging
from urllib.parse import urljoin, urlparse
import tldextract  # Importa la librería para extraer subdominios

BANNER = """
Herramienta desarrollada por @Zuk4r1

--------------------------------------------------------------------
 ______      _    _      _  __        _         _____       _____  
|___  /     | |  | |    | |/ /       / \       |  __ \     |_   _| 
   / /      | |  | |    | ' /       / _ \      | |__) |      | |   
  / /       | |  | |    |  <       / ___ \     |  _  /       | |   
 / /__      | |__| |    | . \     / /   \ \    | | \ \      _| |_  
/_____|      \____/     |_|\_\   /_/     \_\   |_|  \_\    |_____|  

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

    def setup_logger(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        return logging.getLogger("Scrapper")

    @staticmethod
    def load_config(config_path="config.yml"):  # Cambiado a "config.yml"
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

    def extract_subdomains(self, url):
        """Extrae los subdominios de una URL."""
        ext = tldextract.extract(url)
        # Si tiene subdominio, lo devuelve; si no, devuelve una lista vacía
        subdomains = ext.subdomain.split('.') if ext.subdomain else []
        return subdomains

    def save_results(self, links, subdomains, filename="resultados.txt"):
        """Guarda los resultados en un archivo .txt."""
        with open(filename, "w") as file:
            file.write(f"URL objetivo: {self.url}\n")
            file.write("\nEnlaces encontrados:\n")
            for link in links:
                file.write(f"{link}\n")
            file.write("\nSubdominios extraídos:\n")
            for subdomain in subdomains:
                file.write(f"{subdomain}\n")
            self.logger.info(f"Resultados guardados en {filename}")

if __name__ == "__main__":
    print(BANNER)  # Imprimir el banner al iniciar
    config = Scrapper.load_config()  # Cargar configuración desde config.yml
    url = config.get("scraping", {}).get("url", "http://example.com")

    # Crear la instancia de Scrapper con la configuración cargada
    scrapper = Scrapper(url, config)
    page_content = scrapper.fetch_page()
    if page_content:
        links = scrapper.parse_links(page_content)
        print("Enlaces encontrados:", links)

        # Extraer subdominios de la URL principal
        subdomains = scrapper.extract_subdomains(url)
        print("Subdominios extraídos:", subdomains)

        # Guardar resultados en un archivo .txt
        scrapper.save_results(links, subdomains)



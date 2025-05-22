import sys
import requests
import logging
from urllib.parse import urlparse
import tldextract
import dns.resolver
import random

BANNER = """
Herramienta desarrollada por @Zuk4r1

--------------------------------------------------------------
  ______   _    _    _  __   _  _     _____    __   _______
 |___  /  | |  | |  | |/ /  | || |   |  __ \  /_ | |       |
    / /   | |  | |  | ' /   | || |_  | |__) |  | | |  OPEN |
   / /    | |  | |  |  <    |__   _| |  _  /   | | |_______|
  / /__   | |__| |  | . \      | |   | | \ \   | |   || ||
 /_____|   \____/   |_|\_\     |_|   |_|  \_\  |_|   ||_||
                                                   SCANNING...
---------------------------------------------------------------

"""

class Scrapper:
    def __init__(self, url, proxies=None, user_agents=None):
        self.url = url
        self.proxies = proxies
        self.user_agents = user_agents or ["ScrapperBot/1.0"]
        self.timeout = 5
        self.logger = self.setup_logger()

    def setup_logger(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        return logging.getLogger("Scrapper")

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.scheme) and bool(parsed.netloc)

    def extract_subdomains(self, url):
        """Extrae los subdominios de una URL usando tldextract y consultas DNS."""
        ext = tldextract.extract(url)
        domain = f"{ext.domain}.{ext.suffix}"

        try:
            subdomains = []
            resolver = dns.resolver.Resolver()
            records = resolver.query(domain, 'NS')
            for record in records:
                subdomain = str(record.target).rstrip('.')
                if subdomain:
                    subdomains.append(subdomain)
            return subdomains
        except Exception as e:
            self.logger.error(f"Error al extraer subdominios: {e}")
            return []

    def save_results(self, subdomains, filename="resultados.txt"):
        """Guarda los subdominios en un archivo .txt con el prefijo https://."""
        with open(filename, "w") as file:
            file.write(f"URL objetivo: {self.url}\n")
            file.write("\nSubdominios extraídos:\n")
            for subdomain in subdomains:
                file.write(f"https://{subdomain}\n")
            self.logger.info(f"Resultados guardados en {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: python {sys.argv[0]} <URL>")
        sys.exit(1)

    print(BANNER)  # Imprimir el banner al iniciar
    url = sys.argv[1]

    # Configuración de proxies y user agents para eludir firewalls
    proxies = {
        "http": "http://proxyserver:port",
        "https": "https://proxyserver:port"
    }
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/87.0.664.66",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
    ]

    # Crear la instancia de Scrapper con la configuración proporcionada
    scrapper = Scrapper(url, proxies=proxies, user_agents=user_agents)

    if scrapper.is_valid_url(url):
        # Extraer subdominios de la URL principal
        subdomains = scrapper.extract_subdomains(url)
        print("Subdominios extraídos:", subdomains)

        # Guardar resultados en un archivo .txt con el prefijo https://
        scrapper.save_results(subdomains)
    else:
        print("La URL proporcionada no es válida.")

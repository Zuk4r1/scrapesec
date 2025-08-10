import sys
import requests
import logging
from urllib.parse import urlparse
import tldextract
import dns.resolver
import random
import argparse
import threading
from queue import Queue

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
except ImportError:
    class DummyColor:
        RESET = RED = GREEN = YELLOW = CYAN = ""
    Fore = Style = DummyColor()

BANNER = f"""{Fore.CYAN}
Herramienta desarrollada por 🐉 @Zuk4r1

--------------------------------------------------------------
  ______   _    _    _  __   _  _     _____    __   _______
 |___  /  | |  | |  | |/ /  | || |   |  __ \  /_ | |       |
    / /   | |  | |  | ' /   | || |_  | |__) |  | | |  OPEN |
   / /    | |  | |  |  <    |__   _| |  _  /   | | |_______|
  / /__   | |__| |  | . \      | |   | | \ \   | |   || ||
 /_____|   \____/   |_|\_\     |_|   |_|  \_\  |_|   ||_||
                                                   SCANNING...
---------------------------------------------------------------

{Style.RESET_ALL}
"""

DEFAULT_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/87.0.664.66",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
]

class Scrapper:
    def __init__(self, url, proxies=None, user_agents=None, timeout=5, logger=None):
        self.url = url
        self.proxies = proxies
        self.user_agents = user_agents or DEFAULT_USER_AGENTS
        self.timeout = timeout
        self.logger = logger or self.setup_logger()

    def setup_logger(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        return logging.getLogger("Scrapper")

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.scheme) and bool(parsed.netloc)

    def get_domain(self):
        ext = tldextract.extract(self.url)
        return f"{ext.domain}.{ext.suffix}"

    def extract_subdomains_dns(self):
        """Extrae subdominios usando registros NS y CNAME vía DNS."""
        domain = self.get_domain()
        subdomains = set()
        try:
            resolver = dns.resolver.Resolver()
            for rtype in ['NS', 'CNAME']:
                try:
                    records = resolver.resolve(domain, rtype)
                    for record in records:
                        sub = str(record.target if hasattr(record, 'target') else record).rstrip('.')
                        if sub and sub != domain:
                            subdomains.add(sub)
                except Exception:
                    continue
        except Exception as e:
            self.logger.error(f"Error DNS: {e}")
        return list(subdomains)

    def extract_subdomains_bruteforce(self, wordlist, threads=20):
        """Fuerza bruta de subdominios usando diccionario."""
        domain = self.get_domain()
        found = set()
        q = Queue()
        for word in wordlist:
            q.put(word.strip())
        def worker():
            while not q.empty():
                sub = q.get()
                fqdn = f"{sub}.{domain}"
                try:
                    dns.resolver.resolve(fqdn, 'A', lifetime=self.timeout)
                    found.add(fqdn)
                    print(f"{Fore.GREEN}[+] Encontrado: {fqdn}{Style.RESET_ALL}")
                except Exception:
                    pass
                q.task_done()
        threads_list = []
        for _ in range(threads):
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()
            threads_list.append(t)
        q.join()
        return list(found)

    def extract_subdomains_crtsh(self):
        """Consulta la API de crt.sh para obtener subdominios."""
        domain = self.get_domain()
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        try:
            resp = requests.get(url, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                subdomains = set()
                for entry in data:
                    name = entry.get('name_value', '')
                    for sub in name.split('\n'):
                        if sub.endswith(domain):
                            subdomains.add(sub.strip())
                return list(subdomains)
        except Exception as e:
            self.logger.error(f"Error consultando crt.sh: {e}")
        return []

    def save_results(self, subdomains, filename="resultados.txt"):
        """Guarda los subdominios en un archivo .txt con el prefijo https://."""
        with open(filename, "w") as file:
            file.write(f"URL objetivo: {self.url}\n")
            file.write("\nSubdominios extraídos:\n")
            for subdomain in sorted(subdomains):
                file.write(f"https://{subdomain}\n")
        self.logger.info(f"Resultados guardados en {filename}")

def load_wordlist(path):
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{Fore.RED}No se pudo cargar el diccionario: {e}{Style.RESET_ALL}")
        return []

def parse_args():
    parser = argparse.ArgumentParser(description="Subdomain Advanced Scrapper")
    parser.add_argument("url", help="URL objetivo (ej: https://example.com)")
    parser.add_argument("-w", "--wordlist", help="Archivo de diccionario para fuerza bruta de subdominios")
    parser.add_argument("-p", "--proxies", help="Proxies en formato http://host:port,https://host:port")
    parser.add_argument("-u", "--user-agents", help="Archivo con user-agents personalizados")
    parser.add_argument("-t", "--timeout", type=int, default=5, help="Timeout de requests/DNS")
    parser.add_argument("-m", "--mode", choices=["dns", "brute", "crtsh", "all"], default="all", help="Modo de extracción")
    parser.add_argument("-o", "--output", default="resultados.txt", help="Archivo de salida")
    return parser.parse_args()

def main():
    args = parse_args()
    print(BANNER)
    proxies = None
    if args.proxies:
        try:
            http, https = args.proxies.split(",")
            proxies = {"http": http, "https": https}
        except Exception:
            print(f"{Fore.YELLOW}Formato de proxies inválido, ignorando...{Style.RESET_ALL}")
    user_agents = DEFAULT_USER_AGENTS
    if args.user_agents:
        user_agents = load_wordlist(args.user_agents)
    scrapper = Scrapper(args.url, proxies=proxies, user_agents=user_agents, timeout=args.timeout)
    if not scrapper.is_valid_url(args.url):
        print(f"{Fore.RED}La URL proporcionada no es válida.{Style.RESET_ALL}")
        sys.exit(1)
    all_subdomains = set()
    if args.mode in ("dns", "all"):
        print(f"{Fore.CYAN}[*] Extrayendo subdominios por DNS...{Style.RESET_ALL}")
        all_subdomains.update(scrapper.extract_subdomains_dns())
    if args.mode in ("crtsh", "all"):
        print(f"{Fore.CYAN}[*] Extrayendo subdominios por crt.sh...{Style.RESET_ALL}")
        all_subdomains.update(scrapper.extract_subdomains_crtsh())
    if args.mode in ("brute", "all") and args.wordlist:
        print(f"{Fore.CYAN}[*] Fuerza bruta de subdominios...{Style.RESET_ALL}")
        wordlist = load_wordlist(args.wordlist)
        all_subdomains.update(scrapper.extract_subdomains_bruteforce(wordlist))
    print(f"{Fore.YELLOW}Subdominios extraídos: {len(all_subdomains)}{Style.RESET_ALL}")
    for sub in sorted(all_subdomains):
        print(f"{Fore.GREEN}{sub}{Style.RESET_ALL}")
    scrapper.save_results(all_subdomains, filename=args.output)

if __name__ == "__main__":
    main()


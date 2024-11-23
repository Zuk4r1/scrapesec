  GNU nano 8.2                                                                                                                                                                                                                                                                                                          scanner.py                                                                                                                                                                                                                                                                                                                    
import requests
import yaml
import time
import logging
import os
import random

BANNER = r"""
Herramienta desarrollada por @Zuk4r1
--------------------------------------------------------------------------
  ______   _    _    _  __   _  _     _____    __   ┌─────────────────┐ 
 |___  /  | |  | |  | |/ /  | || |   |  __ \  /_ |  │ ████████████░░  │
    / /   | |  | |  | ' /   | || |_  | |__) |  | |  │ ████████████░░  │
   / /    | |  | |  |  <    |__   _| |  _  /   | |  │ ██████░░░░░░░░  │
  / /__   | |__| |  | . \      | |   | | \ \   | |  │ ░░░░░░░░░░░░░░  │ 
 /_____|   \____/   |_|\_\     |_|   |_|  \_\  |_|  └─────────────────┘  
                                                     Analyzing Threats...
---------------------------------------------------------------------------
"""

class VulnerabilityScanner:
    def __init__(self, config):
        self.config = config
        self.payloads = config["scanner"]
        self.detection = config["scanner"]["detection"]
        self.delay = config["scan_parameters"].get("delay_between_requests", 2)
        self.retry_on_failure = config["scan_parameters"].get("retry_on_failure", True)
        self.max_retries = config["scan_parameters"].get("max_retries", 3)
        self.proxies = config["scraping"].get("proxy", None)
        self.user_agents = config["scraping"].get("user_agents", ["ScrapperBot/1.0"])
        self.logger = self.setup_logger()

    @staticmethod
    def load_config(config_path="config.yml"):
        with open(config_path, "r") as file:
            return yaml.safe_load(file)

    def setup_logger(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        return logging.getLogger("VulnerabilityScanner")

    def make_request(self, url):
        retries = 0
        headers = {"User-Agent": random.choice(self.user_agents)}
        while retries < self.max_retries:
            try:
                response = requests.get(url, headers=headers, proxies=self.proxies, timeout=5)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                self.logger.error(f"Error en la solicitud a {url}: {e}")
                if not self.retry_on_failure:
                    return None
                retries += 1
                self.logger.info(f"Reintentando ({retries}/{self.max_retries}) en {self.delay} segundos...")
                time.sleep(self.delay)
        return None

    def test_xss(self):
        for payload in self.payloads["xss_payloads"]:
            test_url = f"{self.url}?q={payload}"
            response = self.make_request(test_url)
            if response and any(indicator in response.text for indicator in self.detection["xss_indicators"]):
                result = f"[!] Posible XSS encontrado en: {test_url} con payload '{payload}'"
                print(result)
                self.logger.info(result)
                self.results.append(result)

    def test_sql_injection(self):
        for payload in self.payloads["sql_injection_payloads"]:
            test_url = f"{self.url}?id={payload}"
            response = self.make_request(test_url)
            if response and any(indicator in response.text.lower() for indicator in self.detection["sql_injection_indicators"]):
                result = f"[!] Posible inyección SQL encontrada en: {test_url} con payload '{payload}'"
                print(result)
                self.logger.info(result)
                self.results.append(result)

    def scan_urls(self, urls):
        self.results = []
        for url in urls:
            print(f"Escaneando URL: {url}")
            self.url = url
            self.test_xss()
            self.test_sql_injection()
        self.save_results(self.results)

    def save_results(self, results, file_path="resultados_vulnerabilidades.txt"):
        with open(file_path, "a") as file:
            for result in results:
                file.write(result + "\n")

if __name__ == "__main__":
    print(BANNER)

    config = VulnerabilityScanner.load_config("config.yml")
    scanner = VulnerabilityScanner(config=config)

    resultados_file = "resultados.txt"
    if not os.path.exists(resultados_file):
        print(f"El archivo {resultados_file} no existe. Asegúrate de ejecutar el scrapper primero.")
        exit(1)

    with open(resultados_file, "r") as file:
        lines = file.readlines()
        urls = [line.strip() for line in lines if "http" in line]

    scanner.scan_urls(urls)

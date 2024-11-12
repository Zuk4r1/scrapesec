# scanner.py
import requests
import yaml
import time
import logging

BANNER = """
Herramienta desarrollada por @Zuk4r1
--------------------------------------------------------------------
 ______      _    _      _  __        _         _____       _______  
|___  /     | |  | |    | |/ /       / \       |  __ \     |__   __| 
   / /      | |  | |    | ' /       / _ \      | |__) |       | |   
  / /       | |  | |    |  <       / ___ \     |  _  /        | |   
 / /__      | |__| |    | . \     / /   \ \    | | \ \      __| |__ 
/_____|      \____/     |_|\_\   /_/     \_\   |_|  \_\    |_______|  

--------------------------------------------------------------------
"""


class VulnerabilityScanner:
    def __init__(self, url, config):
        self.url = url
        self.config = config
        self.payloads = config["scanner"]
        self.detection = config["scanner"]["detection"]
        self.delay = config["scan_parameters"].get("delay_between_requests", 2)
        self.retry_on_failure = config["scan_parameters"].get("retry_on_failure", True)
        self.max_retries = config["scan_parameters"].get("max_retries", 3)
        self.logger = self.setup_logger()

    @zuk4r1
    def setup_logger():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        return logging.getLogger("VulnerabilityScanner")

    @zuk4r1
    def load_config(config_path="config.yml"):
        with open(config_path, "r") as file:
            return yaml.safe_load(file)

    def make_request(self, url):
        """Realiza la solicitud HTTP con reintentos en caso de fallo."""
        retries = 0
        while retries < self.max_retries:
            try:
                response = requests.get(url, timeout=5)
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
        """Prueba de XSS usando payloads configurados y busca indicadores en la respuesta."""
        for payload in self.payloads["xss_payloads"]:
            test_url = f"{self.url}?q={payload}"
            response = self.make_request(test_url)
            if response and any(indicator in response.text for indicator in self.detection["xss_indicators"]):
                print(f"[!] Posible XSS encontrado en: {test_url} con payload '{payload}'")
                self.logger.info(f"Posible XSS encontrado en: {test_url} con payload '{payload}'")

    def test_sql_injection(self):
        """Prueba de inyección SQL usando payloads configurados y busca indicadores en la respuesta."""
        for payload in self.payloads["sql_injection_payloads"]:
            test_url = f"{self.url}?id={payload}"
            response = self.make_request(test_url)
            if response and any(indicator in response.text.lower() for indicator in self.detection["sql_injection_indicators"]):
                print(f"[!] Posible inyección SQL encontrada en: {test_url} con payload '{payload}'")
                self.logger.info(f"Posible inyección SQL en: {test_url} con payload '{payload}'")

if __name__ == "__main__":
    print(BANNER)  # Imprimir el banner al iniciar
    config = VulnerabilityScanner.load_config()
    url = config.get("scanner", {}).get("url", "http://example.com")

    # Ejecutar el escáner de vulnerabilidades
    scanner = VulnerabilityScanner(url, config)
    scanner.test_xss()
    scanner.test_sql_injection()

# Scrapper

## Descripción general

Scrapper es una herramienta en Python desarrollada para realizar scraping en aplicaciones web y, adicionalmente, probar vulnerabilidades comunes, como Cross-Site Scripting (XSS) y SQL Injection. La herramienta realiza una exploración inicial de enlaces en el sitio objetivo y prueba distintas cargas útiles para detectar posibles vulnerabilidades de seguridad. Este proyecto está dirigido a pentesters y desarrolladores que buscan un enfoque básico para detectar estas vulnerabilidades en sus aplicaciones web.

> **Advertencia**: El uso de esta herramienta para realizar pruebas en aplicaciones sin el permiso explícito de los propietarios puede ser ilegal. Pentester Zuk4r1 y los contribuidores de este proyecto no se responsabilizan por el uso indebido de esta herramienta.

## Características
- **Scraping de enlaces**: Extrae enlaces desde el HTML de la página objetivo para una mejor exploración de la aplicación.
- **Pruebas de vulnerabilidades**: Pruebas básicas para XSS y SQL Injection en los enlaces extraídos.
- **Configuración de payloads**: Los payloads utilizados para las pruebas de seguridad son configurables en el archivo `config.yml`.

## Instalación y uso

### Requisitos previos
- Python 3.x
- `pip` para gestionar las dependencias de Python

### Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/PentesterZuk4r1/Scrapper.git
   cd Scrapper

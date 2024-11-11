- ## **Documentación de uso**

Este archivo describe cómo utilizar los componentes principales de la herramienta desarrollada por Zuk4r1 : el Scrapper para la recopilación de enlaces y el VulnerabilityScanner para probar vulnerabilidades comunes.

## **¿Quién mantiene y contribuye al proyecto?**

Scrapper es desarrollado y mantenido por @zuk4r1

- ## **Introducción**

Este proyecto permite recopilar enlaces de un sitio web objetivo utilizando Scrappery probar vulnerabilidades comunes de tipo XSS e inyección SQL utilizando VulnerabilityScanner. Los resultados de cada ejecución se muestran en la terminal y se registran en el archivo de registro.

- ## **Requisitos previos**

Python 3.7 o superior
Acceso a Internet para instalar dependencias
Acceso a la línea de comandos

- ## **Instalación**

**Clonar el repositorio:**

```bash
git clone https://github.com/Zuk4r1/scrapper.py.git
cd scrapper.py
pip install -r requisitos.txt


- ## **Ejecución del Scrapper**

--bash
python scrapper.py


- ## **Opciones de configuración del Scrapper**

**user_agent:** User-Agent que se usará en las solicitudes HTTP

**timeout:** Tiempo máximo de espera para la respuesta de cada solicitud

**max_links:** Número máximo de enlaces a recopilar

- ## **Ejecución del VulnerabilityScanner**

--bash
python scanner.py


- ## **Opciones de configuración del VulnerabilityScanner**

**xss_payloads:** Lista de cargas útiles para probar vulnerabilidades XSS

**sql_injection_payloads:** Lista de cargas útiles para probar inyecciones SQL

**delay_between_requests:** Tiempo de espera entre solicitudes para evitar ser bloqueado

**retry_on_failure:** Intentos adicionales en caso de error en la solicitud

**max_retries:** Número máximo de reintentos permitidos.

"El archivo config/config.ymlpermite personalizar los parámetros clave para ambas herramientas."

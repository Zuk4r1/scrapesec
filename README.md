- ## **Documentación de uso** ##

Este archivo describe cómo utilizar los componentes principales de la herramienta desarrollada por **@Zuk4r1** el proyecto **ScrapeSec** para la recopilación de enlaces con **scrapper.py** y el **scanner.py** para probar vulnerabilidades comunes,avanzadas y bypass del firewall.

## **¿Quién mantiene y contribuye al proyecto?** ##

**ScrapeSec** es desarrollado y mantenido por [@Zuk4r1](https://github.com/Zuk4r1).
  <br />
	<br/>
      	<p width="20px"><b>Se aceptan donaciones para mantener este proyecto</p></b>
	      <a href="https://buymeacoffee.com/investigacq"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=investigacqc&button_colour=FF5F5F&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00" /></a><br />
      	<a href="https://www.paypal.com/paypalme/babiloniaetica"><img title="Donations For Projects" height="25" src="https://ionicabizau.github.io/badges/paypal.svg" /></a>
</div>

- ## **Introducción** ##

Este proyecto permite recopilar enlaces de un sitio web objetivo utilizando **scrapper.py** y probar vulnerabilidades comunes de tipo XSS e inyección SQL utilizando **scanner.py** . Los resultados de cada ejecución se muestran en la terminal y se registran en el archivo de resultados ( resultados.txt).

- ## **Requisitos previos** ##

Python 3.7 o superior

Acceso a Internet para instalar dependencias

Acceso a la línea de comandos

- ## **Instalación** ##

**1. Clonar el repositorio:**
```
git clone https://github.com/Zuk4r1/scrapper.py.git
```

**2. Cambia al directorio del proyecto:**
```
cd ScrapeSec
```

**3. Da permisos de ejecución a los scripts:**
```
chmod +x scanner.py
chmod +x scrapper.py
```


**4. Instale las dependencias necesarias:**
```
pip install -r requirements.txt
```

- ## **Ejecución del ScrapeSec simplemente corre el siguiente comando:** ##
```
python scrapper.py https://ejemplo.com/
```

- ## **Ejecución del scanner.py:** ##
```
python scanner.py
```

- ## **Opciones de configuración del scanner.py** ##

**xss_payloads:** Lista de cargas útiles para probar vulnerabilidades XSS

**sql_injection_payloads:** Lista de cargas útiles para probar inyecciones SQL

**delay_between_requests:** Tiempo de espera entre solicitudes para evitar ser bloqueado

**retry_on_failure:** Intentos adicionales en caso de error en la solicitud

**max_retries:** Número máximo de reintentos permitidos.

- ## **Archivo de configuración config.yml** ##
El archivo config.ymlpermite personalizar los parámetros clave para ambas herramientas. Aquí se pueden definir los parámetros de escaneo, como las cargas útiles de inyección y XSS, así como los ajustes de red y retrasos entre solicitudes.

- ## **Funcionamiento** ##
1. **Scrapper.py** recorre el sitio web objetivo, recopilando enlaces y guardándolos en el archivo resultados.txt.

2. **scanner.py** utiliza esos enlaces, escaneando cada uno de ellos en busca de vulnerabilidades comunes, como XSS e inyecciones SQL.

3. Los resultados del escaneo se guardan en el mismo archivo resultados.txto en un archivo de registro según se configure.

- ## **Notas importantes** ##
  
Asegúrese de haber ejecutado **scrapper.py** antes de ejecutar **scanner,py** ya que este último depende de los enlaces recopilados en el archivo **resultados.txt**.

La herramienta no está pensada para ser utilizada en sitios web sin permiso explícito del propietario. Asegúrese de contar con autorización para escanear el sitio objetivo.

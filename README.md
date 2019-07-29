# Integration_tbk
Modulo de integración hacia webpay en django
Este módulo usa la libreria python-tbk hecha por cornershop, este modulo su fin es una facil integración con django

# Requerimientos:

Django 1.9 o superior
Zeep
python-tbk

# Se asume que se tiene un proyecto de django instalado con su ambiente virtual

# Instalación de Django
pip install Django

# Instalación de python-tbk
Instalación

Ejecuta:

$ pipenv install python-tbk

ó:

$ pip install python-tbk

Uso

Tan simple como llamar los métodos del API de Webpay (pero snakecased):

>>> from tbk.services import WebpayService
>>> from tbk.commerce import Commerce
>>> from tbk import INTEGRACION
>>> commerce = Commerce(commerce_code, key_data, cert_data, tbk_cert_data, INTEGRACION)
>>> webpay = WebpayService(commerce)
>>> transaction = webpay.init_transaction(amount, buy_order, return_url, final_url)
>>> print(transaction['token'])
e87df74f7af4dcfdc1d17521b07413ff9a004a7b423dc47ad09f6a8166a73842

Convenciones

La librería usa una convención de nombres snakecased para ser más pythonica. Cada nombre camelcased en el API de Webpay se transformó a snakecased:

initTransaction(amount, buyOrder, returnURL, finalURL, sessionId)

se traduce en:

init_transaction(amount, buy_order, return_url, final_url, session_id)

Documentación

La documentación oficial se encuentra disponible en http://www.transbankdevelopers.cl/?m=api. La documentación de esta librería está en desarrollo.
Loggers

Se encuentran definidos dos niveles de logger:

tbk.services
tbk.soap

El logger específico de un servicio está definido por su nombre de clase:

tbk.services.WebpayService

# Instalación de Zeep
pip install zeep

# en urls del proyecto principal se agrega:
url(r'^integracion_tbk/',include('integracion_tbk.urls'))

# en el settings del proyecto principal se agrega
INSTALLED_APPS = (
    ...
    'integracion_tbk'
)


from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import detail_route
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

import os
import logging
from datetime import datetime
import random
import flask
import tbk

CERTIFICATES_DIR = os.path.join(os.path.dirname(__file__), 'commerces')


def load_commerce_data(commerce_code):
    with open(os.path.join(CERTIFICATES_DIR, commerce_code, commerce_code + '.key'), 'r') as file:
        key_data = file.read()
    with open(os.path.join(CERTIFICATES_DIR, commerce_code, commerce_code + '.crt'), 'r') as file:
        cert_data = file.read()
    with open(os.path.join(CERTIFICATES_DIR, 'tbk.pem'), 'r') as file:
        tbk_cert_data = file.read()

    return {
        'key_data': key_data,
        'cert_data': cert_data,
        'tbk_cert_data': tbk_cert_data
    }


# app = flask.Flask(__name__)
# app.secret_key = 'TBKSESSION'

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)
# logging.getLogger("tbk").setLevel(logging.DEBUG)
# logging.getLogger('suds.transport.http').setLevel(logging.DEBUG)

HOST = os.getenv('HOST', 'http://127.0.0.1')
PORT = os.getenv('PORT', '8086')
BASE_URL = '{host}:{port}'.format(host=HOST, port=PORT)

NORMAL_COMMERCE_CODE = "597020000541"
ONECLICK_COMMERCE_CODE = "597020000593"


normal_commerce_data = load_commerce_data(NORMAL_COMMERCE_CODE)
normal_commerce = tbk.commerce.Commerce(
    commerce_code=NORMAL_COMMERCE_CODE,
    key_data=normal_commerce_data['key_data'],
    cert_data=normal_commerce_data['cert_data'],
    tbk_cert_data=normal_commerce_data['tbk_cert_data'],
    environment=tbk.environments.DEVELOPMENT)
webpay_service = tbk.services.WebpayService(normal_commerce)


oneclick_commerce_data = load_commerce_data(ONECLICK_COMMERCE_CODE)
oneclick_commerce = tbk.commerce.Commerce(
    commerce_code=ONECLICK_COMMERCE_CODE,
    key_data=oneclick_commerce_data['key_data'],
    cert_data=oneclick_commerce_data['cert_data'],
    tbk_cert_data=oneclick_commerce_data['tbk_cert_data'],
    environment=tbk.environments.DEVELOPMENT)


oneclick_service = tbk.services.OneClickPaymentService(oneclick_commerce)
oneclick_commerce_service = tbk.services.CommerceIntegrationService(oneclick_commerce)

#pagina de inicio de la transaccion de transbank
def init(request):
	template_name = 'integracion_tbk/base.html'

	return render(request,template_name)

#pagina de inicio para transaccion normal
def normal_index(request):
	template_name = 'integracion_tbk/index_normal.html'

	return render(request, template_name)

#metodo que inicia la conexion de la transaccion con webpay
@detail_route(methods=['post'])
def normal_init_transaction(request):
	template_name = 'integracion_tbk/init_normal.html'
	context = {}
	
	transaction = webpay_service.init_transaction(
	    amount=request.POST.get('amount'),
	    buy_order=request.POST.get('buy_order'),
	    return_url=BASE_URL + "/integracion_tbk/return",
	    final_url=BASE_URL + "/",
	    session_id=request.POST.get('session_id')
	)
	context['transaction'] = transaction
	# print context
	# return flask.render_template(template_name, transaction=transaction)
	return render_to_response(template_name, context ,context_instance=RequestContext(request))


#metodo que redirige segun la respuesta de webpay 
@csrf_exempt
def normal_return_from_webpay(request):
	token = request.POST.get('token_ws')
	transaction = webpay_service.get_transaction_result(token)
	transaction_detail = transaction['detailOutput'][0]
	webpay_service.acknowledge_transaction(token)

	if transaction_detail['responseCode'] == 0:
		template_name =  'integracion_tbk/success_normal.html'
		context = {}
		context['transaction'] = transaction

		if len(transaction_detail) != 0:
			context['transaction_detail'] = transaction_detail

		context['token'] = token

		return render_to_response(template_name, context, context_instance=RequestContext(request))

	else:
		template_name = 'integracion_tbk/failure_normal.html'
		context = {}
		context['transaction'] = transaction

		if len(transaction_detail) != 0:
			context['transaction_detail'] = transaction_detail

		context['token'] = token

		return render_to_response(template_name, context, context_instance=RequestContext(request))

#termino de la transaccion
@csrf_exempt
@detail_route(methods=['post'])
def normal_final(request):
	template_name = 'integracion_tbk/final_normal.html'
	context = {}

	token = request.POST.get('token_ws')
	context['token'] = token
	return render_to_response(template_name, context, context_instance=RequestContext(request))


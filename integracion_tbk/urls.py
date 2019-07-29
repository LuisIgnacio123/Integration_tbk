from django.conf.urls import url,include

from integracion_tbk import views


from django.contrib.auth.views import login

app_name = "integracion_tbk"
urlpatterns = [
	url(r'^$', views.init, name='init'),
	url(r'^normal_index/$', views.normal_index, name='normal_index'),
	url(r'^normal_init_transaction$', views.normal_init_transaction, name='normal_init_transaction'),
	url(r'^return$', views.normal_return_from_webpay, name='normal_return_from_webpay'),
	url(r'^final$', views.normal_final, name='normal_final'),
]
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^wish_items/delete/(\d+)/$', views.delete),
    url(r'^remove/(\d+)/$', views.remove),
    url(r'^wish_items/add/(\d+)/$', views.add),
    url(r'^wish_items/create$', views.create),
    url(r'^show_dashboard$', views.show_dashboard),
    url(r'^registration$', views.registration),
    url(r'^logoff$', views.logoff),
    url(r'^login$', views.login),
    url(r'^wish_items/create_item/$', views.create_item),
    url(r'^wish_items/(\d+)/$', views.show_item),
    # url(r'^dashboard/$', views.dashboard),
    url(r'^$', views.index)
]

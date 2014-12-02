from django.conf.urls import patterns, url

from pedidos import views

urlpatterns = patterns('',
                       url(r'^$', views.index),
                       url(r'^todos/$', views.todos),
                       url(r'^(?P<produto_codigo>\w+)/produto/$', views.produto),
                       url(r'^(?P<cliente_id>\d+)/cliente/$', views.cliente),
                       url(r'^data/$', views.bydate),
                       url(r'^(?P<container_num>\d+)/container/$', views.container),
                       url(r'^listcontainers/$', views.listcontainers),
                       url(r'^(?P<redirect_name>\S+)/(?P<pedido_id>\d+)/delete/$', views.delete),
                       url(r'^vencehoje/$', views.vencehoje),
                       url(r'^vencidos/$', views.vencidos),
                       url(r'^vencem/$', views.vencem),
                       url(r'^prodscontainer/$', views.prodscontainer),
                       # url(r'^prodsdesistencia/$', views.prodsdesistencia),
                       url(r'^prodsdesistencia/$', views.pedidosdesistencia),
                       url(r'^produtos/$', views.produtos),
                       url(r'^prodsreserva/$', views.prodsreserva),
                       url(r'^clientes/$', views.clientes),
                       url(r'^(?P<codigo>\w+)/foto/$', views.showimg),
                       url(r'^total/$', views.listtotal),
                       url(r'^(?P<codigo>\w+)/total/$', views.total),
                       url(r'^newtotal/$', views.listnewtotal),
                       url(r'^(?P<codigo>\w+)/newtotal/$', views.newtotal),
                       url(r'^(?P<pedido_id>\d+)/pedido/$', views.singlepedido),
                       
                       url(r'^(?P<keyword>\w+)/$', views.em_observacoes),
                       )

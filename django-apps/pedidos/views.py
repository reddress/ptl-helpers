# Create your views here.
from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from pedidos.models import Pedido, Cliente, Produto, LineItem, PAC

def listpedidos(request, pedidos, location):
    return render(request, "pedidos/listpedidos.html",
                  {'pedidos': pedidos, 'location': location})

def index(request):
    return render(request, "pedidos/index.html")

def todos(request):
    pedidos = Pedido.objects.order_by('data')
    return listpedidos(request, pedidos, "todos")
    
def produto(request, produto_codigo):
    pedidos = Pedido.objects.filter(lineitem__produto__codigo = produto_codigo).order_by('data')
    return listpedidos(request, pedidos, produto_codigo + "/produto")
    
def cliente(request, cliente_id):
    pedidos = Pedido.objects.filter(cliente__id = cliente_id).order_by('data')
    return listpedidos(request, pedidos, cliente_id + "/cliente")

def bydate(request):
    pedidos = Pedido.objects.order_by('data')
    return listpedidos(request, pedidos, "data/")

def em_observacoes(request, keyword):
    pedidos = Pedido.objects.filter(observacoes__icontains=keyword).order_by('data')
    return listpedidos(request, pedidos, keyword)

def container(request, container_num):
    pedidos = Pedido.objects.filter(container=container_num).order_by('cliente__vendedor')
    return listpedidos(request, pedidos, container_num + "/container")

def listcontainers(request):
    containers = set()
    pedidos = Pedido.objects.all()
    for p in pedidos:
        if p.container:
            containers.add(p.container)
    return render(request, "pedidos/listcontainers.html", {'containers': sorted(containers) })

def delete(request, redirect_name, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    with open('trash.py', 'a') as trash:
        print(pedido.data, file=trash)
        print(pedido.cliente, file=trash)
        print(pedido.condicoes + " -" + str(pedido.desconto) + "% desconto", file=trash)
        for lineitem in list(pedido.lineitem_set.all()):
            print(str(lineitem.quantidade) + " " + lineitem.unidade + " " +
                  lineitem.produto.codigo + " " +
                  lineitem.produto.descricao, file=trash)
        print(pedido.observacoes, file=trash)
        if pedido.container:
            print(str(pedido.container) + " ", file=trash)
        if pedido.extra:
            print(pedido.extra, file=trash)
        print("--------------------------------------------------", file=trash)
    pedido.delete()
    return HttpResponseRedirect("/pedidos/" + redirect_name)

def vencehoje(request):
    now = datetime.now()
    pedidos = Pedido.objects.filter(vencimento__year=now.year,
                                    vencimento__month=now.month,
                                    vencimento__day=now.day).order_by('data')
    return listpedidos(request, pedidos, "vencehoje")

def vencidos(request):
    pedidos = Pedido.objects.filter(vencimento__lte=datetime.now()).order_by('data')
    return listpedidos(request, pedidos, "vencidos")

def vencem(request):
    pedidos = Pedido.objects.filter(vencimento__isnull=False).order_by('data')
    return listpedidos(request, pedidos, "vencem")

def prodscontainer(request):
    pedidos = Pedido.objects.filter(observacoes__icontains="container")
    codigos = {}
    labels = set()
    for pedido in pedidos:
        for lineitem in list(pedido.lineitem_set.all()):
            label = str(pedido.container) + " - " + lineitem.produto.codigo + " " + lineitem.produto.descricao
            labels.add(label)
            codigos[label] = lineitem.produto.codigo
    labels = sorted(labels)
    return render(request, "pedidos/listcodigoslabels.html", {'codigos': codigos, 'labels': labels})

def prodsdesistencia(request):
    produtos = Produto.objects.filter(lineitem__pedido__observacoes__icontains="desistencia").order_by('codigo').distinct()
    return render(request, "pedidos/listprodutosnewtotal.html", {'produtos': produtos})

def pedidosdesistencia(request):
    produtos = Produto.objects.filter(lineitem__pedido__observacoes__icontains="desistencia").order_by('codigo').distinct()
    pedidos_dict = {}
    cobrar_dict = {}
    container_dict = {}
    pac_dict = {}
    for produto in list(produtos):
        #pedidos_dict[produto.codigo] = Pedido.objects.filter(lineitem__produto__codigo=produto.codigo).filter(observacoes__icontains="desistencia")
        
        pedidos_dict[produto.codigo] = LineItem.objects.filter(produto__codigo=produto.codigo).filter(pedido__observacoes__icontains="desistencia").order_by('pedido__data')
        
        cobrar_dict[produto.codigo] = LineItem.objects.filter(produto__codigo=produto.codigo).filter(pedido__observacoes__icontains="cobrar").order_by('pedido__data')

        container_dict[produto.codigo] = LineItem.objects.filter(produto__codigo=produto.codigo).filter(pedido__observacoes__icontains="container").order_by('pedido__data')

        pac_dict[produto.codigo] = PAC.objects.filter(produto__codigo=produto.codigo)
    return render(request, "pedidos/listpedidosnewtotal.html",
                  {'produtos': produtos, 'pedidos_dict': pedidos_dict,
                   'pac_dict': pac_dict, 'cobrar_dict': cobrar_dict,
                   'container_dict': container_dict, })

def produtos(request):
    produtos = Produto.objects.order_by('codigo')
    return render(request, "pedidos/listprodutos.html", {'produtos': produtos})

def prodsreserva(request):
    produtos = Produto.objects.filter(lineitem__pedido__observacoes__icontains="reserva").order_by('codigo').distinct()
    return render(request, "pedidos/listprodutos.html", {'produtos': produtos})

def clientes(request):
    clientes = Cliente.objects.order_by('nome')
    return render(request, "pedidos/listclientes.html", {'clientes': clientes})

def showimg(request, codigo):
    return render(request, "pedidos/showimg.html", {'codigo': codigo})

def listtotal(request):
    produtos = Produto.objects.order_by('codigo')
    return render(request, "pedidos/listprodutostotal.html", {'produtos': produtos})

def total(request, codigo):
    lineitems = LineItem.objects.filter(produto__codigo=codigo)
    produto = list(Produto.objects.filter(codigo=codigo))
    pac = PAC.objects.filter(produto__codigo=codigo)
    label = codigo + " - " + produto[0].descricao
    
    pecas = 0
    volumes = 0
    des_pecas = 0
    des_volumes = 0

    pedidos = []
    des_pedidos = []
    
    for lineitem in list(lineitems):
        if "desistencia" in lineitem.pedido.observacoes.lower():
            des_pedidos.append({'id': lineitem.pedido.id,
                            'label': str(lineitem.pedido.container) + " - " +
                            str(lineitem.quantidade) + " " +
                            lineitem.unidade + " " +
                            lineitem.pedido.cliente.nome + " (" +
                            lineitem.pedido.cliente.vendedor.nome + ")"
                            })
            if lineitem.unidade[0:2] == "pç":
                des_pecas += lineitem.quantidade
            else:
                des_volumes += lineitem.quantidade
        else:
            pedidos.append({'id': lineitem.pedido.id,
                            'label': str(lineitem.pedido.container) + " - " +
                            str(lineitem.quantidade) + " " +
                            lineitem.unidade + " " +
                            lineitem.pedido.cliente.nome + " (" +
                            lineitem.pedido.cliente.vendedor.nome + ")"
                            })
            if lineitem.unidade[0:2] == "pç":
                pecas += lineitem.quantidade
            else:
                volumes += lineitem.quantidade
                
    return render(request, "pedidos/total.html",
                  {'label': label, 'pecas': pecas, 'volumes': volumes,
                   'des_pecas': des_pecas, 'des_volumes': des_volumes,
                   'pedidos': pedidos, 'des_pedidos': des_pedidos,
                   'pac': pac, })

def singlepedido(request, pedido_id):
    pedidos = Pedido.objects.filter(id=pedido_id)
    return listpedidos(request, pedidos, "todos")

def listnewtotal(request):
    produtos = Produto.objects.order_by('codigo')
    return render(request, "pedidos/listprodutosnewtotal.html", {'produtos': produtos})

def newtotal(request, codigo):
    lineitems = LineItem.objects.filter(produto__codigo=codigo).order_by('pedido__data')
    produto = get_object_or_404(Produto, codigo=codigo)
    pac = PAC.objects.filter(produto__codigo=codigo)
    toplabel = codigo + " - " + produto.descricao
    pedidos_dict = {}
    pecas_total = {}
    vol_total = {}
    pac_dict = {}
    container_list = []

    for p in list(pac):
        pac_dict[str(p.container)] = p

    containers = Pedido.objects.filter(lineitem__produto__codigo=codigo).values("container").distinct()

    print(type(containers))
    for i in list(containers):
        container_num = str(i['container'])
        container_list.append(container_num)
        pedidos_dict[container_num] = []
        pecas_total[container_num] = 0
        vol_total[container_num] = 0
        # sum pecas and vol
        if container_num == 'None':
            container_lineitems = lineitems.filter(pedido__container=None).order_by('pedido__data')
        else:
            container_lineitems = lineitems.filter(pedido__container=container_num).order_by('pedido__data')
        for lineitem in container_lineitems:
            ###
            if lineitem.unidade[0] == 'p':
                pecas_total[container_num] += lineitem.quantidade
            else:
                vol_total[container_num] += lineitem.quantidade

    for lineitem in list(lineitems):
        pedidos_dict[str(lineitem.pedido.container)].append(lineitem)

    return render(request, "pedidos/newtotal.html",
                  {'toplabel': toplabel, 'pac': pac,
                   'containers': reversed(sorted(container_list)),
                   'lineitems': lineitems,
                   'pedidos_dict': pedidos_dict,
                   'pecas_total': pecas_total, 'vol_total': vol_total,
                   'pac_dict': pac_dict, })

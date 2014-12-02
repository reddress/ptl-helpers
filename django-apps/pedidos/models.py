from django.db import models
from datetime import datetime
# Create your models here.

class Produto(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    descricao = models.CharField(max_length=60)
    def __str__(self):
        return "%s %s" % (self.codigo, self.descricao)

class Vendedor(models.Model):
    nome = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.nome
    
class Cliente(models.Model):
    codigo = models.IntegerField(unique=True)
    nome = models.CharField(max_length=80)
    vendedor = models.ForeignKey(Vendedor)
    def __str__(self):
        return "%d %s (%s)" % (self.codigo, self.nome, self.vendedor)

class Pedido(models.Model):
    data = models.DateTimeField(default=datetime.now)
    # vencimento = models.DateTimeField(null=True, blank=True)
    vencimento = models.DateTimeField(default=datetime.now)
    cliente = models.ForeignKey(Cliente)
    condicoes = models.CharField(max_length=30, default="a vista")
    desconto = models.IntegerField(default=20)
    observacoes = models.CharField(max_length=300)
    container = models.IntegerField(null=True, blank=True)
    extra = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        firstitem = "<sem produtos>"
        anyextra = ""
        lineitems = list(LineItem.objects.filter(pedido__pk=self.id))
        if lineitems:
            lineitem = lineitems[0]
            firstitem = "%s: %s %s" % (lineitem.produto.codigo,
                                       str(lineitem.quantidade),
                                       lineitem.unidade)
        if self.extra:
            anyextra = "[" + self.extra + "]"
        return "%s, %s %s" % (firstitem, self.cliente, anyextra)
    #class Meta:
    #    ordering = ["data"]

class LineItem(models.Model):
    quantidade = models.IntegerField(default=1)
    unidade = models.CharField(max_length=10, default="pç")
    produto = models.ForeignKey(Produto)
    pedido = models.ForeignKey(Pedido)
    def __str__(self):
        return "%d %s %s %s (%s) %s" % (self.quantidade, self.unidade, self.produto.codigo, self.pedido.cliente.nome, self.pedido.cliente.vendedor, self.pedido.extra)
    #class Meta:
    #    ordering = ["pedido__data"]

class PAC(models.Model):
    produto = models.ForeignKey(Produto)
    quantidade = models.IntegerField()
    container = models.IntegerField()
    def __str__(self):
        return "%s - %d pçs (%d)" % (self.produto.codigo, self.quantidade, self.container)

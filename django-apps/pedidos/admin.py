from django.contrib import admin
from django import forms
from pedidos.models import Produto, Vendedor, Cliente, Pedido, LineItem, PAC

class LineItemInline(admin.StackedInline):
    model = LineItem
    extra = 3
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "produto":
            kwargs["queryset"] = Produto.objects.order_by('codigo')
        return super(LineItemInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'data')
    inlines = [LineItemInline]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cliente":
            kwargs["queryset"] = Cliente.objects.order_by('codigo')
        return super(PedidoAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

class PACAdmin(admin.ModelAdmin):
    list_display = ('container', '__str__')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "produto":
            kwargs["queryset"] = Produto.objects.order_by('codigo')
        return super(PACAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)
    
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'vendedor')

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao')

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Vendedor)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(LineItem)
admin.site.register(PAC, PACAdmin)

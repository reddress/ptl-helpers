from django.http import HttpResponse

def home(request):
    return HttpResponse("""
<pre>
<a href="/pedidos/">Pedidos</a>
<a href="/people/">People</a>
</pre>
""")

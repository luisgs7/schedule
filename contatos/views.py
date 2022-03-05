from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from .models import Contato
from django.db.models import Q, Value
from django.db.models.functions import Concat


def index(request):
    contatos = Contato.objects.order_by('-nome').filter(
        mostrar=True
    )
    paginator = Paginator(contatos, 3)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })

def ver_contato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    
    if not contato.mostrar:
        raise Http404()
    
    return render(request, 'contatos/ver_contato.html', {
        'contato': contato
    })

def busca(request):
    termo = request.GET.get('termo')

    if termo is None or not termo:
        contatos = Contato.objects.all()

        paginator = Paginator(contatos, 4)

        page = request.GET.get('p')
        contatos = paginator.get_page(page)

        return render(request, 'contatos/busca.html', {
            'contatos': contatos
        })
    
    campos = Concat('nome', Value(' '), 'sobrenome',)

    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
    )
    
    #print(contatos.query)
    paginator = Paginator(contatos, 3)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })

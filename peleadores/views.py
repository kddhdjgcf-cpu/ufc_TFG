from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Peleador
import re
from django.core.paginator import Paginator
from django.utils.http import urlencode
from django.conf import settings
import requests
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from .decorators import editor_required
from .forms import PeleadorForm
from django.contrib.auth.decorators import login_required




@login_required
def index(request):
    puede_editar = request.user.is_superuser or request.user.groups.filter(name="Editor").exists()
    return render(request, "principal/principal.html", {"puede_editar": puede_editar})

@login_required
def lista_peleadores(request):
    peleadores = Peleador.objects.all()  # trae todos los peleadores de la base de datos

    nombre2 = request.GET.get('nombre2')
    if nombre2:  # Solo filtramos si el usuario escribió algo
        peleadores = peleadores.filter(nombre__icontains=nombre2)


    peso_min = request.GET.get('peso_min')
    peso_max = request.GET.get('peso_max')

    def extraer_numero(peso_str):
        """Extrae solo los números de la cadena"""
        if peso_str:
            numero= re.search(r'\d+',peso_str)
            if numero:
                return int(numero.group())
        return None
    
    peso_min_val = extraer_numero(peso_min)
    peso_max_val = extraer_numero(peso_max)

    if peso_min_val is not None:
        peleadores = peleadores.filter(peso__gte=peso_min_val)
    if peso_max_val is not None:
        peleadores = peleadores.filter(peso__lte=peso_max_val)


    # ---------- PAGINACIÓN ----------
    paginator = Paginator(peleadores, 12)  # peleadores por página
    page_number = request.GET.get('page')  # página actual
    page_obj = paginator.get_page(page_number)  # devuelve solo los peleadores de esa página

    query_params = {}
    if nombre2:
        query_params['nombre2'] = nombre2
    if peso_min:
        query_params['peso_min'] = peso_min
    if peso_max:
        query_params['peso_max'] = peso_max

    querystring = '&'.join([f'{k}={v}' for k,v in query_params.items()]) #esta línea convierte un diccionario de parámetros en un query string de URL, listo para usar en enlaces.

    context = {
        'page_obj': page_obj,
        'querystring': querystring,
    }

    return render(request, 'peleadores/lista.html', context)

@login_required
def detalle_peleador(request, id):
    peleador = get_object_or_404(Peleador, id=id)

    # Variable booleana para el template
    puede_editar = request.user.is_superuser or request.user.groups.filter(name__iexact="Editor").exists()

    return render(request, 'peleadores/detalle.html', {
        'peleador': peleador,
        'puede_editar': puede_editar
    })

@login_required
def comparar_peleadores(request):
    # Peleadores seleccionados (por ids)
    peleadores_seleccionados = Peleador.objects.filter(id__in=request.GET.getlist('ids'))

    # Todos los peleadores para el select
    todos_peleadores = Peleador.objects.all()

    context = {
        'peleadores': peleadores_seleccionados,
        'todos_peleadores': todos_peleadores,
    }
    return render(request, 'peleadores/comparar_peleadores.html', context)

@login_required
def ufc_noticias(request):
    api_key = settings.NEWS_API_KEY
    url = f"https://newsapi.org/v2/everything?q=UFC&sortBy=publishedAt&apiKey={api_key}"

    
    response = requests.get(url)
    data = response.json()
    
    articulos = data.get("articles", [])
    
    return render(request, "peleadores/ufc_noticias.html", {"articulos": articulos})

@login_required
def estadisticas(request):
    peleadores = Peleador.objects.all()

    # --- Calculos ---
    total_peleadores = peleadores.count()
    promedio_victorias = peleadores.aggregate(Avg('victorias'))['victorias__avg'] or 0
    promedio_derrotas = peleadores.aggregate(Avg('derrotas'))['derrotas__avg'] or 0
    promedio_edad = peleadores.aggregate(Avg('edad'))['edad__avg'] or 0

    # Ranking: top 10 peleadores con mas victorias
    top_victorias = peleadores.order_by('-victorias')[:10]

    # Ranking: top 10 peleadores con más golpes por minuto
    top_golpes_minuto= peleadores.order_by('-golpes_por_minuto')[:10]

    context = {
        'total_peleadores': total_peleadores,
        'promedio_victorias': round(promedio_victorias, 2),
        'promedio_derrotas': round(promedio_derrotas, 2),
        'promedio_edad': round(promedio_edad, 2),
        'top_victorias': top_victorias,
        'top_golpes_minuto': top_golpes_minuto,
    }

    return render(request, 'peleadores/estadisticas.html', context)

@login_required
def ufc_eventos(request):
    # API para próximos eventos
    url_next = "https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=4497"

    # API para eventos pasados
    url_past = "https://www.thesportsdb.com/api/v1/json/3/eventspastleague.php?id=4497"

    eventos_proximos = []
    eventos_pasados = []

    try:
        r1 = requests.get(url_next)
        eventos_proximos = r1.json().get("events", [])

        r2 = requests.get(url_past)
        eventos_pasados = r2.json().get("events", [])

    except Exception as e:
        print("Error cargando eventos:", e)

    return render(request, "peleadores/ufc_eventos.html", {
        "eventos_proximos": eventos_proximos,
        "eventos_pasados": eventos_pasados
    })

@login_required
@editor_required
def crear_peleador(request):
    form = PeleadorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("lista_peleadores")
    return render(request, "peleadores/form_peleador.html", {"form": form})


@login_required
@editor_required
def editar_peleador(request, id):
    peleador = get_object_or_404(Peleador, id=id)
    form = PeleadorForm(request.POST or None, instance=peleador)
    if form.is_valid():
        form.save()
        return redirect("detalle_peleador", id=peleador.id)
    return render(request, "peleadores/form_peleador.html", {"form": form})


@login_required
@editor_required
def eliminar_peleador(request, id):
    peleador = get_object_or_404(Peleador, id=id)
    peleador.delete()
    return redirect("lista_peleadores")

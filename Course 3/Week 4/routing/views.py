from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST


@require_GET
def simple_route(request):
    return HttpResponse(status=200)


def slug_route(request, body):
    return HttpResponse(content=body)


def sum_route(request, a, b):
    return HttpResponse(content=int(a)+int(b))


@require_GET
def sum_get_method(request):
    try:
        return HttpResponse(content=int(request.GET.get('a'))+int(request.GET.get('b')), status=200)
    except:
        return HttpResponse(status=400)


@require_POST
def sum_post_method(request):
    try:
        return HttpResponse(content=int(request.POST.get('a'))+int(request.POST.get('b')), status=200)
    except:
        return HttpResponse(status=400)

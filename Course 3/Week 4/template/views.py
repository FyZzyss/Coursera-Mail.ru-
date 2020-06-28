from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def echo(request):
    data = None
    if request.method == 'GET':
        data = request.GET
    elif request.method == 'POST':
        data = request.POST
    meta = request.META.get('HTTP_X_PRINT_STATEMENT', None)
    return render(request, 'echo.html', {'data': data, 'method': request.method.lower(), 'meta': meta})


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })

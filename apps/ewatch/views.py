from django.http import HttpResponse

def index(request):
    output = 'FART FART'
    return HttpResponse(output)

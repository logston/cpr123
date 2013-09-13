from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def main_page(request):
    return render_to_response('ewatch/index.html')

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect(reverse('apps.ewatch.views.index'))
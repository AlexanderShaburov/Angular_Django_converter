from django.shortcuts import render
from django.middleware.csrf import get_token
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)
# Create your views here.




def homepage(request):
    
    return render(
        request=request,
        template_name='index.html',
    )
def provide_token(request):
    
    token = get_token(request)
    response = JsonResponse({'csrfToken': token})
    response["Access-Control-Allow-Origin"] = "https://localhost:4200"
    response["Access-Control-Allow-Credentials"] = "true"
    response.set_cookie(
        'csrftoken',
        value=token,
        domain='127.0.0.1',  
        path='/',
        httponly=False,
        secure=False,
        samesite='None',
    )
    print('csrf token: ', token)
    return response
    
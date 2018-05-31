from django.shortcuts import render
from django.http import HttpResponse
import rsa


def testrsa(request):
    (public_key,private_key)=rsa.newkeys(512)
    return render(request, template_name='testrsa/testrsa.html', context={
        'public_key': public_key,
    })

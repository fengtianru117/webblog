from django.shortcuts import render
from .models import PrivateKey
from django.http import HttpResponse
import rsa


def testrsa(request):
    if request.method == 'GET':
        (public_key, private_key) = rsa.newkeys(512)
        key = PrivateKey(
            n=private_key.n,
            e=private_key.e,
            d=private_key.d,
            p=private_key.p,
            q=private_key.q,
        )
        key.save()
        return render(request, template_name='testrsa/testrsa.html', context={
            'public_key': public_key,
        })
    '''
    elif request.method == 'POST':
        crypto = request.POST.get('crypto')
        k = PrivateKey.objects.last()
        priv_key = rsa.PrivateKey(int(k.n), int(k.e), int(k.d), int(k.p), int(k.q))
        # ddd = rsa.decrypt(crypto, priv_key)
        return render(request, 'testrsa/test.html', context={
            'message': crypto,
        })
        '''


def encrypt(request):
    if request.method == 'POST':
        message = request.POST.get('message').encode('utf8')
        n = int(request.POST.get('N'))
        e = int(request.POST.get('E'))
        pub_key = rsa.PublicKey(n, e)
        k = PrivateKey.objects.last()
        priv_key = rsa.PrivateKey(int(k.n), int(k.e), int(k.d), int(k.p), int(k.q))
        crypto = rsa.encrypt(message, pub_key)  # crypto is a bytes tpye
        message = rsa.decrypt(crypto, priv_key).decode('utf8')
        return render(request, 'testrsa/encrypt.html', context={
            'crypto': crypto,
            'message': message,
        })
    else:
        return render(request, 'testrsa/encrypt.html', context={})

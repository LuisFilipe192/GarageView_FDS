from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Anuncio
from django.db import models
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse

class ProfileView(View):
    def get(self, request):
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        q = request.GET.get('q', '')
        return render(request, 'forum/perfil.html', {'min_price': min_price, 'max_price': max_price, 'q': q, 'request': request})
from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Anuncio
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse

class MainView(View):
    def get(self, request):
        anuncios = Anuncio.objects.order_by('-data_criacao')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        q = request.GET.get('q', '').strip()
        try:
            if min_price:
                anuncios = anuncios.filter(preco__gte=min_price)
            if max_price:
                anuncios = anuncios.filter(preco__lte=max_price)
        except Exception:
            pass
        if q:
            anuncios = anuncios.filter(
                models.Q(titulo__icontains=q) | models.Q(descricao__icontains=q)
            )
        contexto = {'anuncios': anuncios, 'min_price': min_price or '', 'max_price': max_price or '', 'q': q, 'request': request}
        return render(request, 'forum/index.html', contexto)

class AdDetailView(View):
    def get(self, request, ad_id):
        try:
            ad = Anuncio.objects.get(pk=ad_id)
        except Anuncio.DoesNotExist:
            raise Http404('Anúncio inexistente')
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        q = request.GET.get('q', '')
        contexto = {'ad': ad, 'min_price': min_price, 'max_price': max_price, 'q': q, 'request': request}
        return render(request, 'forum/ad_detail.html', contexto)

class CreateAdView(View):
    def get(self, request):
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        q = request.GET.get('q', '')
        return render(request, 'forum/create_ad.html', {'min_price': min_price, 'max_price': max_price, 'q': q, 'request': request})

    def post(self, request):
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        preco_str = request.POST.get('preco')
        preco = Decimal(preco_str.replace(',', '.')) if preco_str else Decimal(0)
        imagem_url = request.POST.get('imagem_url')
        vendedor = request.user.username if request.user.is_authenticated else request.POST.get('vendedor') or 'anônimo'
        contato = request.POST.get('contato')

        ad = Anuncio(titulo=titulo, descricao=descricao, preco=preco, imagem_url=imagem_url, vendedor=vendedor, contato=contato)
        ad.save()
        if request.POST.get('next') == 'novo':
            return redirect(reverse('forum:ad_create'))
        return redirect(reverse('forum:ad_detail', args=[ad.id]))

class SellerAdsView(View):
    def get(self, request):
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        q = request.GET.get('q', '')
        if request.user.is_authenticated:
            vendedor = request.user.username
            anuncios = Anuncio.objects.filter(vendedor=vendedor).order_by('-data_criacao')
            return render(request, 'forum/seller_ads.html', {'anuncios': anuncios, 'vendedor': vendedor, 'min_price': min_price, 'max_price': max_price, 'q': q, 'request': request})
        return render(request, 'forum/seller_ads.html', {'anuncios': [], 'vendedor': None, 'min_price': min_price, 'max_price': max_price, 'q': q, 'request': request})

class EditAdView(View):
    def get(self, request, ad_id):
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')
        q = request.GET.get('q', '')
        try:
            ad = Anuncio.objects.get(pk=ad_id)
        except Anuncio.DoesNotExist:
            raise Http404('Anúncio inexistente')
        return render(request, 'forum/edit_ad.html', {'ad': ad, 'min_price': min_price, 'max_price': max_price, 'q': q, 'request': request})

    def post(self, request, ad_id):
        try:
            ad = Anuncio.objects.get(pk=ad_id)
        except Anuncio.DoesNotExist:
            raise Http404('Anúncio inexistente')
        ad.titulo = request.POST.get('titulo')
        ad.descricao = request.POST.get('descricao')
        preco_str = request.POST.get('preco')
        if preco_str:
            ad.preco = Decimal(preco_str.replace(',', '.'))
        ad.imagem_url = request.POST.get('imagem_url')
        ad.vendedor = request.POST.get('vendedor') or ad.vendedor
        ad.contato = request.POST.get('contato')
        ad.save()
        return redirect(reverse('forum:ad_detail', args=[ad.id]))

class DeleteAdView(View):
    def post(self, request, ad_id):
        try:
            ad = Anuncio.objects.get(pk=ad_id)
        except Anuncio.DoesNotExist:
            raise Http404('Anúncio inexistente')
        ad.delete()
        return redirect(reverse('forum:index'))

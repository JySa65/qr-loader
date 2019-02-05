from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView, View, DetailView
from django.core import serializers
from app import models
# Create your views here.


class HomeView(TemplateView):
    template_name = "app/home.html"


class ScanQrCode(View):
    model = models.User
    second_model = models.TokenQr

    def get(self, request, *args, **kwargs):
        r_token = request.GET.get('token')
        try:
            token = self.second_model.objects.get(token=r_token)
            user = self.model.objects.filter(token=token).first()
            if (not user):
                data = dict(
                    status=True,
                    msg="Este Qr No Tiene Usuario Registrado",
                    data=dict(
                        token=token.token,
                        type=False
                    )
                )
                return JsonResponse(data)
            data = dict(
                status=True,
                msg="Usuario Encontrado",
                data=dict(
                    user=serializers.serialize("json", [user, ]),
                    token=user.token.token,
                    type=True
                )
            )
            return JsonResponse(data, safe=False)
        except Exception as e:
            print(e)
            data = dict(
                status=False,
                msg='No Existe El Qr Indicado'
            )
            return JsonResponse(data)


class UserDetailView(DetailView):
    model = models.User

    def get_object(self):
        token = self.kwargs.get('token')
        object = get_object_or_404(self.model, token__token=token)
        return object

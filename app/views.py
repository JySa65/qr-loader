from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.views.generic import TemplateView, View, DetailView, \
    CreateView, ListView, UpdateView, DeleteView
from django.core import serializers
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from app import models, forms
# Create your views here.


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "app/home.html"


class ScanQrCode(LoginRequiredMixin, View):
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


class UserDetailView(LoginRequiredMixin, DetailView):
    model = models.User

    def get_object(self):
        token = self.kwargs.get('token')
        object = get_object_or_404(self.model, token__token=token)
        return object


class UserCreateView(LoginRequiredMixin, CreateView):
    model = models.User
    form_class = forms.UserForm

    def form_valid(self, form):
        token = get_object_or_404(
            models.TokenQr, token=self.kwargs.get('token'))
        _object = form.save(commit=False)
        _object.token = token
        self.object = _object.save()
        return super(UserCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('app:user_detail', args=(self.object.token.token,))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = models.User
    form_class = forms.UserForm

    def get_object(self):
        object = self.model.objects.filter(
            pk=self.kwargs.get('pk'),
            token__token=self.kwargs.get('token')).first()
        if (object == None):
            raise Http404
        return object

    def form_valid(self, form):
        token = get_object_or_404(
            models.TokenQr, token=self.kwargs.get('token'))
        _object = form.save(commit=False)
        _object.token = token
        self.object = _object.save()
        return super(UserUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('app:user_detail', args=(self.object.token.token,))


class TokenQrCreateView(LoginRequiredMixin, CreateView):
    model = models.TokenQr
    form_class = forms.TokenQrForm
    template_name = 'app/home.html'

    def get_success_url(self):
        return reverse_lazy('app:token_detail', args=(self.object.pk,))


class TokenQrDetailView(LoginRequiredMixin, DetailView):
    model = models.TokenQr

    def get_context_data(self, **kwargs):
        context = super(TokenQrDetailView, self).get_context_data(**kwargs)
        context['user'] = models.User.objects.filter(token=self.object).first()
        return context


class UserListView(LoginRequiredMixin, ListView):
    model = models.User
    paginate_by = 10


class TokenQrListView(LoginRequiredMixin, ListView):
    model = models.TokenQr
    paginate_by = 10


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = models.User

    def get_object(self):
        object = self.model.objects.filter(
            pk=self.kwargs.get('pk'),
            token__token=self.kwargs.get('token')).first()
        if (object == None):
            raise Http404
        return object


    def post(self, *args, **kwargs):
        self.get_object().token.delete()
        return HttpResponseRedirect(reverse_lazy('app:user_list'))

class TokenQrDeleteView(LoginRequiredMixin, DeleteView):
    model = models.TokenQr
    success_url = reverse_lazy('app:token_list')

    def get_context_data(self, **kwargs):
        context = super(TokenQrDeleteView, self).get_context_data(**kwargs)
        context['user'] = models.User.objects.filter(token=self.object).first()
        return context

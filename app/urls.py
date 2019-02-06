from django.urls import path, include
from app.views import HomeView, ScanQrCode, \
    UserDetailView, UserCreateView, UserListView, UserUpdateView, UserDeleteView, \
    TokenQrCreateView, TokenQrDetailView, TokenQrListView, TokenQrDeleteView
app_name = "app"

urlpatterns = [
    path('scan-qr/', ScanQrCode.as_view(), name="scan-qr"),

    # user

    path('user/', UserListView.as_view(), name="user_list"),
    path('user/detail/<token>/', UserDetailView.as_view(), name="user_detail"),
    path('user/create/<token>/', UserCreateView.as_view(), name="user_create"),
    path('user/update/<pk>/<token>/',
         UserUpdateView.as_view(), name="user_update"),
    path('user/delete/<pk>/<token>/',
         UserDeleteView.as_view(), name="user_delete"),

    # token
    path('token/', TokenQrListView.as_view(), name="token_list"),
    path('', TokenQrCreateView.as_view(), name="token_create"),
    path('token/detail/<pk>/', TokenQrDetailView.as_view(), name="token_detail"),
    path('token/delete/<pk>/', TokenQrDeleteView.as_view(), name="token_delete"),
]

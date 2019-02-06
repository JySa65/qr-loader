from django.urls import path
from app.views import HomeView, ScanQrCode, \
                    UserDetailView, UserCreateView, UserListView, UserUpdateView, \
                    TokenQrCreateView, TokenQrDetailView, TokenQrListView
app_name = "app"

urlpatterns = [
    # path('', HomeView.as_view(), name="home"),
    path('scan-qr/', ScanQrCode.as_view(), name="scan-qr"),
    
    #user
    
    path('user/', UserListView.as_view(), name="user_list"),
    path('user/detail/<token>/', UserDetailView.as_view(), name="user_detail"),
    path('user/create/<token>/', UserCreateView.as_view(), name="user_create"),
    path('user/update/<pk>/<token>/',
         UserUpdateView.as_view(), name="user_update"),
    
    #token
    path('token/', TokenQrListView.as_view(), name="token_list"),
    path('', TokenQrCreateView.as_view(), name="token_create"),
    path('token/detail/<pk>/', TokenQrDetailView.as_view(), name="token_detail"),
]

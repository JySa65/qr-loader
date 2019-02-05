from django.urls import path
from app.views import HomeView, ScanQrCode, UserDetailView
app_name = "app"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('scan-qr/', ScanQrCode.as_view(), name="scan-qr"),
    path('user/detail/<token>/', UserDetailView.as_view(), name="user_detail"),
]

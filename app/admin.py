from django.contrib import admin
from app.models import User, TokenQr
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('ci', 'name', 'last_name')
    readonly_fields = ('created_at', 'updated_at',)
    empty_value_display = 'No Disponible'
    ordering = ('ci', 'created_at')
    search_fields = ('email', 'ci')


@admin.register(TokenQr)
class TokenQrAdmin(admin.ModelAdmin):
    list_display = ('token', 'user', 'get_img_qr')

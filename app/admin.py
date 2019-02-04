from django.contrib import admin
from django.http import HttpResponse
from app.models import User, TokenQr
from django.utils.html import format_html
from django.urls import reverse
from django.urls import path
from django.template.response import TemplateResponse
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
    list_display = ('qrcode_link', 'token', 'getUser',
                    'is_active', 'qrcode_table',)
    readonly_fields = ('token', 'created_at', 'updated_at',
                       'qrcode_table', 'is_active')
    fieldsets = (
        ('Info', {
            'fields': ('token', 'is_active')
        }),
        ('Date', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def getUser(self, obj):
        try:
            user = User.objects.get(token=obj)
            return user.get_full_name()
        except Exception:
            return 'No Hay Persona'
    getUser.short_description = "Usuario"

    def get_urls(self):
        urls = [
            path('<pk>/config/', self.admin_site.admin_view(self.config_view),
                 name='qr_config'),
            path('<pk>/qrcode/', self.admin_site.admin_view(self.qrcode_view),
                 name='qr_code'),
        ] + super(TokenQrAdmin, self).get_urls()

        return urls

    def config_view(self, request, pk):
        token = TokenQr.objects.get(pk=pk)
        try:
            user = User.objects.get(token=token)
        except Exception:
            user = ''

        context = dict(
            self.admin_site.each_context(request),
            token=token,
            user=user
        )

        return TemplateResponse(request, 'admin/qr_template.html', context)

    def qrcode_view(self, request, pk):
        token = TokenQr.objects.get(pk=pk)

        try:
            import qrcode
            import qrcode.image.svg
            qr = qrcode.QRCode(
                version=5,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            qr.add_data(token.token)
            qr.make(fit=True)

            img = qr.make_image(
                fill_color="black", back_color="white", image_factory=qrcode.image.svg.SvgImage)
            response = HttpResponse(content_type='image/svg+xml')
            img.save(response)
        except ImportError:
            response = HttpResponse('', status=503)

        return response

    def qrcode_table(self, obj):
        try:
            href = reverse('admin:qr_code',
                           kwargs={'pk': obj.pk})
            link = format_html('<img src="{}" >', href)

        except Exception:
            link = ''

        return link
    qrcode_table.short_description = "QR Code"

    def qrcode_link(self, obj):
        try:
            href = reverse('admin:qr_config',
                           kwargs={'pk': obj.pk})
            link = format_html('<a href="{}">Ver Qr</a>', href)

        except Exception:
            link = ''

        return link
    qrcode_link.short_description = "Ver Qr"

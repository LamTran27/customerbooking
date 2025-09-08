from django.contrib import admin
from .models import Customer
from .forms import CustomerForm
from .models import Pictures
from .forms import PicturesForm
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserAccount

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    list_display = ('name', 'plate', 'KHDV', 'CVDV', 'adddate', 'isdelete')
    list_filter = ('isdelete', 'KHDV', 'CVDV')
    search_fields = ('name', 'plate')
    readonly_fields = ('lastupdatedate', 'deletedate')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-adddate')  # Sắp xếp mới nhất lên đầu
    
@admin.register(Pictures)
class PicturesAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.PictureName:
            return format_html('<img src="{}" style="max-height:100px;"/>', obj.PictureName.url)
        return "-"
    image_tag.short_description = 'Preview'
    form = PicturesForm
    list_display = ('id', 'pictureName', 'adddate', 'isDeleted', 'lastupdateuserid', 'lastUpdateDate')
    list_filter = ('isDeleted',)
    readonly_fields = ('lastUpdateDate',)
    search_fields = ('id',)

from django.contrib import admin
from .models import UserAccount

class UserAccountInline(admin.StackedInline):
    model = UserAccount
    can_delete = False
    verbose_name_plural = 'Thông tin mở rộng'
    fk_name = 'user'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserAccountInline,)
    list_display = ('username', 'email', 'get_hotline','get_store', 'get_isadmin', 'get_adddate', 'is_staff', 'is_superuser')

    def get_hotline(self, obj):
        return obj.account.hotline if hasattr(obj, 'account') else '-'
    get_hotline.short_description = 'Hotline'

    def get_store(self, obj):
        return obj.account.store if hasattr(obj, 'account') else '-'
    get_hotline.short_description = 'Store'

    def get_isadmin(self, obj):
        return obj.account.isadmin if hasattr(obj, 'account') else False
    get_isadmin.boolean = True
    get_isadmin.short_description = 'Là Admin'

    def get_adddate(self, obj):
        return obj.account.adddate.strftime('%d/%m/%Y %H:%M') if hasattr(obj, 'account') else '-'
    get_adddate.short_description = 'Ngày tạo'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

    


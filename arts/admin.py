from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Arts, Like
# Register your models here.

class ArtsAdmin(admin.ModelAdmin):
    list_display = ('photo_image','author')
    #"photo_image"を追加
    
    #以下、photo_imageの定義を追加する。サイズ等の設定は自由です。
    def photo_image(self, obj):
        return mark_safe('<img src="{}" style="width:200px; height:auto;">'.format(obj.image.url))


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'art')


admin.site.register(Arts, ArtsAdmin)
admin.site.register(Like, LikeAdmin)
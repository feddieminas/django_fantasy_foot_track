from django.contrib import admin
from .models import Influence, Comment, UpVote, Likeability

# Register your models here.
class InfluenceAdmin(admin.ModelAdmin):
    exclude = ('views',)

admin.site.register(Influence, InfluenceAdmin)
admin.site.register(Comment)
admin.site.register(UpVote)
admin.site.register(Likeability)
    
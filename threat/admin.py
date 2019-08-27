from django.contrib import admin
from .models import Threat, Comment, UpVote, Likeability

# Register your models here.
class ThreatAdmin(admin.ModelAdmin):
    exclude = ('views',)

admin.site.register(Threat, ThreatAdmin)
admin.site.register(Comment)
admin.site.register(UpVote)
admin.site.register(Likeability)
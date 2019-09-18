from django.contrib import admin
from .models import Creativity, Comment, UpVote, Likeability

class CreativityAdmin(admin.ModelAdmin):
    exclude = ('views',)

admin.site.register(Creativity, CreativityAdmin)
admin.site.register(Comment)
admin.site.register(UpVote)
admin.site.register(Likeability)

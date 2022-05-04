from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(AudioBook)
admin.site.register(Language)
admin.site.register(HistoryAudioBook)
admin.site.register(HistoryBook)
admin.site.register(Client)
admin.site.register(ReytingAudioBook)
admin.site.register(ReytingBook)


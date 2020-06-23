from django.contrib import admin
from .models import LikedVideos
from .models import SearchQuery
from .models import CacheResult


admin.site.register(LikedVideos)
admin.site.register(SearchQuery)
admin.site.register(CacheResult)

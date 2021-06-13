"""
Admin module. Register models here.
"""

from django.contrib import admin
from .models import ShowToWatch, ShowFullWatched


admin.site.register(ShowToWatch)
admin.site.register(ShowFullWatched)

"""
Admin module. Register models here.
"""

from django.contrib import admin
from .models import LaterWatchShow, FullWatchedShow


admin.site.register(LaterWatchShow)
admin.site.register(FullWatchedShow)

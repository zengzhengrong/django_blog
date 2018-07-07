from django.contrib import admin
from django.forms import ModelForm
from suit.widgets import SuitSplitDateTimeWidget
from .models import OnlineStatus

class OnlineStatusform(ModelForm):
    class Meta:
        widgets = {
            'last_login':SuitSplitDateTimeWidget
            }
class OnlineStatusAdmin(admin.ModelAdmin):
    form = OnlineStatusform
    class Meta:
        model = OnlineStatus
# Register your models here.

admin.site.register(OnlineStatus,OnlineStatusAdmin)
from django.contrib import admin
from .models import *


admin.site.register(Question)
admin.site.register(Test)
admin.site.register(Options)
admin.site.register(Answer)
admin.site.register(Statistics)


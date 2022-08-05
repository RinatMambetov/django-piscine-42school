from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
	readonly_fields = ('created',)	#для отображения в админке ридонли полей


admin.site.register(Todo, TodoAdmin)

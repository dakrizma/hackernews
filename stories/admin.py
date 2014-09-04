from django.contrib import admin
from stories.models import Story

class StoryAdmin(admin.ModelAdmin):		# definiramo izgled admin stranice
	list_display = ('__str__', 'domain', 'moderator', 'points', 'creatd_at', 'updatd_at')
	list_filter = ('created_at', 'updated_at')
	search_fields = ('title', 'moderator__username', 'moderator__first_name')

	fieldsets = [									# definiramo polja
		('Story', {									# 1. polje se zove Story
			'fields': ('title', 'url', 'points')
		}),
		('Moderator', {
			'classes': ('grp-collapse grp-closed'),		# 2. polje se može collapsati - postavljeno je kao otvoreno
			'fields': ('moderator',)
		}),
		('Change history', {
			'classes': ('collapse',),				# 3. polje se može collapsati
			'fields': ('creatd_at', 'updatd_at')
		})
	]
	readonly_fields = ('creatd_at', 'updatd_at')	# ove datume ne možemo mijenjati

	def creatd_at(self, obj):
		return obj.created_at.strftime("%e.%m.%Y. %H:%M")
	creatd_at.short_description = 'created at'
	
	def updatd_at(self, obj):
		return obj.updated_at.strftime("%e.%m.%Y. %H:%M")
	updatd_at.short_description = 'updated at'
	
admin.site.register(Story, StoryAdmin)	# admin stranice
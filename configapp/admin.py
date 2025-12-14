from django.contrib import admin
from .models import ContactInfo, ContactMessage, PortfolioItem, Service, Skill, Home, About, ResumeEntry


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
	list_display = ('address','phone','email')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ('name','email','subject','created_at')
	readonly_fields = ('name','email','subject','message','created_at')

# register other content models for convenience
admin.site.register(PortfolioItem)
admin.site.register(Service)
admin.site.register(Skill)
admin.site.register(Home)
admin.site.register(About)
admin.site.register(ResumeEntry)

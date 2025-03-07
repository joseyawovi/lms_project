from django.contrib import admin
from .models import Categories, Author,Course,Level, What_you_learn, Requirements,Video,Lesson

# Register your models here.
class What_you_learn_TabularInline(admin.TabularInline):
    model =What_you_learn

class Requirements_TabularInline(admin.TabularInline):
    model =Requirements
    
class Video_TabularInline(admin.TabularInline):
    model =Video

class Course_admin(admin.ModelAdmin):
    inlines =(What_you_learn_TabularInline,Requirements_TabularInline,Video_TabularInline)



admin.site.register(Categories)
admin.site.register(Course,Course_admin)
admin.site.register(Author)
admin.site.register(Level)
admin.site.register(What_you_learn)
admin.site.register(Requirements)
admin.site.register(Video)
admin.site.register(Lesson)

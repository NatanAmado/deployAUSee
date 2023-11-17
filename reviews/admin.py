from django.contrib import admin
from .models import Course, Review

class ReviewInline(admin.TabularInline):  
    model = Review
    extra = 0  # Number of empty forms to display; set to 0 to only show existing reviews

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'level')
    list_filter = ('level', )
    search_fields = ('name', 'code')
    inlines = [ReviewInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'rating', 'text', 'created_date')
    list_filter = ('course', 'rating', 'created_date')
    search_fields = ('text', 'course__name')



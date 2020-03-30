from typing import List

from django.contrib import admin


from product.models import Category, Activity, Trip, ImageTrip, ImageActivity


class TripImageInline(admin.TabularInline):
    model = ImageTrip
    extra = 5


class ActivityImageInline(admin.TabularInline):
    model = ImageActivity
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    # admin ekraninda status ve title i gosterir 07 tutorial
    list_display = ['title', 'status', 'image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status']


class ActivityAdmin(admin.ModelAdmin):
    # admin ekraninda status ve title i gosterir 07 tutorial
    list_display = ['title', 'category', 'image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [ActivityImageInline]


class TripAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [TripImageInline]


class ImageTripAdmin(admin.ModelAdmin):
    list_display = ['title', 'trip', 'image']


class ImageActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity', 'image']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(ImageTrip, ImageTripAdmin)
admin.site.register(ImageActivity, ImageActivityAdmin)

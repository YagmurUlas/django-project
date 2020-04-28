from typing import List

from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from product.models import Category, Activity, Product, Images, ImageActivity, Comment


class TripImageInline(admin.TabularInline):
    model = Images
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


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [TripImageInline]
    prepopulated_fields = {'slug': ('title',)}


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'image']


class ImageActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity', 'image']


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'product','user', 'status']
    list_filter = ['status']



admin.site.register(Category, CategoryAdmin2)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Comment, CommentAdmin)

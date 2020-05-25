from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, TextInput, Select, FileInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True', 'Yes'),
        ('False', 'No'),
    )
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    # category tree belirtmek icin trip >> summer season gibi
    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' > ' .join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = "Image"

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

class Menu(MPTTModel):
    STATUS = (
        ('True', 'Yes'),
        ('False', 'No'),
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMETA:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' > ' .join(full_path[::-1])

TYPE = (
    ('Travel', 'Travel'),
    ('Activity', 'Activity'),
    ('Menu', 'Menu'),

)
STATUS = (
    ('True', 'Yes'),
    ('False', 'No'),
)

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE,null=True)
    type = models.CharField(max_length=10, choices=TYPE, default="Category")
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField(null=True)
    person_number = models.IntegerField(blank=True, null=True)
    day_number = models.IntegerField(blank=True, null=True)
    shortDetail = RichTextUploadingField(max_length=1400)
    detail = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = "Image"

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

class ContentForm(ModelForm):
    class Meta:
        model = Product
        fields=['type','title','slug','keywords','description','image','detail']
        widgets = {
            'title': TextInput(attrs={'class':'form-control','placeholder':'title',}),
            'slug' : TextInput(attrs={'class': 'form-control', 'placeholder': 'slug', }),
            'keywords': TextInput(attrs={'class': 'form-control', 'placeholder': 'keywords', }),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'description', }),
            'type': Select(attrs={'class': 'form-control', 'placeholder': 'city'}, choices=TYPE),
            'image': FileInput(attrs={'class': 'form-control', 'placeholder': 'image', }),
            'detail': CKEditorWidget(),

        }

class Images(models.Model):
    content = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = "Image"

class ContentImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title','image']


class Comment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Yes'),
        ('False', 'No'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.TextField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment']

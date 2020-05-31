from django.db import models
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField

# Create your models here.

class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, unique=True)
    content = models.TextField()
    # content = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)



# class MyImage(models.Model):
#     file = models.FileField()
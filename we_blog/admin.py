from doctest import OutputChecker
from django.contrib import admin
from we_blog.models import OurBlog

# Register your models here.

admin.site.register(OurBlog)
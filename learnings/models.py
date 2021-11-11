from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.

class Category(models.Model):
    
    Category_Name = (
        ('Crime', 'Crime'),
        ('Fantacy', 'Fantacy'),
        ('Horror', 'Horror'),
        ('Romance', 'Romance'),
        ('Thriller', 'Thriller'),
        ('True Story', 'True Story')
    )
    category  =  models.CharField(max_length=100,choices=Category_Name)

    class  Meta: 
        verbose_name_plural  =  "Categories" 
        
    def  __str__(self):
        return  self.category
    
class Publisher(models.Model):
    publisher_name  =  models.CharField(max_length=100)
    publish_date  =  models.DateField

    def  __str__(self):
        return  self.publisher_name

class Author(models.Model):
    Gender_Choice=(
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Other', 'Other')
    )
    name  =  models.CharField(max_length=100)
    gender  =  models.CharField(max_length=100,choices=Gender_Choice)
    country  =  models.CharField(max_length=100)

    author_pic = models.ImageField(upload_to='images/', null=True)

    def  image_tag(self):
        if self.author_pic != None:
            return mark_safe('<img src="/../../media/%s" width="100" height="100" />' % (self.author_pic))
        else:
            return mark_safe('<img src="/../../media/images/No.png" width="90" height="90" />')
            

    image_tag.allow_tags = True 

    def  __str__(self):
        return  self.name

class Details(models.Model):
    book_name  =  models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pages = models.IntegerField(default=1)
    publisher  =  models.ForeignKey(Publisher, on_delete=models.CASCADE)
    Author  =  models.ForeignKey(Author, on_delete=models.CASCADE)

    class  Meta:
        verbose_name_plural  =  "Details"

    def  __str__(self):
        return  self.book_name
    

from pyexpat import model
from unicodedata import category
from django.db import models
from ckeditor.fields import RichTextField
# from .app.models import MainCategory
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.


class Slider(models.Model):
    DISCOUNT_DEAL = (
        ('HOT DEALS', 'HOT DEALS'),
        ('New Arraivels', 'New Arraivels'),
    )

    Image = models.ImageField(upload_to='media/slider_imgs')
    Discount_Deal = models.CharField(choices=DISCOUNT_DEAL, max_length=100)
    SALE = models.IntegerField()
    Brand_Name = models.CharField(max_length=200)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=200)

    def __str__(self):
        # return self.Brand_Name
        return str(self.Brand_Name)


class BannerArea(models.Model):
    Image = models.ImageField(upload_to='media/banner_imgs')
    Discount_details = models.CharField(max_length=100)
    Quote = models.CharField(max_length=100)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=200, null=True, default='/')

    def __str__(self):
        return str(self.Quote)


class MainCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Category(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(str(self.name) + " <-- " + str(self.main_category))


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.category.main_category.name} --> {self.category.name} --> {self.name}"



class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)
    
    
class Color(models.Model):
    code = models.CharField(max_length=100)
    def __str__(self):
        return str(self.code)


class BrandName(models.Model):
    brandname = models.CharField(max_length=100)
    def __str__(self):
        return str(self.brandname)


class Product(models.Model):
    total_quantity = models.IntegerField()
    Availability = models.IntegerField()
    featured_image = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    
    brand_name = models.ForeignKey(BrandName,on_delete=models.CASCADE,null=True)
    price = models.IntegerField()
    Discount = models.IntegerField()
    # Product_information = models.TextField()
    Product_information = RichTextField()
    model_Name = models.CharField(max_length=100)
    Categories = models.ForeignKey(Category,on_delete=models.CASCADE)
    
    color = models.ForeignKey(Color,on_delete=models.CASCADE,null=True)
    Tags = models.CharField(max_length=100)
    # Description = models.TextField()
    Description = RichTextField()
    section = models.ForeignKey(Section,on_delete=models.DO_NOTHING)
    slug = models.SlugField(default='', max_length=700, null=True, blank=True)

    def __str__(self):
        return str(self.product_name)


    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = "app_Product"

def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.bjects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)




class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Image_url = models.CharField(max_length=500)
    # Image_url = models.URLField(max_length=500)

class AdditionalInformation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)
	
	
 
 
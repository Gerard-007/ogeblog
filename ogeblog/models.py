# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
#from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


def upload_dir(instance, filename):
    return "{}/{}".format(instance.author, filename)

class ArticleQuerySet(models.query.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)

class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().not_draft()


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
    # cat_icon = models.ImageField(upload_to=upload_dir, height_field='photo_height', width_field='photo_width', blank=True, null=True)
    # photo_height = models.PositiveIntegerField(blank = True, default = 400)
    # photo_width = models.PositiveIntegerField(blank = True, default = 800)
	creator = models.ForeignKey(settings.AUTH_USER_MODEL)

	class Meta:
		verbose_name_plural = "Categories"
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("articles_by_category", args=[self.name])


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to=upload_dir, blank=True, null=True)
    slug = models.SlugField(max_length=255)
    body = models.TextField(blank=True, null=True)
    # body = RichTextField(blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    draft = models.BooleanField(default=True)
    # published = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category)
    objects = ArticleManager()

    # def publish(self):
    #     self.published_date = timezone.now()
    #     self.save()

    def __str__(self):
        return self.title

    # @property
    # def get_img_url(self, default_path="static/img/icons/musicadence.jpg"):
    #     if self.image:
    #         return self.image.url
    #     else:
    #         return default_path

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return 'https://res.cloudinary.com/hwz12fud7/image/upload/v1538131159/media/musicadence/musicadence.jpg'
            # return "static/img/icons/musicadence.png"

    """ Informative name for model """
    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
            return "Photo <{}:{}>".format(self.title, public_id)

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ('-created',)
        unique_together = ["slug", "title",]
        db_table = "article"


def article_pre_save_signal(sender, instance, *args, **kwargs):
    # instance = "Second Article" -- Article title
    if not instance.slug:
        instance.slug = slugify(instance.title)
        new_slug = "{}-{}" .format(instance.title, instance.id)
        try:
            slug_exists = Article.objects.get(slug=instance.slug)
            instance.slug = slugify(new_slug)
        except Article.DoesNotExist:
            instance.slug = instance.slug
        except Article.MultipleObjectsReturned:
            instance.slug = slugify(new_slug)
        except:
            pass

pre_save.connect(article_pre_save_signal, sender=Article)


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name="comments")
    by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #settings.AUTH_USER_MODEL, default=1
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def approved(self):
    	self.approved = True
    	self.save()

    # def __str__(self):
    #     return self.by
    #
    # def __str__(self):
    #     if self.by==None:
    #         return "ERROR-USER NAME IS NULL"
    #     return self.by

    class Meta:
        ordering = ['created_on']

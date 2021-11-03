from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Subject(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(Subject, self).save(*args, **kwargs)


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='documents/%Y/%m/%d/', null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    room_number = models.CharField(max_length=5)
    subjects = models.ManyToManyField(Subject)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return ' '.join(filter(None, [self.first_name, self.last_name]))

    def get_absolute_url(self):
        return reverse('teacher_detail', kwargs={'pk': self.pk})


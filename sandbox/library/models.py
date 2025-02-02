from django.db import models

from hashid_field import HashidAutoField, HashidField, BigHashidAutoField, BigHashidField

from django.urls import reverse


class Author(models.Model):
    id = BigHashidAutoField(primary_key=True, prefix="a_", alphabet="0123456789abcdef")
    name = models.CharField(max_length=40)
    uid = models.UUIDField(null=True, blank=True)
    id_str = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.id_str = str(self.id)
        super().save(*args, **kwargs)


class Editor(models.Model):
    id = HashidAutoField(primary_key=True, salt="A different salt", min_length=20)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=40)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True, related_name='books')
    reference_id = HashidField(salt="alternative salt", allow_int_lookup=True, prefix="ref_")
    key = HashidField(min_length=10, alphabet="abcdlmnotuvwxyz0123789", null=True, blank=True)
    alt = HashidField(min_length=10, enable_hashid_object=False, null=True, blank=True)
    some_number = models.IntegerField(null=True, blank=True)
    editors = models.ManyToManyField(Editor, blank=True)

    def get_absolute_url(self):
        return reverse("library:book-detail", kwargs={'pk': self.pk})

    def __str__(self):
        return "{} ({})".format(self.name, self.reference_id)

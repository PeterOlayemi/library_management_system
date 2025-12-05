from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Category(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    name = models.CharField(max_length=99, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.ManyToManyField(Category, related_name='book')
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to="book_covers/", blank=True, null=True)
    rating = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    @property
    def available_copies(self):
        borrowed = BorrowRecord.objects.filter(
            book=self, returned=False
        ).count()
        return self.copies - borrowed

def default_due_date():
    return timezone.now() + timedelta(days=7)

class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=default_due_date)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    review = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("book", "user")

    def __str__(self):
        return f"{self.book.name} - {self.rating}"
    
    def update_book_rating(self):
        avg = self.book.reviews.aggregate(models.Avg('rating'))['rating__avg']
        self.book.rating = round(avg) if avg else 0
        self.book.save(update_fields=['rating'])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_book_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_book_rating()

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "book")

    def __str__(self):
        return f"{self.user} - {self.book}"

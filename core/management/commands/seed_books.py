from django.core.management.base import BaseCommand
from core.models import Category, Book
from django.core.files import File
import random
import requests
from io import BytesIO

class Command(BaseCommand):
    help = "Seed 50 books with random categories, ratings, copies, and online cover images"

    def handle(self, *args, **kwargs):
        # 8 sample categories
        categories = [
            "Fiction", "Science", "History", "Mathematics",
            "Biography", "Technology", "Fantasy", "Horror"
        ]

        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name)

        all_categories = list(Category.objects.all())

        # 50 books
        books = []
        for i in range(1, 51):
            books.append({
                "title": f"Book Title {i}",
                "author": f"Author {i}",
                "description": f"This is a sample description for book {i}.",
                "copies": random.randint(1, 5),
                "rating": random.randint(1, 5),
                "cover_url": random.choice([
                    "https://images.unsplash.com/photo-1518779578993-ec3579fee39f?q=80&w=1200&auto=format&fit=crop&s=placeholder",
                    "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?q=80&w=1200&auto=format&fit=crop&s=placeholder",
                    "https://images.unsplash.com/photo-1503602642458-232111445657?q=80&w=1200&auto=format&fit=crop&s=placeholder",
                ])
            })

        for book_data in books:
            book, created = Book.objects.get_or_create(
                title=book_data["title"],
                author=book_data["author"],
                defaults={
                    "description": book_data["description"],
                    "copies": book_data["copies"],
                    "rating": book_data["rating"]
                }
            )

            # Assign 1-2 random categories
            book.category.set(random.sample(all_categories, k=random.randint(1, 2)))

            # Download cover image
            try:
                response = requests.get(book_data["cover_url"])
                if response.status_code == 200:
                    img_temp = BytesIO()
                    img_temp.write(response.content)
                    img_temp.seek(0)
                    filename = f"book_{book.id}.jpg"
                    book.cover.save(filename, File(img_temp), save=False)
            except Exception as e:
                print(f"Failed to download image for {book.title}: {e}")

            book.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created book: {book.title}"))

        self.stdout.write(self.style.SUCCESS("Seeding 50 books completed!"))

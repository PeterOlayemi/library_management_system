from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views import View
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from django.core.paginator import Paginator

from .mixins import UserRequiredMixin
from .models import *
from core.models import *
from core.forms import *

# Create your views here.

class UserDashboardView(UserRequiredMixin, TemplateView):
    template_name = "user/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Querysets
        borrowed_qs = BorrowRecord.objects.filter(
            user=self.request.user,
            returned=False
        ).order_by("-borrowed_at")
        history_qs = BorrowRecord.objects.filter(
            user=self.request.user
        ).order_by("-borrowed_at")

        # Paginate borrowed books
        borrowed_paginator = Paginator(borrowed_qs, 5)  # 5 per page
        borrowed_page = self.request.GET.get("borrowed_page")
        context["borrowed"] = borrowed_paginator.get_page(borrowed_page)

        # Paginate history
        history_paginator = Paginator(history_qs, 5)
        history_page = self.request.GET.get("history_page")
        context["history"] = history_paginator.get_page(history_page)

        return context

class BorrowBookView(UserRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['pk']
        book = get_object_or_404(Book, id=book_id)
        if BorrowRecord.objects.filter(user=request.user, book=book, returned=False).exists():
            messages.error(request, "Return this book you borrowed first.")
            return redirect("book_detail", pk=book.pk)
        return render(request, "user/borrow.html", {"book":book})

    def post(self, request, *args, **kwargs):
        book_id = self.kwargs['pk']
        book = get_object_or_404(Book, id=book_id)
        if book.available_copies < 1:
            messages.error(request, "This book is not available.")
            return redirect("book_detail", pk=book.pk)
        BorrowRecord.objects.create(user=request.user, book=book)
        messages.success(request, "Book borrowed successfully!")
        return redirect("user_home")
    
class ReturnBookView(UserRequiredMixin, View):

    def get(self, request, record_id, *args, **kwargs):
        record = get_object_or_404(BorrowRecord, id=record_id, user=request.user)
        if record.returned:
            messages.info(request, "This book is already returned.")
        else:
            record.returned = True
            record.save()
            messages.success(request, "Book returned successfully!")
        return redirect("user_home")

class AddReviewView(UserRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "user/update_review.html"  # same template you used

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, id=self.kwargs["book_id"])

        # Prevent duplicate review
        if Review.objects.filter(book=self.book, user=self.request.user).exists():
            messages.error(request, "You have already reviewed this book.")
            return redirect("book_detail", pk=self.book.pk)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.book = self.book
        form.instance.user = self.request.user
        messages.success(self.request, "Review submitted successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("book_detail", kwargs={"pk": self.book.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = self.book
        return context
    
class UpdateReviewView(UserRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "user/update_review.html"

    def dispatch(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            messages.error(request, "You cannot edit this review.")
            return redirect("book_detail", pk=review.book.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "Review updated successfully.")
        return reverse("book_detail", kwargs={"pk": self.object.book.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = self.object.book
        context["review"] = self.object
        return context

class DeleteReviewView(UserRequiredMixin, DeleteView):
    model = Review
    template_name = "user/delete_review_confirm.html"

    def dispatch(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            messages.error(request, "You cannot delete this review.")
            return redirect("book_detail", pk=review.book.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "Review deleted successfully.")
        return reverse("book_detail", kwargs={"pk": self.object.book.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = self.object.book
        return context

class ToggleBookmarkView(UserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs["book_id"])
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user, book=book
        )

        if created:
            messages.success(request, "Book added to bookmarks.")
        else:
            bookmark.delete()
            messages.success(request, "Book removed from bookmarks.")

        return redirect("book_detail", pk=book.pk)

class BookmarkListView(UserRequiredMixin, ListView):
    model = Bookmark
    template_name = "user/bookmarks.html"
    context_object_name = "bookmarks"

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

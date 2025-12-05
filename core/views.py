from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q

from core.models import *

# Create your views here.

class HomeView(TemplateView):
    template_name = 'core/home.html'

class BookListView(ListView):
    model = Book
    template_name = "core/book_list.html"
    context_object_name = "books"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()

        return queryset
    
class BookDetailView(DetailView):
    model = Book
    template_name = "core/book_detail.html"
    context_object_name = "book"
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_bookmarked = False
        if Bookmark.objects.filter(user=self.request.user, book=self.object).exists():
            is_bookmarked = True

        context["is_bookmarked"] = is_bookmarked
        return context

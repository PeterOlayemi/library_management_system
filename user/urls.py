from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard/', UserDashboardView.as_view(), name='user_home'),
    path("book/<int:pk>/borrow/", BorrowBookView.as_view(), name="borrow_book"),
    path("return/<int:record_id>/", ReturnBookView.as_view(), name="return_book"),
    path("book/<int:book_id>/review/add/", AddReviewView.as_view(), name="add_review"),
    path("review/<int:pk>/update/", UpdateReviewView.as_view(), name="update_review"),
    path("review/<int:pk>/delete/", DeleteReviewView.as_view(), name="delete_review"),
    path("book/<int:book_id>/bookmark/", ToggleBookmarkView.as_view(), name="toggle_bookmark"),
    path("bookmarks/", BookmarkListView.as_view(), name="bookmarks"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:TITLE>", views.entry, name="wiki_entry"),
    path("search", views.search, name="search"),
    path("new_page", views.newpage, name="new_page"),
    path("edit_page/<str:title>", views.editpage, name="edit_page"),
    path("random", views.random, name="random"),
]

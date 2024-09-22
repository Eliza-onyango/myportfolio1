from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_page, name="create"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("random/", views.random_page, name="random")
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("choose", views.choose, name="choose"),
    path("groups", views.groups, name="groups"),
    path("browse", views.browse, name="browse"),
    path("group/<str:group_id>", views.group, name="group"),
    path("shuffle/<str:group_id>", views.pairup, name="shuffle"),
    path("delete_group/<str:group_id>", views.delete_group, name="delete_group"),
    path("leave_group/<str:group_id>", views.leave_group, name="leave_group"),
    path("read/<str:alert_id>", views.read, name="read"),
    path("edit/<str:group_id>", views.edit, name="edit"),
    path("like/<str:gift_id>/<str:group_id>", views.like, name="like"),
    path("edit_notes/<str:wishlist_id>", views.edit_notes, name="edit_notes")

]
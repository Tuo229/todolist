from django.urls import path
from .views import (
    create_user_view, user_list_view, login_view,
    LogOut, create_projet_view, projet_list_view,
    delete_tache, update_projet_view, create_sous_tache_view
    
    )


app_name = "apptache"
urlpatterns = [

    path("create-user", create_user_view, name="create_user"),
    path("user-list", user_list_view, name="user_list"),

    path("login", login_view, name="login"),
    path("logout", LogOut, name="logout"),

    path("create-projet", create_projet_view, name="create_projet"),
    path("list-projet", projet_list_view, name="liste_projet"),
    path("<str:pk>/del-projet", delete_tache, name="delete_projet"),
    path("<str:pk>/update-projet", update_projet_view, name="update_projet"),
    path("<str:pk>/sous-tache-projet", create_sous_tache_view, name="sous_tache_projet"),

]
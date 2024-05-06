from django.urls import path, include
from . import views
app_name='mthapp'

urlpatterns = [

    path('', views.login,name='login'),
    path('index', views.index, name='index'),
    path('navbar_with_dropdown/', views.navbar_with_dropdown, name='navbar_with_dropdown'),

    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('logout', views.logout, name='logout'),
    # path('upload', views.upload, name='upload'),
    path('add_post', views.add_post, name='add_post'),

    path('movie/<int:movieid>/', views.detail, name='detail'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    # path('fav/<int:id>/', views.fav, name='fav'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('settings', views.settings, name='settings'),
    path('detail', views.detail, name='detail'),
    path('favourites/', views.favourite_list, name='favourite_list'),
    path('fav/<int:id>/', views.favourites, name='favourites'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('change_username', views.change_username, name='change_username'),
    path('change_password', views.change_password, name='change_password'),

    path('deletecomment/<int:id>/', views.deletecomment, name='deletecomment'),

]
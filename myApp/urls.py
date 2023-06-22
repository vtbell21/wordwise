from . import views
from django.urls import path
from .views import generate_random_word
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.process_sentence, name="process_sentence"),
    path("generate-random-word/", views.generate_random_word,
         name="generate-random-word"),
    path('process-sentence/<str:random_word>/',
         login_required(views.process_sentence), name='process_sentence'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('navigation/', views.navigation, name='navigation'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),

]

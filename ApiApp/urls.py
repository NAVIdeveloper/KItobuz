from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *


urlpatterns = [
    path("token/",TokenObtainPairView.as_view()),
    path("token/refresh/",TokenRefreshView.as_view()),
    path("books/",AllBookView.as_view()),
    path("books/<int:pk>/",OneBookView.as_view()),
    path("audio/books/",AllAudioBookView.as_view()),
    path("audio/books/<int:pk>/",OneAudioBookView.as_view()),
    path("rating/audio/add/<int:pk>/",RatingAudioBookAddView.as_view()),
    path("rating/simple/add/<int:pk>/",RatingBookAddView.as_view()),
    path("recomended/simple/",RecomendedBookView.as_view()),
    path("recomended/audio/",RecomendedAudioBookView.as_view()),
    path("login/register/",LoginRegister.as_view()),

    path("add/simple/going-to-read/",GoingToReadAdd.as_view()),
    path("add/simple/reading/",ReadingAdd.as_view()),
    path("add/simple/readed/",ReadedAdd.as_view()),

    path("add/audio/going-to-read/",GoingToReadAudioAdd.as_view()),
    path("add/audio/reading/",ReadingAudioAdd.as_view()),
    path("add/audio/readed/",ReadedAudioAdd.as_view()),    

    path("search/audio/",SearchAudioBook.as_view()),
    path("search/simple/",SearchBook.as_view()),

    path("category/<int:pk>/",CategoryView.as_view()),
]

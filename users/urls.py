from django.urls import path
from .views import RegisterView, LoginView, LogoutView, LoggedInUsersView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logged-in-users/', LoggedInUsersView.as_view(), name='logged-in-users'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]

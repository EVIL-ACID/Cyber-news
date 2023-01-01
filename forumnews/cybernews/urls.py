
from django.urls import path
from . import views
from .views import RegisterView


urlpatterns = [
    path('', views.home_view, name='home'),
    path('add_post/', views.add_view, name='add'),
    path('post/<int:postid>', views.post_view, name='post'),
    path('post/update/<int:postid>', views.update_post_view, name='post_update'),
    path('post/delete/<int:postid>', views.delete_post_view, name='delete_post'),
    path('user/', views.profile_view, name='profile'),
    path('user/<str:username>', views.profile_view, name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('comment/<int:id>', views.display_comment, name='comment'),
    path('comment/update/<int:commentid>', views.update_comment_view, name="update_comment"),
    path('comment/delete/<int:commentid>', views.delete_comment_view, name='delete_comment'),
    path('post/upvote/(<int:post_id>)', views.upvote, name='upvote'),
]
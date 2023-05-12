from django.urls import path
from app.views import *

#app_name = 'app'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create/', create_blog, name='create_blog'),
    path('read/<int:blog_id>/', read_blog, name='read_blog'),
    path('update/<int:blog_id>/', update_blog, name='update_blog'),
    path('delete/<int:blog_id>/', delete_blog, name='delete_blog'),
    path('comment/<int:blog_id>/', create_comment, name='create_comment'),
    path('view_all_blogs/', view_all_blogs, name='view_all_blogs'),
    path('blogs/<int:blog_id>/comment/', comment_on_blog, name='comment_on_blog'),
    path('blogs/<int:blog_id>/', view_blog, name='view_blog'),
    path('admins/', admin, name='admins'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
]

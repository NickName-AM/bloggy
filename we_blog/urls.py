from django.urls import path
from we_blog import views

urlpatterns = [
    path('home/', views.we_blog, name='home'),
    path('', views.we_blog),

    path('blog/<int:b_id>', views.show_blog, name='show_blog'),
    path('add/', views.create, name='add'),
    path('edit/<int:b_id>/<int:w_id>', views.edit, name='edit'),
    path('remove/<int:b_id>/<int:w_id>', views.remove, name='remove'),
    path('my_blogs/<int:u_id>', views.my_blogs, name='my_blogs'),
    path('user_blogs/<int:u_id>', views.user_blogs, name='user_blogs'),

    path('register/', views.register,name='register'),
    path('login/', views.signin,name='signin'),
    path('logout/', views.signout,name='signout'),
    path('profile/<int:u_id>', views.profile, name='profile'),
    path('bloggers/', views.bloggers, name='bloggers'),
]

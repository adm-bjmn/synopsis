from . import views
from django.urls import path


# urls for the User functions and members views only.
urlpatterns = [
    path('login_user/', views.login_user, name='login_user'),
    path('login_demo/', views.login_demo, name='login_demo'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('register_user/', views.register_user, name='register_user'),
    path('profile/<user_id>', views.user_profile, name='profile'),
    path('update_profile/<user_id>', views.update_profile, name='update_profile'),
    path('change_password/<user_id>',
         views.change_password, name='change_password'),
    path('delete_user/<user_id>', views.delete_user, name='delete_user'),
    path('reset_synopsis/<user_id>', views.reset_synopsis, name='reset_synopsis'),
    path('toggle_instrustions/<user_id>',
         views.toggle_instructions, name='toggle_instructions'),

]

from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('logout/', views.logout_request, name= 'logout'),
    path('signup/', views.signup_request, name='signup'),
    path('login/', views.login_request, name='login'),
    
    path('',views.index, name = 'index'),
    # path('home/<int:id>',views.index, name = 'index'),
    path('delete/<int:id>',views.delete, name='delete'),
    path('edit/<str:id>',views.editquestion, name='editquestion'),
    path('share/<str:id>',views.share, name='share'),
    # path('check/',views.check, name='check'),

    # Manage page
    path('manage',views.manage, name='manage'),
    path('searcheachquestion/', views.searcheachquestion, name='searcheachquestion'),
    # path('manage/<int:id>',views.managecourse, name='managecourse'),

    # path('createcourse/',views.createcourse, name='createcourse'),
    # path('savecourse/',views.savecourse, name='savecourse'),
]
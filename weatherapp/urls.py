from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('app/', views.home, name='home'),
    path('app/', views.city_detail, name='detail'),
    path('delete/<int:pk>/', views.city_delete, name='delete'),
    path('update/<int:pk>/', views.city_update, name='update'),

    path('signup/', views.sign_up, name='signup'),
    path('logout/', views.user_logout, name='logout'),

    path('plot/', views.plot_graph, name='plot_graph'),
    path('plot2/', views.plot2, name='plot_graph'),

    path('map/', views.map, name='map'),
]
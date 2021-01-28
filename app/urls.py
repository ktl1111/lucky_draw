from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("list", views.list, name="list"),
    path("draw", views.draw, name="draw"),
    path(r'^export/xls/$', views.export_users_xls_verylucky,name='export_users_xls_verylucky'),
    path(r'^export/xls/$', views.export_users_xls,name='export_users_xls'),
]


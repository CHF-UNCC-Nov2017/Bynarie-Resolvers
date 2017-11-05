from django.conf.urls import url

from . import views

app_name = 'mockup'
urlpatterns = [
    url('^$', views.index, name='index'),
    url('^dashboard/', views.detail, name='dash'),
]

from django.urls import path
from . import views

app_name = 'property'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('category/<int:category_id>/page/<int:page_num>/',  views.category, name='page'),
    path('object/<int:object_id>', views.object, name="object"),
    path('page/<int:page_id>/', views.page, name="page"),
    path('search', views.search, name="search"),
]

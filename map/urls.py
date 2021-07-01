from django.urls import path

from map.views import (
	show_map,
	add_rep,
	ShowWorkshop,
)

app_name= 'map'
urlpatterns = [
    path('',show_map, name='show_map'),
    path('addrepairman/',add_rep.as_view(),name='addrep'),
    path('<slug>',ShowWorkshop.as_view(),name='showWorkshop'),
]
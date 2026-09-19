from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.deal_list,
        name='sales'
    ),

    path(
        'add/',
        views.add_deal,
        name='add_deal'
    ),

    path(
        'edit/<int:id>/',
        views.edit_deal,
        name='edit_deal'
    ),

    path(
        'delete/<int:id>/',
        views.delete_deal,
        name='delete_deal'
    ),

]
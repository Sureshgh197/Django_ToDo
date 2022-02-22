from django.urls import path
from . import views

urlpatterns=[
        path('',views.TaskList.as_view()),
        path('create',views.create),
        path('update/<int:id>',views.update),
        path('update_data',views.update_data),
        path('delete/<int:id>',views.delete),
        path('deleteRecycle/<int:id>',views.deleteRecycle),
        path('rlistDelete',views.rlistDelete),
        path('tlistDelete',views.tlistDelete),
        path('restore',views.restore),
        path('restoreSelect/<int:id>',views.restoreSelect),
        path('cat_add',views.cat_add_page)
        ]

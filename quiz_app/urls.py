from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

from . import views
from . import channel_views
from . import results_views

results_patterns = [
    path('', results_views.available_models, name='available_models'),
    path('<str:model_name>/list/',
         results_views.model_list, name='item_list'),
    path('<str:model_name>/create/',
         results_views.model_create, name='item_create'),
    path('<str:model_name>/update/<str:pk>/',
         results_views.model_update, name='item_update'),
    path('<str:model_name>/delete/<str:pk>/',
         results_views.model_delete, name='item_delete'),
    path('details/', results_views.detailed_results_view,
         name='detailed_results'),

]

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls, name='admin'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('start_test/', views.start_test, name='start_test'),
    path('instruction/<str:test>/', views.instruction,
         name='instruction'),
    path('test/<str:test>/', views.test, name='test'),
    path('test_submit/<str:test>/', views.test_submit,
         name='test_submit'),
    path('end_test/', views.thank_you, name='end_test'),

    path('results/', include((results_patterns, 'results')),
         name='results'),
]

websocket_urlpatterns = [
    path('ws/quiz/', channel_views.QuizConsumer.as_asgi(), name='async'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)

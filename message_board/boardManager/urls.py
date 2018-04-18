from django.urls import path
from django.conf.urls import url
from message_board import settings
from .models import upload_path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('forum/<forum_name>', views.forum, name='forum'),
    path('forum/<forum_name>/<thread_id>', views.thread, name='thread'),
    url(r'^signup/$', views.signup, name='signup'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.urls import path
from . import views

urlpatterns = [
    path("", views.conversation_list, name="conversation_list"),
    path(
        "conversation/<int:conversation_id>/",
        views.conversation_detail,
        name="conversation_detail",
    ),
    path(
        "conversation/<int:conversation_id>/send/",
        views.send_message,
        name="send_message",
    ),
    path(
        "conversation/<int:conversation_id>/rename/",
        views.rename_conversation,
        name="rename_conversation",
    ),
    path(
        "conversation/<int:conversation_id>/delete/",
        views.delete_conversation,
        name="delete_conversation",
    ),
    path("new/", views.new_conversation, name="new_conversation"),
]

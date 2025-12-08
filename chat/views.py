from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Conversation, Message
from .ai_utils import (
    get_ai_response,
    format_messages_for_gemini,
    generate_conversation_title,
    execute_ai_command,
)
import json
import time


def conversation_list(request):
    conversations = Conversation.objects.all().order_by("-updated_at")
    return render(
        request, "chat/conversation_list.html", {"conversations": conversations}
    )


def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.all()
    conversations = Conversation.objects.all().order_by("-updated_at")
    return render(
        request,
        "chat/conversation_detail.html",
        {
            "conversation": conversation,
            "messages": messages,
            "conversations": conversations,
        },
    )


@require_POST
def send_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    data = json.loads(request.body)
    content = data.get("content", "").strip()

    if not content:
        return JsonResponse({"error": "Message cannot be empty"}, status=400)

    user_message = Message.objects.create(
        conversation=conversation, content=content, is_user=True
    )

    # Check if this is an AI command first
    command_result = execute_ai_command(content)
    if command_result:
        ai_response = command_result
    else:
        # Generate title if this is the first message and title is still "New Chat"
        if conversation.title == "New Chat" and conversation.messages.count() == 1:
            try:
                ai_title = generate_conversation_title(content)
                conversation.title = ai_title
            except Exception as e:
                # Keep default title if generation fails
                pass

        conversation_messages = conversation.messages.all()
        gemini_messages = format_messages_for_gemini(conversation_messages)

        try:
            ai_response = get_ai_response(gemini_messages)
        except Exception as e:
            ai_response = f"Error: {str(e)}"
    ai_message = Message.objects.create(
        conversation=conversation, content=ai_response, is_user=False
    )

    conversation.updated_at = ai_message.created_at
    conversation.save()

    return JsonResponse(
        {
            "user_message": {
                "id": user_message.id,
                "content": user_message.content,
                "created_at": user_message.created_at.isoformat(),
            },
            "ai_message": {
                "id": ai_message.id,
                "content": ai_message.content,
                "created_at": ai_message.created_at.isoformat(),
            },
            "conversation_title": conversation.title,
        }
    )


@require_POST
def rename_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    data = json.loads(request.body)
    new_title = data.get("title", "").strip()

    if not new_title:
        return JsonResponse({"error": "Title cannot be empty"}, status=400)

    conversation.title = new_title
    conversation.save()
    return JsonResponse({"success": True, "title": new_title})


@require_POST
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    conversation.delete()
    return JsonResponse({"success": True})


def new_conversation(request):
    if request.method == "POST":
        # Create conversation with default title first
        conversation = Conversation.objects.create(title="New Chat")
        return redirect("conversation_detail", conversation_id=conversation.id)

    return render(request, "chat/new_conversation.html")

import markdown2
from django.shortcuts import render
from .LLMAdapters.Qwen_1_point_5_B import Qwen_1_point_5_B
from .models import ChatHistory

qwen_1_point_5_B = Qwen_1_point_5_B()

def view_chats(request):
    chats = ChatHistory.objects.all()
    return render(request, 'LLMService/view_chats.html', {'chats': chats})

def llm_request(request):
    if 'clear' in request.POST:
        qwen_1_point_5_B.clear_context()
        conversation_history = []
    elif request.method == 'POST':
        content = request.POST.get('content', '')
        raw_markdown = qwen_1_point_5_B.send_message(content)
        formatted_response = markdown2.markdown(raw_markdown)
        conversation_history = qwen_1_point_5_B.get_history()

        for entry in conversation_history:
            entry['response'] = markdown2.markdown(entry['response'])

        conversation_history = conversation_history[::-1]

        return render(request, 'LLMService/form.html', {
            'response': formatted_response,
            'content': content,
            'conversation_history': conversation_history
        })
    else:
        conversation_history = qwen_1_point_5_B.get_history()

        for entry in conversation_history:
            entry['response'] = markdown2.markdown(entry['response'])

        conversation_history = conversation_history[::-1]

    return render(request, 'LLMService/form.html', {'conversation_history': conversation_history})

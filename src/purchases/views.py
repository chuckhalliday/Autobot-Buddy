from django.shortcuts import render
from django.conf import settings

base = settings.PROTECTED_MEDIA_ROOT

# Create your views here.
from products.models import Vehicle
from queries import create_embeddings, get_embeddings, user_question_embedding_creator, answer_users_question

def chat_view(request):
    vehicle = Vehicle.objects.filter(handle='JF2SKASC2KH496845').first()

    create_embeddings(f'{base}/manuals/2019subaruforester.txt', '2019subaruforester', vehicle)
    embeddings, snippets = get_embeddings(f'{base}/embeddings/2019subaruforester.json')

    user_question = 'How do you check the oil?'

    user_embedding = user_question_embedding_creator(user_question)

    answer = answer_users_question(user_question, user_embedding, embeddings, snippets, 'gpt-3.5-turbo')

    print(answer)

    return render(request, 'purchases/chat.html')
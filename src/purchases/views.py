from django.shortcuts import render
from django.conf import settings
from autohome.storages.utils import generate_presigned_url

#base = settings.PROTECTED_MEDIA_ROOT

# Create your views here.
from .models import Product, ChatLog
from products.models import Vehicle
from .forms import QuestionForm
from queries import create_embeddings, get_embeddings, user_question_embedding_creator, answer_users_question

def chat_view(request):
    vin = request.session.get('vehicle_id')
    handle = request.session.get('vehicle_handle')
    vehicle = Vehicle.objects.filter(handle=vin).first()
    product = vehicle.product
    gpt_model = product.model
    #base = 'https://autoadvisorbucket.s3.us-west-2.amazonaws.com/protected'

    text_path = generate_presigned_url(f'manuals/{handle}.txt') # f'{base}/manuals/{handle}.txt'
    json_path = generate_presigned_url(f'embeddings/{handle}.json') #f'{base}/embeddings/{handle}.txt'

    create_embeddings(text_path, handle, vehicle)
    embeddings, snippets = get_embeddings(json_path)

    context = {}
    answer = ''
    form = QuestionForm(request.POST or None)
    if form.is_valid():
        user_question = form.cleaned_data['question']
        user_embedding = user_question_embedding_creator(user_question)

        answer = answer_users_question(user_question, user_embedding, embeddings, snippets, gpt_model)

        obj = form.save(commit=False)
        obj.user = request.user
        obj.vehicle = vehicle
        obj.chat_model = Product.objects.filter(model=gpt_model).first()
        obj.question = form.cleaned_data['question']
        obj.answer = answer
        last_chatlog = ChatLog.objects.filter(vehicle=vehicle).order_by('-id').first()
        if last_chatlog:
            obj.previous = last_chatlog
        obj.save() 
    context['form'] = form
    context['answer'] = answer

    return render(request, 'purchases/chat.html', context)
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from PIL import Image
import numpy as np
import io
from .ml_models.ml_model import predict_class
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

# Функция и переменные для загрузки сторонней модели

# tokenizer = None
# model_neo = None
# model_loaded = False

# def load_mistral_model():
#     global tokenizer, model_neo, model_loaded
#
#     if model_loaded:
#         return
#
#     login(token="")
#
#     model_id = "mistralai/Mistral-7B-Instruct-v0.2"
#
#     tokenizer = AutoTokenizer.from_pretrained(model_id)
#     model_neo = AutoModelForCausalLM.from_pretrained(
#         model_id,
#         device_map="auto",
#         torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
#     )
#     model_loaded = True


# def get_prompt(dish_name):
#     return f"[INST] Ты диетолог. Оцени, сколько калорий примерно содержит блюдо '{dish_name}'. Укажи калорийность и в 5 слов прокомментируй, подходит ли оно для сбалансированного питания. [/INST]"
#
#
# def get_answer_from_neo(prompt):
#     input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model_neo.device)
#
#     output = model_neo.generate(
#         input_ids,
#         do_sample=True,
#         temperature=0.7,
#         max_new_tokens=250,
#         pad_token_id=tokenizer.eos_token_id,
#         top_p=0.85,
#         repetition_penalty=1.1,
#         no_repeat_ngram_size=3
#     )
#
#     generated_text = tokenizer.decode(output[0][input_ids.shape[1]:], skip_special_tokens=True)
#     return generated_text.strip()


def main_page(request):
    return render(request, 'AIWebProject/main-page.html')

def second_page(request):
    uploaded_file_url = None
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']
        fs = FileSystemStorage(location='media/uploads/')
        filename = fs.save(upload.name, upload)
        uploaded_file_url = fs.url('uploads/' + filename)

    return render(request, 'AIWebProject/second-page.html')


def predict_image(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image_file = request.FILES['image']
        predicted_label = predict_class(image_file)

        print(predicted_label)

        # Для сторонней модели
        # load_mistral_model()
        #
        # prompt = get_prompt(predicted_label)
        # gpt_response = get_answer_from_neo(prompt)
        #
        # print(gpt_response)
        #
        # return JsonResponse({
        #     'prediction': predicted_label,
        #     'ai_nutrition_comment': gpt_response
        # })

        return JsonResponse({
            'prediction': predicted_label
        })

    return JsonResponse({'error': 'Please POST an image'}, status=400)
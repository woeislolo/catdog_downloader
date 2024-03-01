from django.shortcuts import render
from django.shortcuts import redirect
           
from . import tasks


def index(request):
    return render(request, "main/base.html")


def home(request):
    request = request.POST.dict()
    animal = request['animal']
    image_num = int(request['image_num'])
    for i in range(image_num):
        tasks.download_cat_dog.delay(animal)
    return redirect("index")

from django.shortcuts import render

# Create your views here.
def home(request):
    template_name = 'index.html'
    content = {}
    return render(request, template_name, content)


def encode(request):
    template_name = 'encode.html'
    content = {}
    return render(request, template_name, content)

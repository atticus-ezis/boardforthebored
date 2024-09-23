from django.shortcuts import render

def index_view(request):
    return render(request, 'index.html') 

def test_index_view(request):
    return render(request, 'test_index.html')
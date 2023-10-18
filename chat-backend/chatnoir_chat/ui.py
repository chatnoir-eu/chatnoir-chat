from django.shortcuts import render

def veutify_page(request):
    context = {}
    return render(request, 'vuetify_index.html', {})

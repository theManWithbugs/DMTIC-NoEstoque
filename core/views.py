from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def loginView(request):
    
    template_name = 'account/login.html'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('base_page')
  
    return render(request, template_name)

def baseView(request):
    template_name = 'base.html'
    return render(request, template_name)

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/uitspraken')
        else:
            error_message = "Invalid credentials. Please try again"
    else:
        error_message = None

    context = {'error_message': error_message}
    return render(request, 'uitspraken/login.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            
            # Authenticate the user
            user = authenticate(request, email=email, password=raw_password)
            
            # Check if authentication was successful
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('https://openroboticmetaverse.org/')  # Replace 'home' with your actual homepage URL
            else:
                # Handle cases where the authentication fails (optional)
                form.add_error(None, "Authentication failed. Please try logging in.")
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('https://openroboticmetaverse.org/')  # Change to your homepage URL
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('https://openroboticmetaverse.org/')  # Change to your homepage URL

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import MRIImage
from django.contrib.auth.decorators import login_required
from ml_model.predict import predict_tumor

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please choose another username.")
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(request, "Registration successful!")

        return redirect('login')

    return render(request, 'register.html')
def user_login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']


        user = authenticate(
            username=username,
            password=password
        )


        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            messages.error(request, "Invalid username or password")


    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')
@login_required
def upload_mri(request):
    result = None

    if request.method == "POST":
        image_file = request.FILES['image']

        mri = MRIImage.objects.create(
            user=request.user,
            image=image_file
        )

        result = predict_tumor(
            mri.image.path
        )
        mri.prediction = result
        mri.save()

        return render(request, 'result.html', {
            'prediction': result,
            'image': mri
        })
    return render(
        request,
        "upload.html",
        {
            "result": result
        }
    )
@login_required
def mri_history(request):

    images = MRIImage.objects.filter(
        user=request.user
    )

    return render(
        request,
        'history.html',
        {'images': images}
    )



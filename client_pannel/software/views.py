from django.shortcuts import render, redirect
from .models import *
from .forms import ProjectForm, ProfileForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def home(request):
    return render(request, 'home.html')


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})
    


def delete_project(request, pk):
    ProjectS.objects.get(pk=pk).delete()
    return redirect('dashboard')
'''
def view_profile(request):
    profile = Profile.objects.all()
    return render(request, 'view_profile.html', {'profile': profile})
'''
def view_profile(request):
    profile = Profile.objects.get()
    profile_user = User.objects.filter()
    return render(request, 'view_profile.html', 
    {'profile':profile, 'profile_user':profile_user})

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


'''def update_project(request, pk):
    project = ProjectS.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'update_project.html', {'form': form})'''

def update_project(request, pk):
    if not pk:
        return redirect('dashboard')
    project = ProjectS.objects.get(pk=pk)
    form = ProjectForm(request.POST or None, request.FILES or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'update_project.html', 
    {'project':project, 'form':form})
'''
def create_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        deadline = request.POST.get('deadline')
        budget = request.POST.get('budget')
        file1 = request.FILES.get('file1')
        file2 = request.FILES.get('file2')
        file3 = request.FILES.get('file3')
        closed = request.POST.get('closed') == 'on'
        
        project = ProjectS.objects.create(
            name=name,
            description=description,
            image1=image1,
            image2=image2,
            image3=image3,
            deadline=deadline,
            budget=budget,
            file1=file1,
            file2=file2,
            file3=file3,
            closed=closed
        )
        project.save()
        return redirect('dashboard')
    
    context = {}
    return render(request, 'create_project.html', context)
'''

def dashboard(request):
    projects = ProjectS.objects.all()
    if not projects:
        return redirect('dashboard')
    for project in projects:
        if not project.pk:
            return redirect('dashboard')
    return render(request, 'dashboard.html', {'projects': projects})




#User Auth

'''def signupUser(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = ProfileForm()
    return render(request, 'signupUser.html', {'form': form})


def loginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'loginUser.html', {'form': form})'''

'''
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('loginUser')

        profile_obj = Profile.objects.filter(user=user_obj).first()

        if profile_obj is None or not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified. Check your email.')
            return redirect('loginUser')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('loginUser')
        
        login(request, user)
        return redirect('home')
    return render(request, 'loginUser.html')'''

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong credentials')
            return redirect('loginUser')
    return render(request, 'loginUser.html')

def registerUser(request):

    if request.method == 'POST':
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')
        profile_pic = request.FILES.get('profile_pic')
        
        try:
            print('hi')
            if User.objects.filter(username = username).first():
                print('second')
                messages.success(request, 'Username is taken')
                return redirect('/registerUser/')
        

            if User.objects.filter(email = email).first():
                messages.success(request, 'email is taken')
                return redirect('/registerUser/')
            print('third')
            user_obj = User.objects.create(
                username = username,
                email = email,
                
            )
            print(phone_number)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token, 
            phone_number = phone_number,
            
            country = country,
            profile_pic = profile_pic )

            profile_obj.save()
            send_verification_email(email, auth_token)
            return redirect('/token_send/')
        except Exception as e:
            print(e)
    return render(request, 'registerUser.html')

def success(request):
    return render(request, 'success.html')


def token_send(request):
    return render(request, 'token_send.html')

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('loginUser')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('loginUser')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('home')

def error_page(request):
    return  render(request , 'error.html')



def send_verification_email(email, token_send):
    subject = "Your account need to be verified"
    message = f"paste the link for verify your account http://127.0.0.1:8000/verify/{token_send}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
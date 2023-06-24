from django.shortcuts import render, redirect
import random
from .forms import SentenceForm
import requests
from django.shortcuts import redirect
from .forms import RegistrationForm
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from myApp.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
import os
from dotenv import load_dotenv
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.conf import settings
from django.contrib.auth.models import AnonymousUser


# Load the environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
# api_key = os.getenv('OPENAI_API_KEY')


def home(request):
    context = {}
    return render(request, "myApp/home.html", context)


def generate_random_word(request):
    encodings = ['utf-8', 'latin-1', 'utf-16']

    # Get the absolute path of the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the file path to engmix.txt
    file_path = os.path.join(current_directory, 'engmix.txt')

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                words = file.read().split('\n')
            break
        except UnicodeDecodeError:
            continue

    random_word = random.choice(words)
    request.session['random_word'] = random_word
    return redirect('process_sentence')


def sentence_form(request):
    if request.method == 'POST':
        # Process the form submission
        word = request.POST.get('word')  # Access the submitted word
        # Access the submitted sentence
        sentence = request.POST.get('sentence')
        # Perform any additional processing or validation here
        # Save the data to the database or perform any other actions
        # Redirect the user to another page or display a success message
        # return redirect('success_page')
    else:
        # Display the form
        context = {
            'word': 'brilliant',  # Pass the word to be generated
        }
        return render(request, 'myApp/sentence_form.html', context)


# @login_required(login_url='login')

def process_sentence(request):
    random_word = request.session.get('random_word', '')
    api_key = settings.API_KEY

    if request.method == 'POST':
        form = SentenceForm(request.POST)
        if form.is_valid():
            sentence = form.cleaned_data['sentence']
            generate_word = random_word

            # Call the Chat GPT API
            api_endpoint = 'https://api.openai.com/v1/chat/completions'
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            }
            payload = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'system',
                     'content': f'You are given the word: {generate_word}'},
                    {'role': 'user',
                     'content': f'respond "valid" if the following sentence is a valid sentence given the generated word, and "invalid" if the following sentence is invalid given the generated word: {sentence}'},
                ],
            }

            response = requests.post(
                api_endpoint, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                choices = result['choices']
                print("API Response:")
                print(response.json())

                # Perform your validation logic
                is_valid = any(
                    'valid' in choice['message']['content'].lower() for choice in choices)
                is_invalid = any(
                    'invalid' in choice['message']['content'].lower() for choice in choices)

                if is_invalid:
                    # The sentence is invalid
                    result = 'Invalid'
                elif is_valid:
                    # The sentence is valid
                    result = 'Valid'
                else:
                    # Neither valid nor invalid keyword found
                    result = 'Unknown'

                # Update user profile statistics
                user = request.user
                if isinstance(user, AnonymousUser):
                    user_id = None
                else:
                    user_id = user.id

                if user_id:
                    profile, created = UserProfile.objects.get_or_create(
                        user_id=user_id)
                    profile.valid_attempts += 1  # Increment total attempts
                    if is_invalid:
                        profile.invalid_attempts += 1  # Increment invalid attempts
                    profile.save()

                return render(request, 'myApp/sentence_form.html', {
                    'form': form,
                    'random_word': random_word,
                    'result': result
                })
    else:
        form = SentenceForm()

    return render(request, 'myApp/sentence_form.html', {
        'form': form,
        'random_word': random_word
    })


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a user profile for the newly registered user
            UserProfile.objects.create(user=user)
            username = form.cleaned_data['username']
            messages.success(
                request, f'Account created successfully for {username}. You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'myApp/registration.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        # User is already logged in, redirect to the home page
        return redirect('process_sentence')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the home page
                return redirect('process_sentence')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'myApp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    # Redirect to the desired page after logout
    return redirect(reverse('login'))


def profile(request):
    user = request.user
    profile = None
    total_valid_attempts = 0
    total_invalid_attempts = 0
    total_attempts = 0
    valid_accuracy = 0

    if user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=user)
            total_valid_attempts = int(profile.valid_attempts)
            total_invalid_attempts = int(profile.invalid_attempts)
            total_attempts = total_valid_attempts + total_invalid_attempts

            if total_attempts > 0:
                valid_accuracy = (total_valid_attempts / total_attempts) * 100
                # Round to two decimal places
                valid_accuracy = round(valid_accuracy, 2)
        except UserProfile.DoesNotExist:
            pass

    return render(request, 'myApp/profile.html', {
        'user': user,
        'profile': profile,
        'total_valid_attempts': total_valid_attempts,
        'total_invalid_attempts': total_invalid_attempts,
        'total_attempts': total_attempts,
        'valid_accuracy': valid_accuracy,
    })


def navigation(request):
    return render(request, 'myApp/navigation.html')


def leaderboard(request):
    top_users = UserProfile.objects.order_by(
        '-valid_attempts')[:10]  # Retrieve top 10 users
    return render(request, 'myApp/leaderboard.html', {'top_users': top_users})


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].help_text = ''
        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].help_text = ''


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')


def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(
            user=request.user, data=request.POST)

        if form.is_valid() and password_form.is_valid():
            form.save()
            # Keep the user authenticated after password change
            password_form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'myApp/update_profile.html', {'form': form, 'password_form': password_form})

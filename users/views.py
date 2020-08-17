from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import *

def logout_view(request):
    """Log the user out."""
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def register(request):
    """Register a new user."""
    if (request.method != 'POST'):
        form = SignUpForm()
    else:
        form = SignUpForm(data=request.POST)

        if (form.is_valid()):
            data = form.cleaned_data
            new_usr = User.objects.create_user(username=data['username'], email=data['email'],
                                                password=data['password'])
            new_usr.first_name = data['first_name']
            new_usr.last_name = data['last_name']
            new_usr.save()

            new_usr.refresh_from_db()

            return HttpResponseRedirect(reverse('admin_pages:manage_users'))

    context = { 'form': form }
    return render(request, 'users/register.html', context)


@login_required
def confirm_delete_user(request, user_id):
    """Display a confirmation dialog view before deleting a user."""
    user = User.objects.get(id=user_id)

    context = { 'user': user }
    return render(request, 'users/confirm_delete_user.html', context)

@login_required
def delete_user(request, user_id):
    """Delete the user."""
    User.objects.get(id=user_id).delete()
    return HttpResponseRedirect(reverse('admin_pages:manage_users'))
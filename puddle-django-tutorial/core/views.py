from django.shortcuts import render, redirect

from item.models import Category, Item

from .forms import SignupForm

def index(request):
    items = Item.objects.filter(is_sold=False)[:6]
    categories = Category.objects.all()
    context = {'categories': categories, 'items': items}
    return render(request, 'core/index.html', context)

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:login')
        else:
            context = {
                'form': form,
                'error_message': 'Please correct the highlighted fields and try again.',
                'form_errors': form.errors
            }
            return render(request, 'core/signup.html', context)
    form = SignupForm()
    context = {'form': form}
    return render(request, 'core/signup.html', context)
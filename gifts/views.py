from django.shortcuts import render, get_object_or_404, redirect
from .models import Gift, Category, Profile, SavedItem
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Like, Comment



def home(request):
    from django.core.paginator import Paginator

    categories = Category.objects.all()
    qs = Gift.objects.select_related('category').all().order_by('-created_at')
    cat = request.GET.get('category')
    selected_cat = None
    if cat:
        qs = qs.filter(category__id=cat)
        try:
            selected_cat = int(cat)
        except Exception:
            selected_cat = None
    paginator = Paginator(qs, 12)
    page = request.GET.get('page')
    gifts = paginator.get_page(page)
    return render(request, 'gifts/home.html', {'categories': categories, 'gifts': gifts, 'selected_cat': selected_cat})


@login_required
def profile(request):
    profile = getattr(request.user, 'profile', None)
    saved = SavedItem.objects.filter(user=request.user).select_related('gift')
    return render(request, 'gifts/profile.html', {'profile': profile, 'saved': saved, 'hide_sidebar': True})


@login_required
def edit_profile(request):
    profile = getattr(request.user, 'profile', None)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('gifts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'gifts/edit_profile.html', {'form': form})


@login_required
def toggle_like(request, gift_id):
    gift = get_object_or_404(Gift, id=gift_id)
    like, created = Like.objects.get_or_create(user=request.user, gift=gift)
    if not created:
        like.delete()
        status = 'unliked'
    else:
        status = 'liked'
    return JsonResponse({'status': status, 'likes_count': gift.likes.count()})


@login_required
def toggle_save(request, gift_id):
    gift = get_object_or_404(Gift, id=gift_id)
    saved, created = SavedItem.objects.get_or_create(user=request.user, gift=gift)
    if not created:
        saved.delete()
        status = 'unsaved'
    else:
        status = 'saved'
    return JsonResponse({'status': status})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # create profile
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('gifts:home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def gift_detail(request, gift_id):
    gift = get_object_or_404(Gift, id=gift_id)
    # prepare user's conversations list for client-side quick share (id + label)
    user_convs = []
    if request.user.is_authenticated:
        for c in request.user.conversations.all().order_by('-created_at'):
            others = c.participants.exclude(id=request.user.id)
            other = others.first() if others.exists() else None
            label = other.username if other else f'Розмова {c.id}'
            user_convs.append({'id': c.id, 'label': label})
    return render(request, 'gifts/gift_detail.html', {'gift': gift, 'user_conversations': user_convs})


@require_POST
@login_required
def add_comment(request, gift_id):
    gift = get_object_or_404(Gift, id=gift_id)
    text = request.POST.get('text')
    if text:
        Comment.objects.create(user=request.user, gift=gift, text=text)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

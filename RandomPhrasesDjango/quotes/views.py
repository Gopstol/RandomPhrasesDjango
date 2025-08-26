import random
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Quote
from .forms import QuoteForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages


def random_quote_view(request):
    quotes = Quote.objects.all()
    if not quotes.exists():
        return render(request, "random_quote.html", {"quote": None})

    quotes_list = list(quotes)
    weights = []
    for q in quotes_list:
        ratio = (q.likes - q.dislikes) / max(1, q.views)
        dynamic_weight = max(1, q.weight * (1 + ratio))
        weights.append(dynamic_weight)

    chosen = random.choices(quotes_list, weights=weights, k=1)[0]
    chosen.views += 1
    chosen.save(update_fields=["views"])

    return render(request, "random_quote.html", {"quote": chosen})


@login_required
def add_quote_view(request):
    if request.method == "POST":
        text = request.POST.get("text")
        source = request.POST.get("source")
        weight = request.POST.get("weight")
        if Quote.objects.filter(text=text, source=source).exists():
            return render(request, "add_quote.html", {"error": "Такая цитата уже есть"})
        if Quote.objects.filter(source=source).count() >= 3:
            messages.error(request, "Из одного источника можно добавить не более 3 цитат.")
            return redirect("add_quote")
        Quote.objects.create(text=text, source=source, author=request.user, weight=weight)
        return redirect("random_quote")
    else:
        form = QuoteForm()
    return render(request, "add_quote.html", {"form": form})


@login_required
def like_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    quote.likes += 1
    quote.save(update_fields=["likes"])
    return redirect("random_quote")


@login_required
def dislike_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    quote.dislikes += 1
    quote.save(update_fields=["dislikes"])
    return redirect("random_quote")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("random_quote")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def top_quotes_view(request):
    sort_by = request.GET.get("by", "likes")

    if sort_by == "dislikes":
        quotes = Quote.objects.order_by("-dislikes")[:10]
    elif sort_by == "views":
        quotes = Quote.objects.order_by("-views")[:10]
    elif sort_by == "weight":
        quotes = list(Quote.objects.all())
        for q in quotes:
            ratio = (q.likes - q.dislikes) / max(1, q.views)
            q.dynamic_weight = max(1, q.weight * (1 + ratio))
        quotes = sorted(quotes, key=lambda x: x.dynamic_weight, reverse=True)[:10]
    else:  # likes
        quotes = Quote.objects.order_by("-likes")[:10]

    return render(request, "top_quotes.html", {"quotes": quotes, "sort_by": sort_by})


@login_required
def profile(request):
    quotes = Quote.objects.filter(author=request.user).order_by("-created_at")
    return render(request, "profile.html", {"quotes": quotes})


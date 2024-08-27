from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
import random

def index(request):
    return render(request, "wiki/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "wiki/error.html", {
            "message": "The requested page was not found."
        })
    return render(request, "wiki/entry.html", {
        "title": title,
        "content": util.convert_markdown_to_html(content)
    })

def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    if query in entries:
        return redirect("entry", title=query)
    results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "wiki/search.html", {
        "results": results,
        "query": query
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if util.get_entry(title) is not None:
            return render(request, "wiki/new_page.html", {
                "error": "An entry with this title already exists."
            })
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "wiki/new_page.html")

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect("entry", title=title)
    content = util.get_entry(title)
    if content is None:
        return render(request, "wiki/error.html", {
            "message": "The requested page was not found."
        })
    return render(request, "wiki/edit_page.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect("entry", title=random_entry)

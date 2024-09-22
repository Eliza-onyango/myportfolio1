from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from . import util
import markdown2
import random


def entry(request, title):
    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    
    # Convert Markdown to HTML
    content_html = markdown2.markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content_html
    })
def search(request):
    query = request.GET.get('q', '').lower()
    entries = util.list_entries()

    # Filter entries that contain the search query
    search_results = [entry for entry in entries if query in entry.lower()]

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": search_results
    })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def create_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title):
            return render(request, "encyclopedia/create.html", {
                "error": "Page with this title already exists."
            })
        util.save_entry(title, content)
        return redirect('entry', title=title)
    return render(request, "encyclopedia/create.html")
def edit_page(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        new_content = request.POST.get("content")
        util.save_entry(title, new_content)
        return redirect('entry', title=title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })


def random_page(request):
    entries = util.list_entries()  # Get all available entries
    if entries:
        random_entry = random.choice(entries)  # Pick a random entry
        return redirect('entry', title=random_entry)  # Redirect to the selected entry page
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries available."
        })

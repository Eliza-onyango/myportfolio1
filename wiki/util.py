import os
import re
import markdown2
from django.conf import settings

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    filenames = os.listdir(os.path.join(settings.BASE_DIR, "entries"))
    return list(sorted(re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md")))

def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown content.
    """
    filename = f"entries/{title}.md"
    with open(os.path.join(settings.BASE_DIR, filename), "w") as f:
        f.write(content)

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. Returns None if no such entry exists.
    """
    try:
        with open(os.path.join(settings.BASE_DIR, f"entries/{title}.md")) as f:
            return f.read()
    except FileNotFoundError:
        return None

def convert_markdown_to_html(content):
    """
    Converts Markdown content to HTML.
    """
    return markdown2.markdown(content)

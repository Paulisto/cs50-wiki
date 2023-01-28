from django.http.response import HttpResponse
from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
import re
from random import choice
import markdown2

# Home page (index)
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Entry page
def entry(request, TITLE):
    
    content = util.get_entry(TITLE)
    
    if content:
        
        return render(request, "encyclopedia/entry.html", {
            "title": TITLE,
            "content": markdown2.markdown(content)
        })

    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Sorry, this page cannot be found!!!"
        })

# Search
def search(request):

    q = request.GET['q']
    content = util.get_entry(q)

    if content:
        return HttpResponseRedirect(reverse('wiki_entry', args=[q]))

    else:
        entries = util.list_entries()
        possibilities = []
        string = re.compile("(?i)(" + q + ")")
        for entry in entries:
            if string.search(entry):
                possibilities.append(entry)

        return render(request, "encyclopedia/search.html", {
            "string": q,
            "possibilities": possibilities
        })

# Form for filling in a new entry
class NewPageForm(forms.Form):
    title = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'class':'form-control w-75 mb-2'}))
    textarea  = forms.CharField(label="Description:", widget=forms.Textarea(attrs={'class':'form-control w-75'}),)

# New page
def newpage (request):

    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            markdown = form.cleaned_data["textarea"]
        
            if (util.get_entry(title)):
                return render(request, "encyclopedia/error.html",{
                    "message": "This entry already exists."
                })
            else:
                util.save_entry(title, markdown)
                return HttpResponseRedirect(reverse("wiki_entry", args=[title]))

    else:
        return render(request, "encyclopedia/new_page.html",{
            "form": NewPageForm()
        })               

# Form for editing the an entry
class EditPageForm(forms.Form):
    edit_content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'cols': '90'}), label="Description")

def editpage(request, title):
    
    form = EditPageForm(initial={'edit_content': util.get_entry(title)})
    
    if request.method == "POST":
        update = EditPageForm(request.POST)

        if update.is_valid():
            newcontent = update.cleaned_data["edit_content"]

            util.save_entry(title, newcontent)
            return HttpResponseRedirect(reverse('wiki_entry', args=[title]))

    else:

        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "form": form
        })       

# Will lead to random entry
def random (request):

    title = choice(util.list_entries())

    return HttpResponseRedirect(reverse('wiki_entry', args=[title]))
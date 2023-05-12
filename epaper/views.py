from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from .forms import *

class EPaperView(FormView):
    template_name = "epaper/epaper.html"

    form_class = EPaperForm
    success_url = '/epaper/thanks/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if not EPaperEmail.objects.filter(email=self.object.email):
            self.object.save()
        return super().form_valid(form)
    
class EPaperThanksView(TemplateView):
    template_name = "epaper/thanks.html"
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView
from django.views import View


class IndexView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class AddView(FormView):
    template_name = "add.html"
    form_class = 

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class EditView(FormView):
    template_name = "edit.html"

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic, View

from Barnyard_Web.barnyard.forms import ItemForm
from Barnyard_Web.barnyard.sheets import utils


class IndexView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class AddView(generic.FormView):
    form_class = ItemForm
    success_url = "/"
    template_name = "add.html"

    def form_valid(self, form_object):
        form = form_object.cleaned_data

        if form["price"] and form["quantity"] is not None and \
           form["on_robot"] is not None and form["exempt"] is not None and \
           form["asap"] is not None and form["order_link"] is not None:
            utils.add_part_bom(form["name"], form["description"],
                               form["location"], form["image_url"],
                               form["component_group"], form["price"],
                               form["quantity"], form["on_robot"],
                               form["exempt"], form["asap"], form["order_link"])
        else:
            utils.add_part(form["name"], form["description"], form["location"],
                           form["image_url"], form["component_group"])

        return super().form_valid(form_object)

    def post(self, request, *args, **kwargs):
        # the scientists were so preoccupied with whether they could,
        # they didn't consider whether they should.
        form = self.form_class(request.POST)

        if form.is_valid():
            self.form_valid(form)

            return redirect("/")
        else:
            return render(request, self.template_name, {"form": self.form_class})


class ListView(generic.ListView):
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)

        context["parts"] = utils.get_parts(utils.get_setting("Default part limit in ListView"))

        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

from datetime import date
from django import forms

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path

from django.contrib.admin.widgets import AdminDateWidget


class ReportsForm(forms.Form):
    start_date = forms.DateField(
        initial=date.today().strftime('%d-%m-%Y'), 
        required=True,
        label="Fecha Inicial",
        widget=forms.DateInput(attrs={"type": "date"}, format='%d-%m-%Y'),
        # widget=forms.SelectDateWidget(),
    )
    end_date = forms.DateField(
        initial=date.today().strftime('%d-%m-%Y'), 
        label="Fecha Final",
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}, format='%d-%m-%Y'),
    )


class CustomAdminSite(admin.AdminSite):
    site_header = "Administración de Mechatronics House"
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("reportes/", self.admin_view(self.reports_view), name="reportes")]
        
        return my_urls + urls

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        if app_label is None or app_label == 'general':
            app_list.append(
                {
                    "name": "General",
                    "app_label": "general",
                    "models": [
                        {
                            "name": "Reportes",
                            "object_name": "reportes",
                            "admin_url": "/admin/reportes",
                            "view_only": True,
                        }
                    ],
                }
            )
        
        return app_list

    def reports_view(self, request):

        if request.method == 'GET':
            form = ReportsForm()
    
            data = {
                "text": "Hello Admin",
            }

            context = {
                "data": data,
                "form": form,
                "page_name": "Reportes",
                "app_list": self.get_app_list(request),
                **self.each_context(request),
            }

        elif request.method == 'POST':
            form = ReportsForm(request.POST)

            if form.is_valid():

                start_date = form.cleaned_data["start_date"]
                end_date = form.cleaned_data["end_date"]

                data = {
                    'start_date': start_date,
                    'end_date': end_date
                }

                context = {
                    "data": data,
                    "form": form,
                    "page_name": "Reportes",
                    "app_list": self.get_app_list(request),
                    **self.each_context(request),
                }

            # else:
            #     print('ERROR ERROR ERROR ERROR ERROR')
            #     print(form)

        print("****************************************************")

        return TemplateResponse(request, 'admin/reportes.html', context)

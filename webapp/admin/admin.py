from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path


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
        data = {
            "text": "Hello Admin",
        }
        context = {
            "data": data,
            "page_name": "Reportes",
            "app_list": self.get_app_list(request),
            **self.each_context(request),
        }

        return TemplateResponse(request, 'admin/reportes.html', context)

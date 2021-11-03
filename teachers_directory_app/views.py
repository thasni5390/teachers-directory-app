from django.shortcuts import redirect
from django.views import View


class Index(View):
    def get(self, request, *args, **kwargs):
        return redirect('teachers_list')

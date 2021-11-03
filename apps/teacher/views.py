import csv
from io import StringIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from apps.teacher.forms import TeachersModelForm, AdvancedFilterForm, TeacherForm
from apps.teacher.models import Teacher, Subject
import zipfile


class TeachersList(ListView):
    model = Teacher

    paginate_by = 5  # this variable is used for pagination

    def get_queryset(self):
        subject = self.request.GET.get('subject', None)
        first_name = self.request.GET.get('first_name', None)
        last_name = self.request.GET.get('last_name', None)
        query = {}
        if subject:
            query['subjects__in'] = [subject]
        if first_name:
            query['first_name__istartswith'] = first_name
        if last_name:
            query['last_name__istartswith'] = last_name
        return self.model.objects.filter(**query)

    def get_context_data(self, **kwargs):
        context = super(TeachersList, self).get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['advanced_filter_form'] = AdvancedFilterForm(self.request.GET)
        return context


class TeacherDetail(DetailView):
    model = Teacher


class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject_list'] = Subject.objects.all()
        return context

class TeacherUpdateView(UpdateView):
    model = Teacher
    form_class = TeacherForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject_list'] = Subject.objects.all()
        return context



@method_decorator(login_required, name='dispatch')
class TeachersBulkUpload(View):
    template_name = 'teacher/bulk_upload.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        success_count = 0
        error_count = 0
        csv_header_mapper = {
            'First Name': 'first_name',
            'Last Name': 'last_name',
            'Profile picture': 'profile_picture',
            'Email Address': 'email',
            'Phone Number': 'phone_number',
            'Room Number': 'room_number',
            'Subjects taught': 'subjects'
        }
        file = request.FILES.get('file', None)
        imagezip = request.FILES.get('imagezip', None)
        uploaded_images = []
        if imagezip and zipfile.is_zipfile(imagezip.file):
            zfile = zipfile.ZipFile(imagezip.file)
            uploaded_images = zfile.namelist()
        data_list = []
        if not file:
            messages.error(self.request, 'No file uploaded. Please upload a file')
            return redirect('teachers_bulk_upload')
        else:
            try:
                csvf = StringIO(file.read().decode())
                for row in csv.DictReader(csvf, delimiter=","):
                    if row.get('Email Address', None):
                        data = {}
                        try:
                            for key, value in csv_header_mapper.items():
                                if value == 'subjects':
                                    data[value] = row[key].split(',')
                                else:
                                    data[value] = row[key]
                        except:
                            messages.error(self.request, "Incorrect csv header format")
                            return redirect('teachers_bulk_upload')
                        form = TeachersModelForm(data)
                        if form.is_valid():
                            obj = form.save(commit=False)
                            profile_pic = data.get('profile_picture', None)
                            if profile_pic and profile_pic in uploaded_images:
                                obj.profile_picture.save(profile_pic, ContentFile(zfile.read(profile_pic)), save=True)
                            obj.created_by = request.user
                            obj.save()
                            obj.subjects.add(*form.cleaned_data.get('subjects'))
                            success_count += 1
                            data['status'] = "success"
                            data['message'] = ""
                        else:
                            error_count += 1
                            data['status'] = "failed"
                            data['message'] = form.errors
                        data_list.append(data)
                messages.success(self.request, f'Successfully uploaded {success_count} data. Rejected {error_count}')
            except Exception as e:
                messages.error(self.request, f'Error in processing the file please check the uploaded files format')
        return render(request, self.template_name, context={'data': data_list})

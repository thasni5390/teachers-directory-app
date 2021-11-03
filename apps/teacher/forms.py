from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django.core.exceptions import ValidationError

from apps.teacher.models import Teacher, Subject


class TeachersModelForm(forms.ModelForm):
    subjects = SimpleArrayField(forms.CharField(max_length=100), required=False)

    class Meta:
        model = Teacher
        exclude = ['created_by', 'created_at', 'modified_at']

    def __init__(self, *args, **kwargs):
        super(TeachersModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def get_subjects(self):
        return self.cleaned_data.get('subjects', None)

    def clean_subjects(self):
        subjects = self.get_subjects()
        if subjects:
            subjects = [subject.title().strip() for subject in subjects]
            objs = (Subject(name='%s' % subject) for subject in subjects)
            Subject.objects.bulk_create(objs, ignore_conflicts=True)
            if len(subjects) > 5:
                raise ValidationError(
                f"A teacher can teach no more than 5 subjects"
            )
        return Subject.objects.filter(name__in=subjects)


class TeacherForm(TeachersModelForm):

    def get_subjects(self):
        return self.data.getlist('subjects', None)


def get_subject_choices():
    return [('', 'Any')] + [(subject.pk, subject.name) for subject in Subject.objects.all()]


class AdvancedFilterForm(forms.Form):
    first_name = forms.CharField(required=False, label='First Name Starts With')
    last_name = forms.CharField(required=False, label='Last Name Starts With')
    subject = forms.ChoiceField(required=False, choices=get_subject_choices, label='Select Subject')

    def __init__(self, *args, **kwargs):
        super(AdvancedFilterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

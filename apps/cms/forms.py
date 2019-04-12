
from apps.forms import FormMixin
from django import forms
from apps.news.models import News,Banners
from apps.course.models import Course



class EditNewsCategroyForm(forms.Form):
    pk = forms.IntegerField(error_messages={'require':'必须传入分类的ID'})
    name = forms.CharField(max_length=100)


class writeNewsForm(forms.ModelForm,FormMixin):
    categroy = forms.IntegerField()
    class Meta:
        model = News
        exclude = ['categroy','author','pub_tiem']

class addBannersForm(forms.ModelForm,FormMixin):
    class Meta:
        model = Banners
        fields = ('priority','link_to','image_url')

class editBannerForm(forms.ModelForm,FormMixin):
    pk = forms.IntegerField()
    class Meta:
        model = Banners
        fields = ('priority','link_to','image_url')

class pubCourseForm(forms.ModelForm,FormMixin):
    categroy_id = forms.IntegerField()
    teacher_id = forms.IntegerField()
    class Meta:
        model = Course
        exclude = ['categroy','teacher']




from django import forms
from guestbook.models import Guestbook_Post,Guestbook_Category
from taggit.models import Tag
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostForm(forms.ModelForm):
    title = forms.CharField(label='标题',max_length=128)   
    content = forms.CharField(label='内容',widget = CKEditorUploadingWidget(config_name='guestbook'))
    category = forms.ModelChoiceField(label='分类',queryset=Guestbook_Category.objects.all()) 
    #tags = forms.ModelMultipleChoiceField(label='标签(选填)',queryset=Tag.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={'class':'checkbox'}),required=False)
    
    class Meta:
        model = Guestbook_Post
        fields = ('title','tags','content','category')
    def clean(self):
        cleanedData = self.cleaned_data
        title = cleanedData.get('title')
        content = cleanedData.get('content')
        bans = ('草你妈','傻逼','caonima','fuck','你妈')
        for ban in bans:
            # If title and content were not find ban word return cleanedData
            # The find funtion is not find ban word will output -1
            if title.find(ban)==-1 and content.find(ban)==-1:
                pass
            else:
                raise forms.ValidationError(('标题或正文含有违禁词'+'(' + ban + ')'),code = 'invalid')
        return cleanedData
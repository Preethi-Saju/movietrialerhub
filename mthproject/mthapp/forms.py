from django import forms
from . models import Post,Comment,Category
from django.contrib.auth.models import User


class PForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['moviename','descriptions','category','actors_name','youtube_link','images','rdate']

    def __init__(self, *args, **kwargs):
        super(PForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
class Postform(forms.ModelForm):
    CATEGORY_CHOICES = (
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Thriller', 'Thriller'),
        # Add more categories if needed
    )

    # Override the categories field to use a dropdown list
    categories = forms.ChoiceField(choices=CATEGORY_CHOICES)
    class Meta:
        model=Post
        fields=['moviename','descriptions','categories','actors_name','youtube_link','images','rdate']

class Commentformm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
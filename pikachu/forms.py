from django import forms
from .models import UserModel,PostModel, LikeModel, CommentModel

#SignUp Page Form
class SignupForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['email','name','username','password']

#Login Page Form
class LoginForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username','password']

#Post Page Form
class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields=['image', 'caption']

#Like Page Form
class LikeForm(forms.ModelForm):

    class Meta:
        model = LikeModel
        fields=['post']

#Comment Page Form
class CommentForm(forms.ModelForm):

    class Meta:
        model = CommentModel
        fields = ['comment_text', 'post']
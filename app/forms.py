from django.contrib.auth.forms import AuthenticationForm


class CleanForm(AuthenticationForm):

    def clean_username(self):
        return self.cleaned_data['username'].lower()

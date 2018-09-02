from django import forms
from accounts.models import Staff, Student

class StaffSignupForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password",
        widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
        widget=forms.PasswordInput)

    class Meta:
        model = Staff
        fields = ("username","email","first_name","last_name","phone_number")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, school, commit=True):
        staff = super(StaffSignupForm, self).save(commit=False)
        staff.set_password(self.cleaned_data["password1"])
        staff.is_super_staff = False
        staff.is_active = True
        staff.staff_school = school
        if commit:
            staff.save()

        return staff


class StudentCreationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
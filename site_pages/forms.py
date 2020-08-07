from django import forms

class EmailContactForm(forms.Form):

    viewer_email = forms.EmailField(
        label=False,
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your email address'
        })
    )

class PrayerRequestForm(forms.Form):

    name = forms.CharField(
        label='Individual to pray for',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Individual\'s Name'
        })
    )

    comment = forms.CharField(
        label='Comment',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '4',
            'cols': '40',
            'placeholder': 'Anything you would like for us to know.'
        })
    )


class ViewerContactForm(forms.Form):

    fname = forms.CharField(
        label='* First Name',
        required=True
    )

    lname = forms.CharField(
        label='Last Name',
        required=False
    )

    email = forms.EmailField(
        label='* Your Email Address',
        required=True
    )

    comment = forms.CharField(
        label='Comment',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '4',
            'cols': '40',
            'placeholder': ('Anything you would like for us to know.')
        })
    )

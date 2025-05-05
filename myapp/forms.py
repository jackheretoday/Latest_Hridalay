from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, DoctorProfile, PatientProfile, HeartDiseasePrediction
from django.core.validators import RegexValidator

class DoctorSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )],
        required=True
    )
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    gender = forms.ChoiceField(
        choices=DoctorProfile.GENDER_CHOICES,
        required=True
    )
    medical_license_number = forms.CharField(max_length=100, required=True)
    SPECIALIZATION_CHOICES = [
        ('General Cardiology', 'General Cardiology'),
        ('Interventional Cardiology', 'Interventional Cardiology'),
        ('Electrophysiology', 'Electrophysiology'),
        ('Cardiac Surgery', 'Cardiac Surgery'),
        ('Pediatric Cardiology', 'Pediatric Cardiology'),
        ('Cardiac Imaging', 'Cardiac Imaging'),
        ('Heart Failure & Transplant', 'Heart Failure & Transplant'),
        ('Preventive Cardiology', 'Preventive Cardiology'),
        ('Cardiac Rehabilitation', 'Cardiac Rehabilitation'),
        ('Cardiac Anesthesiology', 'Cardiac Anesthesiology'),
        ('Cardiac Critical Care', 'Cardiac Critical Care'),
        ('Cardiac Electrophysiology', 'Cardiac Electrophysiology'),
        ('Cardiac Pathology', 'Cardiac Pathology'),
        ('Cardiac Radiology', 'Cardiac Radiology'),
        ('Cardiac Research', 'Cardiac Research'),
        ('Cardiac Nursing', 'Cardiac Nursing'),
        ('Cardiac Physiotherapy', 'Cardiac Physiotherapy'),
        ('Cardiac Nutrition', 'Cardiac Nutrition'),
        ('Cardiac Psychology', 'Cardiac Psychology'),
        ('Cardiac Genetics', 'Cardiac Genetics'),
    ]
    specialization = forms.ChoiceField(
        choices=SPECIALIZATION_CHOICES,
        required=True
    )
    years_of_experience = forms.IntegerField(
        min_value=0,
        max_value=50,
        required=True
    )
    hospital_name = forms.CharField(max_length=100, required=False)
    license_document = forms.FileField(
        required=True,
        help_text='Upload your medical license document (PDF, JPG, PNG)',
        widget=forms.FileInput(attrs={'accept': '.pdf,.jpg,.jpeg,.png'})
    )
    education = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text='Enter your medical education details'
    )
    consultation_fee = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        help_text='Enter your consultation fee in INR'
    )
    available_days = forms.CharField(
        max_length=200,
        required=False,
        help_text='Enter your available days (e.g., Monday-Friday)'
    )
    available_hours = forms.CharField(
        max_length=100,
        required=False,
        help_text='Enter your available hours (e.g., 9:00 AM - 5:00 PM)'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number',
                 'password1', 'password2', 'dob', 'gender', 'medical_license_number',
                 'specialization', 'years_of_experience', 'hospital_name',
                 'license_document', 'education', 'consultation_fee',
                 'available_days', 'available_hours')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add help text to username field
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        # Add help text to password fields
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters.'
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'doctor'
        if commit:
            user.save()
            # Create the doctor profile
            DoctorProfile.objects.create(
                user=user,
                dob=self.cleaned_data['dob'],
                gender=self.cleaned_data['gender'],
                medical_license_number=self.cleaned_data['medical_license_number'],
                specialization=self.cleaned_data['specialization'],
                years_of_experience=self.cleaned_data['years_of_experience'],
                hospital_name=self.cleaned_data.get('hospital_name'),
                license_document=self.cleaned_data['license_document'],
                education=self.cleaned_data.get('education'),
                consultation_fee=self.cleaned_data.get('consultation_fee'),
                available_days=self.cleaned_data.get('available_days'),
                available_hours=self.cleaned_data.get('available_hours')
            )
        return user

class SimplePatientSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(
        required=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = 'patient'
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class HeartDiseasePredictionForm(forms.Form):
    age = forms.IntegerField(
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    sex = forms.ChoiceField(
        choices=[(0, 'Female'), (1, 'Male')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cp = forms.ChoiceField(
        choices=[
            (0, 'Typical Angina'),
            (1, 'Atypical Angina'),
            (2, 'Non-anginal Pain'),
            (3, 'Asymptomatic')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    trestbps = forms.IntegerField(
        label='Resting Blood Pressure (mm Hg)',
        min_value=90,
        max_value=200,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    chol = forms.IntegerField(
        label='Serum Cholesterol (mg/dl)',
        min_value=100,
        max_value=600,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    fbs = forms.ChoiceField(
        label='Fasting Blood Sugar > 120 mg/dl',
        choices=[(0, 'No'), (1, 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    restecg = forms.ChoiceField(
        label='Resting ECG Results',
        choices=[
            (0, 'Normal'),
            (1, 'ST-T Wave Abnormality'),
            (2, 'Left Ventricular Hypertrophy')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    thalach = forms.IntegerField(
        label='Maximum Heart Rate',
        min_value=60,
        max_value=220,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    exang = forms.ChoiceField(
        label='Exercise Induced Angina',
        choices=[(0, 'No'), (1, 'Yes')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    oldpeak = forms.FloatField(
        label='ST Depression',
        min_value=0.0,
        max_value=6.2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    slope = forms.ChoiceField(
        label='Slope of Peak Exercise ST Segment',
        choices=[
            (0, 'Upsloping'),
            (1, 'Flat'),
            (2, 'Downsloping')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    ca = forms.ChoiceField(
        label='Number of Major Vessels',
        choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    thal = forms.ChoiceField(
        label='Thalassemia',
        choices=[
            (1, 'Normal'),
            (2, 'Fixed Defect'),
            (3, 'Reversible Defect')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class PatientSearchForm(forms.Form):
    """Form for searching patients by username."""
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter patient username'
        })
    )


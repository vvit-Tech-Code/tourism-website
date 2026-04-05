from django import forms
from .models import Destination, LocalGuide, Homestay

class DestinationForm(forms.ModelForm):
    state = forms.ChoiceField(
        choices=[
            ('Andhra Pradesh', 'Andhra Pradesh'),
            ('Telangana', 'Telangana'),
            ('Karnataka', 'Karnataka'),
            ('Tamil Nadu', 'Tamil Nadu'),
            ('Kerala', 'Kerala'),
            ('Maharashtra', 'Maharashtra'),
            ('Jharkhand', 'Jharkhand')
        ],
        initial='Jharkhand',
        widget=forms.Select(attrs={'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 font-bold text-emerald-900'})
    )

    class Meta:
        model = Destination
        fields = [
            'name', 'state', 'category', 'description', 'history', 
            'latitude', 'longitude', 'best_time', 'visiting_time', 'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium'}),
            'category': forms.Select(attrs={'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 font-bold text-emerald-900'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium'}),
            'history': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium'}),
            'latitude': forms.NumberInput(attrs={'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium', 'id': 'id_latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium', 'id': 'id_longitude'}),
            'best_time': forms.TextInput(attrs={'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium'}),
            'visiting_time': forms.TextInput(attrs={'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium'}),
            'image': forms.ClearableFileInput(attrs={'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-black file:bg-emerald-50 file:text-emerald-700 hover:file:bg-emerald-100'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if self.errors and field_name in self.errors:
                existing_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = existing_class.replace('border-none', 'border-2 border-red-500')

class DestinationModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} ({obj.state})"

class GuideAssignmentForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=15, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': '+91XXXXXXXXXX'})
    )
    destination = DestinationModelChoiceField(
        queryset=Destination.objects.all(),
        empty_label="Select a Destination",
    )

    class Meta:
        model = LocalGuide
        fields = ['destination', 'name', 'phone_number', 'languages', 'fee', 'is_verified']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            classes = 'w-full px-4 py-3 rounded-xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none text-sm font-medium'
            if self.errors and field_name in self.errors:
                classes = classes.replace('border-none', 'border-2 border-red-500')
            field.widget.attrs['class'] = classes

class HomestayForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=15, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': '+91XXXXXXXXXX'})
    )
    destination = DestinationModelChoiceField(
        queryset=Destination.objects.all(),
        empty_label="Select a Destination",
    )

    class Meta:
        model = Homestay
        fields = ['destination', 'name', 'phone_number', 'price_per_night', 'amenities', 'is_verified']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            classes = 'w-full px-4 py-3 rounded-xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none text-sm font-medium'
            if self.errors and field_name in self.errors:
                classes = classes.replace('border-none', 'border-2 border-red-500')
            field.widget.attrs['class'] = classes
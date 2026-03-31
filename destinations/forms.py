from django import forms
from .models import Destination, LocalGuide, Homestay

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = [
            'name', 'state', 'category', 'description', 'history', 
            'latitude', 'longitude', 'best_time', 'visiting_time', 'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium'}),
            'state': forms.TextInput(attrs={'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium'}),
            'category': forms.Select(attrs={'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 font-bold text-emerald-900'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium'}),
            'history': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium'}),
            'latitude': forms.NumberInput(attrs={'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium'}),
            'longitude': forms.NumberInput(attrs={'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium'}),
            'best_time': forms.TextInput(attrs={'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium'}),
            'visiting_time': forms.TextInput(attrs={'class': 'w-full px-6 py-4 rounded-2xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none font-medium'}),
            'image': forms.ClearableFileInput(attrs={'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-black file:bg-emerald-50 file:text-emerald-700 hover:file:bg-emerald-100'}),
        }

class GuideAssignmentForm(forms.ModelForm):
    class Meta:
        model = LocalGuide
        # FIXED: Changed 'contact' to 'phone' to match models.py
        fields = ['destination', 'name', 'phone', 'languages', 'fee', 'is_verified']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none text-sm'
            })

class HomestayForm(forms.ModelForm):
    class Meta:
        model = Homestay
        fields = ['destination', 'name', 'contact', 'price_per_night', 'amenities', 'is_verified']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border-none focus:ring-2 focus:ring-emerald-500 outline-none text-sm'
            })
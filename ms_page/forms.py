from django import forms
from .models import UploadAudio


class UploadAudioForm(forms.ModelForm):
    class Meta:
        model = UploadAudio
        fields = ["audio_file"]

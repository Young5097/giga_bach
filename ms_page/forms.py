from django import forms
from .models import UploadAudio


class UploadAudioForm(forms.ModelForm):
    class Meta:
        model = UploadAudio
        fields = ["audio_file"]

    audio_file = forms.FileField(label="오디오 파일", required=False)

from django.shortcuts import render, redirect
from .forms import DatasetForm

def upload_dataset(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'upload_success.html')
    else:
        form = DatasetForm()
    return render(request, 'upload_dataset.html',{'form':form})


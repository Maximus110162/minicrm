from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .models import Complaint, CustomUser
from .forms import ComplaintForm, CustomUserForm
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth import get_user_model
User = get_user_model()
@login_required
def complaint_list(request):
    query = request.GET.get('q')
    # Оператор видит все жалобы
    if request.user.role == 'operator':
        complaints = Complaint.objects.all()
    else:
        # Специалист бэк-офиса видит только свои жалобы или решенные
        complaints = Complaint.objects.filter(
            Q(assigned_to=request.user) | Q(status='resolved')
        )
    if query:
        complaints = complaints.filter(
            Q(client_account__icontains=query) |
            Q(client_name__icontains=query) |
            Q(client_phone__icontains=query)
        )
    return render(request, 'crm_app/complaint_list.html', {'complaints': complaints, 'query': query})
@login_required
def complaint_create(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            # Найдите специалиста бэк-офиса с наименьшим количеством жалоб
            complaint.created_by = request.user
            back_office_specialist = CustomUser.objects.filter(role='back_office').annotate(num_complaints=Count('assigned_complaints')).order_by('num_complaints').first()
            complaint.assigned_to = back_office_specialist
            complaint.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm()
    return render(request, 'crm_app/complaint_form.html', {'form': form})
# @login_required
# def complaint_edit(request, pk):
#     complaint = get_object_or_404(Complaint, pk=pk)
#     if request.method == 'POST':
#         if request.user.role == 'back_office':
#             form = CommentForm(request.POST, instance=complaint)
#         else:
#             form = ComplaintForm(request.POST, instance=complaint)
        
#         if form.is_valid():
#             form.save()
#             return redirect('complaint_list')
#     else:
#         if request.user.role == 'back_office':
#             form = CommentForm(instance=complaint)
#         else:
#             form = ComplaintForm(instance=complaint)
    
#     return render(request, 'crm_app/complaint_form.html', {'form': form, 'complaint': complaint})
@login_required
def complaint_edit(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)

    if request.method == 'POST':
        if request.user.role == 'back_office':
            form = ComplaintForm(request.POST, instance=complaint, fields=['comments'])
        else:
            form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('complaint_list')
    else:
        if request.user.role == 'back_office':
            form = ComplaintForm(instance=complaint, fields=['comments'])
        else:
            form = ComplaintForm(instance=complaint)
            form.fields['comments'].widget.attrs['readonly'] = True

    return render(request, 'crm_app/complaint_form.html', {'form': form, 'complaint': complaint})
# @login_required
# def complaint_edit(request, pk):
#     complaint = get_object_or_404(Complaint, pk=pk)
#     if request.method == "POST":
#         if request.user.role == 'back_office':
#             form = ComplaintForm(request.POST, instance=complaint, fields=['comments'])
#         else:
#             form = ComplaintForm(request.POST, instance=complaint, exclude_fields=['comments'])
#         if form.is_valid():
#             form.save()
#             return redirect('complaint_list')
#     else:
#         if request.user.role == 'back_office':
#             form = ComplaintForm(instance=complaint, fields=['comments'])
#         else:
#             form = ComplaintForm(instance=complaint, exclude_fields=['comments'])
#     return render(request, 'crm_app/complaint_form.html', {'form': form})
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('complaint_list')
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, 'crm_app/profile_form.html', {'form': form})
@login_required
@require_POST
def update_complaint_status(request):
    complaint_id = request.POST.get('id')
    new_status = request.POST.get('status')
    try:
        complaint = Complaint.objects.get(id=complaint_id)
        if request.user.role == 'back_office' and request.user == complaint.assigned_to:
            complaint.status = new_status
            complaint.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    except Complaint.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Complaint not found'}, status=404)
@login_required
def complaint_update_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST' and request.user.role == 'back_office':
        new_status = request.POST.get('status')
        if new_status in ['open', 'in_progress', 'closed']:
            complaint.status = new_status
            complaint.save()
    return redirect('complaint_list')
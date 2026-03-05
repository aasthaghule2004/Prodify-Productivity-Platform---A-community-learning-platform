from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Task


@login_required
def todo_list(request):
    if request.method == 'POST':
        title = (request.POST.get('title') or '').strip()
        if title:
            Task.objects.create(user=request.user, title=title)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': True})
        return redirect('todo')

    tasks = Task.objects.filter(user=request.user).order_by('-created_at')

    total_count = tasks.count()
    completed_count = tasks.filter(completed=True).count()

    return render(request, 'todo/todo.html', {
        'tasks': tasks,
        'total_count': total_count,
        'completed_count': completed_count
    })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.completed_at = timezone.now() if task.completed else None
    task.save(update_fields=['completed', 'completed_at'])
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'ok': True, 'completed': task.completed})
    return redirect('todo')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'ok': True})
    return redirect('todo')

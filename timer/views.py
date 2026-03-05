import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import FocusSession

@login_required
def timer_view(request):
    time_options = [5,10,15,20,25,30,35,40,45,50,60]
    
    return render(request, 'timer/timer.html', {
        'time_options': time_options
    })


@login_required
@require_POST
def start_session(request):
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload."}, status=400)

    planned_minutes = int(payload.get("planned_minutes", 25))
    planned_minutes = max(1, min(planned_minutes, 600))
    task_name = (payload.get("task_name") or "").strip()[:200]

    session = FocusSession.objects.create(
        user=request.user,
        task_name=task_name,
        planned_minutes=planned_minutes,
    )
    return JsonResponse({"session_id": session.id})


@login_required
@require_POST
def update_session(request):
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload."}, status=400)

    session_id = payload.get("session_id")
    elapsed_seconds = int(payload.get("elapsed_seconds", 0))
    is_completed = bool(payload.get("is_completed", False))

    if not session_id:
        return JsonResponse({"error": "Missing session_id."}, status=400)

    session = get_object_or_404(FocusSession, id=session_id, user=request.user)
    session.elapsed_seconds = max(session.elapsed_seconds, max(elapsed_seconds, 0))

    if is_completed:
        session.completed = True
        if not session.ended_at:
            session.ended_at = timezone.now()

    session.save(update_fields=["elapsed_seconds", "completed", "ended_at"])
    return JsonResponse({"ok": True})

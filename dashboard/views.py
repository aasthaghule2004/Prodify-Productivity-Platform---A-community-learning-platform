from calendar import monthrange
from datetime import datetime, time, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.db.models.functions import ExtractHour, TruncDate
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET

from timer.models import FocusSession
from todo.models import Task


def _parse_selected_date(date_str):
    if not date_str:
        return timezone.localdate()
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return timezone.localdate()


def _aware_start(date_obj):
    return timezone.make_aware(datetime.combine(date_obj, time.min))


@login_required
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html', {"default_date": timezone.localdate().isoformat()})


@login_required
@require_GET
def dashboard_metrics(request):
    range_type = request.GET.get("range", "week").lower()
    if range_type not in {"day", "week", "month"}:
        range_type = "week"
    selected_date = _parse_selected_date(request.GET.get("date"))

    if range_type == "day":
        start_date = selected_date
        end_date = selected_date + timedelta(days=1)
        start_dt, end_dt = _aware_start(start_date), _aware_start(end_date)
        labels = [f"{hour:02d}:00" for hour in range(24)]
        study_map = {hour: 0 for hour in range(24)}
        task_map = {hour: 0 for hour in range(24)}

        study_rows = (
            FocusSession.objects.filter(user=request.user, started_at__gte=start_dt, started_at__lt=end_dt)
            .annotate(bucket=ExtractHour("started_at"))
            .values("bucket")
            .annotate(total=Sum("elapsed_seconds"))
        )
        for row in study_rows:
            study_map[int(row["bucket"])] = int(row["total"] or 0)

        task_rows = (
            Task.objects.filter(
                user=request.user,
                completed=True,
                completed_at__isnull=False,
                completed_at__gte=start_dt,
                completed_at__lt=end_dt,
            )
            .annotate(bucket=ExtractHour("completed_at"))
            .values("bucket")
            .annotate(total=Count("id"))
        )
        for row in task_rows:
            task_map[int(row["bucket"])] = int(row["total"] or 0)

        study_seconds = [study_map[idx] for idx in range(24)]
        tasks_done = [task_map[idx] for idx in range(24)]

    elif range_type == "week":
        start_date = selected_date - timedelta(days=selected_date.weekday())
        end_date = start_date + timedelta(days=7)
        start_dt, end_dt = _aware_start(start_date), _aware_start(end_date)

        labels = [(start_date + timedelta(days=i)).strftime("%a %d") for i in range(7)]
        keys = [start_date + timedelta(days=i) for i in range(7)]
        study_map = {d: 0 for d in keys}
        task_map = {d: 0 for d in keys}

        study_rows = (
            FocusSession.objects.filter(user=request.user, started_at__gte=start_dt, started_at__lt=end_dt)
            .annotate(bucket=TruncDate("started_at"))
            .values("bucket")
            .annotate(total=Sum("elapsed_seconds"))
        )
        for row in study_rows:
            study_map[row["bucket"]] = int(row["total"] or 0)

        task_rows = (
            Task.objects.filter(
                user=request.user,
                completed=True,
                completed_at__isnull=False,
                completed_at__gte=start_dt,
                completed_at__lt=end_dt,
            )
            .annotate(bucket=TruncDate("completed_at"))
            .values("bucket")
            .annotate(total=Count("id"))
        )
        for row in task_rows:
            task_map[row["bucket"]] = int(row["total"] or 0)

        study_seconds = [study_map[d] for d in keys]
        tasks_done = [task_map[d] for d in keys]

    else:
        start_date = selected_date.replace(day=1)
        days = monthrange(selected_date.year, selected_date.month)[1]
        end_date = start_date + timedelta(days=days)
        start_dt, end_dt = _aware_start(start_date), _aware_start(end_date)

        labels = [str(i) for i in range(1, days + 1)]
        keys = [start_date + timedelta(days=i - 1) for i in range(1, days + 1)]
        study_map = {d: 0 for d in keys}
        task_map = {d: 0 for d in keys}

        study_rows = (
            FocusSession.objects.filter(user=request.user, started_at__gte=start_dt, started_at__lt=end_dt)
            .annotate(bucket=TruncDate("started_at"))
            .values("bucket")
            .annotate(total=Sum("elapsed_seconds"))
        )
        for row in study_rows:
            study_map[row["bucket"]] = int(row["total"] or 0)

        task_rows = (
            Task.objects.filter(
                user=request.user,
                completed=True,
                completed_at__isnull=False,
                completed_at__gte=start_dt,
                completed_at__lt=end_dt,
            )
            .annotate(bucket=TruncDate("completed_at"))
            .values("bucket")
            .annotate(total=Count("id"))
        )
        for row in task_rows:
            task_map[row["bucket"]] = int(row["total"] or 0)

        study_seconds = [study_map[d] for d in keys]
        tasks_done = [task_map[d] for d in keys]

    study_hours = [round(seconds / 3600, 2) for seconds in study_seconds]
    total_hours = round(sum(study_hours), 2)
    total_tasks = int(sum(tasks_done))

    return JsonResponse(
        {
            "labels": labels,
            "study_hours": study_hours,
            "tasks_done": tasks_done,
            "totals": {
                "hours": total_hours,
                "tasks": total_tasks,
                "avg_daily_hours": round(total_hours / max(len(labels), 1), 2),
            },
            "range": range_type,
            "selected_date": selected_date.isoformat(),
        }
    )

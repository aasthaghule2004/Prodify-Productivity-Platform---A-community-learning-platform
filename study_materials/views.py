from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Folder, StudyMaterial


@login_required
def folders_list(request):
    if request.method == "POST":
        name = request.POST.get("folder_name")
        if name:
            Folder.objects.create(user=request.user, name=name)
        return redirect("folders")

    folders = Folder.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "study_materials/folders.html", {"folders": folders})




@login_required
def folder_detail(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)

    #PDF Upload
    if request.method == "POST":
        title = request.POST.get("title")
        pdf_file = request.FILES.get("pdf_file")

        if title and pdf_file:
            StudyMaterial.objects.create(
                folder=folder,
                title=title,
                pdf_file=pdf_file
            )
            return redirect("folder_detail", folder_id=folder.id)

    #materials
    materials = folder.materials.all().order_by("-uploaded_at")

    selected_pdf = None
    pdf_id = request.GET.get("pdf")

    if pdf_id:
        selected_pdf = get_object_or_404(
            StudyMaterial,
            id=pdf_id,
            folder__user=request.user
        )

    return render(request, "study_materials/folder_detail.html", {
        "folder": folder,
        "materials": materials,
        "selected_pdf": selected_pdf,
    })
@login_required
def delete_material(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id, folder__user=request.user)
    folder_id = material.folder.id
    material.delete()
    return redirect("folder_detail", folder_id=folder_id)


@login_required
def toggle_pin(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id, folder__user=request.user)
    material.is_pinned = not material.is_pinned
    material.save()
    return redirect("folder_detail", folder_id=material.folder.id)
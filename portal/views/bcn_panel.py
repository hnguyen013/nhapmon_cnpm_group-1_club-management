@login_required(login_url="portal:auth:login")
def event_create(request):
    club = _get_bcn_club_or_403(request.user)

    if request.method == "POST":
        form = BCNEventCreateForm(request.POST)
        if form.is_valid():
            ev = form.save(commit=False)
            ev.club = club
            # giữ nguyên dòng cũ (không ảnh hưởng nếu model không có field)
            ev.created_by = request.user
            ev.save()
            messages.success(request, "Tạo sự kiện thành công.")
            return redirect("portal:bcn_panel:event_list")
    else:
        form = BCNEventCreateForm()

    return render(request, "portal/bcn_panel/event_form.html", {"form": form, "club": club})


# =========================
# ✅ US-C3.3 — Huỷ sự kiện (soft cancel) + xác nhận trước
# =========================
@login_required(login_url="portal:auth:login")
def event_cancel_confirm(request, event_id: int):
    club = _get_bcn_club_or_403(request.user)
    event = get_object_or_404(Event, id=event_id, club=club)

    # Nếu đã huỷ rồi thì quay lại danh sách, tránh thao tác lặp
    if getattr(event, "is_cancelled", False):
        messages.info(request, "Sự kiện này đã được huỷ trước đó.")
        return redirect("portal:bcn_panel:event_list")

    return render(
        request,
        "portal/bcn_panel/event_cancel_confirm.html",
        {"club": club, "event": event},
    )


@login_required(login_url="portal:auth:login")
def event_cancel(request, event_id: int):
    """
    Chỉ nhận POST để đảm bảo có xác nhận (AC1).
    Huỷ mềm: set is_cancelled=True (AC3).
    """
    club = _get_bcn_club_or_403(request.user)
    event = get_object_or_404(Event, id=event_id, club=club)

    if request.method != "POST":
        return redirect("portal:bcn_panel:event_cancel_confirm", event_id=event.id)

    if getattr(event, "is_cancelled", False):
        messages.info(request, "Sự kiện này đã được huỷ trước đó.")
        return redirect("portal:bcn_panel:event_list")

    event.is_cancelled = True
    event.save(update_fields=["is_cancelled"])

    messages.success(request, "✅ Đã huỷ sự kiện (không xoá dữ liệu).")
    return redirect("portal:bcn_panel:event_list")


# =========================
# ✅ Sửa sự kiện
# =========================
@login_required(login_url="portal:auth:login")
def event_edit(request, event_id: int):
    club = _get_bcn_club_or_403(request.user)

    # AC2: BCN chỉ sửa event thuộc CLB của mình
    event = get_object_or_404(Event, id=event_id, club=club)

    if request.method == "POST":
        form = BCNEventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật sự kiện thành công.")
            return redirect("portal:bcn_panel:event_list")
    else:
        form = BCNEventEditForm(instance=event)

    return render(
        request,
        "portal/bcn_panel/event_edit.html",
        {"form": form, "event": event, "club": club},
    )

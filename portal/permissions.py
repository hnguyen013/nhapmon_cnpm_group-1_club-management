# portal/permissions.py
from django.core.exceptions import PermissionDenied

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

def is_bcn(user):
    # BCN = user có bcn_profile (vì bạn đang dùng BCNProfile)
    return user.is_authenticated and hasattr(user, "bcn_profile")

def bcn_club_id(user):
    # BCN được gán 1 club qua BCNProfile.club
    if not is_bcn(user):
        return None
    return getattr(user.bcn_profile, "club_id", None)

def ensure_club_access(user, club_id: int):
    """
    AC4: check quyền trước mọi thao tác theo club_id
    """
    if is_admin(user):
        return
    if is_bcn(user) and bcn_club_id(user) == club_id:
        return
    raise PermissionDenied("Bạn không có quyền truy cập CLB này.")

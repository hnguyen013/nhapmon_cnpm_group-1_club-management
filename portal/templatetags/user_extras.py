from django import template

register = template.Library()

@register.filter
def is_bcn(user):
    """
    Return True if user has BCNProfile and is assigned to a club.
    Safe: never raises exception even if user has no bcn_profile.
    """
    try:
        if not user or not getattr(user, "is_authenticated", False):
            return False
        profile = getattr(user, "bcn_profile", None)
        if not profile:
            return False
        return bool(profile.club_id)
    except Exception:
        return False

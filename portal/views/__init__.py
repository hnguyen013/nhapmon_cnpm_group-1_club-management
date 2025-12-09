# Import views authentication
from .auth import login_view, logout_view

# Import views cho các trang public
from .public import home, club_list, club_detail

# Export các view (cho Django dùng)
__all__ = [
    "login_view",
    "logout_view",
    "home",
    "club_list",
    "club_detail",
]

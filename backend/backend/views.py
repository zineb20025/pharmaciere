from pathlib import Path

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods


def _get_dist_index_html() -> str:
    # Pharmacie/backend/backend/views.py -> Pharmacie/frontend/dist/index.html
    dist_index = Path(__file__).resolve().parents[2] / "frontend" / "dist" / "index.html"
    if not dist_index.exists():
        raise FileNotFoundError(f"React build not found: {dist_index}")
    return dist_index.read_text(encoding="utf-8")


@require_http_methods(["GET"])
def spa_index(request, *args, **kwargs):
    """Serve the React SPA index.html (SPA fallback for client-side routing)."""
    try:
        html = _get_dist_index_html()
    except FileNotFoundError:
        # Fallback to the legacy Django dashboard if frontend isn't built yet.
        return redirect("dashboard")

    return HttpResponse(html, content_type="text/html; charset=utf-8")



# ============================================================
# pylearn/urls.py — Enrutador principal
# ============================================================
# ENLACE con el HTML:
#   El HTML hace dos llamadas:
#     1. GET  /        → muestra index.html  (vista: home)
#     2. POST /run/    → ejecuta código      (vista: run_code)
#
#   El JS del HTML usa exactamente estas rutas:
#     fetch('/run/', { method: 'POST', ... })
# ============================================================

from django.urls import path
from runner import views

urlpatterns = [
    # Sirve el index.html (tu 1.html) con {% csrf_token %} resuelto
    path('', views.home, name='home'),

    # Recibe el código Python del navegador, lo ejecuta y devuelve JSON
    # {"output": "..."} o {"error": "..."}
    path('run/', views.run_code, name='run_code'),
]

import json
import subprocess
import sys
import textwrap

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def home(request):
    return render(request, 'runner/index.html')


_BLOCKED_IMPORTS = {
    'os', 'sys', 'subprocess', 'socket', 'shutil',
    'importlib', 'ctypes', 'multiprocessing', 'threading',
    'pathlib', 'glob', 'tempfile', 'signal', 'pty',
    'ftplib', 'http', 'urllib', 'requests', 'smtplib',
}


def _contains_blocked_import(code: str) -> str | None:
    import ast
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = (
                [alias.name for alias in node.names]
                if isinstance(node, ast.Import)
                else [node.module or '']
            )
            for name in names:
                root = name.split('.')[0]
                if root in _BLOCKED_IMPORTS:
                    return root
    return None


@require_POST
def run_code(request):
    try:
        payload = json.loads(request.body)
        code = payload.get('code', '')
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': '⚠️ Petición inválida.'}, status=400)

    if not code.strip():
        return JsonResponse({'error': '⚠️ No hay código para ejecutar.'})

    blocked = _contains_blocked_import(code)
    if blocked:
        return JsonResponse({
            'error': f"⛔ El módulo '{blocked}' no está permitido en el playground."
        })

    timeout = getattr(settings, 'CODE_TIMEOUT', 5)
    try:
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            output = result.stdout or '(sin salida)'
            return JsonResponse({'output': output})
        else:
            error_lines = result.stderr.strip().splitlines()
            friendly = error_lines[-1] if error_lines else 'Error desconocido'
            return JsonResponse({'error': friendly})

    except subprocess.TimeoutExpired:
        return JsonResponse({
            'error': f'⏱️ Tiempo límite superado ({timeout}s). ¿Tienes un bucle infinito?'
        })
    except Exception as exc:
        return JsonResponse({'error': f'Error interno: {exc}'}, status=500)

# PyLearn — Django Backend

## Estructura del proyecto

```
pylearn/
├── manage.py                        ← punto de entrada Django
├── requirements.txt
├── pylearn/                         ← paquete de configuración
│   ├── settings.py                  ← configuración general
│   ├── urls.py                      ← rutas: / y /run/
│   └── wsgi.py
└── runner/                          ← app principal
    ├── views.py                     ← home() y run_code()
    ├── apps.py
    └── templates/
        └── runner/
            └── index.html           ← tu 1.html (template Django)
```

## Cómo arrancar (primera vez)

```bash
# 1. Crea y activa un entorno virtual
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Instala Django
pip install -r requirements.txt

# 3. Aplica migraciones (crea db.sqlite3)
python manage.py migrate

# 4. Arranca el servidor de desarrollo
python manage.py runserver

# 5. Abre en el navegador
#    http://127.0.0.1:8000/
```

## Cómo está enlazado el HTML con Django

| HTML / JS                          | Django                              |
|------------------------------------|-------------------------------------|
| `{{ csrf_token }}`                 | Inyectado por el motor de templates |
| `const CSRF = '{{ csrf_token }}'`  | Leído en JS y mandado como header   |
| `GET /`                            | `views.home` → renderiza index.html |
| `POST /run/` + `X-CSRFToken`       | `views.run_code` → ejecuta código   |
| `data.output` / `data.error`       | JSON devuelto por `run_code()`      |

## Seguridad del ejecutor

- Corre el código en un **subproceso** separado (no `exec()`)
- **Timeout** de 5 segundos (configurable en `settings.CODE_TIMEOUT`)
- Lista de **módulos bloqueados**: os, sys, subprocess, socket, etc.
- Solo captura stdout/stderr; el proceso hijo no afecta al servidor

> ⚠️ Para producción real considera ejecutar el subproceso dentro
> de un contenedor Docker o con restricciones seccomp/AppArmor.

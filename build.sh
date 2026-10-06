#!/bin/sh
set -eu

python -m pip install -r requirements.txt
python -m pip check
python -c "from weasyprint import HTML; pdf = HTML(string='<p>PDF deployment check</p>').write_pdf(); assert pdf.startswith(b'%PDF-')"
python manage.py check
python manage.py collectstatic --noinput

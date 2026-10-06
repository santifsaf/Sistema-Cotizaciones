import json
import os
import subprocess
import sys

from django.test import SimpleTestCase


class PruebasConfiguracionBaseDeDatos(SimpleTestCase):
    def cargar_configuracion(self, database_url, debug, ssl_require):
        environment = os.environ.copy()
        environment.update({
            'DATABASE_URL': database_url,
            'DEBUG': debug,
            'DATABASE_SSL_REQUIRE': ssl_require,
            'PYTHONDONTWRITEBYTECODE': '1',
        })
        script = (
            'import json; from proyectoWeb import settings; '
            'print(json.dumps(settings.DATABASES["default"]))'
        )
        result = subprocess.run(
            [sys.executable, '-c', script],
            env=environment,
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_postgres_externo_exige_ssl_con_debug(self):
        database = self.cargar_configuracion(
            'postgresql://user:password@database.example.com/app', 'True', 'True',
        )
        self.assertEqual(database['OPTIONS']['sslmode'], 'require')

    def test_postgres_local_permite_desactivar_ssl_sin_debug(self):
        database = self.cargar_configuracion(
            'postgresql://user:password@db/app', 'False', 'False',
        )
        self.assertEqual(database['HOST'], 'db')
        self.assertNotIn('sslmode', database.get('OPTIONS', {}))

    def test_sqlite_no_recibe_opciones_ssl(self):
        database = self.cargar_configuracion('sqlite:///:memory:', 'False', 'True')
        self.assertEqual(database['ENGINE'], 'django.db.backends.sqlite3')
        self.assertNotIn('sslmode', database.get('OPTIONS', {}))

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.db import connection

from pathlib import Path
from datetime import datetime
import shutil


class Command(BaseCommand):
    help = "Backup bazy danych (JSON dump + kopia pliku SQLite jeśli używasz SQLite)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--out",
            type=str,
            default="backups",
            help="Folder docelowy na backup (domyślnie: backups/ w BASE_DIR).",
        )

    def handle(self, *args, **options):
        base_dir = Path(settings.BASE_DIR)
        out_dir = base_dir / options["out"]
        out_dir.mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # 1) Zawsze: dump danych do JSON (przenośne między bazami)
        json_path = out_dir / f"db_dump_{ts}.json"
        self.stdout.write(f"-> Tworzę dump JSON: {json_path}")
        call_command(
            "dumpdata",
            "--natural-foreign",
            "--natural-primary",
            "--indent",
            "2",
            exclude=["contenttypes", "auth.permission", "admin.logentry", "sessions.session"],
            stdout=open(json_path, "w", encoding="utf-8"),
        )

        # 2) Jeśli SQLite: kopia pliku bazy (pełny backup)
        engine = connection.settings_dict.get("ENGINE", "")
        db_name = connection.settings_dict.get("NAME", "")

        if "sqlite3" in engine and db_name:
            db_path = Path(db_name)
            if not db_path.is_absolute():
                db_path = base_dir / db_path

            if db_path.exists():
                sqlite_copy = out_dir / f"db_file_{ts}.sqlite3"
                self.stdout.write(f"-> Kopiuję plik SQLite: {sqlite_copy}")
                shutil.copy2(db_path, sqlite_copy)
            else:
                self.stdout.write(self.style.WARNING(f"Uwaga: nie znaleziono pliku SQLite: {db_path}"))

        self.stdout.write(self.style.SUCCESS("Backup gotowy."))
        self.stdout.write(f"Folder: {out_dir}")

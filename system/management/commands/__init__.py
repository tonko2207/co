# animals/management/commands/backup.py
from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
from datetime import datetime
import shutil

class Command(BaseCommand):
    help = "Tworzy kopiê zapasow¹ bazy danych (SQLite) oraz katalogu MEDIA."

    def handle(self, *args, **options):
        base_dir = Path(settings.BASE_DIR)
        backup_dir = base_dir / "backups"
        backup_dir.mkdir(exist_ok=True)

        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # 1) backup bazy (SQLite)
        db_path = base_dir / "db.sqlite3"
        if db_path.exists():
            db_backup = backup_dir / f"db_{ts}.sqlite3"
            shutil.copy2(db_path, db_backup)
            self.stdout.write(self.style.SUCCESS(f"OK: backup bazy -> {db_backup}"))
        else:
            self.stdout.write(self.style.WARNING(f"Brak db.sqlite3 w: {db_path}"))

        # 2) backup MEDIA (zdjêcia/dokumenty)
        media_root = getattr(settings, "MEDIA_ROOT", None)
        if media_root:
            media_root = Path(media_root)
            if media_root.exists():
                media_backup = backup_dir / f"media_{ts}"
                shutil.copytree(media_root, media_backup)
                self.stdout.write(self.style.SUCCESS(f"OK: backup media -> {media_backup}"))
            else:
                self.stdout.write(self.style.WARNING(f"Brak MEDIA_ROOT: {media_root}"))
        else:
            self.stdout.write(self.style.WARNING("Brak ustawionego MEDIA_ROOT w settings.py"))

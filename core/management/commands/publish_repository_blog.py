from django.conf import settings
from django.core.management.base import BaseCommand

from core.blog_publishing import publish_repository_posts


class Command(BaseCommand):
    help = "Publish reviewed repository blog manifests, refusing unknown or modified rows."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true", help="Validate without changing rows."
        )

    def handle(self, *args, **options):
        results = publish_repository_posts(
            settings.BASE_DIR / "content" / "blog", dry_run=options["dry_run"]
        )
        if not results:
            self.stdout.write("No repository blog manifests; no rows changed.")
        for slug, action, digest in results:
            prefix = "would " if options["dry_run"] and action != "unchanged" else ""
            self.stdout.write(f"{slug}: {prefix}{action}; publication_sha256={digest}")

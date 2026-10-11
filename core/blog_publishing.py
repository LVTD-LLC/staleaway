"""Fail-closed publication of reviewed repository content into existing blog rows."""

import hashlib
import json
import re
import uuid
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.management.base import CommandError
from django.db import connection, transaction
from django.db.models import Q

from core.choices import BlogPostStatus
from core.models import BlogPost

PUBLIC_FIELDS = ("slug", "title", "description", "tags", "content", "status", "icon", "image")
MANIFEST_FIELDS = {
    "schema_version",
    "slug",
    "title",
    "description",
    "tags",
    "author",
    "content_sha256",
    "expected_previous_sha256",
}


def repository_post_uuid(slug):
    return uuid.uuid5(
        uuid.NAMESPACE_URL, f"https://github.com/LVTD-LLC/staleaway/content/blog/{slug}"
    )


def is_repository_post(post):
    return post.uuid == repository_post_uuid(post.slug)


def publication_digest(post):
    """Include every public field so editorial/visibility edits cannot be overwritten."""
    data = {field: str(getattr(post, field)) for field in PUBLIC_FIELDS}
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def validate_manifest(manifest, manifest_path):
    if not isinstance(manifest, dict) or set(manifest) != MANIFEST_FIELDS:
        raise ValueError("Manifest fields do not match the publication contract.")
    if manifest["schema_version"] != 1 or manifest["author"] != "Staleaway":
        raise ValueError("Unsupported schema version or author.")
    slug = manifest["slug"]
    if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("Invalid publication slug.")
    if manifest_path.stem != slug:
        raise ValueError("Manifest filename must match its slug.")
    for field in ("title", "description", "tags"):
        if not isinstance(manifest[field], str):
            raise ValueError(f"{field} must be a string.")
    for field in ("content_sha256", "expected_previous_sha256"):
        digest = manifest[field]
        if field == "expected_previous_sha256" and digest is None:
            continue
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"Invalid {field}.")


def load_publication(manifest_path):
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        validate_manifest(manifest, manifest_path)
        content_bytes = manifest_path.with_suffix(".md").read_bytes()
        if hashlib.sha256(content_bytes).hexdigest() != manifest["content_sha256"]:
            raise ValueError("Markdown digest does not match the approved manifest.")
        content = content_bytes.decode("utf-8")
        if not content.strip():
            raise ValueError("Markdown content must not be empty.")
        post = BlogPost(
            uuid=repository_post_uuid(manifest["slug"]),
            slug=manifest["slug"],
            title=manifest["title"],
            description=manifest["description"],
            tags=manifest["tags"],
            content=content,
            status=BlogPostStatus.PUBLISHED,
        )
        post.full_clean()
        return post, manifest["expected_previous_sha256"]
    except (OSError, ValueError, TypeError, ValidationError) as exc:
        raise CommandError(f"Invalid publication manifest {manifest_path.name}: {exc}") from exc


def load_publications(directory):
    directory = Path(directory)
    if not directory.exists():
        return []
    if not directory.is_dir():
        raise CommandError("Repository blog path must be a directory.")
    return [load_publication(path) for path in sorted(directory.glob("*.json"))]


@transaction.atomic
def publish_repository_posts(directory, *, dry_run=False):
    publications = load_publications(directory)
    if not publications:
        return []
    # Slugs and UUIDs are not unique in the legacy model. Serialize all blog writes
    # during this short transaction, including concurrent deployment containers.
    if connection.vendor == "postgresql":
        with connection.cursor() as cursor:
            cursor.execute("SET LOCAL lock_timeout = '10s'")
            table = connection.ops.quote_name(BlogPost._meta.db_table)
            cursor.execute(f"LOCK TABLE {table} IN SHARE ROW EXCLUSIVE MODE")
    elif connection.vendor != "sqlite":
        raise CommandError("Repository publication requires PostgreSQL (or SQLite tests).")
    return [publish_one(desired, previous, dry_run=dry_run) for desired, previous in publications]


def publish_one(desired, previous_digest, *, dry_run):
    """Apply a single transition inside publish_repository_posts' locked transaction."""
    candidates = list(
        BlogPost.objects.select_for_update().filter(Q(slug=desired.slug) | Q(uuid=desired.uuid))
    )
    if not candidates:
        if previous_digest is not None:
            raise CommandError(f"{desired.slug}: expected previous publication is missing.")
        if not dry_run:
            desired.save(force_insert=True)
        return desired.slug, "create", publication_digest(desired)
    if (
        len(candidates) != 1
        or candidates[0].uuid != desired.uuid
        or candidates[0].slug != desired.slug
    ):
        raise CommandError(f"{desired.slug}: existing blog content collision; no rows changed.")
    current = candidates[0]
    current_digest = publication_digest(current)
    desired_digest = publication_digest(desired)
    if current_digest == desired_digest:
        return desired.slug, "unchanged", current_digest
    # Withdrawing a post to draft is an editorial stop, never auto-republish it.
    if current.status != BlogPostStatus.PUBLISHED:
        raise CommandError(
            f"{desired.slug}: existing post is not published; refusing to republish."
        )
    if previous_digest is None or previous_digest != current_digest:
        raise CommandError(
            f"{desired.slug}: existing publication differs from the approved previous digest."
        )
    if not dry_run:
        for field in PUBLIC_FIELDS:
            setattr(current, field, getattr(desired, field))
        current.save(update_fields=[*PUBLIC_FIELDS, "updated_at"])
    return desired.slug, "update", desired_digest

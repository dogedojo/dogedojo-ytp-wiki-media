#!/usr/bin/env python3
"""Validate the media repository's asset manifest and tracked image files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
IMAGE_EXTENSIONS = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}
RIGHTS_BASES = {"original", "permission", "public-domain", "license", "other-reviewed"}
PATH_CATEGORIES = {
    "images/articles/": "article",
    "images/galleries/": "gallery",
    "images/thumbnails/": "thumbnail",
    "images/site/": "site",
    "originals/": "original",
}
ARTICLE_SLUG = re.compile(r"^[a-z0-9-]+(?:/[a-z0-9-]+)+$")


class ValidationError(Exception):
    """Raised when an asset record or repository file is invalid."""


def require_text(value: object, field: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise ValidationError(f"{field} must be {'a string' if allow_empty else 'a non-empty string'}")
    return value


def validate_https_url(value: object, field: str, *, required: bool = False) -> None:
    if value is None and not required:
        return
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be an HTTPS URL or null")
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValidationError(f"{field} must be a valid HTTPS URL")


def validate_record(record: object, index: int) -> str:
    label = f"assets[{index}]"
    if not isinstance(record, dict):
        raise ValidationError(f"{label} must be an object")

    path_value = require_text(record.get("path"), f"{label}.path")
    if "\\" in path_value:
        raise ValidationError(f"{label}.path must use forward slashes")

    relative = Path(path_value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValidationError(f"{label}.path must be a safe repository-relative path")

    normalized = relative.as_posix()
    expected_category = next(
        (category for prefix, category in PATH_CATEGORIES.items() if normalized.startswith(prefix)),
        None,
    )
    if expected_category is None:
        raise ValidationError(
            f"{label}.path must be under images/articles, images/galleries, "
            "images/thumbnails, images/site or originals"
        )

    category = require_text(record.get("category"), f"{label}.category")
    if category != expected_category:
        raise ValidationError(
            f"{label}.category must be {expected_category!r} for path {normalized!r}"
        )

    published = record.get("published")
    if not isinstance(published, bool):
        raise ValidationError(f"{label}.published must be true or false")
    if published != normalized.startswith("images/"):
        raise ValidationError(
            f"{label}.published must be true under images/ and false under originals/"
        )

    if Path(normalized).suffix.lower() not in IMAGE_EXTENSIONS:
        raise ValidationError(f"{label}.path has an unsupported image extension")

    resolved = (ROOT / relative).resolve()
    if not resolved.is_relative_to(ROOT.resolve()):
        raise ValidationError(f"{label}.path resolves outside the repository")
    if not resolved.is_file():
        raise ValidationError(f"{label}.path does not exist: {normalized}")

    article_slug = record.get("article_slug")
    if article_slug is not None:
        if not isinstance(article_slug, str) or not ARTICLE_SLUG.fullmatch(article_slug):
            raise ValidationError(f"{label}.article_slug must be a valid article slug or null")

    require_text(record.get("alt"), f"{label}.alt")
    require_text(record.get("caption"), f"{label}.caption", allow_empty=True)
    require_text(record.get("attribution"), f"{label}.attribution", allow_empty=True)

    source = record.get("source")
    if not isinstance(source, dict):
        raise ValidationError(f"{label}.source must be an object")
    require_text(source.get("title"), f"{label}.source.title")
    validate_https_url(source.get("url"), f"{label}.source.url")
    for key in ("creator", "rights_holder"):
        value = source.get(key)
        if value is not None and not isinstance(value, str):
            raise ValidationError(f"{label}.source.{key} must be a string or null")

    rights = record.get("rights")
    if not isinstance(rights, dict):
        raise ValidationError(f"{label}.rights must be an object")
    basis = require_text(rights.get("basis"), f"{label}.rights.basis")
    if basis not in RIGHTS_BASES:
        raise ValidationError(
            f"{label}.rights.basis must be one of: {', '.join(sorted(RIGHTS_BASES))}"
        )
    require_text(rights.get("details"), f"{label}.rights.details")
    validate_https_url(rights.get("license_url"), f"{label}.rights.license_url")
    if basis == "license" and not rights.get("license_url"):
        raise ValidationError(f"{label}.rights.license_url is required when basis is 'license'")

    notes = record.get("notes", "")
    if not isinstance(notes, str):
        raise ValidationError(f"{label}.notes must be a string")

    return normalized


def tracked_images() -> set[str]:
    found: set[str] = set()
    for folder in (ROOT / "images", ROOT / "originals"):
        if not folder.exists():
            continue
        for path in folder.rglob("*"):
            if not path.is_file() or path.name == ".gitkeep":
                continue
            if path.suffix.lower() not in IMAGE_EXTENSIONS:
                raise ValidationError(
                    f"Unexpected non-image file in asset directory: {path.relative_to(ROOT)}"
                )
            found.add(path.relative_to(ROOT).as_posix())
    return found


def main() -> int:
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("schema_version") != 1:
            raise ValidationError("manifest.json must be an object with schema_version: 1")

        records = data.get("assets")
        if not isinstance(records, list):
            raise ValidationError("manifest.json assets must be a list")

        manifest_paths: set[str] = set()
        for index, record in enumerate(records):
            path = validate_record(record, index)
            if path in manifest_paths:
                raise ValidationError(f"Duplicate manifest path: {path}")
            manifest_paths.add(path)

        actual_paths = tracked_images()
        missing_records = sorted(actual_paths - manifest_paths)
        missing_files = sorted(manifest_paths - actual_paths)
        if missing_records:
            raise ValidationError(
                "Image files missing manifest records: " + ", ".join(missing_records)
            )
        if missing_files:
            raise ValidationError(
                "Manifest entries missing image files: " + ", ".join(missing_files)
            )

        print(f"Validated {len(records)} asset record(s); all tracked image files are accounted for.")
        return 0
    except (OSError, json.JSONDecodeError, ValidationError) as error:
        print(f"Asset validation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

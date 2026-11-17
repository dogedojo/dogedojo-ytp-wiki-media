# Contributing media assets

These rules apply to every image added to this repository. The goal is to make YTP.wiki less dependent on third-party image hosts without creating a poorly sourced collection of files we cannot responsibly serve.

## Before adding an image

- Confirm that the project has a defensible basis to store and publicly serve the image.
- Record the original source and identify the creator and rights holder where known.
- Check the actual license or permission terms. A source being publicly accessible does not mean it can be rehosted.
- If ownership, licensing or permission is unclear, do not add the file. Explain the blocker in the relevant wiki issue instead.
- Do not assume that educational use, transformation, a screenshot, a thumbnail, or a small image automatically makes redistribution permissible.
- Do not use "fair use" as an unexplained checkbox. Any exceptional basis must be specifically reviewed and documented before the asset is added.

## Where files belong

| Directory | Use |
|---|---|
| `images/articles/<article-slug>/` | Images used directly in an article |
| `images/galleries/<gallery-slug>/` | Curated gallery images |
| `images/thumbnails/<article-slug>/` | Locally stored preview and thumbnail images |
| `images/site/` | Site-wide artwork and interface imagery |
| `originals/` | Optional source-quality files that should be preserved but not published |

Use the existing article slug when an image belongs to one article. Keep gallery assets grouped by subject. Do not create a new directory hierarchy for a single file unless it makes future organization clearer.

## File naming and optimization

- Use lowercase kebab-case names, such as `morshu-counter.webp`.
- Avoid spaces, dates without meaning, random download names and duplicate copies.
- Prefer WebP or AVIF for suitable raster images; use PNG for transparency or lossless detail, and JPEG when appropriate.
- Keep intentional animation as animation. Do not strip frames from a GIF merely to reduce its size.
- SVG files must be reviewed for scripts, external references and other unsafe content before they are accepted.
- Keep public delivery files reasonably small. Discuss unusually large files before committing them.
- Do not add videos, audio, executables, archives or unrelated project files.

## Required manifest entry

Every image file in `images/` or `originals/` must be listed in `manifest.json`. A record must include:

- Exact repository-relative path.
- Whether it is published. Files in `images/` are published; files in `originals/` are not.
- Category and related article slug, where applicable.
- Descriptive alt text and a caption.
- Source title and URL, where available, plus creator and rights holder when known.
- A rights basis and a specific explanation of that basis.
- Required attribution, or an empty string when none is required.

For a licensed asset, include the license URL. For permission-based assets, document where the permission evidence is retained without publishing private correspondence or personal contact details. Never commit private emails, personal information or credentials.

Use only the allowed rights-basis values documented in the repository README. Do not invent missing information; use `null` for unknown source fields and explain relevant uncertainty in the notes. An unknown rights basis is a reason not to publish the asset.

## Pull request checklist

Before opening a pull request:

1. Confirm the file is in the correct directory and has a stable filename.
2. Add a complete manifest record.
3. Confirm the alt text describes the meaningful visual content rather than saying "image".
4. Confirm captions and attribution do not claim more than the evidence supports.
5. Run `python scripts/validate_manifest.py`.
6. Explain the intended article or page and the provenance/rights basis in the pull request.

Do not change the main wiki's build or article references in this repository's pull request. Build integration and migration are handled in the main `ytp-wiki` repository under [issue #44](https://github.com/dogedojo/ytp-wiki/issues/44).

## Updating or removing an asset

If an image is replaced, update its manifest record in the same change. If an asset is removed, remove its manifest entry and make sure the main wiki no longer references it before the corresponding media revision is deployed. Do not silently replace an image with a different source or rights status while retaining its old attribution.

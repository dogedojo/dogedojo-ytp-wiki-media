# YTP.wiki media assets

This repository is the version-controlled source of approved static image assets used by [YTP.wiki](https://ytp.wiki/).

It exists so the wiki does not have to depend on unrelated image hosts for assets it can responsibly store and maintain itself.

## Important: this is not the website's image CDN

The intended publishing flow is:

1. Store approved image assets here and record their provenance in `manifest.json`.
2. The main `ytp-wiki` repository pins a specific commit of this repository.
3. Its normal static-site build copies the publishable files from `images/` into the generated site.
4. Visitors receive those files from the YTP.wiki site origin, not from GitHub, an image CDN, or this repository at runtime.

The build integration and migration of existing images are tracked in [ytp-wiki issue #44](https://github.com/dogedojo/ytp-wiki/issues/44). Until that integration is merged, do not use this repository's GitHub or raw-file URLs as image sources in published wiki pages.

## Directory layout

```
images/
  articles/       Images used within individual encyclopedia articles
  galleries/      Curated source-material and other article galleries
  thumbnails/     Locally stored thumbnails and preview images
  site/            Site-wide artwork and interface imagery
originals/         Optional high-quality source files; never published
manifest.json      Provenance and publishing metadata for every image
scripts/           Repository validation tools
```

Use article slugs in paths where practical. For example:

```
images/articles/sources/zelda-cdi/cutscene-still.webp
images/galleries/zelda-cdi/morshu-counter.webp
images/thumbnails/videos/example-ytp.webp
```

Only files under `images/` are intended for the public site. Files under `originals/` are preservation/source material and must never be copied into the generated website.

## Asset records and provenance

Every image file must have an entry in `manifest.json`, including non-published files in `originals/`. Each record identifies the file, intended use, source, creator or rights holder where known, and the documented basis for keeping it.

Example record:

```json
{
  "path": "images/galleries/zelda-cdi/example-scene.webp",
  "published": true,
  "category": "gallery",
  "article_slug": "sources/zelda-cdi",
  "alt": "A character standing behind the shop counter.",
  "caption": "The shopkeeper scene from the original game.",
  "source": {
    "title": "Name of the original source",
    "url": "https://example.com/source",
    "creator": "Known creator, or null if unknown",
    "rights_holder": "Known rights holder, or null if unknown"
  },
  "rights": {
    "basis": "permission",
    "details": "Describe the permission and where its evidence is recorded.",
    "license_url": null
  },
  "attribution": "Required attribution text, or an empty string if none is required.",
  "notes": ""
}
```

Allowed `rights.basis` values:

- `original` — original artwork created for the project by a contributor who retains the necessary rights.
- `permission` — documented permission to host and serve the image.
- `public-domain` — a verified public-domain basis, with the jurisdiction and reasoning documented.
- `license` — an applicable license that permits this use; include its URL.
- `other-reviewed` — another specifically documented and reviewed basis. Explain it in detail.

A source URL by itself is not permission. Do not assume that an image is safe to redistribute because it is publicly viewable, appears in search results, is used for educational purposes, or seems transformative. Do not use "fair use" as a casual substitute for a documented hosting decision. When the basis is unclear, do not add the image.

This repository has no blanket content license. Rights and reuse conditions are asset-specific and must be read from the manifest and the underlying source or permission. Do not assume that the presence of a file grants permission to reuse it elsewhere.

## Adding or updating an image

1. Read [CONTRIBUTING.md](CONTRIBUTING.md).
2. Add a production-ready image under the appropriate `images/` directory. Add a high-quality source file under `originals/` only when preserving it is useful.
3. Add or update its record in `manifest.json`.
4. Run:

   ```sh
   python scripts/validate_manifest.py
   ```

5. Open a pull request describing the asset, intended wiki use, provenance and rights basis.

The GitHub Actions workflow runs the same validator on pushes and pull requests.

## Supported formats and practical guidance

- Prefer WebP or AVIF for photographic and raster web images when quality and browser support are suitable.
- Use PNG when lossless detail or transparency is needed.
- Use JPEG where it is a better fit for photographic compatibility.
- Keep GIF only when the animation itself is useful; avoid converting a meaningful animation into a static image.
- Use SVG only when it is trusted, reviewed and free of scripts, unsafe external references and unnecessary metadata.
- Use lowercase kebab-case filenames without spaces.
- Keep published files reasonably optimized. Discuss unusually large files before adding them.
- Do not add video or audio files. This repository is for static image assets.

## Project boundaries

- Do not hotlink this repository from the live website.
- Do not add copyrighted material without a defensible, documented basis for hosting it.
- Do not invent creators, credits, licenses or permissions.
- Do not use AI-generated or stock images as filler for historical/source imagery.
- VidLii may be linked as an ordinary external source, but must never be embedded, framed, preloaded, auto-previewed or used as a player on YTP.wiki.

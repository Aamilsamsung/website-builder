# Forma Studio

A visual editor and curated gallery of original, redistribution-permitted website layouts, with a static frontend and a Supabase-backed account and export service.

## Development

```sh
npm ci
npm run build
python -m http.server 8000
npm test
node tests/browser.cjs
```

The generated root `index.html` includes all app code, the template catalog, dependency files and browser-rendered thumbnails, so the existing Render static build (`mkdir -p dist && cp index.html dist/`) remains compatible. Use `npm run build` after modifying frontend sources or template files.

## Catalog

Six distinct official Bootstrap 5.3.3 examples: Aperture (product), Cover, Carousel, Editorial (blog), Album, and Pricing. Source links are stored in `templates/catalog.json`. The MIT license is bundled with every project; Bootstrap CSS and JavaScript are local, and SVG placeholders come from the upstream examples. The original example layouts are retained; Hugo shortcodes are rendered into static HTML. The blog uses a system serif fallback instead of an external font. External demo links are not complete business workflows. Templates with unverified third-party photos are intentionally excluded.

## Backend setup

1. Create a dedicated Supabase project; apply `supabase/migrations/20261125_forma.sql`.
2. Deploy `supabase/functions/export` with JWT verification enabled. The function verifies the JWT again, validates filenames and size, includes local dependencies and original licensing, and records downloads. Configure the production URL in Supabase Auth redirect settings; add Google OAuth credentials if desired.
3. Create `src/config.json` with `url`, `key` (publishable key only), and `exportUrl` (backend function URL). Never commit service role keys. Run `npm run build`.
4. After the owner signs up, provision their admin role via a privileged database operation: insert their verified user ID into `public.user_roles` as `admin`. Never grant admin from a public client.

Without the backend configuration, users may browse, preview and edit, but account actions and official ZIP downloads are disabled. Local drafts survive login attempts. The frontend includes account sync and admin status controls, while database RLS limits writes to owners/admins. The publicly delivered static catalog remains inspectable; hiding a template filters the gallery, not the bundled source bytes.

## Exported sites

The ZIP contains every customized HTML page, CSS, JavaScript, local dependencies, README and license. Extract and open `index.html` or serve the extracted folder. Uploaded raster images are embedded as data URLs. The original demo navigation may contain placeholder links requiring customization. The editor preview uses an opaque sandboxed iframe with no same-origin access and a restrictive content security policy.

## Limitations

The initial catalog is intentionally small. It does not include framework templates, commercial checkout, hosted publishing or third-party form services. Advanced asset library, animations inspector, verified remote authentication, password-recovery completion, Google OAuth, admin analytics and public API separation remain to be finished. The static frontend requires the backend setup before production rollout.

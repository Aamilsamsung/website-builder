# Forma — Website Studio

**Live template gallery, visual website editor and complete source-code ZIP export.**

## Get started
This is a dependency-free, single-file web app. Open `index.html` in a browser, or deploy the repository as a static site using Cloudflare Pages, GitHub Pages or Netlify.

- **Cloudflare Pages:** Framework preset: None, build command: (empty), output directory: `/`.
- **GitHub Pages:** Settings → Pages → Deploy from branch → `main` → `/ (root)`.

## What's implemented
- 12 original template presets spanning portfolio, agency, business, SaaS, e-commerce, restaurant and blog.
- Category filtering and search.
- Live colour, font, heading, description, branding, button label and image URL editing.
- Page section adding, duplication, deletion, editing and ordering by drag/drop or arrow controls.
- Desktop, tablet and mobile canvas, plus fullscreen preview.
- Undo/redo, keyboard shortcuts and local project saving.
- Generated source preview and downloadable standalone website ZIP (HTML/CSS/JS/README).
- No external JS packages or build tools required.

## Important limitations
This is a working **first MVP**, not a completed hosted SaaS. Projects are stored in your current browser via localStorage; there is no account system or cross-device sync. The presets share a layout structure with different themes, content, fonts and photos rather than 12 fundamentally distinct component trees. ZIP outputs contain static sites, not React/Next.js projects. There is no general element-by-element drag/drop, integrated image upload, managed publishing, checkout, AI generation, or custom-domain management yet.

Generated websites use externally hosted photos and Google Fonts; these resources may need internet access, and users must ensure suitable licenses. The placeholder contact email should be replaced before publishing. Browser content is escaped in exports to reduce injection risk, but further security review is required before a public multi-user release.

## Next steps
Develop unique template structures, richer block editing, asset management, optional authentication and database storage, multi-page support, automated deployment, and creator marketplace.

## Ownership
Exported source files are yours to modify and host elsewhere, subject to any third-party asset licenses.

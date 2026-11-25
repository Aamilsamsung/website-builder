from pathlib import Path
import re,json,shutil,html,subprocess
root=Path(__file__).resolve().parents[1]; upstream=root.parent/'sources/bootstrap'; examples=upstream/'site/content/docs/5.3/examples'
items=[('product','Aperture','Business','Product-focused landing page with responsive navigation.'),('cover','Cover','Landing page','Minimal full-screen landing page.'),('carousel','Carousel','Business','Responsive sliding hero and marketing sections.'),('blog','Editorial','Blog','Magazine-style editorial layout and article sidebar.'),('album','Album','Portfolio','Responsive project and image gallery.'),('pricing','Pricing','SaaS','Subscription plans and feature comparison.')]
meta=[]
for slug,name,cat,desc in items:
 d=root/'templates'/slug; d.mkdir(parents=True,exist_ok=True); raw=(examples/slug/'index.html').read_text(); front,body=raw.split('---',2)[1:]; cls=re.search(r'body_class: "([^"]+)"',front); hcls=re.search(r'html_class: "([^"]+)"',front)
 def ph(m):
  a=dict(re.findall(r'(\w+)="([^"]*)"',m.group(1))); w=a.get('width','100%'); h=a.get('height','250'); label=a.get('text',f'{w} × {h}'); label='' if label=='false' else label
  return f'<svg class="bd-placeholder-img {a.get("class","")}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Placeholder" preserveAspectRatio="xMidYMid slice"><rect width="100%" height="100%" fill="{a.get("background","#ddd")}"/><text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle" fill="{a.get("color","#777")}">{html.escape(label)}</text></svg>'
 body=re.sub(r'\{\{< placeholder (.*?) >\}\}',ph,body); body=body.replace('{{< year >}}','2024').replace('/docs/{{< param docs_version >}}/assets/brand/bootstrap-logo.svg','bootstrap-logo.svg'); body=re.sub(r'\{\{< docsref "([^"]*)" >\}\}',r'https://getbootstrap.com/docs/5.3\1/',body); body=body.replace('href="/"','href="https://getbootstrap.com/"'); assert '{{<' not in body,slug
 css=(examples/slug/f'{slug}.css'); extra=css.read_text() if css.exists() else ''; (d/'styles.css').write_text(extra); (d/'index.html').write_text(f'<!doctype html><html lang="en" class="{hcls.group(1) if hcls else ""}" data-bs-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{name}</title><link rel="stylesheet" href="bootstrap.min.css"><link rel="stylesheet" href="styles.css"></head><body class="{cls.group(1) if cls else ""}">{body}<script src="bootstrap.bundle.min.js"></script></body></html>')
 if slug=='pricing': shutil.copy(upstream/'site/static/docs/5.3/assets/brand/bootstrap-logo.svg',d/'bootstrap-logo.svg')
 (d/'LICENSE').write_text((upstream/'LICENSE').read_text()); (d/'README.md').write_text(f'# {name}\n\nAdapted from Bootstrap 5.3.3 official {slug} example. MIT license, see LICENSE.\n\nExtract and open index.html, or run python -m http.server 8000. Demo content and placeholder links require customization before publication.\n\nOriginal source: https://github.com/twbs/bootstrap/tree/v5.3.3/site/content/docs/5.3/examples/{slug}\n')
 meta.append(dict(id=slug,name=name,category=cat,description=desc,source=f'https://github.com/twbs/bootstrap/tree/v5.3.3/site/content/docs/5.3/examples/{slug}',license='MIT'))
 common=root/'templates/common'; common.mkdir(exist_ok=True)
 for f,p in [('bootstrap.min.css','css'),('bootstrap.bundle.min.js','js')]: shutil.copy(upstream/'dist'/p/f,common/f)
(root/'templates/catalog.json').write_text(json.dumps(meta,indent=2))

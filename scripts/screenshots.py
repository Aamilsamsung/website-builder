from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]; common=root/'templates/common'
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/tmp/chromium',args=['--no-sandbox']); page=browser.new_page(viewport={'width':1120,'height':690},device_scale_factor=1)
 for d in (root/'templates').iterdir():
  if not d.is_dir() or d==common: continue
  html=(d/'index.html').read_text().replace('<link rel="stylesheet" href="bootstrap.min.css">','<style>'+ (common/'bootstrap.min.css').read_text()+'</style>').replace('<link rel="stylesheet" href="styles.css">','<style>'+ (d/'styles.css').read_text()+'</style>').replace('<script src="bootstrap.bundle.min.js"></script>','<script>'+ (common/'bootstrap.bundle.min.js').read_text()+'</script>');
  if (d/'bootstrap-logo.svg').exists(): html=html.replace('src="bootstrap-logo.svg"','src="data:image/svg+xml;base64,'+__import__('base64').b64encode((d/'bootstrap-logo.svg').read_bytes()).decode()+'"')
  page.set_content(html); page.screenshot(path=str(d/'thumbnail.webp'),type='webp' if False else 'jpeg',quality=82); (d/'thumbnail.webp').rename(d/'thumbnail.jpg')
 browser.close()

from pathlib import Path
root=Path(__file__).resolve().parent
html=(root/'index.html').read_text()
html=html.replace('<link rel="stylesheet" href="src/style.css">','<style>'+ (root/'src/style.css').read_text()+'</style>')
for name in ["config","engine","auction","ui"]:
 html=html.replace(f'<script src="src/{name}.js"></script>','<script>'+ (root/f'src/{name}.js').read_text()+'</script>')
(root/'kalkulator.html').write_text(html)

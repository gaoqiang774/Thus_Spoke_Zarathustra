import zipfile
import re

def convert(epub, md):
    with zipfile.ZipFile(epub, 'r') as z:
        content = []
        files = [f for f in z.namelist() if f.endswith('.html') and 'chapter' in f]
        files.sort() # alphabetical chapter2, chapter3...
        for f in files:
            html = z.read(f).decode('utf-8', errors='ignore')
            # Extract body
            body_m = re.search(r'<body[^>]*>(.*?)</body>', html, re.IGNORECASE|re.DOTALL)
            if body_m:
                html = body_m.group(1)
            
            # Simple Markdown
            html = re.sub(r'<h[1-6][^>]*>(.*?)</h[1-6]>', r'\n# \1\n\n', html, flags=re.IGNORECASE|re.DOTALL)
            html = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\1\n', html, flags=re.IGNORECASE|re.DOTALL)
            html = re.sub(r'<br\s*/?>', r'\n', html, flags=re.IGNORECASE)
            # Remove remaining tags
            html = re.sub(r'<[^>]+>', '', html)
            # Unescape
            html = html.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            html = re.sub(r'\n{3,}', '\n\n', html)
            content.append(html.strip())
            
        with open(md, 'w', encoding='utf-8') as out:
            out.write('# 查拉图斯特拉如是说\n\n')
            out.write('\n\n---\n\n'.join(content))

convert('弗里德里希·尼采：查拉图斯特拉如是说.epub', '查拉图斯特拉如是说.md')

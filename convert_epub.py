import zipfile
import re
import os
from xml.etree import ElementTree as ET

def get_epub_content(epub_path, md_path):
    with zipfile.ZipFile(epub_path, 'r') as z:
        # Find container.xml
        container_xml = z.read('META-INF/container.xml')
        root = ET.fromstring(container_xml)
        ns = {'n': 'urn:oasis:names:tc:opendocument:xmlns:container'}
        opf_path = root.find('.//n:rootfile', ns).attrib['full-path']
        
        opf_data = z.read(opf_path)
        opf_root = ET.fromstring(opf_data)
        opf_ns = {'opf': 'http://www.idpf.org/2007/opf'}
        
        # Get manifest dictionary id -> href
        manifest = {}
        for item in opf_root.findall('.//opf:item', opf_ns):
            manifest[item.attrib['id']] = item.attrib['href']
            
        # Get spine order
        spine = []
        for itemref in opf_root.findall('.//opf:itemref', opf_ns):
            spine.append(manifest[itemref.attrib['idref']])
            
        # Read files in spine order
        opf_dir = os.path.dirname(opf_path)
        full_text = []
        for html_file in spine:
            full_path = os.path.normpath(os.path.join(opf_dir, html_file))
            # normpath might produce backslashes on windows, fix for zip
            full_path = full_path.replace('\\', '/')
            try:
                html = z.read(full_path).decode('utf-8', errors='ignore')
                # Strip head
                html = re.sub(r'<head.*?>.*?</head>', '', html, flags=re.IGNORECASE|re.DOTALL)
                # Simple markdown conversions
                html = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n# \1\n\n', html, flags=re.IGNORECASE|re.DOTALL)
                html = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n\n', html, flags=re.IGNORECASE|re.DOTALL)
                html = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n\n', html, flags=re.IGNORECASE|re.DOTALL)
                html = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\1\n', html, flags=re.IGNORECASE|re.DOTALL)
                html = re.sub(r'<br\s*/?>', r'\n', html, flags=re.IGNORECASE)
                # Remove script and style
                html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.IGNORECASE|re.DOTALL)
                html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.IGNORECASE|re.DOTALL)
                # Remove all remaining HTML tags
                text = re.sub(r'<[^>]+>', '', html)
                # Unescape basics
                text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')
                # Cleanup excessive newlines
                text = re.sub(r'\n{3,}', '\n\n', text)
                full_text.append(text.strip())
            except Exception as e:
                pass
                
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write('\n\n---\n\n'.join(full_text))

get_epub_content('弗里德里希·尼采：查拉图斯特拉如是说.epub', '查拉图斯特拉如是说.md')

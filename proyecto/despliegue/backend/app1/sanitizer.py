import os
import re

def get_file_extension(filename: str):
    return os.path.splitext(filename)[1].lower()

def verify_file_content(content: str, ext: str) -> bool:
    if ext == '.html':
        return bool(re.search(r'<\s*(html|!doctype)', content, re.IGNORECASE))
    elif ext == '.css':
        return bool(re.search(r'\{[^}]*\}', content))
    return False

def sanitize_html(content: str) -> str:
    content = re.sub(r'<footer.*?>.*?</footer>', '', content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', '', content, flags=re.IGNORECASE | re.DOTALL)
    content += """
    <footer>
        <p>Creado por TuMarca - Todos los derechos reservados.</p>
    </footer>
    """
    return content

def sanitize_css(content: str) -> str:
    content = re.sub(r'expression\s*\([^)]*\)', '', content, flags=re.IGNORECASE)
    content = re.sub(r'url\s*\(\s*[\'"]?\s*javascript:[^)]*\)', 'url()', content, flags=re.IGNORECASE)
    return content

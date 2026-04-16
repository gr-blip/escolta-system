import subprocess, sys

path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
cwd  = r'D:\Sistema Escolta\escolta_system'

result = subprocess.run(['git', 'show', 'e2aeeaf:cadastros/views.py'],
    capture_output=True, cwd=cwd)
content = result.stdout.decode('utf-8', errors='replace')
print(f'Base: {len(content.splitlines())} linhas')
open(path, 'w', encoding='utf-8').write(content)
print('OK')

import subprocess, sys

path = r'D:\Sistema Escolta\escolta_system\cadastros\models.py'
local = open(path, encoding='utf-8').read()
print(f'Arquivo local: {len(local.splitlines())} linhas')
print('FotoMarco no local:', 'FotoMarco' in local)

result = subprocess.run(['git', 'show', 'HEAD:cadastros/models.py'],
    capture_output=True, cwd=r'D:\Sistema Escolta\escolta_system')
git_content = result.stdout.decode('utf-8', errors='replace')
print(f'Arquivo no git: {len(git_content.splitlines())} linhas')
print('FotoMarco no git:', 'FotoMarco' in git_content)

# -*- coding: utf-8 -*-
"""
Script que adiciona as funcoes ausentes no views.py restaurado.
Execute: python add_missing.py
"""

path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()

# ── 1. Fix: adiciona 'op' no contexto da os_detalhe ─────────────────────────
old_op = "        'operacional': getattr(os, 'operacional', None),\n        'veiculos': veiculos_qs,"
new_op = "        'operacional': getattr(os, 'operacional', None),\n        'op': getattr(os, 'operacional', None),\n        'veiculos': veiculos_qs,"
if old_op in content:
    content = content.replace(old_op, new_op)
    print('OK: fix op no contexto da os_detalhe')
elif "'op': getattr" in content:
    print('OK: fix op ja estava presente')
else:
    print('AVISO: fix op nao encontrado - verificar manualmente')

# ── 2. Views de Usuarios ──────────────────────────────────────────────────────
USUARIOS_CODE = '''

# ── USUÁRIOS ──────────────────────────────────────────────────────────────────

from django.contrib.auth.decorators import login_required as _lr

@_lr
def usuario_list(request):
    from django.contrib.auth.models import User
    usuarios = User.objects.all().order_by('username')
    from django.shortcuts import render as _r
    return _r(request, 'cadastros/usuario_list.html', {'usuarios': usuarios})


@_lr
def usuario_create(request):
    from django.contrib.auth.models import User
    from django.shortcuts import render as _r, redirect as _red
    from django.contrib import messages as _msg
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password1', '')
        is_staff = bool(request.POST.get('is_staff'))
        erros = []
        if not username:
            erros.append('Nome de usuário é obrigatório.')
        if User.objects.filter(username=username).exists():
            erros.append('Nome de usuário já existe.')
        if not password:
            erros.append('Senha é obrigatória.')
        if erros:
            return _r(request, 'cadastros/usuario_form.html', {'erros': erros, 'values': request.POST})
        u = User.objects.create_user(username=username, email=email, password=password)
        u.is_staff = is_staff
        u.save()
        _msg.success(request, f'Usuário {username} criado com sucesso.')
        return _red('usuario_list')
    from django.shortcuts import render as _r
    return _r(request, 'cadastros/usuario_form.html', {})


@_lr
def usuario_edit(request, pk):
    from django.contrib.auth.models import User
    from django.shortcuts import render as _r, redirect as _red, get_object_or_404 as _get
    from django.contrib import messages as _msg
    u = _get(User, pk=pk)
    if request.method == 'POST':
        u.username = request.POST.get('username', u.username).strip()
        u.email    = request.POST.get('email', u.email).strip()
        u.is_staff = bool(request.POST.get('is_staff'))
        u.save()
        _msg.success(request, 'Usuário atualizado.')
        return _red('usuario_list')
    return _r(request, 'cadastros/usuario_form.html', {'usuario': u})


@_lr
def usuario_senha(request, pk):
    from django.contrib.auth.models import User
    from django.shortcuts import render as _r, redirect as _red, get_object_or_404 as _get
    from django.contrib import messages as _msg
    u = _get(User, pk=pk)
    if request.method == 'POST':
        senha = request.POST.get('password1', '')
        if senha:
            u.set_password(senha)
            u.save()
            _msg.success(request, 'Senha alterada com sucesso.')
        else:
            _msg.error(request, 'Senha não pode ser vazia.')
        return _red('usuario_list')
    return _r(request, 'cadastros/usuario_senha_form.html', {'usuario': u})


@_lr
def usuario_delete(request, pk):
    from django.contrib.auth.models import User
    from django.shortcuts import render as _r, redirect as _red, get_object_or_404 as _get
    from django.contrib import messages as _msg
    u = _get(User, pk=pk)
    if request.method == 'POST':
        u.delete()
        _msg.success(request, 'Usuário removido.')
        return _red('usuario_list')
    return _r(request, 'cadastros/confirm_delete.html', {'obj': u, 'tipo': 'Usuário'})
'''

if 'def usuario_list' not in content:
    content = content + USUARIOS_CODE
    print('OK: views de usuario adicionadas')
else:
    print('OK: views de usuario ja existiam')

# ── 3. Salva ──────────────────────────────────────────────────────────────────
open(path, 'w', encoding='utf-8').write(content)

# ── 4. Verifica ───────────────────────────────────────────────────────────────
checks = ['def usuario_list', 'def usuario_create', 'def usuario_edit',
          'def usuario_senha', 'def usuario_delete',
          'def os_field_link', 'def os_field_veiculo_salvar',
          "'op': getattr"]
for c in checks:
    status = 'OK' if c in content else 'FALTA'
    print(f'{status}: {c}')

lines = len(content.splitlines())
print(f'\nTotal: {lines} linhas')
print('DONE - execute: git add . && git commit -m "fix: restaura views" && git push')

"""
Endpoint temporário para forçar recompressão de fotos via browser.
REMOVER após uso.
"""
import io
import os
from django.http import HttpResponse
from django.conf import settings
from PIL import Image, ExifTags
from cadastros.models import FotoMarco, FotoParada, FotoIncidente, FotoVeiculoEscoltado, FotoTrocaMotorista

SECRET = "compress2026jr"
MAX_LARGURA = 1280
QUALIDADE = 72
LIMITE_SKIP_KB = 200

MODELOS = [
    ('FotoMarco', FotoMarco),
    ('FotoParada', FotoParada),
    ('FotoIncidente', FotoIncidente),
    ('FotoVeiculoEscoltado', FotoVeiculoEscoltado),
    ('FotoTrocaMotorista', FotoTrocaMotorista),
]


def _corrigir_orientacao(img):
    try:
        exif = img._getexif()
        if exif:
            for tag, val in exif.items():
                if ExifTags.TAGS.get(tag) == 'Orientation':
                    if val == 3: img = img.rotate(180, expand=True)
                    elif val == 6: img = img.rotate(270, expand=True)
                    elif val == 8: img = img.rotate(90, expand=True)
                    break
    except Exception:
        pass
    return img


def compress_photos_view(request):
    token = request.GET.get('token', '')
    if token != SECRET:
        return HttpResponse('Acesso negado.', status=403)

    linhas = [f'MEDIA_ROOT = {settings.MEDIA_ROOT}', '']
    total_processadas = 0
    total_ignoradas = 0
    total_erros = 0
    economia_kb = 0

    for nome_model, ModelClass in MODELOS:
        count = ModelClass.objects.exclude(foto='').count()
        linhas.append(f'{nome_model}: {count} registros com foto')

        for obj in ModelClass.objects.exclude(foto='').iterator():
            try:
                caminho = obj.foto.path
            except Exception as e:
                linhas.append(f'  [ERRO path] #{obj.pk} foto={obj.foto.name!r}: {e}')
                total_erros += 1
                continue

            if not os.path.exists(caminho):
                linhas.append(f'  [AUSENTE] #{obj.pk}: {caminho}')
                total_erros += 1
                continue

            tamanho_antes = os.path.getsize(caminho) // 1024
            if tamanho_antes < LIMITE_SKIP_KB:
                total_ignoradas += 1
                continue

            try:
                with Image.open(caminho) as img:
                    img = _corrigir_orientacao(img)
                    if img.mode in ('RGBA', 'P', 'LA'):
                        img = img.convert('RGB')
                    if img.width > MAX_LARGURA:
                        ratio = MAX_LARGURA / img.width
                        img = img.resize((MAX_LARGURA, int(img.height * ratio)), Image.LANCZOS)
                    buffer = io.BytesIO()
                    img.save(buffer, format='JPEG', quality=QUALIDADE, optimize=True)
                    buffer.seek(0)

                novo_caminho = os.path.splitext(caminho)[0] + '.jpg'
                with open(novo_caminho, 'wb') as f:
                    f.write(buffer.read())
                if novo_caminho != caminho:
                    os.remove(caminho)

                tamanho_depois = os.path.getsize(novo_caminho) // 1024
                economia_kb += tamanho_antes - tamanho_depois
                total_processadas += 1
                linhas.append(f'  OK #{obj.pk}: {tamanho_antes}KB → {tamanho_depois}KB')

                novo_nome = os.path.splitext(obj.foto.name)[0] + '.jpg'
                if novo_nome != obj.foto.name:
                    ModelClass.objects.filter(pk=obj.pk).update(foto=novo_nome)

            except Exception as e:
                linhas.append(f'  [ERRO compress] #{obj.pk}: {e}')
                total_erros += 1

        linhas.append('')

    linhas.append('=' * 50)
    linhas.append(f'Processadas : {total_processadas}')
    linhas.append(f'Ignoradas   : {total_ignoradas}')
    linhas.append(f'Erros       : {total_erros}')
    linhas.append(f'Espaço liberado: {economia_kb / 1024:.1f} MB')

    return HttpResponse('\n'.join(linhas), content_type='text/plain; charset=utf-8')

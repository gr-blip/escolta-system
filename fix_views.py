content = open(r'D:\Sistema Escolta\escolta_system\cadastros\views.py', encoding='utf-8').read()
# Remove o trecho corrompido e recria corretamente
import re
content = re.sub(
    r'   from django\.conf import settings\ndef debug_media.*?return JsonResponse\(\{.+?\}\) return JsonResponse\(\{.+?\}\)',
    '''    obj.delete()
    return JsonResponse({'ok': True})


from django.conf import settings

def debug_media(request):
    import os
    files = []
    for root, dirs, filenames in os.walk(settings.MEDIA_ROOT):
        for f in filenames:
            files.append(os.path.join(root, f))
    return JsonResponse({
        'MEDIA_ROOT': settings.MEDIA_ROOT,
        'MEDIA_URL': settings.MEDIA_URL,
        'exists': os.path.exists(settings.MEDIA_ROOT),
        'files': files[:20],
    })''',
    content,
    flags=re.DOTALL
)
open(r'D:\Sistema Escolta\escolta_system\cadastros\views.py', 'w', encoding='utf-8').write(content)
print('DONE')

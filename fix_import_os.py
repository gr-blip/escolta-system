path = r'D:\Sistema Escolta\escolta_system\cadastros\views.py'
content = open(path, encoding='utf-8').read()

old = 'from .models import Agente, Viatura, Rastreador, Armamento, Cliente, Colete, Equipe, \\\n    FotoMarco, Parada, FotoParada, Incidente, FotoIncidente, FotoVeiculoEscoltado, \\\n    TrocaMotorista, FotoTrocaMotorista, AssinaturaOS, DespesaOS'

new = 'from .models import Agente, Viatura, Rastreador, Armamento, Cliente, Colete, Equipe, \\\n    FotoMarco, Parada, FotoParada, Incidente, FotoIncidente, FotoVeiculoEscoltado, \\\n    TrocaMotorista, FotoTrocaMotorista, AssinaturaOS, DespesaOS, OrdemServico'

if old in content:
    content = content.replace(old, new)
    open(path, 'w', encoding='utf-8').write(content)
    print('OK')
else:
    print('ERRO - verificando imports atuais:')
    idx = content.find('from .models import')
    print(repr(content[idx:idx+300]))

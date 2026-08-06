"""
Diagnóstico da integração Omnilink (GPS).

Chama a API Omnilink diretamente e mostra:
  1. Se o cliente SOAP conecta ao WSDL
  2. A resposta crua de ObtemAllPosicoesAtuais (posição atual de todas as viaturas)
  3. Quantas posições foram parseadas e quais placas
  4. Fallback: BuscarUltimoIdPost + ObtemEventosNormais (buffer)
  5. Cruzamento com as viaturas cadastradas (mct_id)

Uso:
    python manage.py diag_omnilink
    python manage.py diag_omnilink --raw     # imprime XML cru completo

Rode na máquina que alcança a internet do Omnilink (local ou Railway).
Não altera nada no banco — é somente leitura.
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Diagnostica a conexão e as respostas da API Omnilink (GPS)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--raw', action='store_true',
            help='Imprime o XML cru completo das respostas.'
        )

    def handle(self, *args, **opts):
        raw = opts['raw']
        w = self.stdout.write

        def linha(txt=''):
            w(txt)

        linha('=' * 70)
        linha('DIAGNÓSTICO OMNILINK')
        linha('=' * 70)

        # ── 1. Conexão com o WSDL ────────────────────────────────────────────
        from cadastros import omnilink as om
        linha(f'\n[1] WSDL: {om.URL_WSDL}')
        linha(f'    Usuário: {om.USUARIO}')
        try:
            client = om._get_client()
            linha(self.style.SUCCESS('    ✔ Cliente SOAP criado (WSDL acessível).'))
        except Exception as e:
            linha(self.style.ERROR(f'    X FALHA ao criar cliente SOAP: {type(e).__name__}: {e}'))
            linha('\n>>> Sem conexão com o Omnilink. Verifique internet/firewall/endpoint.')
            return

        # ── 2. ObtemAllPosicoesAtuais (método principal) ─────────────────────
        linha('\n[2] ObtemAllPosicoesAtuais (método principal do mapa)')
        try:
            xml_str = client.service.ObtemAllPosicoesAtuais(
                Usuario=om.USUARIO, Senha=om.SENHA_MD5
            )
            s = str(xml_str) if xml_str else ''
            linha(f'    Resposta: {len(s)} caracteres')
            if len(s) < 50:
                linha(self.style.WARNING(
                    f'    ⚠ Resposta MUITO curta — provável erro de auth/serviço: {s!r}'
                ))
            if raw:
                linha('    ── XML cru ──')
                linha(s)
            else:
                linha(f'    Início: {s[:400]}')

            posicoes = om._parse_posicoes_atuais_xml(s)
            placas = sorted({p['placa'] for p in posicoes if p['placa']})
            linha(f'    Posições parseadas: {len(posicoes)}')
            linha(f'    Placas retornadas: {placas}')
            for p in posicoes[:20]:
                linha(
                    f"      • {p['placa']:>10}  "
                    f"lat={p['lat']}  lng={p['lng']}  "
                    f"vel={p['velocidade']}  ign={p['ignicao']}  "
                    f"data={p['data_hora']}"
                )
        except Exception as e:
            linha(self.style.ERROR(
                f'    ✗ ERRO em ObtemAllPosicoesAtuais: {type(e).__name__}: {e}'
            ))

        # ── 3. Fallback: BuscarUltimoIdPost + ObtemEventosNormais ────────────
        linha('\n[3] Fallback — BuscarUltimoIdPost + ObtemEventosNormais')
        try:
            ultimo = om._buscar_ultimo_id_post()
            linha(f"    BuscarUltimoIdPost -> id={ultimo.get('id')} idctrl={ultimo.get('idctrl')}")
            if not ultimo.get('id') or str(ultimo.get('id')) == '0':
                linha(self.style.WARNING(
                    '    ⚠ id=0 — sem buffer de eventos disponível (auth ou sem dados).'
                ))
            eventos = om._get_eventos_normais()
            linha(f'    ObtemEventosNormais -> {len(eventos)} eventos')
            terminais = sorted({ev.get('id_terminal', '') for ev in eventos if ev.get('id_terminal')})
            linha(f'    Terminais com evento: {terminais[:30]}')
        except Exception as e:
            linha(self.style.ERROR(
                f'    ✗ ERRO no fallback: {type(e).__name__}: {e}'
            ))

        # ── 4. Cruzamento com viaturas cadastradas ───────────────────────────
        linha('\n[4] Viaturas cadastradas com mct_id')
        try:
            from cadastros.models import Viatura
            viaturas = Viatura.objects.filter(
                mct_id__isnull=False
            ).exclude(mct_id='').order_by('placa')
            linha(f'    Total no cadastro: {viaturas.count()}')
            for v in viaturas:
                try:
                    term = om._mct_id_to_terminal(v.mct_id)
                except Exception:
                    term = '?'
                linha(f"      • {v.placa:>10}  mct_id={v.mct_id!r:>12}  -> terminal_hex={term}")
        except Exception as e:
            linha(self.style.ERROR(f'    ✗ ERRO ao ler viaturas: {type(e).__name__}: {e}'))

        linha('\n' + '=' * 70)
        linha('INTERPRETAÇÃO RÁPIDA:')
        linha('  • [2] com 0 posições e resposta curta  -> credenciais/contrato Omnilink')
        linha('  • [2] com placas MAS diferentes das do cadastro -> divergência de placa')
        linha('  • [2] e [3] vazios, mas WSDL ok -> rastreadores sem reportar / conta')
        linha('  • Erro de auth explícito -> senha MD5 mudou no painel Omnilink')
        linha('=' * 70)

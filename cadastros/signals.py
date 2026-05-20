"""
cadastros/signals.py
━━━━━━━━━━━━━━━━━━━━
Signal para consulta automática de processos judiciais ao criar
FuncionarioPatrimonial.
"""
import logging
import threading

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


def _executar_consulta(funcionario):
    """Executa a consulta DriverID em background thread."""
    from .models import ConsultaProcesso
    from .services.driverid_service import consultar_cpf, DriverIDError
    from .pdf_processo import gerar_pdf_consulta
    from django.core.files.base import ContentFile

    try:
        resultado = consultar_cpf(funcionario.cpf)

        consulta = ConsultaProcesso.objects.create(
            funcionario=funcionario,
            cpf=resultado['cpf'],
            nome_retornado=resultado['nome'],
            status_cpf=resultado['status_cpf'],
            total_processos=resultado['total_processos'],
            resultado_json={'data': {
                'data': resultado['processos'],
                'result': {
                    'name': resultado['nome'],
                    'documentStatusMessage': resultado['status_cpf'],
                },
            }},
            transaction_id=resultado['transaction_id'],
            origem='auto_save',
        )

        try:
            pdf_buf = gerar_pdf_consulta(consulta)
            consulta.pdf_file.save(
                f'consulta_{funcionario.cpf}_{consulta.criado_em:%Y%m%d_%H%M}.pdf',
                ContentFile(pdf_buf.read()),
                save=True,
            )
        except Exception as e:
            logger.warning(f'Falha ao gerar PDF para {funcionario.cpf}: {e}')

        logger.info(
            f'DriverID auto: {funcionario.nome} — '
            f'{resultado["status_cpf"]} — {resultado["total_processos"]} proc.'
        )

    except DriverIDError as e:
        logger.error(f'DriverID auto falhou para {funcionario.cpf}: {e}')
    except Exception as e:
        logger.error(f'Erro inesperado na consulta auto para {funcionario.cpf}: {e}')


@receiver(post_save, sender='cadastros.FuncionarioPatrimonial')
def consultar_ao_salvar(sender, instance, created, **kwargs):
    """Disparar consulta automática ao criar novo FuncionarioPatrimonial."""
    if created:
        threading.Thread(target=_executar_consulta, args=(instance,), daemon=True).start()

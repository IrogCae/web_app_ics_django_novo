import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from ics_app.models import RdaSemPedido


class Command(BaseCommand):
    help = (
        "Importa rda_sem_pedido_resumo.xlsx para o modelo RdaSemPedido, preservando "
        "o histórico de follow-ups de e-mail"
    )

    def handle(self, *args, **options):
        # Carrega o arquivo Excel
        df = pd.read_excel(settings.RDA_SEM_PEDIDO_PATH)

        # Converte coluna de data para datetime.date, se existir
        if "Data do documento" in df.columns:
            df["Data do documento"] = pd.to_datetime(
                df["Data do documento"], dayfirst=True, errors="coerce"
            ).dt.date

        total = 0
        total_created = 0
        total_updated = 0

        # Use transação atômica para consistência
        with transaction.atomic():
            for _, row in df.iterrows():
                nro = row.get("Nº doc.de referência")

                # Campos do Excel a serem atualizados
                defaults = {
                    'total_valor_moeda_objeto':  row.get("Total Valor/moeda objeto"),
                    'definicao_do_projeto':      row.get("Definição do projeto"),
                    'elemento_pep':              row.get("Elemento PEP"),
                    'data_do_documento':         row.get("Data do documento"),
                    #'tipo_documento_referencia': row.get("Tipo documento referência"),
                    'empresa':                   row.get("Empresa"),
                    # Não inclua aqui campos de followup para não sobrescrever histórico
                }

                # Upsert: cria ou atualiza sem apagar histórico de follow-ups
                obj, created = RdaSemPedido.objects.update_or_create(
                    nro_doc_referencia=nro,
                    defaults=defaults
                )

                total += 1
                if created:
                    total_created += 1
                else:
                    total_updated += 1

        # Log de conclusão
        self.stdout.write(
            self.style.SUCCESS(
                f"{total} registros processados — {total_created} criados, {total_updated} atualizados."
            )
        )

import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from ics_app.models import Survey

class Command(BaseCommand):
    help = (
        "Importa survey_export.xlsx para o modelo Survey, preservando "
        "os dados existentes e atualizando apenas o que tiveram mudança."
    )

    def handle(self, *args, **options):
        # Carrega o arquivo Excel
        df = pd.read_excel(settings.DADOS_SURVEY_PATH)

        # Converte coluna de data para datetime.date, se existir
        if "date_answer" in df.columns:
            df["date_answer"] = pd.to_datetime(
                df["date_answer"], dayfirst=True, errors="coerce"
            ).dt.date

        total = 0
        total_created = 0
        total_updated = 0

        with transaction.atomic():
            for _, row in df.iterrows():
                # Você pode escolher uma chave única. Exemplo: (survey_code, sap_code, version)
                survey_code = row.get("survey_code")
                sap_code = row.get("sap_code")
                version = row.get("version")

                # Campos para atualizar/criar
                defaults = {
                    "supplier":    row.get("supplier"),
                    "user_name":   row.get("user_name"),
                    "date_answer": row.get("date_answer"),
                    "company":     row.get("company"),
                    "partnumber":  row.get("partnumber"),
                    "description": row.get("description"),
                }

                # Upsert por survey_code, sap_code e version (ajuste se preferir outra chave)
                obj, created = Survey.objects.update_or_create(
                    survey_code=survey_code,
                    sap_code=sap_code,
                    version=version,
                    defaults=defaults
                )

                total += 1
                if created:
                    total_created += 1
                else:
                    total_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{total} registros processados — {total_created} criados, {total_updated} atualizados."
            )
        )

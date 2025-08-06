import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from ics_app.models import SurveyBaseCompleta

class Command(BaseCommand):
    help = (
        "Importa survey_export.xlsx para a tabela de Base Completa, "
        "atualizando registros existentes ou criando novos."
    )

    def handle(self, *args, **options):

        df = pd.read_excel(settings.DADOS_SURVEY_BASE_COMPLETA_PATH)

        if "date_answer" in df.columns:
            df["date_answer"] = pd.to_datetime(
                df["date_answer"], dayfirst=True, errors="coerce"
            ).dt.date

        total = 0
        total_created = 0
        total_updated = 0

        with transaction.atomic():
            for _, row in df.iterrows():
                survey_code = row.get("survey_code")
                sap_code = row.get("sap_code")
                version = row.get("version")
                defaults = {
                    "supplier": row.get("supplier"),
                    "user_name": row.get("user_name"),
                    "date_answer": row.get("date_answer"),
                    "company": row.get("company"),
                    "partnumber": row.get("partnumber"),
                    "description": row.get("description"),
                    "january": row.get("january"),
                    "february": row.get("february"),
                    "march": row.get("march"),
                    "april": row.get("april"),
                    "may": row.get("may"),
                    "june": row.get("june"),
                    "july": row.get("july"),
                    "august": row.get("august"),
                    "september": row.get("september"),
                    "october": row.get("october"),
                    "november": row.get("november"),
                    "december": row.get("december"),
                    "annual_volume_2026": row.get("annual_volume_2026"),
                    "weekly_peak_pico_semanal": row.get("weekly_peak_pico_semanal"),
                    "status": row.get("status"),
                    "currency": row.get("currency"),
                    "investment_dolares": row.get("investment_dolares"),
                    "investment_reais": row.get("investment_reais"),
                    #"comments": row.get("comments"),
                }

                obj, created = SurveyBaseCompleta.objects.update_or_create(
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

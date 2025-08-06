import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from ics_app.models import SurveyBaseOk

class Command(BaseCommand):
    help = (
        "Importa survey_export.xlsx filtrando registros com SAP Code "
        "preenchido para a Base OK."
    )

    def handle(self, *args, **options):
        df = pd.read_excel(settings.DADOS_SURVEY_BASE_EXCLUIDOS_PATH)
        df = df[df['sap_code'].notna()]
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
                }
                obj, created = SurveyBaseOk.objects.update_or_create(
                    survey_code=survey_code,
                    sap_code=sap_code,
                    version=version,
                    defaults=defaults,
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
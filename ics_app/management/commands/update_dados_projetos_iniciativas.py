import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from ics_app.models import ProjetoIniciativa

class Command(BaseCommand):
    help = (
        "Importa o Excel de projetos/iniciativas "
        "e faz upsert no modelo ProjetoIniciativa."
    )

    def handle(self, *args, **options):
        # 1) Carrega o Excel (primeira aba)
        df = pd.read_excel(settings.PROJETOS_INICIATIVAS_PATH, sheet_name=0)

        # 2) Mapeia colunas do Excel para os campos do modelo
        df = df.rename(columns={
            "Projetos para Extração": "projetos_para_extracao",
            "Iniciativa":              "iniciativa",
            "Descrição":               "descricao",
            "Planta":                  "planta",
            "Orçamento":               "orcamento",
            "Status":                  "status",
            "Provisão":                "provisao",
            "Ano Aprovação":           "ano_aprovacao",
            "E-car":                   "e_car",
            "Comitê":                  "comite",
        })

        total = 0
        total_created = 0
        total_updated = 0

        # 3) Transação atômica
        with transaction.atomic():
            for row in df.itertuples(index=False, name="Row"):
                defaults = {
                    "comite":                     getattr(row, "comite", None),
                    "e_car":                      getattr(row, "e_car", None),
                    "projetos_para_extracao":     getattr(row, "projetos_para_extracao", None),
                    "iniciativa":                 getattr(row, "iniciativa", None),
                    "descricao":                  getattr(row, "descricao", None),
                    "planta":                     getattr(row, "planta", None),
                    "ano_aprovacao":              getattr(row, "ano_aprovacao", None),
                    "bdgt":                       getattr(row, "bdgt", None),
                    "status":                     getattr(row, "status", None),
                    "orcamento":                  getattr(row, "orcamento", None),
                    "disposto_sem_imposto":       getattr(row, "disposto_sem_imposto", None),
                    "valor_total_pedidos_emitidos": getattr(row, "valor_total_pedidos_emitidos", None),
                    "valor_pedidos_com_impostos": getattr(row, "valor_pedidos_com_impostos", None),
                    "valor_total_pedidos_pagos": getattr(row, "valor_total_pedidos_pagos", None),
                    "provisao":                   getattr(row, "provisao", None),
                }

                # 4) Upsert usando 'iniciativa' como chave única
                obj, created = ProjetoIniciativa.objects.update_or_create(
                    iniciativa=row.iniciativa,
                    defaults=defaults
                )

                total += 1
                if created:
                    total_created += 1
                else:
                    total_updated += 1

        # 5) Log de conclusão
        self.stdout.write(self.style.SUCCESS(
            f"{total} registros processados — "
            f"{total_created} criados, {total_updated} atualizados."
        ))
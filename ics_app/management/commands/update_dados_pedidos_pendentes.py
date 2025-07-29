import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from ics_app.models import DadosPedidosPendentes

class Command(BaseCommand):
    help = "Importa dados de DadosPedidosPendentes do Excel para o modelo DadosPedidosPendentes"

    def handle(self, *args, **options):
        # 1) Leia o Excel de DadosPedidosPendentes
        df = pd.read_excel(settings.DADOS_PEDIDOS_PENDENTES_PATH)

        # 2) Converta colunas de data
        date_cols = ['data_do_documento']
        for col in date_cols:
            if col in df.columns:
                df[col] = (
                    pd.to_datetime(df[col], dayfirst=True, errors='coerce')
                      .dt.date
                )

        # 3) Limpa dados antigos e prepara instâncias
        DadosPedidosPendentes.objects.all().delete()
        objs = []
        for _, row in df.iterrows():
            objs.append(DadosPedidosPendentes(
                doc_compra = row.get('doc_compra'),
                definicao_do_projeto = row.get('definicao_do_projeto'),
                elemento_pep = row.get('elemento_pep'),
                data_do_documento = row.get('data_do_documento'),
                #tipo_documento_referencia = row.get('tipo_documento_referencia'),
                empresa = row.get('empresa'),
                #codigo_de_eliminacao = row.get('codigo_de_eliminacao'),
                #valor_moeda_objeto = row.get('valor_moeda_objeto'),
                fornecedor = row.get('fornecedor'),
                valor_liquido_pedido = row.get('valor_liquido_pedido'),
            ))

        # 4) Insere tudo de uma vez
        DadosPedidosPendentes.objects.bulk_create(objs)

        # 5) Mensagem de sucesso
        self.stdout.write(self.style.SUCCESS(
            f"{len(objs)} registros de DadosPedidosPendentes importados com sucesso."
        ))

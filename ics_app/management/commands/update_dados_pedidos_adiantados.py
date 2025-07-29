import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from ics_app.models import DadosPedidosAdiantados

class Command(BaseCommand):
    help = "Importa dados de Pedidos Adiantados do Excel para o modelo DadosPedidosAdiantados"

    def handle(self, *args, **options):
        # 1) Leia o Excel de Pedidos Adiantados
        df = pd.read_excel(settings.DADOS_PEDIDOS_ADIANTADOS_PATH)

        # 2) Converta colunas de data
        date_cols = [
            'Data de Criação_agrp_rda_po',
            'data_da_rda',
        ]
        for col in date_cols:
            if col in df.columns:
                df[col] = (
                    pd.to_datetime(df[col], dayfirst=True, errors='coerce')
                      .dt.date
                )

        # 3) Limpa dados antigos e prepara instâncias
        DadosPedidosAdiantados.objects.all().delete()
        objs = []
        for _, row in df.iterrows():
            objs.append(DadosPedidosAdiantados(
                doc_compra                          = row.get('doc_compra'),
                empresa_agrp_rda_po                 = row.get('empresa_agrp_rda_po'),
                centro_agrp_rda_po                  = row.get('centro_agrp_rda_po'),
                data_de_criacao_agrp_rda_po         = row.get('data_de_criacao_agrp_rda_po'),
                centro_de_lucro_agrp_rda_po         = row.get('centro_de_lucro_agrp_rda_po'),
                centro_de_custo_agrp_rda_po         = row.get('centro_de_custo_agrp_rda_po'),
                elemento_pep_agrp_rda_po            = row.get('elemento_pep_agrp_rda_po'),
                requisicao_de_compras_agrp_rda_po    = row.get('requisicao_de_compras_agrp_rda_po'),
                item_de_requisicao_de_compras_agrp_rda_po = row.get('item_de_requisicao_de_compras_agrp_rda_po'),
                fornecedor_agrp_rda_po               = row.get('fornecedor_agrp_rda_po'),
                item_do_pedido_de_compras_agrp_rda_po = row.get('item_do_pedido_de_compras_agrp_rda_po'),
                codigo_de_liberacao_agrp_rda_po     = row.get('codigo_de_liberacao_agrp_rda_po'),
                no_servico_agrp_rda_po               = row.get('no_servico_agrp_rda_po'),
                material_agrp_rda_po                = row.get('material_agrp_rda_po'),
                descricao_do_material_agrp_rda_po   = row.get('descricao_do_material_agrp_rda_po'),
                val_comp_em_ef_moed_int_sq01        = row.get('val_comp_em_ef_moed_int_sq01'),
                montante_sq01                       = row.get('montante_sq01'),
                valor_faturas_registrada_sq01       = row.get('valor_faturas_registrada_sq01'),
                data_da_rda                         = row.get('data_da_rda'),
            ))

        # 4) Insere tudo de uma vez
        DadosPedidosAdiantados.objects.bulk_create(objs)

        # 5) Mensagem de sucesso
        self.stdout.write(self.style.SUCCESS(
            f"{len(objs)} registros de Pedidos Adiantados importados com sucesso."
        ))

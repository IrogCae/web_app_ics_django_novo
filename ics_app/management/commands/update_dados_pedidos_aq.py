import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from ics_app.models import DadosPedidosAQ

class Command(BaseCommand):
    help = "Importa dados de DadosPedidosAQ do Excel para o modelo DadosPedidosAQ"

    def handle(self, *args, **options):
        # 1) Leia o Excel de DadosPedidosAQ
        df = pd.read_excel(settings.DADOS_PEDIDOS_AQ_PATH)

        # 2) Converta colunas de data
        date_cols = ['data_de_criacao_agrp_rda_po', 'data_do_documento_compromisso', 'data_do_documento_me2n', 'data_de_lancamento_sq01', 'data_nf_sq01', 'data_da_rda']
        for col in date_cols:
            if col in df.columns:
                df[col] = (
                    pd.to_datetime(df[col], dayfirst=True, errors='coerce')
                      .dt.date
                )

        # 3) Limpa dados antigos e prepara instâncias
        DadosPedidosAQ.objects.all().delete()
        objs = []
        for _, row in df.iterrows():
            objs.append(DadosPedidosAQ(
                doc_compra = row.get('doc_compra'),
                empresa_agrp_rda_po = row.get('empresa_agrp_rda_po'),
                centro_agrp_rda_po = row.get('centro_agrp_rda_po'),
                data_de_criacao_agrp_rda_po = row.get('data_de_criacao_agrp_rda_po'),
                centro_de_lucro_agrp_rda_po = row.get('centro_de_lucro_agrp_rda_po'),
                centro_de_custo_agrp_rda_po = row.get('centro_de_custo_agrp_rda_po'),
                elemento_pep_agrp_rda_po = row.get('elemento_pep_agrp_rda_po'),
                requisicao_de_compras_agrp_rda_po = row.get('requisicao_de_compras_agrp_rda_po'),
                item_de_requisicao_de_compras_agrp_rda_po = row.get('item_de_requisicao_de_compras_agrp_rda_po'),
                fornecedor_agrp_rda_po = row.get('fornecedor_agrp_rda_po'),
                item_do_pedido_de_compras_agrp_rda_po = row.get('item_do_pedido_de_compras_agrp_rda_po'),
                codigo_de_liberacao_agrp_rda_po = row.get('codigo_de_liberacao_agrp_rda_po'),
                no_servico_agrp_rda_po = row.get('no_servico_agrp_rda_po'),
                material_agrp_rda_po = row.get('material_agrp_rda_po'),
                descricao_do_material_agrp_rda_po = row.get('descricao_do_material_agrp_rda_po'),
                grupo_de_mercadoria_agrp_rda_po = row.get('grupo_de_mercadoria_agrp_rda_po'),
                grupo_de_compradores_agrp_rda_po = row.get('grupo_de_compradores_agrp_rda_po'),
                categoria_de_classificacao_contabil_agrp_rda_po = row.get('categoria_de_classificacao_contabil_agrp_rda_po'),
                tipo_do_documento_de_compras_agrp_rda_po = row.get('tipo_do_documento_de_compras_agrp_rda_po'),
                criado_por_agrp_rda_po = row.get('criado_por_agrp_rda_po'),
                id_do_controller_agrp_rda_po = row.get('id_do_controller_agrp_rda_po'),
                status_agrp_rda_po = row.get('status_agrp_rda_po'),
                definicao_do_projeto_compromisso = row.get('definicao_do_projeto_compromisso'),
                elemento_pep_compromisso = row.get('elemento_pep_compromisso'),
                data_do_documento_compromisso = row.get('data_do_documento_compromisso'),
                tipo_documento_referencia_compromisso = row.get('tipo_documento_referencia_compromisso'),
                empresa_compromisso = row.get('empresa_compromisso'),
                codigo_de_eliminacao_compromisso = row.get('codigo_de_eliminacao_compromisso'),
                valor_moeda_objeto_compromisso = row.get('valor_moeda_objeto_compromisso'),
                fornecedor_compromisso = row.get('fornecedor_compromisso'),
                data_do_documento_me2n = row.get('data_do_documento_me2n'),
                codigo_de_eliminacao_me2n = row.get('codigo_de_eliminacao_me2n'),
                fornecedor_centro_fornecedor_me2n = row.get('fornecedor_centro_fornecedor_me2n'),
                codigo_de_imposto_me2n = row.get('codigo_de_imposto_me2n'),
                valor_liquido_pedido_me2n = row.get('valor_liquido_pedido_me2n'),
                moeda_me2n = row.get('moeda_me2n'),
                centro_me2n = row.get('centro_me2n'),
                empr_sq00 = row.get('empr_sq00'),
                centro_sq00 = row.get('centro_sq00'),
                tipo_sq00 = row.get('tipo_sq00'),
                emissao_sq00 = row.get('emissao_sq00'),
                del_sq00 = row.get('del_sq00'),
                fornec_sq00 = row.get('fornec_sq00'),
                razsoc_sq00 = row.get('razsoc_sq00'),
                cpgt_sq00 = row.get('cpgt_sq00'),
                pgto_em_sq00 = row.get('pgto_em_sq00'),
                idioma_sq00 = row.get('idioma_sq00'),
                denomi_sq00 = row.get('denomi_sq00'),
                item_sq00 = row.get('item_sq00'),
                eli_sq00 = row.get('eli_sq00'),
                material_sq00 = row.get('material_sq00'),
                codfam_sq00 = row.get('codfam_sq00'),
                mesa_sq00 = row.get('mesa_sq00'),
                comprador_sq00 = row.get('comprador_sq00'),
                empr_sq01 = row.get('empr_sq01'),
                dt_criacao_sq01 = row.get('dt_criacao_sq01'),
                fornecedor_sq01 = row.get('fornecedor_sq01'),
                nome_1_sq01 = row.get('nome_1_sq01'),
                txtbreve_sq01 = row.get('txtbreve_sq01'),
                qtd_pedido_sq01 = row.get('qtd_pedido_sq01'),
                moeda_sq01 = row.get('moeda_sq01'),
                tipo_de_operacao_sq01 = row.get('tipo_de_operacao_sq01'),
                doc_mat_sq01 = row.get('doc_mat_sq01'),
                ctg_de_historico_de_pedido_sq01 = row.get('ctg_de_historico_de_pedido_sq01'),
                codigo_debito_credito_sq01 = row.get('codigo_debito_credito_sq01'),
                doc_ref_sq01 = row.get('doc_ref_sq01'),
                quantidade_sq01 = row.get('quantidade_sq01'),
                data_de_lancamento_sq01 = row.get('data_de_lancamento_sq01'),
                no_doc_referencia_sq01 = row.get('no_doc_referencia_sq01'),
                data_nf_sq01 = row.get('data_nf_sq01'),
                criado_por_sq01 = row.get('criado_por_sq01'),
                nome_completo_sq01 = row.get('nome_completo_sq01'),
                iniciativa = row.get('iniciativa'),
                preco_liq_sq01 = row.get('preco_liq_sq01'),
                val_comp_em_ef_moed_int_sq01 = row.get('val_comp_em_ef_moed_int_sq01'),
                montante_sq01 = row.get('montante_sq01'),
                valor_faturas_registrada_sq01 = row.get('valor_faturas_registrada_sq01'),
                data_da_rda = row.get('data_da_rda'),
            ))

        # 4) Insere tudo de uma vez
        DadosPedidosAQ.objects.bulk_create(objs)

        # 5) Mensagem de sucesso
        self.stdout.write(self.style.SUCCESS(
            f"{len(objs)} registros de DadosPedidosAQ importados com sucesso."
        ))

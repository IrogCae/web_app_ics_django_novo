import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from ics_app.models import RdaAprovada


class Command(BaseCommand):
    help = "Importa rda_aprovada.xlsx para o modelo RdaAprovada"

    def handle(self, *args, **options):
        df = pd.read_excel(settings.RDA_APROVADA_PATH)  # Caminho definido no settings

        date_columns = [
            "data_de_criacao",
            "dt_criacao_sq01",
            "data_de_lancamento_sq01",
            "data_nf_sq01",
            "emissao_sq00",
            "data_do_documento_me2n"
        ]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce").dt.date

        updated = 0
        created = 0

        for _, row in df.iterrows():
            row = row.where(pd.notnull(row), None)
            
            obj, created_flag = RdaAprovada.objects.update_or_create(
                requisicao_de_compras_agrp_rda_po = row["requisicao_de_compras"],
                defaults={
                    "doc_compra": row["doc_compra"],
                    "data_de_criacao_agrp_rda_po": row["data_de_criacao"],
                    "iniciativa": row["iniciativa"],
                    "definicao_do_projeto_compromisso": row["definicao_do_projeto_Compromisso"],
                    "elemento_pep_agrp_rda_po": row["elemento_pep"],
                    "fornec_sq00": row["fornec_sq00"],
                    "razsoc_sq00": row["razsoc_sq00"],
                    "empresa_agrp_rda_po": row["empresa"],
                    "centro_agrp_rda_po": row["centro"],
                    "centro_de_lucro_agrp_rda_po": row["centro_de_lucro"],
                    # "fornecedor_agrp_rda_po": row["fornecedor"],
                    # "empr_sq01": row["empr_sq01"],
                    #"dt_criacao_sq01": row["dt_criacao_sq01"],
                    # "qtd_pedido_sq01": row["qtd_pedido_sq01"],
                    # "preco_liq_sq01": row["preco_liq_sq01"],
                    # "moeda_sq01": row["moeda_sq01"],
                    "ctg_de_historico_de_pedido_sq01": row["ctg_de_historico_de_pedido_sq01"],
                    # "codigo_debito_credito_sq01": row["codigo_debito_credito_sq01"],
                    # "doc_ref_sq01": row["doc_ref_sq01"],
                    # "quantidade_sq01": row["quantidade_sq01"],
                    "data_de_lancamento_sq01": row["data_de_lancamento_sq01"],
                    # "val_comp_em_ef_moed_int_sq01": row["val_comp_em_ef_moed_int_sq01"],
                    "valor_liquido_pedido_me2n": row["valor_liquido_pedido_me2n"],
                    # "montante_sq01": row["montante_sq01"],
                    #"valor_moeda_objeto_compromisso": row["valor_moeda_objeto_Compromisso"],
                    "data_nf_sq01": row["data_nf_sq01"],
                    "valor_faturas_registrada_sq01": row["valor_faturas_registrada_sq01"],
                    # "criado_por_sq01": row["criado_por_sq01"],
                    # "nome_completo_sq01": row["nome_completo_sq01"],
                    # "centro_sq00": row["centro_sq00"],
                    # "tipo_sq00": row["tipo_sq00"],
                    # "emissao_sq00": row["emissao_sq00"],
                    "cpgt_sq00": row["cpgt_sq00"],
                    # "idioma_sq00": row["idioma_sq00"],
                    "denomi_sq00": row["denomi_sq00"],
                    "comprador_sq00": row["comprador_sq00"],
                    # "data_do_documento_me2n": row["data_do_documento_me2n"],
                    "codigo_de_imposto_me2n": row["codigo_de_imposto_me2n"],
                    "moeda_me2n": row["moeda_me2n"],
                }
            )
            if created_flag:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Importação concluída: {created} criados, {updated} atualizados."))

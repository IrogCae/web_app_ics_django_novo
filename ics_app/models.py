from django.db import models
from django.conf import settings
from datetime import datetime, time, timezone, timedelta, date
from django.utils import timezone as dj_timezone

class Survey(models.Model):
    survey_code     = models.IntegerField("Survey Code", blank=True, null=True)
    sap_code        = models.IntegerField("SAP Code", blank=True, null=True)
    supplier        = models.CharField("Supplier", max_length=100,  blank=True, null=True)
    version         = models.IntegerField("Version", blank=True, null=True)
    user_name      = models.CharField("User Name", max_length=100, blank=True, null=True)
    date_answer    = models.DateField("Date Answer", blank=True, null=True)
    company        = models.CharField("Company", max_length=100, blank=True, null=True)
    partnumber     = models.CharField("Part Number", max_length=100, blank=True, null=True)
    description    = models.TextField("Description", blank=True, null=True)

    class Meta:
        db_table = 'dados_survey'
        verbose_name = 'Base Survey'
        verbose_name_plural = 'Bases Surveys'


class ProvisaoGasto(models.Model):
    id_projeto      = models.CharField("ID do Projeto", max_length=100)
    projeto         = models.CharField("Projeto", max_length=100)
    iniciativa      = models.CharField("Iniciativa", max_length=100)
    descricao       = models.CharField("Descrição", max_length=100)
    sap             = models.CharField("SAP", max_length=100, blank=True, null=True)  
    fornecedor      = models.CharField("Fornecedor", max_length=255, blank=True, null=True)
    provisao        = models.DecimalField("Provisão (R$)", max_digits=15, decimal_places=2)
    data_criacao    = models.DateTimeField("Data de Criação", auto_now_add=True)

    class Meta:
        db_table = 'provisao_gasto'
        verbose_name = 'Provisao Gasto'
        verbose_name_plural = 'Provisoes Gastos'

    def __str__(self):
        return f"{self.iniciativa} – R$ {self.provisao}"

class ProjetoIniciativa(models.Model):
    comite                      = models.CharField("Comitê",max_length=255,blank=True,null=True)
    e_car                       = models.CharField("E-car",max_length=255,blank=True,null=True)
    projetos_para_extracao      = models.CharField("Projetos para Extração",max_length=255,blank=True,null=True)
    iniciativa                  = models.CharField("Iniciativa",max_length=255,blank=True,null=True)
    descricao                   = models.CharField("Descrição",max_length=255,blank=True,null=True)
    planta                      = models.CharField("Planta",max_length=255,blank=True,null=True)
    ano_aprovacao               = models.IntegerField("Ano Aprovação",blank=True,null=True)
    bdgt                        = models.CharField("Planta",max_length=255,blank=True,null=True)
    status                      = models.CharField("Status",max_length=100,blank=True,null=True)
    orcamento                   = models.DecimalField("Orçamento",max_digits=14,decimal_places=2,blank=True,null=True)
    disposto_sem_imposto        = models.DecimalField("Disposto S/ Imposto",max_digits=14,decimal_places=2,blank=True,null=True)
    valor_total_pedidos_emitidos = models.DecimalField("Total Pedidos Emitidos",max_digits=14,decimal_places=2,blank=True,null=True)
    valor_total_pedidos_pagos   = models.DecimalField("Total Pedidos Pagos",max_digits=14,decimal_places=2,blank=True,null=True)
    provisao                    = models.CharField("Provisão",max_length=100,blank=True,null=True)


    class Meta:
        db_table = 'projeto_iniciativa'
        verbose_name = 'Projeto Iniciativa'
        verbose_name_plural = 'Projetos Iniciativas'

    def __str__(self):
        return f"{self.iniciativa} ({self.status})"

class RdaAprovada(models.Model):
    iniciativa                          = models.CharField("Iniciativa", max_length=255, blank=True, null=True)
    definicao_do_projeto_compromisso    = models.CharField("Projeto", max_length=255, blank=True, null=True)
    elemento_pep_agrp_rda_po            = models.CharField("Elemento PEP", max_length=255, blank=True, null=True)
    requisicao_de_compras_agrp_rda_po   = models.IntegerField("RDA", blank=True, null=True)
    data_emissao_rda                    = models.DateField("Emissão RDA", blank=True, null=True)
    doc_compra                          = models.IntegerField("Pedido", blank=True, null=True)
    data_de_criacao_agrp_rda_po         = models.DateField("Emissão Pedido", blank=True, null=True)
    fornec_sq00                         = models.CharField("SAP", max_length=255, blank=True, null=True)
    razsoc_sq00                         = models.CharField("Fornecedor", max_length=255, blank=True, null=True)
    #fornecedor_agrp_rda_po              = models.CharField(max_length=255, blank=True, null=True)
    #empr_sq01                           = models.CharField(max_length=255, blank=True, null=True)
    #dt_criacao_sq01                     = models.DateField(blank=True, null=True)
    #qtd_pedido_sq01                     = models.IntegerField(blank=True, null=True)
    data_de_lancamento_sq01             = models.DateField("Data Pag/Adiant", blank=True, null=True)
    #preco_liq_sq01                      = models.FloatField(blank=True, null=True)
    #moeda_sq01                          = models.CharField(max_length=50, blank=True, null=True)
    ctg_de_historico_de_pedido_sq01     = models.CharField("Tipo de Pag", max_length=255, blank=True, null=True)
    #codigo_debito_credito_sq01          = models.CharField("Débito/Crédito", max_length=255, blank=True, null=True)
    #doc_ref_sq01                        = models.CharField(max_length=255, blank=True, null=True)
    #quantidade_sq01                     = models.IntegerField(blank=True, null=True)
    #val_comp_em_ef_moed_int_sq01        = models.FloatField(blank=True, null=True)
    montante_sq01                       = models.FloatField("Valor Adiantamento", blank=True, null=True)
    valor_liquido_pedido_me2n           = models.FloatField("Valor Emissão", blank=True, null=True)
    #valor_moeda_objeto_compromisso      = models.FloatField("Valor Emissão", blank=True, null=True)
    empresa_agrp_rda_po                 = models.CharField("Planta", max_length=255, blank=True, null=True)
    moeda_me2n                          = models.CharField("Moeda", max_length=50, blank=True, null=True)
    centro_agrp_rda_po                  = models.CharField("Centro", max_length=255, blank=True, null=True)
    centro_de_lucro_agrp_rda_po         = models.CharField("Centro de Lucro", max_length=255, blank=True, null=True)
    data_nf_sq01                        = models.DateField("Data NF", blank=True, null=True)
    valor_faturas_registrada_sq01       = models.FloatField("Valor NF", blank=True, null=True)
    #criado_por_sq01                     = models.CharField(max_length=255, blank=True, null=True)
    #nome_completo_sq01                  = models.CharField(max_length=255, blank=True, null=True)
    #centro_sq00                         = models.CharField(max_length=255, blank=True, null=True)
    #tipo_sq00                           = models.CharField(max_length=255, blank=True, null=True)
    #emissao_sq00                        = models.DateField(blank=True, null=True)
    cpgt_sq00                           = models.CharField("Código Pg", max_length=255, blank=True, null=True)
    #idioma_sq00                         = models.CharField(max_length=50, blank=True, null=True)
    denomi_sq00                         = models.CharField("Descrição de Pagamento", max_length=255, blank=True, null=True)
    comprador_sq00                      = models.CharField("Comprador", max_length=255, blank=True, null=True)
    #data_do_documento_me2n              = models.DateField(blank=True, null=True)
    codigo_de_imposto_me2n              = models.CharField("Código Imposto", max_length=255, blank=True, null=True)
    erro_rda                            = models.BooleanField(default=False)
    email1_enviado                      = models.BooleanField(default=False)
    email2_enviado                      = models.BooleanField(default=False)
    progresso                           = models.IntegerField(default=0)

    class Meta:
        db_table = 'dados_rda_aprovada'
        verbose_name = "RDA Aprovada"
        verbose_name_plural = "RDAs Aprovadas"

    def __str__(self):
        return f"{self.iniciativa}"
    

class RdaSemPedido(models.Model):
    definicao_do_projeto               = models.CharField("Definição do projeto", max_length=50, blank=True, null=True)
    elemento_pep                       = models.CharField("Elemento PEP", max_length=20, blank=True, null=True)
    nro_doc_referencia                 = models.CharField("Nº doc. de referência", max_length=20, blank=True,null=True)
    total_valor_moeda_objeto           = models.FloatField("Total Valor/moeda objeto", blank=True, null=True)
    data_do_documento                  = models.DateField("Data emissão RDA", blank=True, null=True)
    #tipo_documento_referencia         = models.CharField("Tipo documento referência", max_length=10, blank=True, null=True)
    empresa                            = models.CharField("Planta", max_length=100, blank=True, null=True)
    # Campos adicionais inputáveis manualmente:
    sap_cofor                          = models.CharField("SAP/COFOR", max_length=100, blank=True, null=True)
    nome_fornecedor                    = models.CharField("Nome Fornecedor", max_length=255, blank=True, null=True)
    erro_rda = models.BooleanField(blank=True, null=True, verbose_name='Erro na RDA')

    class Meta:
        db_table = 'rda_sem_pedido'
        verbose_name = "RDA Sem Pedido"
        verbose_name_plural = "RDAs Sem Pedido"

    def __str__(self):
        return f"{self.nro_doc_referencia} – {self.empresa}"
    
    @property
    def has_email1(self):
        return self.email_actions.filter(tipo='email1').exists() # type: ignore[attr-defined]

    @property
    def has_email2(self):
        return self.email_actions.filter(tipo='email2').exists() # type: ignore[attr-defined]

    @property
    def progress(self):
        sent = int(self.has_email1) + int(self.has_email2)
        return int(sent / 2 * 100)
    
    @property
    def _age(self) -> timedelta:
        """Idade da RDA desde a data_do_documento até agora."""
        if not self.data_do_documento:
            return timedelta(0)

        # 1) converte o date em datetime à meia-noite
        created_dt_naive = datetime.combine(self.data_do_documento, time.min)
        # 2) aplica o timezone do Django (UTC ou o que você configurou)
        created = dj_timezone.make_aware(created_dt_naive, dj_timezone.get_current_timezone())

        # 3) pega agora (já ciente do timezone)
        now = dj_timezone.now()

        return now - created

    @property
    def business_days(self) -> int:
        """
        Conta quantos dias úteis (segunda a sexta) se passaram
        desde self.data_do_documento até hoje.
        """
        if not self.data_do_documento:
            return 0

        start = self.data_do_documento
        end   = date.today()
        # inclua o dia de emissão no cálculo (+1)
        total_days = (end - start).days
        return sum(
            1
            for i in range(total_days + 1)
            if (start + timedelta(days=i)).weekday() < 5
        )

    @property
    def row_color(self) -> str:
        # tenta converter a referência para inteiro
        try:
            req_int = int(float(self.nro_doc_referencia))
        except (ValueError, TypeError):
            # se não der pra converter, cai nas regras originais
            req_int = None

        # 1) Se já existe na tabela de aprovadas, pinta de verde
        if req_int is not None and RdaAprovada.objects.filter(
            requisicao_de_compras_agrp_rda_po=req_int
        ).exists():
            return 'table-success'

        # 2) Regras originais
        dias_uteis = self.business_days

        if dias_uteis >= 1 and not self.has_email1:
            return 'table-warning'
        if dias_uteis >= 6:
            if not self.has_email2:
                return 'table-warning'
            return 'table-danger'
        return ''
    
    @property
    def status_summary(self) -> str:
        """
        Retorna um texto resumido do status da RDA para exibir no tooltip:
        - Dias úteis desde emissão
        - Se Email1 já foi enviado
        - Se Email2 já foi enviado
        - Se ambos os e-mails foram enviados e já passou o prazo (6 dias úteis), indica que
          estamos aguardando a outra área e eles estão atrasados.
        """
        dias = self.business_days  # seu cálculo de dias úteis
        partes = [
            f"{dias} dia{'s' if dias != 1 else ''} útil{'' if dias != 1 else ''} passado{'s' if dias != 1 else ''}"
        ]

        # Status dos e-mails
        if self.has_email1:
            partes.append("Email 1 enviado ✅")
        else:
            partes.append("Email 1 pendente ⏳")

        if self.has_email2:
            partes.append("Email 2 enviado ✅")
        else:
            partes.append("Email 2 pendente ⏳")

        # Nova regra: ambos enviados + > 6 dias úteis = aguardando outra área
        if self.has_email1 and self.has_email2 and dias > 6:
            partes.append("Aguardando ação da outra área ⚠️")

        return " · ".join(partes)


class FollowupIniciativa(models.Model):
    rda = models.ForeignKey(
        RdaSemPedido, 
        on_delete=models.CASCADE,
        related_name='email_actions',
    )
    tipo = models.CharField(max_length=20)  # 'email1' ou 'email2'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enviado_em = models.DateTimeField(auto_now_add=True)
    data_envio_daf = models.DateField(null=True, blank=True)
    dias_uteis = models.IntegerField(null=True, blank=True)
    dias_corridos = models.IntegerField(null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Followup {self.tipo} para RDA {self.rda.pk}"


class Projeto(models.Model):
    id_gerador                   = models.CharField("ID Gerador", max_length=100, unique=True)
    planta                       = models.CharField("Planta", max_length=100, blank=True, null=True)
    gerador_id_projeto           = models.CharField("Gerador ID Projeto", max_length=100, blank=True, null=True)
    analista                     = models.CharField("Analista", max_length=100, blank=True, null=True)
    origem                       = models.CharField("Origem", max_length=100, blank=True, null=True)
    sap                          = models.CharField("SAP", max_length=100, blank=True, null=True)
    fornecedor                   = models.CharField("Fornecedor", max_length=200, blank=True, null=True)
    projeto_investimento         = models.CharField("Projeto Investimento", max_length=200, blank=True, null=True)
    modelos                      = models.CharField("Modelos", max_length=200, blank=True, null=True)
    tipo_de_investimento         = models.CharField("Tipo de Investimento", max_length=100, blank=True, null=True)
    investimento_aprovado        = models.DecimalField("Investimento Aprovado", max_digits=18, decimal_places=2, blank=True, null=True)
    aprovacao_saic               = models.CharField("Aprovação SAIC", max_length=100, blank=True, null=True)
    kick_off_projeto             = models.DateField("Kick Off Projeto", blank=True, null=True)
    lead_time_supplier           = models.IntegerField("Lead Time Supplier (Meses)", blank=True, null=True)
    aprovacao_comercial          = models.CharField("Aprovação Comercial", max_length=100, blank=True, null=True)
    aprovacao_validacao_tecnica  = models.CharField("Aprovação Validação Técnica", max_length=100, blank=True, null=True)
    lead_time_projeto            = models.DecimalField("Lead Time Projeto (Meses)", max_digits=8, decimal_places=2, blank=True, null=True)
    qty_reunioes_previstas       = models.IntegerField("QTY Reuniões Previstas", blank=True, null=True)
    qty_visitas_previstas        = models.IntegerField("QTY Visitas Previstas", blank=True, null=True)
    sop_target                   = models.CharField("SOP Target", max_length=100, blank=True, null=True)
    qtd_reunioes_realizadas      = models.IntegerField("QTD Reuniões Realizadas", blank=True, null=True)
    qtd_visitas_realizadas       = models.IntegerField("QTD Visitas Realizadas", blank=True, null=True)
    last_meeting                 = models.DateField("Last Meeting", blank=True, null=True)
    next_meeting                 = models.DateField("Next Meeting", blank=True, null=True)
    po_data                      = models.DateField("PO (Data)", blank=True, null=True)
    perc_conclusao_ferramental   = models.CharField("% de Conclusão do Ferramental", max_length=50, blank=True, null=True)
    otop                         = models.CharField("OTOP", max_length=50, blank=True, null=True)
    spv                          = models.CharField("SPV", max_length=50, blank=True, null=True)
    iaa                          = models.CharField("IAA", max_length=50, blank=True, null=True)
    data_benestare               = models.DateField("Data Benestare", blank=True, null=True)
    data_ppap_full               = models.DateField("Data PPAP Full", blank=True, null=True)
    status_projeto               = models.CharField("Status Projeto", max_length=50, blank=True, null=True)
    sop_executado                = models.CharField("SOP Executado", max_length=50, blank=True, null=True)
    status_sop                   = models.CharField("Status SOP", max_length=50, blank=True, null=True)
    def __str__(self):
        return self.id_gerador


class Pleito(models.Model):
    data_pleito              = models.DateField("DATA PLEITO", blank=True, null=True)
    origem_pleito            = models.CharField("ORIGEM PLEITO", max_length=100, blank=True, null=True)
    nro_survey               = models.IntegerField("Nº SURVEY", blank=True, null=True)
    sap_supplier             = models.CharField("SAP SUPPLIER", max_length=100, blank=True, null=True)
    fornecedor_solicitado    = models.CharField("FORNECEDOR SOLICITADO", max_length=200, blank=True, null=True)
    projeto_survey           = models.CharField("PROJETO SURVEY", max_length=200, blank=True, null=True)
    pleito_inicial           = models.DecimalField("PLEITO INICIAL", max_digits=18, decimal_places=2, blank=True, null=True)
    pleito_validado          = models.DecimalField("PLEITO VALIDADO", max_digits=18, decimal_places=2, blank=True, null=True)
    pleito_valor_final       = models.DecimalField("PLEITO VALOR FINAL", max_digits=18, decimal_places=2, blank=True, null=True)
    valor_reducao            = models.DecimalField("VALOR DE REDUÇÃO", max_digits=18, decimal_places=2, blank=True, null=True)
    cost_avoidance           = models.DecimalField("COST AVOIDANCE", max_digits=18, decimal_places=2, blank=True, null=True)
    analista_responsavel     = models.CharField("ANALISTA RESPONSÁVEL", max_length=100, blank=True, null=True)
    data_cid_enviado         = models.DateField("DATA CID ENVIADO", blank=True, null=True)
    data_cid_recebido        = models.DateField("DATA CID RECEBIDO", blank=True, null=True)
    analise_de_volume        = models.DecimalField("ANÁLISE DE VOLUME", max_digits=18, decimal_places=2, blank=True, null=True)
    validacao_comercial      = models.CharField("VALIDAÇÃO COMERCIAL", max_length=100, blank=True, null=True)
    validacao_sqd            = models.CharField("VALIDAÇÃO SQD", max_length=100, blank=True, null=True)
    data_saic                = models.DateField("DATA SAIC", blank=True, null=True)
    responsabilidade_sorting = models.CharField("RESPONSABILIDADE SORTING", max_length=100, blank=True, null=True)
    status_pleito            = models.CharField("STATUS PLEITO", max_length=100, blank=True, null=True)
    data_analise_final       = models.DateField("DATA ANÁLISE FINAL", blank=True, null=True)
    id_pleito                = models.CharField("ID PLEITO", max_length=100, unique=True)
    #id_pleito_extendido      = models.CharField("ID PLEITO EXTENDIDO", max_length=100, blank=True, null=True)
    orientativo              = models.CharField("ORIENTATIVO", max_length=100, blank=True, null=True)

    def __str__(self):
        return self.id_pleito


class Pedido(models.Model):
    iniciativa                   = models.CharField("Iniciativa", max_length=255, blank=True, null=True)
    definicao_projeto            = models.CharField("Definição do projeto", max_length=255, blank=True, null=True)
    elemento_pep                 = models.CharField("Elemento PEP", max_length=255, blank=True, null=True)
    requisicao_compras           = models.CharField("Requisição de Compras (RDA)", max_length=100, blank=True, null=True)
    doc_compra                   = models.CharField("Pedido", max_length=100, blank=True, null=True)
    data_documento               = models.DateField("Data emissão PO", blank=True, null=True)
    fornecedor_codigo            = models.CharField("Código Fornecedor", max_length=50, blank=True, null=True)
    razao_social                 = models.CharField("Razão Social", max_length=255, blank=True, null=True)
    empresa_compromisso          = models.CharField("Empresa", max_length=100, blank=True, null=True)
    cpg                          = models.CharField("Cpg", max_length=50, blank=True, null=True)
    denominacao                  = models.CharField("Cond. de Pg", max_length=255, blank=True, null=True)
    moeda                        = models.CharField("Moeda", max_length=10, blank=True, null=True)
    preco_liquido                = models.DecimalField("Preço líq.", max_digits=14, decimal_places=2, blank=True, null=True)
    data_lancamento              = models.DateField("Data de Pagamento", blank=True, null=True)
    montante                     = models.DecimalField("Valor Bruto", max_digits=14, decimal_places=2, blank=True, null=True)
    comprador                    = models.CharField("Comprador", max_length=100, blank=True, null=True)

    class Meta:
        db_table = "dados_pedidos"
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"{self.requisicao_compras} – {self.razao_social}"

class DadosPedidosAdiantados(models.Model):
    doc_compra                                        = models.CharField("doc_compra", max_length=255, blank=True, null=True)
    empresa_agrp_rda_po                               = models.CharField("empresa_agrp_rda_po", max_length=255, blank=True, null=True)
    centro_agrp_rda_po                                = models.CharField("centro_agrp_rda_po", max_length=255, blank=True, null=True)
    data_de_criacao_agrp_rda_po                       = models.CharField("data_de_criacao_agrp_rda_po", max_length=255, blank=True, null=True)
    centro_de_lucro_agrp_rda_po                       = models.CharField("centro_de_lucro_agrp_rda_po", max_length=255, blank=True, null=True)
    centro_de_custo_agrp_rda_po                       = models.CharField("centro_de_custo_agrp_rda_po", max_length=255, blank=True, null=True)
    elemento_pep_agrp_rda_po                          = models.CharField("elemento_pep_agrp_rda_po", max_length=255, blank=True, null=True)
    requisicao_de_compras_agrp_rda_po                 = models.CharField("requisicao_de_compras_agrp_rda_po", max_length=255, blank=True, null=True)
    item_de_requisicao_de_compras_agrp_rda_po         = models.CharField("item_de_requisicao_de_compras_agrp_rda_po", max_length=255, blank=True, null=True)
    fornecedor_agrp_rda_po                            = models.CharField("fornecedor_agrp_rda_po", max_length=255, blank=True, null=True)
    item_do_pedido_de_compras_agrp_rda_po             = models.CharField("item_do_pedido_de_compras_agrp_rda_po", max_length=255, blank=True, null=True)
    codigo_de_liberacao_agrp_rda_po                   = models.CharField("codigo_de_liberacao_agrp_rda_po", max_length=255, blank=True, null=True)
    no_servico_agrp_rda_po                            = models.CharField("no_servico_agrp_rda_po", max_length=255, blank=True, null=True)
    material_agrp_rda_po                              = models.CharField("material_agrp_rda_po", max_length=255, blank=True, null=True)
    descricao_do_material_agrp_rda_po                 = models.CharField("descricao_do_material_agrp_rda_po", max_length=255, blank=True, null=True)
    grupo_de_mercadoria_agrp_rda_po                   = models.CharField("grupo_de_mercadoria_agrp_rda_po", max_length=255, blank=True, null=True)
    grupo_de_compradores_agrp_rda_po                  = models.CharField("grupo_de_compradores_agrp_rda_po", max_length=255, blank=True, null=True)
    categoria_de_classificacao_contabil_agrp_rda_po   = models.CharField("categoria_de_classificacao_contabil_agrp_rda_po", max_length=255, blank=True, null=True)
    tipo_do_documento_de_compras_agrp_rda_po          = models.CharField("tipo_do_documento_de_compras_agrp_rda_po", max_length=255, blank=True, null=True)
    criado_por_agrp_rda_po                            = models.CharField("criado_por_agrp_rda_po", max_length=255, blank=True, null=True)
    id_do_controller_agrp_rda_po                      = models.CharField("id_do_controller_agrp_rda_po", max_length=255, blank=True, null=True)
    status_agrp_rda_po                                = models.CharField("status_agrp_rda_po", max_length=255, blank=True, null=True)
    definicao_do_projeto_compromisso                  = models.CharField("definicao_do_projeto_compromisso", max_length=255, blank=True, null=True)
    elemento_pep_compromisso                          = models.CharField("elemento_pep_compromisso", max_length=255, blank=True, null=True)
    data_do_documento_compromisso                     = models.CharField("data_do_documento_compromisso", max_length=255, blank=True, null=True)
    tipo_documento_referencia_compromisso             = models.CharField("tipo_documento_referencia_compromisso", max_length=255, blank=True, null=True)
    empresa_compromisso                               = models.CharField("empresa_compromisso", max_length=255, blank=True, null=True)
    codigo_de_eliminacao_compromisso                  = models.CharField("codigo_de_eliminacao_compromisso", max_length=255, blank=True, null=True)
    valor_moeda_objeto_compromisso                    = models.CharField("valor_moeda_objeto_compromisso", max_length=255, blank=True, null=True)
    fornecedor_compromisso                            = models.CharField("fornecedor_compromisso", max_length=255, blank=True, null=True)
    data_do_documento_me2n                            = models.CharField("data_do_documento_me2n", max_length=255, blank=True, null=True)
    codigo_de_eliminacao_me2n                         = models.CharField("codigo_de_eliminacao_me2n", max_length=255, blank=True, null=True)
    fornecedor_centro_fornecedor_me2n                 = models.CharField("fornecedor_centro_fornecedor_me2n", max_length=255, blank=True, null=True)
    codigo_de_imposto_me2n                            = models.CharField("codigo_de_imposto_me2n", max_length=255, blank=True, null=True)
    valor_liquido_pedido_me2n                         = models.CharField("valor_liquido_pedido_me2n", max_length=255, blank=True, null=True)
    moeda_me2n                                        = models.CharField("moeda_me2n", max_length=255, blank=True, null=True)
    centro_me2n                                       = models.CharField("centro_me2n", max_length=255, blank=True, null=True)
    empr_sq00                                         = models.CharField("empr_sq00", max_length=255, blank=True, null=True)
    centro_sq00                                       = models.CharField("centro_sq00", max_length=255, blank=True, null=True)
    tipo_sq00                                         = models.CharField("tipo_sq00", max_length=255, blank=True, null=True)
    emissao_sq00                                      = models.CharField("emissao_sq00", max_length=255, blank=True, null=True)
    del_sq00                                          = models.CharField("del_sq00", max_length=255, blank=True, null=True)
    fornec_sq00                                       = models.CharField("fornec_sq00", max_length=255, blank=True, null=True)
    razsoc_sq00                                       = models.CharField("razsoc_sq00", max_length=255, blank=True, null=True)
    cpgt_sq00                                         = models.CharField("cpgt_sq00", max_length=255, blank=True, null=True)
    pgto_em_sq00                                      = models.CharField("pgto_em_sq00", max_length=255, blank=True, null=True)
    idioma_sq00                                       = models.CharField("idioma_sq00", max_length=255, blank=True, null=True)
    denomi_sq00                                       = models.CharField("denomi_sq00", max_length=255, blank=True, null=True)
    item_sq00                                         = models.CharField("item_sq00", max_length=255, blank=True, null=True)
    eli_sq00                                          = models.CharField("eli_sq00", max_length=255, blank=True, null=True)
    material_sq00                                     = models.CharField("material_sq00", max_length=255, blank=True, null=True)
    codfam_sq00                                       = models.CharField("codfam_sq00", max_length=255, blank=True, null=True)
    mesa_sq00                                         = models.CharField("mesa_sq00", max_length=255, blank=True, null=True)
    comprador_sq00                                    = models.CharField("comprador_sq00", max_length=255, blank=True, null=True)
    empr_sq01                                         = models.CharField("empr_sq01", max_length=255, blank=True, null=True)
    dt_criacao_sq01                                   = models.CharField("dt_criacao_sq01", max_length=255, blank=True, null=True)
    fornecedor_sq01                                   = models.CharField("fornecedor_sq01", max_length=255, blank=True, null=True)
    nome_1_sq01                                       = models.CharField("nome_1_sq01", max_length=255, blank=True, null=True)
    txtbreve_sq01                                     = models.CharField("txtbreve_sq01", max_length=255, blank=True, null=True)
    qtd_pedido_sq01                                   = models.CharField("qtd_pedido_sq01", max_length=255, blank=True, null=True)
    moeda_sq01                                        = models.CharField("moeda_sq01", max_length=255, blank=True, null=True)
    tipo_de_operacao_sq01                             = models.CharField("tipo_de_operacao_sq01", max_length=255, blank=True, null=True)
    doc_mat_sq01                                      = models.CharField("doc_mat_sq01", max_length=255, blank=True, null=True)
    ctg_de_historico_de_pedido_sq01                   = models.CharField("ctg_de_historico_de_pedido_sq01", max_length=255, blank=True, null=True)
    codigo_debito_credito_sq01                        = models.CharField("codigo_debito_credito_sq01", max_length=255, blank=True, null=True)
    doc_ref_sq01                                      = models.CharField("doc_ref_sq01", max_length=255, blank=True, null=True)
    quantidade_sq01                                   = models.CharField("quantidade_sq01", max_length=255, blank=True, null=True)
    data_de_lancamento_sq01                           = models.CharField("data_de_lancamento_sq01", max_length=255, blank=True, null=True)
    no_doc_referencia_sq01                            = models.CharField("no_doc_referencia_sq01", max_length=255, blank=True, null=True)
    data_nf_sq01                                      = models.CharField("data_nf_sq01", max_length=255, blank=True, null=True)
    criado_por_sq01                                   = models.CharField("criado_por_sq01", max_length=255, blank=True, null=True)
    nome_completo_sq01                                = models.CharField("nome_completo_sq01", max_length=255, blank=True, null=True)
    iniciativa                                        = models.CharField("iniciativa", max_length=255, blank=True, null=True)
    preco_liq_sq01                                    = models.CharField("preco_liq_sq01", max_length=255, blank=True, null=True)
    val_comp_em_ef_moed_int_sq01                      = models.CharField("val_comp_em_ef_moed_int_sq01", max_length=255, blank=True, null=True)
    montante_sq01                                     = models.CharField("montante_sq01", max_length=255, blank=True, null=True)
    valor_faturas_registrada_sq01                     = models.CharField("valor_faturas_registrada_sq01", max_length=255, blank=True, null=True)
    data_da_rda                                       = models.CharField("data_da_rda", max_length=255, blank=True, null=True)

    class Meta:
        db_table = "dados_pedidos_adiantados"
        verbose_name = "PedidoAdiantados"
        verbose_name_plural = "PedidoAdiantados"



class DadosPedidosAQ(models.Model):
    doc_compra = models.CharField("doc_compra", max_length=255, blank=True, null=True)
    empresa_agrp_rda_po = models.CharField("empresa_agrp_rda_po", max_length=255, blank=True, null=True)
    centro_agrp_rda_po = models.CharField("centro_agrp_rda_po", max_length=255, blank=True, null=True)
    data_de_criacao_agrp_rda_po = models.CharField("data_de_criacao_agrp_rda_po", max_length=255, blank=True, null=True)
    centro_de_lucro_agrp_rda_po = models.CharField("centro_de_lucro_agrp_rda_po", max_length=255, blank=True, null=True)
    centro_de_custo_agrp_rda_po = models.CharField("centro_de_custo_agrp_rda_po", max_length=255, blank=True, null=True)
    elemento_pep_agrp_rda_po = models.CharField("elemento_pep_agrp_rda_po", max_length=255, blank=True, null=True)
    requisicao_de_compras_agrp_rda_po = models.CharField("requisicao_de_compras_agrp_rda_po", max_length=255, blank=True, null=True)
    item_de_requisicao_de_compras_agrp_rda_po = models.CharField("item_de_requisicao_de_compras_agrp_rda_po", max_length=255, blank=True, null=True)
    fornecedor_agrp_rda_po = models.CharField("fornecedor_agrp_rda_po", max_length=255, blank=True, null=True)
    item_do_pedido_de_compras_agrp_rda_po = models.CharField("item_do_pedido_de_compras_agrp_rda_po", max_length=255, blank=True, null=True)
    codigo_de_liberacao_agrp_rda_po = models.CharField("codigo_de_liberacao_agrp_rda_po", max_length=255, blank=True, null=True)
    no_servico_agrp_rda_po = models.CharField("no_servico_agrp_rda_po", max_length=255, blank=True, null=True)
    material_agrp_rda_po = models.CharField("material_agrp_rda_po", max_length=255, blank=True, null=True)
    descricao_do_material_agrp_rda_po = models.CharField("descricao_do_material_agrp_rda_po", max_length=255, blank=True, null=True)
    grupo_de_mercadoria_agrp_rda_po = models.CharField("grupo_de_mercadoria_agrp_rda_po", max_length=255, blank=True, null=True)
    grupo_de_compradores_agrp_rda_po = models.CharField("grupo_de_compradores_agrp_rda_po", max_length=255, blank=True, null=True)
    categoria_de_classificacao_contabil_agrp_rda_po = models.CharField("categoria_de_classificacao_contabil_agrp_rda_po", max_length=255, blank=True, null=True)
    tipo_do_documento_de_compras_agrp_rda_po = models.CharField("tipo_do_documento_de_compras_agrp_rda_po", max_length=255, blank=True, null=True)
    criado_por_agrp_rda_po = models.CharField("criado_por_agrp_rda_po", max_length=255, blank=True, null=True)
    id_do_controller_agrp_rda_po = models.CharField("id_do_controller_agrp_rda_po", max_length=255, blank=True, null=True)
    status_agrp_rda_po = models.CharField("status_agrp_rda_po", max_length=255, blank=True, null=True)
    definicao_do_projeto_compromisso = models.CharField("definicao_do_projeto_compromisso", max_length=255, blank=True, null=True)
    elemento_pep_compromisso = models.CharField("elemento_pep_compromisso", max_length=255, blank=True, null=True)
    data_do_documento_compromisso = models.CharField("data_do_documento_compromisso", max_length=255, blank=True, null=True)
    tipo_documento_referencia_compromisso = models.CharField("tipo_documento_referencia_compromisso", max_length=255, blank=True, null=True)
    empresa_compromisso = models.CharField("empresa_compromisso", max_length=255, blank=True, null=True)
    codigo_de_eliminacao_compromisso = models.CharField("codigo_de_eliminacao_compromisso", max_length=255, blank=True, null=True)
    valor_moeda_objeto_compromisso = models.CharField("valor_moeda_objeto_compromisso", max_length=255, blank=True, null=True)
    fornecedor_compromisso = models.CharField("fornecedor_compromisso", max_length=255, blank=True, null=True)
    data_do_documento_me2n = models.CharField("data_do_documento_me2n", max_length=255, blank=True, null=True)
    codigo_de_eliminacao_me2n = models.CharField("codigo_de_eliminacao_me2n", max_length=255, blank=True, null=True)
    fornecedor_centro_fornecedor_me2n = models.CharField("fornecedor_centro_fornecedor_me2n", max_length=255, blank=True, null=True)
    codigo_de_imposto_me2n = models.CharField("codigo_de_imposto_me2n", max_length=255, blank=True, null=True)
    valor_liquido_pedido_me2n = models.CharField("valor_liquido_pedido_me2n", max_length=255, blank=True, null=True)
    moeda_me2n = models.CharField("moeda_me2n", max_length=255, blank=True, null=True)
    centro_me2n = models.CharField("centro_me2n", max_length=255, blank=True, null=True)
    empr_sq00 = models.CharField("empr_sq00", max_length=255, blank=True, null=True)
    centro_sq00 = models.CharField("centro_sq00", max_length=255, blank=True, null=True)
    tipo_sq00 = models.CharField("tipo_sq00", max_length=255, blank=True, null=True)
    emissao_sq00 = models.CharField("emissao_sq00", max_length=255, blank=True, null=True)
    del_sq00 = models.CharField("del_sq00", max_length=255, blank=True, null=True)
    fornec_sq00 = models.CharField("fornec_sq00", max_length=255, blank=True, null=True)
    razsoc_sq00 = models.CharField("razsoc_sq00", max_length=255, blank=True, null=True)
    cpgt_sq00 = models.CharField("cpgt_sq00", max_length=255, blank=True, null=True)
    pgto_em_sq00 = models.CharField("pgto_em_sq00", max_length=255, blank=True, null=True)
    idioma_sq00 = models.CharField("idioma_sq00", max_length=255, blank=True, null=True)
    denomi_sq00 = models.CharField("denomi_sq00", max_length=255, blank=True, null=True)
    item_sq00 = models.CharField("item_sq00", max_length=255, blank=True, null=True)
    eli_sq00 = models.CharField("eli_sq00", max_length=255, blank=True, null=True)
    material_sq00 = models.CharField("material_sq00", max_length=255, blank=True, null=True)
    codfam_sq00 = models.CharField("codfam_sq00", max_length=255, blank=True, null=True)
    mesa_sq00 = models.CharField("mesa_sq00", max_length=255, blank=True, null=True)
    comprador_sq00 = models.CharField("comprador_sq00", max_length=255, blank=True, null=True)
    empr_sq01 = models.CharField("empr_sq01", max_length=255, blank=True, null=True)
    dt_criacao_sq01 = models.CharField("dt_criacao_sq01", max_length=255, blank=True, null=True)
    fornecedor_sq01 = models.CharField("fornecedor_sq01", max_length=255, blank=True, null=True)
    nome_1_sq01 = models.CharField("nome_1_sq01", max_length=255, blank=True, null=True)
    txtbreve_sq01 = models.CharField("txtbreve_sq01", max_length=255, blank=True, null=True)
    qtd_pedido_sq01 = models.CharField("qtd_pedido_sq01", max_length=255, blank=True, null=True)
    moeda_sq01 = models.CharField("moeda_sq01", max_length=255, blank=True, null=True)
    tipo_de_operacao_sq01 = models.CharField("tipo_de_operacao_sq01", max_length=255, blank=True, null=True)
    doc_mat_sq01 = models.CharField("doc_mat_sq01", max_length=255, blank=True, null=True)
    ctg_de_historico_de_pedido_sq01 = models.CharField("ctg_de_historico_de_pedido_sq01", max_length=255, blank=True, null=True)
    codigo_debito_credito_sq01 = models.CharField("codigo_debito_credito_sq01", max_length=255, blank=True, null=True)
    doc_ref_sq01 = models.CharField("doc_ref_sq01", max_length=255, blank=True, null=True)
    quantidade_sq01 = models.CharField("quantidade_sq01", max_length=255, blank=True, null=True)
    data_de_lancamento_sq01 = models.CharField("data_de_lancamento_sq01", max_length=255, blank=True, null=True)
    no_doc_referencia_sq01 = models.CharField("no_doc_referencia_sq01", max_length=255, blank=True, null=True)
    data_nf_sq01 = models.CharField("data_nf_sq01", max_length=255, blank=True, null=True)
    criado_por_sq01 = models.CharField("criado_por_sq01", max_length=255, blank=True, null=True)
    nome_completo_sq01 = models.CharField("nome_completo_sq01", max_length=255, blank=True, null=True)
    iniciativa = models.CharField("iniciativa", max_length=255, blank=True, null=True)
    preco_liq_sq01 = models.CharField("preco_liq_sq01", max_length=255, blank=True, null=True)
    val_comp_em_ef_moed_int_sq01 = models.CharField("val_comp_em_ef_moed_int_sq01", max_length=255, blank=True, null=True)
    montante_sq01 = models.CharField("montante_sq01", max_length=255, blank=True, null=True)
    valor_faturas_registrada_sq01 = models.CharField("valor_faturas_registrada_sq01", max_length=255, blank=True, null=True)
    data_da_rda = models.CharField("data_da_rda", max_length=255, blank=True, null=True)

    class Meta:
        db_table = "dados_pedidos_aq"
        verbose_name = "PedidoAQ"
        verbose_name_plural = "PedidoAQs"



class DadosPedidosPagos(models.Model):
    definicao_do_projeto_compromisso = models.CharField("Projeto", max_length=255, blank=True, null=True)
    elemento_pep_agrp_rda_po         = models.CharField("Elemento PEP", max_length=255, blank=True, null=True)
    iniciativa                       = models.CharField("Iniciativa", max_length=255, blank=True, null=True)
    requisicao_de_compras_agrp_rda_po = models.CharField("RDA", max_length=255, blank=True, null=True)
    data_da_rda                      = models.CharField("Data Emissão RDA", max_length=255, blank=True, null=True)
    doc_compra                       = models.CharField("Pedido", max_length=255, blank=True, null=True)
    data_de_criacao_agrp_rda_po      = models.CharField("Data Emissão Pedido", max_length=255, blank=True, null=True)
    empresa_agrp_rda_po              = models.CharField("Planta", max_length=255, blank=True, null=True)
    fornecedor_agrp_rda_po           = models.CharField("Fornecedor", max_length=255, blank=True, null=True)
    razsoc_sq00                      = models.CharField("Razão Social", max_length=255, blank=True, null=True)
    montante_sq01                    = models.CharField("Valor Bruto", max_length=255, blank=True, null=True)
    #criado_por_agrp_rda_po           = models.CharField("Criado por", max_length=255, blank=True, null=True)
    #id_do_controller_agrp_rda_po     = models.CharField("ID do Controller", max_length=255, blank=True, null=True)
    #status_agrp_rda_po               = models.CharField("Status", max_length=255, blank=True, null=True)
    #fornecedor_compromisso           = models.CharField("Fornecedor", max_length=255, blank=True, null=True)
    #codigo_de_imposto_me2n           = models.CharField("Código Imposto", max_length=255, blank=True, null=True)
    valor_liquido_pedido_me2n        = models.CharField("Valor Líquido do Pedido", max_length=255, blank=True, null=True)
    moeda_me2n                       = models.CharField("Rate", max_length=255, blank=True, null=True)
    cpgt_sq00                        = models.CharField("Código Pagamento", max_length=255, blank=True, null=True)
    #pgto_em_sq00                     = models.CharField("Pagamento em Dias", max_length=255, blank=True, null=True)
    denomi_sq00                      = models.CharField("Descrição Pagamento", max_length=255, blank=True, null=True)
    comprador_sq00                   = models.CharField("Comprador", max_length=255, blank=True, null=True)
    #ctg_de_historico_de_pedido_sq01  = models.CharField("CTG de Histórico de Pedido", max_length=255, blank=True, null=True)
    #codigo_debito_credito_sq01       = models.CharField("Código Débito Crédito", max_length=255, blank=True, null=True)
    data_de_lancamento_sq01          = models.CharField("Data do Pagamento", max_length=255, blank=True, null=True)
    data_nf_sq01                     = models.CharField("Data emissão NF", max_length=255, blank=True, null=True)
    #criado_por_sq01                  = models.CharField("Criado Por", max_length=255, blank=True, null=True)
    nome_completo_sq01               = models.CharField("Nome Completo", max_length=255, blank=True, null=True)
    #elemento_pep_compromisso         = models.CharField("Elemento PEP", max_length=255, blank=True, null=True)
    #data_do_documento_compromisso    = models.CharField("Data Emissão Pedido", max_length=255, blank=True, null=True)   
    #empresa_compromisso              = models.CharField("Planta", max_length=255, blank=True, null=True)
    #centro_agrp_rda_po               = models.CharField("Centro", max_length=255, blank=True, null=True)
    #centro_de_lucro_agrp_rda_po      = models.CharField("Centro de Lucro", max_length=255, blank=True, null=True)
    #centro_de_custo_agrp_rda_po      = models.CharField("Centro de Custo", max_length=255, blank=True, null=True)
    #item_de_requisicao_de_compras_agrp_rda_po = models.CharField("Item de Requisição de Compras", max_length=255, blank=True, null=True)
    #fornec_sq00                      = models.CharField("Fornecedor SQ00", max_length=255, blank=True, null=True)
    #item_do_pedido_de_compras_agrp_rda_po = models.CharField("Item do Pedido de Compras", max_length=255, blank=True, null=True)
    #codigo_de_liberacao_agrp_rda_po  = models.CharField("Código de Liberação", max_length=255, blank=True, null=True)
    #no_servico_agrp_rda_po           = models.CharField("Número do Serviço", max_length=255, blank=True, null=True)
    #material_agrp_rda_po             = models.CharField("Material", max_length=255, blank=True, null=True)
    #descricao_do_material_agrp_rda_po = models.CharField("Descrição do Material", max_length=255, blank=True, null=True)
    #grupo_de_mercadoria_agrp_rda_po  = models.CharField("Grupo de Mercadoria", max_length=255, blank=True, null=True)
    #grupo_de_compradores_agrp_rda_po = models.CharField("Grupo de Compradores", max_length=255, blank=True, null=True)
    #categoria_de_classificacao_contabil_agrp_rda_po = models.CharField("Categoria de Classificação Contábil", max_length=255, blank=True, null=True)
    #tipo_do_documento_de_compras_agrp_rda_po = models.CharField("Tipo do Documento de Compras", max_length=255, blank=True, null=True)
    #tipo_documento_referencia_compromisso = models.CharField("Tipo do Documento de Referência", max_length=255, blank=True, null=True)
    #codigo_de_eliminacao_compromisso = models.CharField("Código de Eliminação", max_length=255, blank=True, null=True)
    #valor_moeda_objeto_compromisso   = models.CharField("Valor em Moeda", max_length=255, blank=True, null=True)
    #data_do_documento_me2n           = models.CharField("Data do Documento ME2N", max_length=255, blank=True, null=True)
    #codigo_de_eliminacao_me2n        = models.CharField("Código de Eliminação ME2N", max_length=255, blank=True, null=True)
    #fornecedor_centro_fornecedor_me2n = models.CharField("Fornecedor Centro", max_length=255, blank=True, null=True)
    #centro_me2n                      = models.CharField("Centro ME2N", max_length=255, blank=True, null=True)
    #empr_sq00                        = models.CharField("Empr SQ00", max_length=255, blank=True, null=True)
    #centro_sq00                      = models.CharField("Centro SQ00", max_length=255, blank=True, null=True)
    #tipo_sq00                        = models.CharField("Tipo SQ00", max_length=255, blank=True, null=True)
    #emissao_sq00                     = models.CharField("Emissão SQ00", max_length=255, blank=True, null=True)
    #del_sq00                         = models.CharField("Del SQ00", max_length=255, blank=True, null=True)
    #idioma_sq00                      = models.CharField("Idioma SQ00", max_length=255, blank=True, null=True)
    #item_sq00                        = models.CharField("Item SQ00", max_length=255, blank=True, null=True)
    #eli_sq00                         = models.CharField("Eli SQ00", max_length=255, blank=True, null=True)
    #material_sq00                    = models.CharField("Material SQ00", max_length=255, blank=True, null=True)
    #codfam_sq00                      = models.CharField("Código da Família SQ00", max_length=255, blank=True, null=True)
    #mesa_sq00                        = models.CharField("Mesa SQ00", max_length=255, blank=True, null=True)
    #empr_sq01                        = models.CharField("Empr SQ01", max_length=255, blank=True, null=True)
    #dt_criacao_sq01                  = models.CharField("Data de Criação SQ01", max_length=255, blank=True, null=True)
    #fornecedor_sq01                  = models.CharField("Fornecedor", max_length=255, blank=True, null=True)
    #nome_1_sq01                      = models.CharField("Nome 1", max_length=255, blank=True, null=True)
    #txtbreve_sq01                    = models.CharField("Texto Breve", max_length=255, blank=True, null=True)
    #qtd_pedido_sq01                  = models.CharField("Quantidade Pedido", max_length=255, blank=True, null=True)
    #moeda_sq01                       = models.CharField("Moeda", max_length=255, blank=True, null=True)
    #tipo_de_operacao_sq01            = models.CharField("Tipo de Operação SQ01", max_length=255, blank=True, null=True)
    #doc_mat_sq01                     = models.CharField("Doc Mat SQ01", max_length=255, blank=True, null=True)
    #doc_ref_sq01                     = models.CharField("Doc Ref SQ01", max_length=255, blank=True, null=True)
    #quantidade_sq01                  = models.CharField("Quantidade SQ01", max_length=255, blank=True, null=True)
    #no_doc_referencia_sq01           = models.CharField("No Doc Referencia SQ01", max_length=255, blank=True, null=True)
    #preco_liq_sq01                   = models.CharField("Preco Liq", max_length=255, blank=True, null=True)
    val_comp_em_ef_moed_int_sq01     = models.CharField("Val Comp em Ef Moed Int", max_length=255, blank=True, null=True)
    #valor_faturas_registrada_sq01    = models.CharField("Valor Faturas Registrada", max_length=255, blank=True, null=True)

    class Meta:
        db_table = "dados_pedidos_pagos"
        verbose_name = "PedidoPagos"
        verbose_name_plural = "PedidoPagoss"



class DadosPedidosPendentes(models.Model):
    definicao_do_projeto = models.CharField("definicao_do_projeto", max_length=255, blank=True, null=True)
    elemento_pep         = models.CharField("elemento_pep", max_length=255, blank=True, null=True)
    doc_compra           = models.CharField("doc_compra", max_length=255, blank=True, null=True)
    data_do_documento    = models.CharField("data_do_documento", max_length=255, blank=True, null=True)
    #tipo_documento_referencia = models.CharField("tipo_documento_referencia", max_length=255, blank=True, null=True)
    empresa              = models.CharField("empresa", max_length=255, blank=True, null=True)
    #codigo_de_eliminacao = models.CharField("codigo_de_eliminacao", max_length=255, blank=True, null=True)
    #valor_moeda_objeto   = models.CharField("valor_moeda_objeto", max_length=255, blank=True, null=True)
    fornecedor           = models.CharField("fornecedor", max_length=255, blank=True, null=True)
    valor_liquido_pedido = models.CharField("valor_liquido_pedido", max_length=255, blank=True, null=True)

    class Meta:
        db_table = "dados_pedidos_pendentes"
        verbose_name = "PedidoPendentes"
        verbose_name_plural = "PedidoPendentess"

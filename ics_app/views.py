import statistics
import logging
import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import DecimalField, Count, Sum,  F, FloatField
from django.core.management.base import BaseCommand
from .models import (
    RdaAprovada, RdaSemPedido, Projeto, Pleito, Pedido,
    DadosPedidosPendentes, DadosPedidosAdiantados, DadosPedidosPagos,
    FollowupIniciativa, ProjetoIniciativa, ProvisaoGasto
)
from .forms import ProvisaoGastoForm
from .utils.config import EXCEL_PATH, ANALISTAS, RESPONSABILIDADES
from .utils.data_processing import (
    list_sheets, load_dataframe, load_all_surveys,
    filter_pleitos, filter_analista, df_to_html,
    compute_survey_metrics, save_pleitos_dataframe,
    filter_by_column, save_projetos_dataframe
)
from .utils.exceptions import DataProcessingError
from datetime import date, timedelta
import json


logger = logging.getLogger(__name__)

# Mapeamento genérico de sub_tabs para Models
TAB_MODEL_MAP = {
    'pleitos': Pleito,
    'projetos': Projeto,
    'dados_iniciativa': RdaAprovada,
    'rda_sem_pedido': RdaSemPedido,
    'pedidos': Pedido,
}

@login_required(login_url='login')
def home(request: HttpRequest) -> HttpResponse:
    main_tabs = list(EXCEL_PATH.keys()) + ['Iniciativa']
    main_tab  = request.GET.get('main_tab', main_tabs[0])
    if main_tab == 'Survey':
        sub_tabs = ['Data', 'Dash']
    elif main_tab == 'Projetos':
        sub_tabs = ['pleitos', 'projetos']
    elif main_tab == 'Iniciativa':
        sub_tabs = ['dados_iniciativa', 'rda_sem_pedido', 'pedidos']
    else:
        sub_tabs = list_sheets(main_tab)
    sub_tab = request.GET.get('sub_tab') or (sub_tabs[0] if sub_tabs else '')

    id_pleito             = request.GET.get('id_pleito', '').strip()
    id_projeto            = request.GET.get('id_projeto', '').strip()
    planta                = request.GET.get('planta', '').strip()
    analista              = request.GET.get('analista', '').strip()
    responsabilidade      = request.GET.get('responsabilidade', '').strip()
    data_pleito           = request.GET.get('data_pleito', '').strip()
    id_iniciativa         = request.GET.get('id_iniciativa', '').strip()
    numero_documento      = request.GET.get('numero_documento', '').strip()
    definicao_projeto     = request.GET.get('definicao_projeto', '').strip()
    elemento_pep          = request.GET.get('elemento_pep', '').strip()
    fornecedor_solicitado = request.GET.get('fornecedor_solicitado', '').strip()
    sap_supplier          = request.GET.get('sap_supplier', '').strip()

    if request.method == 'POST' and main_tab == 'Projetos' and sub_tab.lower() == 'pleitos':
        try:
            save_pleitos_dataframe(
                selected_id      = request.POST['selected_id_pleito'].strip(),
                analista         = request.POST['analista'].strip(),
                responsabilidade = request.POST['responsabilidade'].strip(),
                id_iniciativa    = request.POST['id_iniciativa'].strip(),
                cid_enviado      = request.POST['cid_enviado'].strip()
            )
        except DataProcessingError as e:
            logger.error("Erro ao atualizar Pleitos: %s", e)
        return redirect(f"{request.path}?main_tab=Projetos&sub_tab=pleitos")

    if request.method == 'POST' and main_tab == 'Projetos' and sub_tab.lower() == 'projetos':
        try:
            save_projetos_dataframe(
                id_gerador = request.POST['id_gerador'].strip(),
                planta     = request.POST['planta'].strip(),
                analista   = request.POST['analista'].strip()
            )
        except DataProcessingError as e:
            logger.error("Erro ao atualizar Projetos: %s", e)
        return redirect(f"{request.path}?main_tab=Projetos&sub_tab=projetos")
    
    # tratamento POST editar Propensão de Gasto
    if request.method == 'POST' and main_tab == 'Iniciativa' and sub_tab.lower() == 'dados_iniciativa':
        provisao_pk = request.POST.get('provisao_pk', '').strip()
        if provisao_pk:
            # Edição
            obj = ProvisaoGasto.objects.filter(pk=provisao_pk).first()
            form = ProvisaoGastoForm(request.POST, instance=obj)
        else:
            # Novo
            form = ProvisaoGastoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path + '?main_tab=Iniciativa&sub_tab=dados_iniciativa')

    # daqui pra baixo é só GET: monta context, incluindo form_provisao e provisoes
    form_provisao = ProvisaoGastoForm()
    provisoes     = ProvisaoGasto.objects.order_by('-data_criacao')
    headers_provisao       = [f.verbose_name for f in ProvisaoGasto._meta.fields]
    provisao_fields  = [f.name for f in ProvisaoGasto._meta.fields]

    # tratamento POST para editar RDA Sem Pedido
    if request.method == 'POST' and main_tab == 'Iniciativa' and sub_tab.lower() == 'rda_sem_pedido':
        rda_pk = request.POST.get('rda_pk')
        obj = RdaSemPedido.objects.filter(pk=rda_pk).first()
        if obj:
            sap_value = request.POST.get('sap_cofor', '').strip()
            nome_value = request.POST.get('nome_fornecedor', '').strip()
            erro_rda_value = request.POST.get('erro_rda', '').strip()

            if sap_value:
                obj.sap_cofor = sap_value
            if nome_value:
                obj.nome_fornecedor = nome_value
            if erro_rda_value == 'Sim':
                obj.erro_rda = True
            elif erro_rda_value == 'Não':
                obj.erro_rda = False
            # ⚠️ Se erro_rda_value vazio, mantém valor existente

            obj.save()

    if request.method == 'POST' and main_tab == 'Iniciativa' and sub_tab == 'pedidos':
        return redirect(f"{request.path}?main_tab=Iniciativa&sub_tab=pedidos")

    if main_tab == 'Iniciativa' and sub_tab == 'pedidos':
        headers_pendentes = [f.verbose_name for f in DadosPedidosPendentes._meta.fields]
        rows_pendentes = [
            [getattr(o, f.name) for f in DadosPedidosPendentes._meta.fields]
            for o in DadosPedidosPendentes.objects.all()
        ]
        headers_adiantados = [f.verbose_name for f in DadosPedidosAdiantados._meta.fields]
        rows_adiantados = [
            [getattr(o, f.name) for f in DadosPedidosAdiantados._meta.fields]
            for o in DadosPedidosAdiantados.objects.all()
        ]
        headers_pagos = [f.verbose_name for f in DadosPedidosPagos._meta.fields]
        rows_pagos = [
            [getattr(o, f.name) for f in DadosPedidosPagos._meta.fields]
            for o in DadosPedidosPagos.objects.all()
        ]
        return render(request, 'ics_app/home.html', {
            'main_tabs': main_tabs,
            'main_tab': main_tab,
            'sub_tabs': sub_tabs,
            'sub_tab': sub_tab,
            'analistas': ANALISTAS,
            'responsabilidades': RESPONSABILIDADES,
            'id_pleito': id_pleito,
            'id_projeto': id_projeto,
            'planta': planta,
            'analista': analista,
            'responsabilidade': responsabilidade,
            'data_pleito': data_pleito,
            'id_iniciativa': id_iniciativa,
            'fornecedor_solicitado': fornecedor_solicitado,
            'sap_supplier': sap_supplier,
            'headers_pendentes': headers_pendentes,
            'rows_pendentes': rows_pendentes,
            'headers_adiantados': headers_adiantados,
            'rows_adiantados': rows_adiantados,
            'headers_pagos': headers_pagos,
            'rows_pagos': rows_pagos,
            'df_html': None,
            'error': None,
            'form_provisao': form_provisao,
            'provisoes': provisoes,
            'headers_provisao': headers_provisao,
            'provisao_fields': provisao_fields,
        })

    # Inicialize variáveis para evitar UnboundLocalError
    headers_projetos = []
    rows_projetos = []
    total_iniciativas = 0

    if main_tab in ['Projetos', 'Iniciativa'] and sub_tab.lower() in TAB_MODEL_MAP:
        Model = TAB_MODEL_MAP[sub_tab.lower()]
        for field in Model._meta.fields:
            if isinstance(field, DecimalField):
                Model.objects.all().update(**{field.name: 0})

        qs = Model.objects.all()

        if main_tab == 'Projetos':
            if sub_tab.lower() == 'pleitos':
                if id_pleito: qs = qs.filter(id_pleito__icontains=id_pleito)
                if id_iniciativa: qs = qs.filter(id_iniciativa__icontains=id_iniciativa)
                if fornecedor_solicitado: qs = qs.filter(fornecedor_solicitado__icontains=fornecedor_solicitado)
                if sap_supplier: qs = qs.filter(sap_supplier__icontains=sap_supplier)
            else:
                if id_projeto: qs = qs.filter(id_gerador__icontains=id_projeto)
                if planta: qs = qs.filter(planta__icontains=planta)
                if analista: qs = qs.filter(analista__icontains=analista)

        if main_tab == 'Iniciativa':
            if sub_tab.lower() == 'rda_sem_pedido':
                qs = RdaSemPedido.objects.all().order_by('-data_do_documento')

                # filtros GET
                if numero_documento:
                    qs = qs.filter(nro_doc_referencia__icontains=numero_documento)
                if definicao_projeto:
                    qs = qs.filter(definicao_do_projeto__icontains=definicao_projeto)
                if elemento_pep:
                    qs = qs.filter(elemento_pep__icontains=elemento_pep)
                if planta:
                    qs = qs.filter(empresa__icontains=planta)

                # cabeçalhos e listas
                headers = [
                    "ID", "Projeto", "PEP", "RDA", "SAP", "Fornecedor", "Valor", "Data Emissão", "Planta",
                    "Dias Corridos", "Dias Úteis", "Erro na RDA", "Email 1", "Email 2", "Progresso", "Status RDA"
                ]
                rda_list = []
                atuacao_correta = necessario_atuar = 0

                # cálculo de dias, progress e flags
                for obj in qs:
                    data_emissao = obj.data_do_documento
                    if data_emissao:
                        delta = date.today() - data_emissao
                        dias_corridos = delta.days
                        dias_uteis = sum(
                            1 for i in range(1, dias_corridos + 1)
                            if (data_emissao + timedelta(days=i)).weekday() < 5
                        )
                    else:
                        dias_corridos = dias_uteis = 0

                    obj.dias_corridos = dias_corridos  # type: ignore[attr-defined]
                    obj.dias_uteis    = dias_uteis     # type: ignore[attr-defined]

                    if obj.has_email1 and (obj.has_email2 or dias_uteis < 6):
                        atuacao_correta += 1
                    if (dias_uteis >= 2 and not obj.has_email1) or (dias_uteis >= 6 and not obj.has_email2):
                        necessario_atuar += 1

                    rda_list.append(obj)

                total_rda    = len(rda_list)
                no_prazo     = sum(1 for o in rda_list if o.dias_uteis < 9)
                fora_prazo   = sum(1 for o in rda_list if o.dias_uteis >= 9)
                rda_com_erro = sum(1 for o in rda_list if o.erro_rda)

                # bloco de RdaAprovada
                numero_documento_aprovada    = request.GET.get('numero_documento_aprovada', '').strip()
                definicao_projeto_aprovada   = request.GET.get('definicao_projeto_aprovada', '').strip()
                elemento_pep_aprovada        = request.GET.get('elemento_pep_aprovada', '').strip()
                mes_ano_emissao_rda          = request.GET.get('mes_ano_emissao_rda', '').strip()
                planta_aprovada              = request.GET.get('planta', '').strip()

                qs_aprovadas = RdaAprovada.objects.all()

                try:
                    if numero_documento_aprovada:
                        req_int = int(float(numero_documento_aprovada))
                        qs_aprovadas = qs_aprovadas.filter(
                            requisicao_de_compras_agrp_rda_po=req_int
                        )
                except ValueError:
                    pass
                if definicao_projeto_aprovada:
                    qs_aprovadas = qs_aprovadas.filter(
                        definicao_do_projeto_compromisso__icontains=definicao_projeto_aprovada
                    )
                if elemento_pep_aprovada:
                    qs_aprovadas = qs_aprovadas.filter(
                        elemento_pep_agrp_rda_po__icontains=elemento_pep_aprovada
                    )
                if mes_ano_emissao_rda:
                    try:
                        ano, mes = map(int, mes_ano_emissao_rda.split('-'))
                        qs_aprovadas = qs_aprovadas.filter(
                            data_emissao_rda__year=ano,
                            data_emissao_rda__month=mes
                        )
                    except ValueError:
                        pass
                if planta_aprovada:
                    qs_aprovadas = qs_aprovadas.filter(
                        empresa_agrp_rda_po__icontains=planta_aprovada
                    )

                # for para calcular os dias úteis
                for obj in qs_aprovadas:
                    data_emissao_rda = getattr(obj, 'data_emissao_rda', None)
                    data_emissao_pedido = getattr(obj, 'data_de_criacao_agrp_rda_po', None) 
                    if data_emissao_rda and data_emissao_pedido:
                        delta = (data_emissao_pedido - data_emissao_rda).days
                        dias_uteis = sum(
                            1 for i in range(1, delta + 1)
                            if (data_emissao_rda + timedelta(days=i)).weekday() < 5
                        )
                    else:
                        dias_uteis = None
                    obj.dias_uteis = dias_uteis             # type: ignore[attr-defined]

                # Cálculo de média e mediana dos dias úteis para aprovação
                dias_uteis_lista = [
                    obj.dias_uteis for obj in qs_aprovadas  # type: ignore[attr-defined]
                    if obj.dias_uteis is not None           # type: ignore[attr-defined]
                ]
                if dias_uteis_lista:
                    media_dias_uteis = round(statistics.mean(dias_uteis_lista), 1)
                    mediana_dias_uteis = round(statistics.median(dias_uteis_lista), 1)
                else:
                    media_dias_uteis = 0
                    mediana_dias_uteis = 0

                headers_aprovadas = [f.verbose_name for f in RdaAprovada._meta.fields]
                rows_aprovadas    = [
                    [getattr(item, f.name) for f in RdaAprovada._meta.fields]
                    for item in qs_aprovadas
                ]

                total_rda_aprovada      = qs_aprovadas.count()
                no_prazo_aprovada       = sum(
                    1 for obj in qs_aprovadas if getattr(obj, 'dias_uteis', 0) is not None and obj.dias_uteis <= 5  #type: ignore[attr-defined]
                )
                fora_prazo_aprovada     = sum(
                    1 for obj in qs_aprovadas if getattr(obj, 'dias_uteis', 0) is not None and obj.dias_uteis > 5   #type: ignore[attr-defined]
                )
                rda_com_erro_aprovada   = sum(
                    1 for obj in qs_aprovadas if getattr(obj, 'erro_rda', False)
                )
                perc_no_prazo_aprovada  = round(
                    (no_prazo_aprovada / total_rda_aprovada * 100), 2
                ) if total_rda_aprovada else 0

                return render(request, 'ics_app/home.html', {
                    'main_tabs': main_tabs,
                    'main_tab': main_tab,
                    'sub_tabs': sub_tabs,
                    'sub_tab': sub_tab,
                    'analistas': ANALISTAS,
                    'responsabilidades': RESPONSABILIDADES,
                    'numero_documento': numero_documento,
                    'definicao_projeto': definicao_projeto,
                    'elemento_pep': elemento_pep,
                    'headers': headers,
                    'rda_list': rda_list,
                    'total_rda': total_rda,
                    'no_prazo': no_prazo,
                    'fora_prazo': fora_prazo,
                    'atuacao_correta': atuacao_correta,
                    'necessario_atuar': necessario_atuar,
                    'rda_com_erro': rda_com_erro,
                    'headers_aprovadas': headers_aprovadas,
                    'rows_aprovadas': rows_aprovadas,
                    'total_rda_aprovada': total_rda_aprovada,
                    'no_prazo_aprovada': no_prazo_aprovada,
                    'fora_prazo_aprovada': fora_prazo_aprovada,
                    'rda_com_erro_aprovada': rda_com_erro_aprovada,
                    'perc_no_prazo_aprovada': perc_no_prazo_aprovada,
                    'media_dias_uteis': media_dias_uteis,
                    'mediana_dias_uteis': mediana_dias_uteis,
                    'numero_documento_aprovada': numero_documento_aprovada,
                    'definicao_projeto_aprovada': definicao_projeto_aprovada,
                    'elemento_pep_aprovada': elemento_pep_aprovada,
                    'mes_ano_emissao_rda': mes_ano_emissao_rda,
                    'planta': planta,
                    'planta_aprovada': planta_aprovada,
                })

        # -------- VISAO DE INICIATIVAS --------

            elif sub_tab.lower() == 'dados_iniciativa':
                qs_projetos = ProjetoIniciativa.objects.all().order_by('-ano_aprovacao')
                headers_projetos = [f.verbose_name for f in ProjetoIniciativa._meta.fields]
                rows_projetos    = [
                    [getattr(item, f.name) for f in ProjetoIniciativa._meta.fields]
                    for item in qs_projetos
                ]
                total_iniciativas = len(rows_projetos)

                # --- conta quantos de cada status há na base ---
                status_counts = {
                    d['status']: d['n']
                    for d in ProjetoIniciativa.objects
                        .values('status')
                        .annotate(n=Count('status'))
                }

                count_AUT  = status_counts.get('AUT',  0)
                count_CHA  = status_counts.get('CH_A', 0)
                count_CHB  = status_counts.get('CH_B', 0)
                count_CHC  = status_counts.get('CH_C', 0)

                total_abertas = count_AUT + count_CHA + count_CHB
                total_fechadas = count_CHC

                # soma orçamento total
                valor_total_liq_iniciativas = qs_projetos.aggregate(total=Sum('orcamento'))['total'] or 0

                valor_total_ativas = qs_projetos.filter(status__in=['AUT','CH_A','CH_B']) \
                                        .aggregate(total=Sum('orcamento'))['total'] or 0
                valor_total_fechadas = qs_projetos.filter(status='CH_C') \
                                            .aggregate(total=Sum('orcamento'))['total'] or 0
                
                total_provisoes = provisoes.count()

                valor_total_provisoes = provisoes.aggregate(total=Sum('provisao'))['total'] or 0

                # === NOVO BLOCO DE FILTRO E GRÁFICO ===
                iniciativas_filtradas = request.GET.getlist('iniciativa')
                qs_projeto = ProjetoIniciativa.objects.all()
                if iniciativas_filtradas:
                    qs_projeto = qs_projeto.filter(iniciativa__in=iniciativas_filtradas)
                todas_iniciativas = ProjetoIniciativa.objects.values_list('iniciativa', flat=True).order_by('iniciativa').distinct()

                # Monta os arrays para o gráfico:
                labels = []
                consumido = []
                proposto = []
                livre = []
                qs_provisao = ProvisaoGasto.objects.all()
                provisao_lookup = {}
                for obj in qs_provisao:
                    chave = getattr(obj, 'iniciativa', None)
                    if chave:
                        provisao_lookup[chave] = provisao_lookup.get(chave, 0) + float(obj.provisao or 0)

                for ini in qs_projeto:
                    id_iniciativa = ini.iniciativa
                    labels.append(ini.descricao or ini.iniciativa or str(id_iniciativa))
                    val_orc = float(ini.orcamento or 0)
                    val_consumido = float(getattr(ini, 'valor_total_pedidos_pagos', 0) or 0)
                    val_proposto = float(provisao_lookup.get(id_iniciativa, 0))
                    val_livre = max(0, val_orc - val_consumido - val_proposto)
                    consumido.append(val_consumido)
                    proposto.append(val_proposto)
                    livre.append(val_livre)

                # Recebe uma lista de iniciativas selecionadas
                iniciativa_selecionada = request.GET.getlist('iniciativa')  # Agora retorna lista!

                return render(request, 'ics_app/home.html', {
                    'main_tabs': main_tabs,
                    'main_tab': main_tab,
                    'sub_tabs': sub_tabs,
                    'sub_tab': sub_tab,
                    'analistas': ANALISTAS,
                    'responsabilidades': RESPONSABILIDADES,

                    'headers_projetos': headers_projetos,
                    'rows_projetos': rows_projetos,
                    'projetos': qs_projetos,

                    'total_iniciativas': total_iniciativas,
                    'valor_total_liq_iniciativas': valor_total_liq_iniciativas,

                    # métricas novas por status
                    'count_AUT': count_AUT,
                    'count_CH_A': count_CHA,
                    'count_CH_B': count_CHB,
                    'count_CH_C': count_CHC,
                    'total_abertas': total_abertas,
                    'total_fechadas': total_fechadas,
                    'valor_total_fechadas': valor_total_fechadas,
                    'valor_total_ativas': valor_total_ativas,

                    # ADICIONE ESTAS LINHAS ABAIXO:
                    'form_provisao': form_provisao,
                    'provisoes': provisoes,
                    'headers_provisao': headers_provisao,
                    'provisao_fields': provisao_fields,
                    'total_previsoes': total_provisoes,
                    'valor_total_provisoes': valor_total_provisoes,
                    
                    'grafico_iniciativas_labels': labels,
                    'grafico_iniciativas_consumido': consumido,
                    'grafico_iniciativas_proposto': proposto,
                    'grafico_iniciativas_livre': livre,
                    'iniciativa_selecionada': iniciativa_selecionada,
                    'todas_iniciativas': todas_iniciativas,
                })

    # ------- SURVEY ---------
    
    context = {
        'main_tabs': main_tabs, 'main_tab': main_tab,
        'sub_tabs': sub_tabs, 'sub_tab': sub_tab,
        'analistas': ANALISTAS, 'responsabilidades': RESPONSABILIDADES,
        'id_pleito': id_pleito, 'id_projeto': id_projeto,
        'planta': planta, 'analista': analista,
        'responsabilidade': responsabilidade,
        'data_pleito': data_pleito, 'id_iniciativa': id_iniciativa,
        'fornecedor_solicitado': fornecedor_solicitado,
        'sap_supplier': sap_supplier,
        'df_html': None, 'error': None,
    }
    try:
        if main_tab == 'Survey' and sub_tab == 'Dash':
            df_survey = load_all_surveys()
            n, codes, rates = compute_survey_metrics(df_survey)
            context.update({
                'n_surveys': n,
                'survey_codes_json': codes,
                'response_rates_json': rates,
            })
        elif main_tab == 'Survey' and sub_tab == 'Data':
            df_all = load_all_surveys()
            context['df_html'] = df_to_html(df_all)
        else:
            df = load_dataframe(main_tab, sub_tab)
            if sub_tab.lower() == 'pleitos':
                df = filter_pleitos(df, id_pleito)
                df = filter_analista(df, analista)
                df = filter_by_column(df, 'DATA PLEITO', data_pleito)
                df = filter_by_column(df, 'ID INICIATIVA', id_iniciativa)
                df = filter_by_column(df, 'FORNECEDOR SOLICITADO', fornecedor_solicitado)
                df = filter_by_column(df, 'SAP SUPPLIER', sap_supplier)
            elif sub_tab.lower() == 'projetos':
                df = filter_by_column(df, 'GERADOR ID PROJETO', id_projeto)
                df = filter_by_column(df, 'PLANTA', planta)
                df = filter_by_column(df, 'ID INICIATIVA', id_iniciativa)
                df = filter_by_column(df, 'ANALISTA', analista)
                df = filter_by_column(df, 'FORNECEDOR', fornecedor_solicitado)
                df = filter_by_column(df, 'SAP', sap_supplier)
            context['df_html'] = df_to_html(df)
    except DataProcessingError as e:
        logger.error("Erro ao processar dados: %s", e)
        context['error'] = str(e)

    return render(request, 'ics_app/home.html', context)

@login_required
def dados_grafico_iniciativas(request):
    # Pega as iniciativas selecionadas (pode ser múltipla!)
    iniciativas = request.GET.getlist('iniciativa')
    qs_provisao_gasto = ProvisaoGasto.objects.all()
    provisao_lookup = {}
    for obj in qs_provisao_gasto:
        chave = getattr(obj, 'iniciativa', None)
        if chave:
            provisao_lookup[chave] = provisao_lookup.get(chave, 0) + float(obj.provisao or 0)

    qs_projeto_iniciativa = ProjetoIniciativa.objects.all()
    if iniciativas:
        qs_projeto_iniciativa = qs_projeto_iniciativa.filter(iniciativa__in=iniciativas)

    # Prepara os dados
    labels, consumido, proposto, livre = [], [], [], []
    for ini in qs_projeto_iniciativa:
        id_iniciativa = ini.iniciativa
        labels.append(ini.descricao or ini.iniciativa or str(id_iniciativa))
        val_orc = float(ini.orcamento or 0)
        val_consumido = float(getattr(ini, 'valor_total_pedidos_pagos', 0) or 0)
        val_proposto = float(provisao_lookup.get(id_iniciativa, 0))
        val_livre = max(0, val_orc - val_consumido - val_proposto)
        consumido.append(val_consumido)
        proposto.append(val_proposto)
        livre.append(val_livre)

    return JsonResponse({
        'labels': labels,
        'consumido': consumido,
        'proposto': proposto,
        'livre': livre,
    })






@login_required(login_url='login')
def pleitos_dashboard(request: HttpRequest) -> HttpResponse:
    """
    View para exibir o dashboard da aba Pleitos com layout detalhado.
    """

    try:
        df = load_dataframe("Projetos", "Pleitos").fillna("")

        # Conversão de data
        df['DATA PLEITO'] = pd.to_datetime(df['DATA PLEITO'], errors='coerce')
        df['DATA ANÁLISE FINAL'] = pd.to_datetime(df['DATA ANÁLISE FINAL'], errors='coerce')

        # Métricas principais
        total_pleitos = len(df)
        pleitos_aprovados = df[df['STATUS PLEITO'] == 'APROVADO'].shape[0]
        total_surveys = df['Nº SURVEY'].replace("-", pd.NA).dropna().nunique()
        total_inicial = df['PLEITO INICIAL'].apply(pd.to_numeric, errors='coerce').sum()
        total_validado = df['PLEITO VALOR FINAL'].apply(pd.to_numeric, errors='coerce').sum()
        total_reducao = df['VALOR DE REDUÇÃO'].apply(pd.to_numeric, errors='coerce').sum()

        df_validos = df[df['DATA ANÁLISE FINAL'].notna() & df['DATA PLEITO'].notna()].copy()
        df_validos['DIAS_ANALISE'] = (df_validos['DATA ANÁLISE FINAL'] - df_validos['DATA PLEITO']).dt.days
        media_dias = round(df_validos['DIAS_ANALISE'].mean(), 2) if not df_validos.empty else 0

        # Em Análise
        df_em_analise = df[df['DATA ANÁLISE FINAL'] == ""]
        total_em_analise_valor = df_em_analise['PLEITO VALOR FINAL'].apply(pd.to_numeric, errors='coerce').sum()
        total_em_analise_qtd = len(df_em_analise)

        # Pleitos por mês (quantidade)
        df_mes = df.copy()
        df_mes = df_mes[df_mes['DATA PLEITO'].notna()]
        df_mes['MES_ANO'] = df_mes['DATA PLEITO'].dt.strftime('%b/%Y')
        pleitos_por_mes = df_mes.groupby('MES_ANO').size().to_dict()

        # Valores dos pleitos por mês
        valores_por_mes = df_mes.groupby('MES_ANO')['PLEITO VALOR FINAL'].apply(lambda x: pd.to_numeric(x, errors='coerce').sum()).to_dict()

        # Fornecedores vs Pleitos (PLEITO VALIDADO + COST AVOIDANCE)
        if 'PLEITO VALIDADO' not in df.columns:
            df['PLEITO VALIDADO'] = 0
        if 'COST AVOIDANCE' not in df.columns:
            df['COST AVOIDANCE'] = 0
        df['PLEITO VALIDADO'] = pd.to_numeric(df['PLEITO VALIDADO'], errors='coerce').fillna(0)
        df['COST AVOIDANCE'] = pd.to_numeric(df['COST AVOIDANCE'], errors='coerce').fillna(0)
        fornecedores_pleitos = (
            df.groupby('FORNECEDOR SOLICITADO')[['PLEITO VALIDADO', 'COST AVOIDANCE']]
            .sum()
            .sort_values(by='PLEITO VALIDADO', ascending=False)
            .head(10)
            .to_dict(orient='index')
        )

        # Status por Fornecedor
        status_fornecedor = (
            df.groupby(['FORNECEDOR SOLICITADO', 'STATUS PLEITO'])
            .size()
            .unstack(fill_value=0)
            .to_dict(orient='index')
        )

        # Origem do Pleito
        origem_pleito = df['ORIGEM PLEITO'].value_counts().to_dict()

        # Responsabilidade Sorting (classificação de triagem)
        triagem = df['RESPONSABILIDADE SORTING'].value_counts().to_dict()

        context = {
            'total_pleitos': total_pleitos,
            'pleitos_aprovados': pleitos_aprovados,
            'total_surveys': total_surveys,
            'total_inicial': f"{total_inicial:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            'total_validado': f"{total_validado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            'total_reducao': f"{total_reducao:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            'media_dias': media_dias,
            'em_analise_valor': f"{total_em_analise_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            'em_analise_qtd': total_em_analise_qtd,
            'pleitos_mes': json.dumps(pleitos_por_mes),
            'valores_mes': json.dumps(valores_por_mes),
            'fornecedores_pleitos': json.dumps(fornecedores_pleitos),
            'status_fornecedor': json.dumps(status_fornecedor),
            'origem_pleito': json.dumps(origem_pleito),
            'triagem': json.dumps(triagem),
        }

        return render(request, 'ics_app/pleitos_dash.html', context)

    except DataProcessingError as e:
        logger.error("Erro ao carregar dados para Dashboard Pleitos: %s", e)
        return HttpResponse("Erro ao carregar dados.", status=500)

@login_required(login_url='login')
def projetos_dashboard(request: HttpRequest) -> HttpResponse:
    """
    View para exibir a aba Projetos usando dados vindos do banco (ORM).
    """
    # filtros vindos da querystring
    id_gerador = request.GET.get('id_gerador', '').strip()
    planta     = request.GET.get('planta', '').strip()
    analista   = request.GET.get('analista', '').strip()

    # monta o queryset e aplica filtros
    qs = Projeto.objects.all()
    if id_gerador:
        qs = qs.filter(id_gerador__icontains=id_gerador)
    if planta:
        qs = qs.filter(planta__icontains=planta)
    if analista:
        qs = qs.filter(analista__icontains=analista)

    # monta cabeçalhos e linhas a partir dos campos do modelo
    headers = [f.verbose_name for f in Projeto._meta.fields]
    rows    = [
        [getattr(obj, f.name) for f in Projeto._meta.fields]
        for obj in qs
    ]

    return render(request, 'ics_app/projetos_dash.html', {
        'headers':    headers,
        'rows':       rows,
        'id_gerador': id_gerador,
        'planta':     planta,
        'analista':   analista,
    })

@login_required
def registrar_email(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método inválido'}, status=405)

    tipo = request.POST.get('tipo')  # 'email1' ou 'email2'
    rda = get_object_or_404(RdaSemPedido, pk=pk)

    # Campos extras opcionais
    data_envio_daf = request.POST.get('data_envio_daf')
    dias_uteis = request.POST.get('dias_uteis')
    dias_corridos = request.POST.get('dias_corridos')
    observacoes = request.POST.get('observacoes')

    # Verifica se já existe follow-up para este tipo
    existing_action = rda.email_actions.filter(tipo=tipo).first() # type: ignore[attr-defined]

    if existing_action:
        # Caso: desmarcar ⇒ apenas superuser pode
        if request.user.is_superuser:
            existing_action.delete()
        else:
            return JsonResponse({'success': False, 'error': 'Apenas superuser pode desmarcar.'})
    else:
        # Caso: registrar follow-up normal
        FollowupIniciativa.objects.create(
            rda=rda,
            tipo=tipo,
            user=request.user,
            data_envio_daf=data_envio_daf,
            dias_uteis=dias_uteis or None,
            dias_corridos=dias_corridos or None,
            observacoes=observacoes
        )

    return JsonResponse({
        'success': True,
        'tipo': tipo,
        'progress': rda.progress,
        'user': request.user.get_full_name() or request.user.username,
    })

@login_required
def aprovar_rda(request, pk):
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    rda = get_object_or_404(RdaSemPedido, pk=pk)

    # 🔧 Conversão robusta para inteiro (corrigindo o erro original)
    try:
        requisicao = int(float(rda.nro_doc_referencia))
    except (ValueError, TypeError):
        return JsonResponse({"error": "Requisição inválida"}, status=400)
    
    valor = rda.total_valor_moeda_objeto
    data_emissao_rda = rda.data_do_documento

    obj, _ = RdaAprovada.objects.update_or_create(
        requisicao_de_compras_agrp_rda_po=requisicao,
        defaults={
            "data_emissao_rda": data_emissao_rda,
        }
    )

    # Campos adicionais: preencher se ainda não preenchidos
    if not obj.data_emissao_rda:
        obj.data_emissao_rda = rda.data_do_documento
    if obj.erro_rda is None:
        obj.erro_rda = rda.erro_rda or False
    if obj.email1_enviado is None:
        obj.email1_enviado = rda.has_email1
    if obj.email2_enviado is None:
        obj.email2_enviado = rda.has_email2
    if not obj.progresso:
        obj.progresso = rda.progress

    obj.save()

    rda.delete()

    return JsonResponse({"success": True})


@login_required
def excluir_provisao_gasto(request, pk):
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)
    obj = get_object_or_404(ProvisaoGasto, pk=pk)
    obj.delete()
    return JsonResponse({"success": True})
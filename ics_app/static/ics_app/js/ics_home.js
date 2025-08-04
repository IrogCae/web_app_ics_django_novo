function getCSRFToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

document.addEventListener('DOMContentLoaded', () => {
      const table = document.querySelector('table.table');
      const form  = document.getElementById('update-form');
      if (form) form.reset();
      if (!table) return;

      // Destaca linha selecionada em todas as tabelas responsivas
      document.querySelectorAll('.table-responsive table').forEach(tbl => {
        tbl.querySelectorAll('tbody tr').forEach(row => {
          row.addEventListener('click', () => {
            tbl.querySelectorAll('tbody tr').forEach(r => r.classList.remove('table-active'));
            row.classList.add('table-active');
          });
        });
      });

      // Editar Provisão de Gasto
      const btnEditarProvisao = document.getElementById('btn-editar-provisao');
      const btnExcluirProvisao = document.getElementById('btn-excluir-provisao');
      if (btnEditarProvisao) {
        btnEditarProvisao.addEventListener('click', () => {
          // Procura a tabela correta (NOVA PROVISAO)
          const table = document.querySelector('.table-responsive table');
          const sel = table.querySelector('tbody tr.table-active');
          if (!sel) return alert('Selecione uma linha da tabela NOVA PROVISÃO antes de editar.');

          const cells = sel.querySelectorAll('td');

          // Pega o PK para edição (do atributo data-id do <tr>)
          document.getElementById('provisao_pk').value = sel.getAttribute('data-id') || '';

          // Agora pula o primeiro <td> (ID), e preenche os campos a partir do 1 (ID do Projeto)
          document.getElementById('id_id_projeto').value = cells[1].innerText.trim();
          document.getElementById('id_projeto').value = cells[2].innerText.trim();
          document.getElementById('id_iniciativa').value = cells[3].innerText.trim();
          document.getElementById('id_descricao').value = cells[4].innerText.trim();
          // Remove R$ e pontos, troca vírgula por ponto para valor decimal
          document.getElementById('id_provisao').value = cells[5].innerText.replace(/[^\d,.-]/g, '').replace(/\./g, '').replace(',', '.');

          // Mostra o botão Excluir (só em modo edição)
          if (btnExcluirProvisao) btnExcluirProvisao.style.display = '';

          // Abre o modal já preenchido
          new bootstrap.Modal(document.getElementById('modalNovaPropensao')).show();
        });
      }

      // Esconde o botão Excluir ao abrir para inserir (quando abrir modal pelo botão "Inserir Propensão de Gasto")
      const btnInserirProvisao = document.querySelector('[data-bs-target="#modalNovaPropensao"]');
      if (btnInserirProvisao && btnExcluirProvisao) {
        btnInserirProvisao.addEventListener('click', () => {
          btnExcluirProvisao.style.display = 'none';
          // Limpa o campo PK (para garantir que será inserção)
          document.getElementById('provisao_pk').value = '';
          // Limpa os campos do form (opcional)
          document.getElementById('id_id_projeto').value = '';
          document.getElementById('id_projeto').value = '';
          document.getElementById('id_iniciativa').value = '';
          document.getElementById('id_descricao').value = '';
          document.getElementById('id_provisao').value = '';
        });
      }

      // Função de excluir propensão de gasto (requisição AJAX)
      if (btnExcluirProvisao) {
        btnExcluirProvisao.addEventListener('click', function () {
          const pk = document.getElementById('provisao_pk').value;
          if (!pk) return;
          if (!confirm('Tem certeza que deseja excluir esta Propensão de Gasto?')) return;

          fetch(`/excluir_provisao_gasto/${pk}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCSRFToken() }
          })
          .then(resp => {
            if (!resp.ok) throw new Error('Erro ao excluir');
            location.reload();
          })
          .catch(err => alert('Erro ao excluir: ' + err));
        });
      }

      // Tabela de iniciativas (segunda tabela na página)
      const tables = document.querySelectorAll('.table-responsive table');
      const tabelaIniciativas = tables.length > 1 ? tables[1] : null;

      // Editar Iniciativa
      const btnEditarIniciativa = document.getElementById('btn-editar-iniciativa');
      const btnExcluirIniciativa = document.getElementById('btn-excluir-iniciativa');
      const btnInserirIniciativa = document.querySelector('[data-bs-target="#modalNovaIniciativa"]');
      if (btnEditarIniciativa && tabelaIniciativas) {
        btnEditarIniciativa.addEventListener('click', () => {
          const sel = tabelaIniciativas.querySelector('tbody tr.table-active');
          if (!sel) return alert('Selecione uma linha da tabela INICIATIVAS antes de editar.');
          const cells = sel.querySelectorAll('td');
          const modal = document.getElementById('modalNovaIniciativa');
          modal.querySelector('#iniciativa_pk').value = sel.getAttribute('data-id') || '';
          modal.querySelector('[name="comite"]').value = cells[1].innerText.trim();
          modal.querySelector('[name="e_car"]').value = cells[2].innerText.trim();
          modal.querySelector('[name="projetos_para_extracao"]').value = cells[3].innerText.trim();
          modal.querySelector('[name="iniciativa"]').value = cells[4].innerText.trim();
          modal.querySelector('[name="descricao"]').value = cells[5].innerText.trim();
          modal.querySelector('[name="planta"]').value = cells[6].innerText.trim();
          modal.querySelector('[name="ano_aprovacao"]').value = cells[7].innerText.trim();
          modal.querySelector('[name="bdgt"]').value = cells[8].innerText.trim();
          modal.querySelector('[name="status"]').value = cells[9].innerText.trim();
          modal.querySelector('[name="orcamento"]').value = cells[10].innerText.replace(/[^\d,.-]/g, '').replace(/\./g, '').replace(',', '.');
          modal.querySelector('[name="disposto_sem_imposto"]').value = cells[11].innerText.replace(/[^\d,.-]/g, '').replace(/\./g, '').replace(',', '.');
          modal.querySelector('[name="valor_total_pedidos_emitidos"]').value = cells[12].innerText.replace(/[^\d,.-]/g, '').replace(/\./g, '').replace(',', '.');
          modal.querySelector('[name="valor_total_pedidos_pagos"]').value = cells[13].innerText.replace(/[^\d,.-]/g, '').replace(/\./g, '').replace(',', '.');
          modal.querySelector('[name="provisao"]').value = cells[14].innerText.trim();

          if (btnExcluirIniciativa) btnExcluirIniciativa.style.display = '';
          new bootstrap.Modal(modal).show();
        });
      }

      if (btnInserirIniciativa && btnExcluirIniciativa) {
        btnInserirIniciativa.addEventListener('click', () => {
          btnExcluirIniciativa.style.display = 'none';
          const modal = document.getElementById('modalNovaIniciativa');
          modal.querySelector('#iniciativa_pk').value = '';
          modal.querySelectorAll('input').forEach(el => { if (el.type !== 'hidden') el.value = ''; });
        });
      }

      if (btnExcluirIniciativa) {
        btnExcluirIniciativa.addEventListener('click', function () {
          const pk = document.getElementById('iniciativa_pk').value;
          if (!pk) return;
          if (!confirm('Tem certeza que deseja excluir esta Iniciativa?')) return;

          fetch(`/excluir_iniciativa/${pk}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCSRFToken() }
          })
          .then(resp => {
            if (!resp.ok) throw new Error('Erro ao excluir');
            location.reload();
          })
          .catch(err => alert('Erro ao excluir: ' + err));
        });
      }

      // Editar RDA
      const btnEditarRda = document.getElementById('btn-editar-rda');
      if (btnEditarRda) {
        btnEditarRda.addEventListener('click', () => {
          const sel = document.querySelector('tbody tr.table-active');
          if (!sel) return alert('Selecione uma linha antes de editar.');

          // Captura diretamente o data-id (pk) da linha selecionada
          const pk = sel.getAttribute('data-id');
          document.getElementById('rda_pk').value = pk;

          // Continua buscando valores para sap_cofor e nome_fornecedor
          const headers = Array.from(document.querySelectorAll('thead th')).map(h =>
            h.innerText.replace(/\n/g, ' ').replace(/\s+/g, ' ').trim().toLowerCase()
          );
          const cells = sel.querySelectorAll('td');
          const idx = {
            sap: headers.indexOf('sap/cofor'),
            nome: headers.indexOf('nome fornecedor'),
          };
          document.getElementById('sap_cofor').value = cells[idx.sap]?.innerText.trim() || '';
          document.getElementById('nome_fornecedor').value = cells[idx.nome]?.innerText.trim() || '';

          new bootstrap.Modal(document.getElementById('modalEditarRda')).show();
        });
      }

      // Editar Projeto
      const btnEditarProj = document.getElementById('btn-editar-projeto');
      if (btnEditarProj) {
        btnEditarProj.addEventListener('click', () => {
          const sel = document.querySelector('tbody tr.table-active');
          if (!sel) return alert('Selecione uma linha antes de editar.');
          const headers = Array.from(document.querySelectorAll('thead th')).map(h =>
            h.innerText.replace(/\n/g, ' ').replace(/\s+/g, ' ').trim().toLowerCase()
          );
          const idx = {
            ger: headers.indexOf('id gerador'),
            planta: headers.indexOf('planta'),
            anal: headers.indexOf('analista')
          };
          document.getElementById('id_gerador').value       = sel.cells[idx.ger]?.innerText.trim() || '';
          document.getElementById('planta').value           = sel.cells[idx.planta]?.innerText.trim() || '';
          document.getElementById('analista_projeto').value = sel.cells[idx.anal]?.innerText.trim() || '';
          new bootstrap.Modal(document.getElementById('modalNovoProjeto')).show();
        });
      }

      // Editar Pleito
      const btnEditar = document.getElementById('btn-editar-pleito');
      if (btnEditar) {
        const modalPleito = new bootstrap.Modal(document.getElementById('modalNovoPleito'));
        btnEditar.addEventListener('click', () => {
          const sel = document.querySelector('tbody tr.table-active');
          if (!sel) return alert('Selecione uma linha antes de editar.');
          const headers = Array.from(table.querySelectorAll('thead th')).map(h => h.innerText.trim().toLowerCase());
          const idx = {
            id: headers.indexOf('id pleito'),
            init: headers.indexOf('id iniciativa'),
            cid: headers.indexOf('cid enviado'),
            analista: headers.indexOf('analista responsável'),
            resp: headers.indexOf('responsabilidade')
          };
          document.getElementById('selected_id_pleito').value           = sel.cells[idx.id]?.innerText.trim() || '';
          document.getElementById('id_iniciativa').value                = sel.cells[idx.init]?.innerText.trim() || '';
          document.getElementById('cid_enviado').value                  = sel.cells[idx.cid]?.innerText.trim() || '';
          document.getElementById('analista_upd').value                 = sel.cells[idx.analista]?.innerText.trim() || '';
          document.getElementById('responsabilidade_upd').value         = sel.cells[idx.resp]?.innerText.trim() || '';
          modalPleito.show();
        });
      }

      // ─── Novo: Preencher e controlar modal de envio de e-mail ─────────────────────
      const emailModalEl = document.getElementById('modalEnvioEmail');
      if (emailModalEl) {
        emailModalEl.addEventListener('show.bs.modal', event => {
          const btn = event.relatedTarget;
          const tr  = btn.closest('tr');
          const cells = tr.querySelectorAll('td');
          // popula a tabela interna do modal
          document.getElementById('modalIniciativa'   ).innerText = cells[0]?.innerText.trim() || '';
          document.getElementById('modalProjeto'      ).innerText = cells[1]?.innerText.trim() || '';
          document.getElementById('modalPep'          ).innerText = cells[2]?.innerText.trim() || '';          
          document.getElementById('modalRda'          ).innerText = cells[3]?.innerText.trim() || '';
          document.getElementById('modalValorEmissao' ).innerText = cells[4]?.innerText.trim() || '';
          document.getElementById('modalDataEmissao'  ).innerText = cells[5]?.innerText.trim() || '';
          document.getElementById('modalPlanta'       ).innerText = cells[6]?.innerText.trim() || '';
          document.getElementById('modalDiasCorridos' ).innerText = cells[7]?.innerText.trim() || '';
          document.getElementById('modalDiasUteis'    ).innerText = cells[8]?.innerText.trim() || '';
          document.getElementById('modalEnvioDaf'     ).innerText = cells[9]?.innerText.trim() || '';

          // monta dinamicamente o HTML da tabela
          const ths = Array.from(document.querySelectorAll('table.table thead th'))
                            .map(th => th.innerText.trim());
          const tds = Array.from(cells).map(td => td.innerText.trim());
          let tableHTML = '<table style="border-collapse:collapse;width:100%;">';
          // cabeçalho
          tableHTML += '<tr>';
          ths.forEach((h,i) => {
            if (i < tds.length) {
              tableHTML += `<th style="border:1px solid #ccc;padding:4px;background:#eee;">${h}</th>`;
            }
          });
          tableHTML += '</tr>';
          // linha de valores
          tableHTML += '<tr>';
          tds.forEach(v => {
            tableHTML += `<td style="border:1px solid #ccc;padding:4px;">${v}</td>`;
          });
          tableHTML += '</tr>';
          tableHTML += '</table>';

          // insere no div editável
          document.getElementById('emailCorpo').innerHTML = tableHTML;

          // guarda pk e tipo para o submit
          const formEmail = emailModalEl.querySelector('#formEnvioEmail');
          formEmail.dataset.pk   = btn.dataset.pk;
          formEmail.dataset.tipo = btn.classList.contains('btn-email1') ? 'email1' : 'email2';
        });
      }

      // Handler do submit do formulário de envio de e-mail
      const emailForm = document.getElementById('formEnvioEmail');
      if (emailForm) {
        emailForm.addEventListener('submit', ev => {
          ev.preventDefault();
          const pk   = emailForm.dataset.pk;
          const tipo = emailForm.dataset.tipo;
          const data = new URLSearchParams(new FormData(emailForm));
          data.append('tipo', tipo);

          fetch(`/rda/${pk}/registrar-email/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCSRFToken() },
            body: data
          })
          .then(r => r.json())
          .then(resp => {
            if (!resp.success) throw new Error('Falha no registro');
            // fecha o modal
            bootstrap.Modal.getInstance(emailModalEl).hide();
            // atualiza o ícone e tooltip na linha
            const row = document.querySelector(`tr[data-id="${pk}"]`);
            const btnSel = row.querySelector(`.btn-${tipo}`);
            const icon = btnSel.querySelector('i');
            icon.classList.remove('text-muted','text-danger');
            icon.classList.add('text-success');
            icon.title = `Enviado em ${new Date(resp.enviado_em).toLocaleString()} por ${resp.user}`;
            // atualiza progresso
            const pb = row.querySelector('.progress-bar');
            pb.style.width   = resp.progress + '%';
            pb.textContent   = resp.progress + '%';
          })
          .catch(console.error);
        });
      }

      // Ajusta largura inicial da barra de progresso
      document.querySelectorAll('.progress-bar').forEach(bar => {
        const v = bar.dataset.prog || '0';
        bar.style.width = `${v}%`;
      });
      // ─── Inicializa todos os tooltips do Bootstrap ───
      const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
      );
      tooltipTriggerList.forEach(el =>
        new bootstrap.Tooltip(el)
      );
    });
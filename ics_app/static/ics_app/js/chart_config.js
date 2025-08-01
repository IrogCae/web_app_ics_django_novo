// Ativa datalabels em todos os gráficos Chart.js
Chart.register(ChartDataLabels);

Chart.defaults.plugins.datalabels = {
  anchor: 'end',
  align: 'top',
  color: '#fff',
  font: {
    weight: 'bold',
    size: 12
  },
  formatter: function(value) {
    if (typeof value === 'number') {
      return value.toLocaleString('pt-BR');
    }
    return value;
  }
};

// Ativa datalabels global
Chart.register(ChartDataLabels);

Chart.defaults.plugins.datalabels = {
  anchor: 'end',
  align: 'top',
  color: '#fff',
  font: {
    weight: 'bold',
    size: 12
  },
  formatter: function(value) {
    // Abrevia milhares para 'K', milhões para 'Mi'
    if (typeof value === 'number') {
      if (value >= 1_000_000) return (value/1_000_000).toFixed(1).replace('.', ',') + 'Mi';
      if (value >= 1_000)     return (value/1_000).toFixed(0) + 'K';
      return value.toLocaleString('pt-BR');
    }
    return value;
  }
};

// GRÁFICO INICIATIVAS (Horizontal)
if (window.graficoIniciativasConfig) {
  const cfg = window.graficoIniciativasConfig;
  new Chart(document.getElementById('graficoIniciativasValores'), {
    type: 'bar',
    data: {
      labels: cfg.labels,
      datasets: [
        {
          label: 'Valor Consumido',
          data: cfg.consumido,
          backgroundColor: '#4960caff',
          stack: 'Total',
          maxBarThickness: 50,
        },
        {
          label: 'Valor Proposto',
          data: cfg.proposto,
          backgroundColor: '#ffe066',
          stack: 'Total',
          maxBarThickness: 50
        },
        {
          label: 'Valor Livre',
          data: cfg.livre,
          backgroundColor: '#406e3fff',
          stack: 'Total',
          maxBarThickness: 50
        }
      ]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        datalabels: {
          anchor: 'center',
          align: 'center',
          color: '#000',
          font: { weight: 'bold' },
          formatter: v => {
            if (typeof v === 'number') {
              return v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 });
            }
            return v;
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          stacked: true,
          title: { display: true, text: 'Orçamento (R$)' },
          ticks: {
            callback: function(value) {
              return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 });
            }
          }
        },
        y: { stacked: true }
      }
    }
  });
}


// GRÁFICO INICIATIVAS POR ANO
if (window.chartAnoConfig) {
  new Chart(document.getElementById('chartAno'), {
    type: 'bar',
    data: {
      labels: window.chartAnoConfig.labels,
      datasets: [{
        label: 'Qtd. de Iniciativas',
        data: window.chartAnoConfig.data,
        backgroundColor: '#007bff'
      }]
    },
    options: { responsive: true }
  });
}

// GRÁFICO ORÇAMENTO POR STATUS
if (window.chartOrcamentoStatusConfig) {
  new Chart(document.getElementById('chartOrcamentoStatus'), {
    type: 'bar',
    data: {
      labels: window.chartOrcamentoStatusConfig.labels,
      datasets: [{
        label: 'Orçamento (R$)',
        data: window.chartOrcamentoStatusConfig.data,
        backgroundColor: '#28a745'
      }]
    },
    options: { responsive: true }
  });
}


document.addEventListener('DOMContentLoaded', function () {
  // Só executa se o canvas da sub-aba existir (evita rodar em outras abas)
  const canvas = document.getElementById('graficoIniciativasSubaba');
  if (canvas && window.graficoIniciativasConfig) {
    const cfg = window.graficoIniciativasConfig;
    // Ajusta altura dinâmica para muitas iniciativas
    canvas.height = (cfg.labels && cfg.labels.length > 20) ? cfg.labels.length * 32 : 480;

    new Chart(canvas, {
      type: 'bar',
      data: {
        labels: cfg.labels,
        datasets: [
          { label: 'Valor Consumido', data: cfg.consumido, backgroundColor: '#310ff0' },
          { label: 'Valor Proposto',  data: cfg.proposto,  backgroundColor: '#e2ba54' },
          { label: 'Valor Livre',     data: cfg.livre,     backgroundColor: '#284b27' }
        ]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' },
          datalabels: {
            anchor: 'end',
            align: 'right',
            color: '#000',
            font: { size: 11 },
            formatter: function(value) {
              return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', minimumFractionDigits: 0 });
            }
          }
        },
        scales: {
          y: { ticks: { font: { size: 11 } } },
          x: {
            beginAtZero: true,
            ticks: {
              callback: v => 'R$ ' + v.toLocaleString('pt-BR')
            }
          }
        }
      }
    });
  }
});
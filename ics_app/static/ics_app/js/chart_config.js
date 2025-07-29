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

import plotly.graph_objects as go
from django.shortcuts import render
from plotly.offline import plot

from .models import FPMining


def simpleFPmining(request):
    all_rows = FPMining.objects.all()
    pigs_in_data = all_rows.order_by('pig').distinct('pig')
    plots = []

    for pig in pigs_in_data:
        trace = go.Bar(x=list(all_rows.filter(pig_id=pig.pig_id).values_list('itemset', flat=True)),
                       y=list(all_rows.filter(pig_id=pig.pig_id).values_list('support', flat=True)))
        layout = dict(
            title=pig.pig.nickname,
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        plots.append(plot_div)

    return render(request, "analysis/fpmining.html", context={'plots': plots})

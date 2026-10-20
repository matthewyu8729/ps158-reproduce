"""Plot published Pew AI sentiment trends. Requires matplotlib.
Run get_data.py first, then: python plot.py
"""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

OUT = Path(__file__).resolve().parent

def main():
    with (OUT / 'ai_sentiment.csv').open() as f:
        data = list(csv.DictReader(f))
    sentiments = ['More concerned than excited', 'Equally concerned and excited', 'More excited than concerned']
    titles = ['More concerned\nthan excited', 'Equally concerned\nand excited', 'More excited\nthan concerned']
    groups = [('Rep/Lean Rep', 'Republican / lean Republican', '#C24D42'),
              ('Dem/Lean Dem', 'Democrat / lean Democrat', '#006B87'),
              ('U.S. adults', 'All U.S. adults', '#222222')]
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11})
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 7.2), sharey=True)
    fig.patch.set_facecolor('#F1F5F6')
    fig.add_artist(Rectangle((0.055, 0.955), 0.045, 0.013, transform=fig.transFigure,
                             facecolor='#E3120B', edgecolor='none'))
    fig.add_artist(Line2D([0.055, 0.98], [0.955, 0.955], transform=fig.transFigure,
                          color='#E3120B', lw=1))
    for ax, sentiment, title in zip(axes, sentiments, titles):
        ax.set_facecolor('#F1F5F6')
        ax.set_title(title, loc='left', fontsize=13, fontweight='bold', pad=14)
        for group, label, color in groups:
            series = sorted([r for r in data if r['group'] == group and r['sentiment'] == sentiment], key=lambda r: int(r['year']))
            x = [int(r['year']) for r in series]
            y = [float(r['percent']) for r in series]
            overall = group == 'U.S. adults'
            ax.plot(x, y, color=color, lw=2.4, marker='D' if overall else 'o',
                    ms=4 if overall else 4.5, linestyle='--' if overall else '-',
                    zorder=4 if overall else 3)
            change = y[-1] - y[0]
            group_idx = [g[0] for g in groups].index(group)
            ypos = -0.23 - 0.09 * group_idx
            short_label = {'Rep/Lean Rep': 'Rep', 'Dem/Lean Dem': 'Dem', 'U.S. adults': 'All adults'}[group]
            ax.text(0, ypos, f'{short_label}  {change:+.0f} pp',
                    transform=ax.transAxes, color=color, fontsize=10)
        ax.text(0, -0.15, 'Change since 2021', transform=ax.transAxes,
                fontsize=10, fontweight='bold', color='#333333')
        # Separate endpoint labels vertically; leaders preserve the exact data position.
        for year, label_x, align in [(2021, 2020.65, 'right'), (2026, 2026.35, 'left')]:
            endpoints = sorted(
                [(next(float(r['percent']) for r in data
                       if r['group'] == group and r['sentiment'] == sentiment
                       and int(r['year']) == year), color, group)
                 for group, _, color in groups], key=lambda item: (item[0], item[2]))
            positions = []
            for value, _, _ in endpoints:
                positions.append(max(value, positions[-1] + 5 if positions else value))
            shift = sum(positions) / len(positions) - sum(v for v, _, _ in endpoints) / len(endpoints)
            positions = [p - shift for p in positions]
            if positions[0] < 2:
                positions = [p + 2 - positions[0] for p in positions]
            for (value, color, _), label_y in zip(endpoints, positions):
                ax.annotate(f'{value:.0f}%', xy=(year, value), xytext=(label_x, label_y),
                            ha=align, va='center', color=color, fontsize=10,
                            fontweight='bold', annotation_clip=False,
                            arrowprops=dict(arrowstyle='-', color=color, lw=0.8,
                                            shrinkA=2, shrinkB=5),
                            bbox=dict(facecolor='#F1F5F6', edgecolor='none', pad=0.5))
        ax.set_ylim(0, 65)
        ax.set_xlim(2019.85, 2027.15)
        ax.set_xticks(range(2021, 2027))
        ax.tick_params(axis='both', length=0, labelsize=10, pad=8)
        ax.yaxis.set_major_formatter(PercentFormatter(100, decimals=0))
        ax.grid(axis='y', color='#C9D1D3', lw=0.65)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.axhline(0, color='#60686B', lw=0.9)
    fig.text(0.055, 0.898, 'Uneasy about AI', fontsize=27, fontweight='bold',
             fontfamily='DejaVu Serif', color='#111111')
    fig.text(0.055, 0.853, 'United States, feelings about increased use of AI in daily life',
             fontsize=13, color='#333333')
    fig.text(0.055, 0.817, 'Share of adults in each group, % • 2021–26', fontsize=11, color='#555555')
    fig.legend(handles=[Line2D([0],[0],color=c,lw=3,marker='D' if g == 'U.S. adults' else 'o',linestyle='--' if g == 'U.S. adults' else '-',label=l) for g,l,c in groups], loc='upper left', bbox_to_anchor=(0.047,0.795), ncol=3, frameon=False)
    fig.text(0.055, 0.048, 'Source: Pew Research Center, September 16, 2026. Latest survey: June 22–28, 2026.\nParty groups include leaning independents. Nonresponses omitted; percentages are not rescaled.', fontsize=9, color='#555555', linespacing=1.6)
    fig.subplots_adjust(left=0.055, right=0.98, top=0.64, bottom=0.30, wspace=0.18)
    for ext in ['png', 'svg', 'pdf']:
        fig.savefig(OUT / f'ai_sentiment_2021_2026.{ext}', dpi=200, facecolor=fig.get_facecolor())
    print('Saved PNG, SVG and PDF figures.')

if __name__ == '__main__':
    main()

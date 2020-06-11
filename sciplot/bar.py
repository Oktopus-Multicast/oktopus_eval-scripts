import itertools
from . import flatui, LEGEND_FONT_SIZE, BAR_PALETTE
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from . import utils

__author__ = 'Khaled Diab (kdiab@sfu.ca)'


def plot_bar(x, y, hue=None, hue_count=1,
             line_values=None, line_label=None, legend=True,
             xaxis_label=None, yaxis_label=None,
             xticks=None,
             y_lim=None,
             x_sci=True, y_sci=True,
             fig_size=None,
             y_err=None,
             name=None):
    fig, ax = plt.subplots()
    if fig_size and isinstance(fig_size, list) and len(fig_size) > 0:
        if len(fig_size) == 1:
            fig.set_figwidth(fig_size[0])
        else:
            fig.set_figwidth(fig_size[0])
            fig.set_figheight(fig_size[1])

    bar_width = 0.2
    new_x = [x_ + bar_width for x_ in x]
    ticks_x = [x_ + 0.5 * bar_width for x_ in new_x]
    if y_err:
        ax.errorbar(ticks_x, y, yerr=y_err, fmt='o', ecolor='r', capthick=1, elinewidth=1)
    plt.bar(new_x, y, width=bar_width)

    if line_values and utils.is_list(line_values):
        x_set = set(x)
        if len(line_values) == len(x_set):
            if line_label:
                ax.plot(ax.get_xticks(), line_values, label=line_label)
                hue_count += 1
            else:
                ax.plot(ax.get_xticks(), line_values)
    if xticks and isinstance(xticks, list):
        plt.xticks(ticks_x, xticks)
    if y_lim and isinstance(y_lim, list) and len(y_lim) > 0:
        if len(y_lim) == 1:
            plt.ylim(ymin=y_lim[0])
        else:
            plt.ylim(ymin=y_lim[0])
            plt.ylim(ymax=y_lim[1])
    if legend:
        utils.set_legend(ncol=hue_count)
    utils.set_sci_axis(ax, x_sci, y_sci)
    utils.set_axis_labels(ax, xaxis_label, yaxis_label)
    utils.finalize(ax, x_grid=False)
    utils.save_fig(name)


def plot_two_bars(ys,
                  labels,
                  yerrs=None,
                  legend=True,
                  xaxis_label=None,
                  yaxis_label=None,
                  xticks=None, xticks_kwargs=None, xticks_params=None,
                  y_lim=None, xtick_step=1, bar_width=0.2,
                  x_sci=True, y_sci=True,
                  fig_size=None,
                  name=None):
    fig, ax = plt.subplots()
    if fig_size and isinstance(fig_size, list) and len(fig_size) > 0:
        if len(fig_size) == 1:
            fig.set_figwidth(fig_size[0])
        else:
            fig.set_figwidth(fig_size[0])
            fig.set_figheight(fig_size[1])

    x = range(1, xtick_step * len(ys[0]) + 1, xtick_step)
    if len(ys) == 2:
        new_x1 = [x_ - bar_width for x_ in x]
        new_x2 = [x_ for x_ in x]
    else:
        new_x1 = [x_ for x_ in x]

    if yerrs:
        rects1 = ax.bar(new_x1, ys[0], width=bar_width, color=flatui[0], hatch='/', yerr=yerrs[0],
                        error_kw=dict(ecolor='gray', lw=2, capsize=5, capthick=2))
        if len(ys) == 2:
            rects2 = ax.bar(new_x2, ys[1], width=bar_width, color=flatui[1], yerr=yerrs[1])
    else:
        rects1 = ax.bar(new_x1, ys[0], width=bar_width, color=flatui[0], hatch='/')
        if len(ys) == 2:
            rects2 = ax.bar(new_x2, ys[1], width=bar_width, color=flatui[1], hatch='\\')

    if xticks and isinstance(xticks, list):
        if xticks_kwargs:
            plt.xticks([x_ for x_ in x], xticks, **xticks_kwargs)
        else:
            plt.xticks([x_ for x_ in x], xticks)

    if xticks_params:
        ax.tick_params(axis='x', **xticks_params)

    if y_lim and isinstance(y_lim, list) and len(y_lim) > 0:
        if len(y_lim) == 1:
            plt.ylim(ymin=y_lim[0])
        else:
            plt.ylim(ymin=y_lim[0])
            plt.ylim(ymax=y_lim[1])
    if legend:
        if y_sci:
            if len(ys) == 2:
                ax.legend((rects1[0], rects2[0]), (labels[0], labels[1]),
                          fontsize=LEGEND_FONT_SIZE, frameon=False,
                          bbox_to_anchor=(0.3, 0.85, 0.5, .10), handlelength=1, handletextpad=0.2,
                          loc=3, ncol=2, mode="expand",
                          borderaxespad=0.)
            else:
                ax.legend((rects1[0],), (labels[0],),
                          fontsize=LEGEND_FONT_SIZE, frameon=False,
                          bbox_to_anchor=(0.3, 0.85, 0.5, .10), handlelength=1, handletextpad=0.2,
                          loc=3, ncol=2, mode="expand",
                          borderaxespad=0.)
        else:
            if len(ys) == 2:
                ax.legend((rects1[0], rects2[0]), (labels[0], labels[1]),
                          fontsize=LEGEND_FONT_SIZE, frameon=False,
                          bbox_to_anchor=(0.3, 0.85, 0.5, .10), handlelength=1, handletextpad=0.2,
                          loc=3, ncol=2, mode="expand",
                          borderaxespad=0.)
            else:
                ax.legend((rects1[0],), (labels[0],),
                          fontsize=LEGEND_FONT_SIZE, frameon=False,
                          bbox_to_anchor=(0.3, 0.85, 0.5, .10), handlelength=1, handletextpad=0.2,
                          loc=3, ncol=2, mode="expand",
                          borderaxespad=0.)
    utils.set_sci_axis(ax, x_sci, y_sci)
    utils.set_axis_labels(ax, xaxis_label, yaxis_label)
    utils.finalize(ax, x_grid=False)
    utils.save_fig(name)


def plot_n_bars(ys,
                labels=None,
                yerrs=None,
                legend=True,
                legend_top=True,
                legend_font_size=LEGEND_FONT_SIZE,
                legend_bbox=None,
                xaxis_label=None,
                yaxis_label=None,
                xticks=None, xticks_kwargs=None, xticks_params=None, xticks_labels=None,
                yticks=None, yticks_kwargs=None, yticks_params=None,
                y_lim=None, xtick_step=1, bar_width=0.2,
                x_sci=False, y_sci=False,
                hatch=False,
                lines=None,
                lines_kw=None,
                arrows=None,
                x_grid=True,
                y_grid=True,
                hlines_dict=None,
                fig_size=None,
                stacked=False,
                secondary=False,
                secondary_x=None,
                secondary_y=None,
                secondary_ylim=None,
                secondary_y_label=None,
                name=None):
    # with BAR_PALETTE:
    ax2 = None
    fig, ax = plt.subplots()


    if fig_size and isinstance(fig_size, list) and len(fig_size) > 0:
        if len(fig_size) == 1:
            fig.set_figwidth(fig_size[0])
        else:
            fig.set_figwidth(fig_size[0])
            fig.set_figheight(fig_size[1])

    n = len(ys)
    x = range(1, xtick_step * len(ys[0]) + 1, xtick_step)

    xs = [[]]*n
    rects = []
    for i in range(n):
        if not stacked:
            if n % 2 == 0:
                if i < n / 2:
                    xs[i] = [x_ - (n / 2 - i) * bar_width for x_ in x]
                else:
                    xs[i] = [x_ + (i - (n / 2)) * bar_width for x_ in x]
            else:
                if i < n / 2:
                    xs[i] = [x_ - (int(n / 2) - i) * bar_width for x_ in x]
                elif i > n / 2:
                    xs[i] = [x_ + (i - int(n / 2)) * bar_width for x_ in x]
                elif i == int(n / 2):
                    xs[i] = [x_ for x_ in x]
        else:
            xs[i] = [x_ for x_ in x]

    # colors = utils.get_color_cycler(colors=BAR_PALETTE)
    # print(colors)
    c_idx = 0
    colors = itertools.cycle(BAR_PALETTE)
    hatches = utils.get_hatch_cycler()
    np_y = []
    for i in range(n):
        np_y.append(np.array(ys[i]))

    for i in range(n):
        bar_args = {}
        if hatch:
            h = next(hatches)
            bar_args['hatch'] = h
        c = BAR_PALETTE[c_idx]
        c_idx += 1
        if c_idx == len(BAR_PALETTE):
            c_idx = 0
        if not stacked:
            rects.append(ax.bar(xs[i], ys[i], align='center', width=bar_width, color=c, lw=0., **bar_args))
        else:
            bottom = np.zeros(np_y[0].shape)
            for j in range(0, i):
                bottom = bottom + np_y[j]
            # print(i, xs[i])
            p = ax.bar(xs[i], ys[i], align='center', width=bar_width, bottom=bottom, color=c, lw=0., **bar_args)
            rects.append(p)

    if xticks and isinstance(xticks, list):
        # print('XX')
        # new_ticks = xticks
        new_ticks = []
        for i in range(len(xs[0])):
            _sum = 0
            for _list in xs:
                _sum += _list[i]
            new_ticks.append(_sum / float(len(xs)))
        # print(new_ticks)
        if xticks_labels:
            if xticks_kwargs:
                plt.xticks([x_ for x_ in new_ticks], xticks_labels, **xticks_kwargs)
            else:
                # print('>>', [x_ for x_ in xticks])
                # print('>>', xticks_labels)
                plt.xticks([x_ for x_ in new_ticks], xticks_labels)
        else:
            if xticks_kwargs:
                plt.xticks([x_ for x_ in new_ticks], xticks, **xticks_kwargs)
            else:
                plt.xticks([x_ for x_ in new_ticks], xticks)

    if xticks_params:
        ax.tick_params(axis='x', **xticks_params)

    if y_lim and isinstance(y_lim, list) and len(y_lim) > 0:
        if len(y_lim) == 1:
            plt.ylim(ymin=y_lim[0])
        else:
            plt.ylim(ymin=y_lim[0])
            plt.ylim(ymax=y_lim[1])

    if hlines_dict:
        colors = utils.get_color_cycler(reverse=True)
        for idx, hline in enumerate(hlines_dict):
            y = hline.get('y', 0)
            xmin = hline.get('xmin', 0)
            xmax = hline.get('xmax', 0)
            line_label = hline.get('label', '')
            line_width = hline.get('lw', '1')
            if line_label:
                ax.plot([xmin, xmax], [y, y], label=line_label, ls='-', markersize=0, color=next(colors), lw=line_width)
            else:
                ax.plot([xmin, xmax], [y, y], ls='-', markersize=0, color=next(colors), lw=line_width)

    if lines:
        for line in lines:
            bar_number = line.get('bar_number', 0)
            line_x = xs[bar_number]
            line_y = ys[bar_number]
            fc = rects[bar_number].patches[0].get_fc()
            if lines_kw:
                ax.plot(line_x, line_y, color=fc)
            else:
                ax.plot(line_x, line_y, color=fc, **lines_kw)

    if legend:
        bbox = (0., 0.95, 1., .10)
        if legend_bbox:
            bbox = legend_bbox
        if legend_top:
            ax.legend(rects, labels,
                      fontsize=legend_font_size, frameon=False,
                      bbox_to_anchor=bbox,
                      handlelength=1, handletextpad=0.2,
                      loc=3, ncol=n, mode="expand",
                      borderaxespad=0.)
        else:
            ax.legend(rects, labels,
                      fontsize=legend_font_size, frameon=False,
                      bbox_to_anchor=bbox,
                      handlelength=1, handletextpad=0.2,
                      borderaxespad=0.)
    if arrows:
        utils.draw_arrows(arrows)

    utils.set_sci_axis(ax, x_sci, y_sci)
    utils.set_axis_labels(ax, xaxis_label, yaxis_label)
    utils.finalize(ax, x_grid=x_grid, y_grid=y_grid)

    # if secondary and secondary_y:
    #     ax2 = fig.add_subplot()

    # line_color = '#0072B2'
    line_color = '#0000FF'
    if secondary and secondary_y:
        ax2 = ax.twinx()
        ax2.plot(secondary_x, secondary_y, color=line_color, ls='-', marker='o', markersize=10)
        ax2.set_ylabel(secondary_y_label, color=line_color)
        if secondary_ylim:
            ax2.set_ylim(secondary_ylim)
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position('right')
        ax2.tick_params('y', colors=line_color)
        # ax2.yaxis.set_ticks([9., 9.2, 9.4, 9.6, 9.8, 10.])
        utils.finalize(ax2, x_grid=x_grid, y_grid=y_grid, despine_right=False)
        plt.tight_layout()

    utils.save_fig(name)
    plt.close()
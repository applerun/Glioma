import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm, colors
from matplotlib.colors import ListedColormap


def create_colormap_lightness(color: tuple, sample = 512, white = (1, 1, 1)):
    """


    :param color:最大值颜色
    :param sample: 颜色采样数量，default=512
    :param white: 设置最大亮度的颜色，默认白色，default = (1, 1, 1)
    :return:ListedColormap：从白色到指定颜色的Colormap（lightness从大到小）
    """
    xs = np.linspace(0, 1, sample)
    color_ = np.array(color)
    res = np.outer(np.ones(sample), np.array(white))
    np.ones((sample, 3))
    res += np.outer(xs, (color_ - 1))
    return ListedColormap(res)


def create_colormap_bluered(red = (1, 0, 0), blue = (0, 0, 1), sample_red = 256, sample_blue = 256, white = (1, 1, 1)):
    sample = sample_red
    xs = np.linspace(0, 1, sample)
    color_red = np.array(red)
    res_red = np.outer(np.ones(sample), np.array(white))
    res_red += np.outer(xs, (color_red - white))
    sample = sample_blue
    color_blue = np.array(blue)
    res_blue = np.outer(np.ones(sample), np.array(white))
    np.ones((sample, 3))
    res_blue += np.outer(xs, (color_blue - white))
    res_blue = res_blue[::-1, ]
    res = np.vstack((res_blue, res_red))
    return ListedColormap(res)


def legend_show(ax, color, hatches, hatch_color, pos = (0, 0), width = 0.8, height = 0.3, interval_y = 0.2):
    len_data = len(hatches)
    for i in range(len_data):
        hatch = hatches[i]
        ax.bar(x = pos[0], height = height, bottom = pos[1] + i * (height + interval_y), width = width, color = color,
               hatch = hatch,
               edgecolor = hatch_color)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.axis("off")
    ax.set_xticks([])
    ax.set_yticks([])


def plotdata(HeatData1,
             HeatData2,
             ax: matplotlib.axes.Axes, cmap = "Reds", hatch_color: str or tuple = "orange", hatchs = None,
             norm = colors.Normalize(0.5, 1, clip = True),
             width = 0.8,
             height = 0.5,
             interval_x = 0,
             interval_1 = 0.2,
             interval_2 = 0.6,
             interval_y = 0.05,
             colorbar_orientation = "vertical",
             count_1 = 3,
             ticksize = 20
             ):
    if hatchs is None:
        hatchs = ['//', '..', r"\\", '|', '-', '+', 'x', 'o', 'O', '.', '*']
    lenx = HeatData2.shape[1]

    if type(cmap) == list:
        cmaps = cmap
    else:
        cmaps = [cmap]

    for x_index in range(2 * lenx):
        mapper = cm.ScalarMappable(norm = norm, cmap = cmaps[x_index % (len(cmaps))])
        data_s = HeatData1[:, x_index] if x_index < lenx else HeatData2[:, x_index - lenx]
        x_pos = (width + interval_x) * x_index \
                + x_index // count_1 * interval_1 \
                + x_index // lenx * interval_2 \
            # + x_index // (2 * count_1) * interval_1
        hatch = hatchs[x_index % 3]
        plot_s(ax, data_s, hatch, x_pos, width, height, mapper = mapper, hatch_color = hatch_color,
               interval_y = interval_y)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.axis("off")
    ax.set_xticks([])
    ax.set_yticks([])
    fig = ax.figure
    if len(cmaps) == 1:
        colorbars(cmaps, fig, norm = norm, colorbar_orientation = colorbar_orientation, ticksize = ticksize)
    return fig


def colorbars(cmaps, fig = None, norm = colors.Normalize(0.5, 1, clip = True), colorbar_orientation = "vertical",
              ticksize = 20):
    if fig is None:
        fig_, axes = plt.subplots(1, len(cmaps), width_ratios = [0.1] * len(cmaps), squeeze = False)
        axes = axes.flatten()
        for ax in axes:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.axis("off")
            ax.set_xticks([])
            ax.set_yticks([])
    else:
        fig_ = fig
    for i in range(len(cmaps) - 1, -1, -1):
        c = cmaps[i]
        mapper = cm.ScalarMappable(norm = norm, cmap = c)
        cb = fig_.colorbar(mapper, ax = axes[i], orientation = colorbar_orientation) if fig is None else fig.colorbar(
            mapper, orientation = colorbar_orientation)
        cb.ax.tick_params(labelsize = ticksize)
    return fig_


def plot_s(ax: matplotlib.axes.Axes, data, hatch, pos, width, height, mapper: cm.ScalarMappable = None,
           hatch_color = "black", interval_y = 0, color = None):
    assert mapper is not None or color is not None
    for i in range(len(data)):
        value = data[-1 - i]
        color_ = mapper.to_rgba(value) if color is None else color
        # color = plt.cm.viridis(norm(value))
        ax.bar(x = pos, height = height, bottom = i * (height + interval_y), width = width, color = color_,
               hatch = hatch,
               edgecolor = hatch_color)
        ax.bar(x = pos, height = height, bottom = i * (height + interval_y), width = width, color = (0, 0, 0, 0),
               edgecolor = color_)
    return


def main_hatchwise():  # 纹理热力图
    plt.rcParams['figure.figsize'] = (24, 9)

    hatches = ['//', '..', r"\\"]
    hatch_color = (1 / 1.5, 165 / 255 / 1.5, 0, 0)
    # cmap = create_colormap_lightness((1, 0, 0))
    # cmap = cmap.reversed()
    cmap = create_colormap_bluered(white = (0.98,0.98,0.97))
    norm = colors.Normalize(0.5, 1, clip = True)
    wh12y = np.array([2, 0.8, 0, 0.2, 1, 0.05])
    wh12y *= 2

    HeatData1 = np.loadtxt("heatdata1.csv", delimiter = ",", skiprows = 1)
    HeatData1_dl = HeatData1[:, 1::3]
    HeatData1_ml = np.delete(HeatData1, list(range(1,HeatData1.shape[1], 3)), axis = 1)
    HeatData2 = np.loadtxt("heatdata2.csv", delimiter = ",", skiprows = 1)
    HeatData2_dl = HeatData2[:, 1::3]
    HeatData2_ml = np.delete(HeatData2, list(range(1,HeatData2.shape[1], 3)), axis = 1)

    fig, ax = plt.subplots(figsize = (12, 9))
    plotdata(HeatData1_dl, HeatData2_dl, ax, cmap, hatch_color, hatches, norm, *wh12y,
             colorbar_orientation = "vertical", ticksize = 25, count_1 = 1)
    legend_show(ax, (0, 0, 0, 0), hatches[::-1], hatch_color,
                pos = (0, 0.8 * 10), interval_y = 0.05)
    plt.savefig("legend_dl.png")

    colorbars([cmap])
    plt.savefig("legend_colorbar_dl.png")

    fig, ax = plt.subplots(figsize = (24, 9))
    plotdata(HeatData1_ml, HeatData2_ml, ax, cmap, hatch_color, hatches, norm, *wh12y,
             colorbar_orientation = "vertical", ticksize = 25, count_1 = 2)
    plt.savefig("legend_colorbar_dl.png")

    fig, ax = plt.subplots(figsize = (36, 9))
    plotdata(HeatData1, HeatData2, ax, cmap, hatch_color, hatches, norm, *wh12y,
             colorbar_orientation = "vertical", ticksize = 25, count_1 = 3)
    plt.savefig("legend_all.png")


def main_colorwise():  # 颜色区分热力图
    plt.rcParams['figure.figsize'] = (28, 10)
    fig, ax = plt.subplots()

    cmap = [
        create_colormap_lightness((0.1, 0.4, 1)),
        create_colormap_lightness((0.2, 0.2, 1)),
        create_colormap_lightness((0.4, 0.1, 1))
    ]
    plotdata(ax, hatch_color = (0, 0, 0, 0), cmap = cmap)
    plt.savefig("legend_color.png")
    # fig, ax = plt.subplots()
    fig = colorbars(cmap)
    fig.savefig("colorbars.png")


if __name__ == '__main__':
    main_hatchwise()
    # main_colorwise()

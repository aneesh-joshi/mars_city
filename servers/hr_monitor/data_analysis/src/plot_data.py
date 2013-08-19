import matplotlib.pyplot as plt
import scipy.stats as st

def plot_distribution(style, name, bins, ratio_log):
    print name
    try:
        name = name.strip()
        dist = st.__getattribute__(name)
        ratioparam = dist.fit(ratio_log)
        ratiofitted = dist.pdf(bins, *ratioparam)
        plt.plot(bins, ratiofitted, style, label=name)
        return (ratioparam, ratiofitted)
    except Exception as inst:
        print inst


def plot_everything(name, data, df_activities, plot_ratio=False):
    colors = {0 : '#000000',
                1 : '#00000f',
                2 : '#0000f0',
                3 : '#0000ff',
                4 : '#000f00',
                5 : '#000f0f',
                6 : '#000ff0',
                7 : '#000fff',
                9 : '#00f000',
                10 : '#00f00f',
                11 : '#00f0f0',
                12 : '#00f0ff',
                13 : '#00ff00',
                16 : '#00ff0f',
                17 : '#00fff0',
                18 : '#00ffff',
                19 : '#0f0000',
                20 : '#0f000f',
                24 : '#0f00f0',
    }

    ratio_log = data.ratio_log

    plt.figure(name + ' fit')
    n, bins, patches = plt.hist(ratio_log, bins=1000,
                                range=(ratio_log.min(), ratio_log.max()),
                                normed=True, alpha=0.5)
    plot_distribution('c-', 'norm', bins, ratio_log)
    plt.legend(loc='best')

    plt.figure(name + ' historical')
    data.acc.plot(alpha=0.5)
    data.hr.plot(alpha=0.5)
    data.ratio_log.plot()
    if plot_ratio:
        data.ratio.plot()

    for name, group in df_activities.groupby('activityID'):
        xmin = min(group.index)
        xmax = max(group.index)
        plt.axvspan(xmin, xmax, facecolor=colors[int(name)], alpha=0.25)

    plt.legend(loc='best')

    plt.show()
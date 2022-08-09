import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
import numpy as np
from PIL import Image


def P1A_to_HSV(cin, vmin=None, vmax=None):
    """\
    Transform a complex array into an RGB image,
    mapping phase to hue, amplitude to value and
    keeping maximum saturation.
    """
    # HSV channels
    h = .5 * np.angle(cin) / np.pi + .5
    s = np.ones(cin.shape)

    v = abs(cin)
    if vmin is None: vmin = 0.
    if vmax is None: vmax = v.max()
    assert vmin < vmax
    v = (v.clip(vmin, vmax) - vmin) / (vmax - vmin)

    return HSV_to_RGB((h, s, v))


def HSV_to_RGB(cin):
    """\
    HSV to RGB transformation.
    """

    # HSV channels
    h, s, v = cin

    i = (6. * h).astype(int)
    f = (6. * h) - i
    p = v * (1. - s)
    q = v * (1. - s * f)
    t = v * (1. - s * (1. - f))
    i0 = (i % 6 == 0)
    i1 = (i == 1)
    i2 = (i == 2)
    i3 = (i == 3)
    i4 = (i == 4)
    i5 = (i == 5)

    imout = np.zeros(h.shape + (3,), dtype=h.dtype)
    imout[:, :, 0] = 255 * (i0 * v + i1 * q + i2 * p + i3 * p + i4 * t + i5 * v)
    imout[:, :, 1] = 255 * (i0 * t + i1 * v + i2 * v + i3 * q + i4 * p + i5 * p)
    imout[:, :, 2] = 255 * (i0 * p + i1 * p + i2 * t + i3 * v + i4 * v + i5 * q)

    return imout


def zplot(imgs, suptitle='Image', savePath=None, cmap=['hot', 'hsv'], title=['Abs', 'Phase'], show=True,
          figsize=(9, 5), scale=None):
    im1, im2 = imgs
    fig = plt.figure(figsize=figsize, dpi=300)
    fig.suptitle(suptitle, fontsize=15, y=0.8)
    gs1 = gridspec.GridSpec(1, 2)
    gs1.update(wspace=0, hspace=0)  # set the spacing between axes.
    ax1 = plt.subplot(gs1[0])
    ax2 = plt.subplot(gs1[1])
    div1 = make_axes_locatable(ax1)
    div2 = make_axes_locatable(ax2)

    imax1 = ax1.imshow(im1, interpolation='nearest', cmap=plt.cm.get_cmap(cmap[0]))
    imax2 = ax2.imshow(im2, interpolation='nearest', cmap=plt.cm.get_cmap(cmap[1]))

    cax1 = div1.append_axes("left", size="10%", pad=0.4)
    cax2 = div2.append_axes("right", size="10%", pad=0.4)

    cbar1 = plt.colorbar(imax1, cax=cax1)
    cbar2 = plt.colorbar(imax2, cax=cax2)

    cax1.yaxis.set_ticks_position('left')
    ax2.yaxis.set_ticks_position('right')

    ax1.set_title(title[0])
    ax2.set_title(title[1])

    if scale is not None:
        fontprops = fm.FontProperties(size=18)
        scalebar = AnchoredSizeBar(ax1.transData,
                                   scale[0], scale[1], 'lower right',
                                   pad=0.1,
                                   color='white',
                                   frameon=False,
                                   size_vertical=im1.shape[0] / 40,
                                   fontproperties=fontprops)

        ax1.add_artist(scalebar)

    ax1.grid(False)
    ax2.grid(False)

    if show:
        plt.show()
    if savePath is not None:
        # print 'saving'
        fig.savefig(savePath + '.png')


def plotAbsAngle(img, suptitle='Image', savePath=None, cmap=['gray', 'gray'], title=['Abs', 'Phase'], show=True,
                 figsize=(10, 10), scale=None):
    zplot([np.abs(img), np.angle(img)], suptitle, savePath, cmap, title, show, figsize, scale)


def plotcxmosaic(img, title='Image', savePath=None, cmap='hot', show=True, figsize=(10, 10), vmax=None):
    fig, ax = plt.subplots(figsize=figsize)
    mos = imsave(mosaic(img))
    cax = ax.imshow(mos, interpolation='nearest', cmap=plt.cm.get_cmap(cmap), vmax=vmax)
    ax.set_title(title)
    plt.grid(False)
    plt.show()
    if savePath is not None:
        # print 'saving'
        fig.savefig(savePath + '.png', dpi=600)


def plotmosaic(img, title='Image', savePath=None, cmap='hot', show=True, figsize=(10, 10), vmax=None):
    fig, ax = plt.subplots(figsize=figsize)
    mos = mosaic(img)
    cax = ax.imshow(mos, interpolation='nearest', cmap=plt.cm.get_cmap(cmap), vmax=vmax)
    cbar = fig.colorbar(cax)
    ax.set_title(title)
    plt.grid(False)
    plt.show()
    if savePath is not None:
        # print 'saving'
        fig.savefig(savePath + '.png', dpi=600)
    return fig


def plot(img, title='Image', savePath=None, cmap='inferno', show=True, vmax=None, figsize=(10, 10), scale=None):
    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(img, interpolation='nearest', cmap=plt.cm.get_cmap(cmap), vmax=vmax)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im, cax=cax)
    ax.set_title(title)
    fontprops = fm.FontProperties(size=18)
    if scale is not None:
        scalebar = AnchoredSizeBar(ax.transData,
                                   scale[0], scale[1], 'lower right',
                                   pad=0.1,
                                   color='white',
                                   frameon=False,
                                   size_vertical=img.shape[0] / 40,
                                   fontproperties=fontprops)

        ax.add_artist(scalebar)
    ax.grid(False)
    if savePath is not None:
        fig.savefig(savePath + '.pdf', dpi=600)
        # fig.savefig(savePath + '.eps', dpi=600)
    if show:
        plt.show()
    return fig


def mosaic(data):
    n, w, h = data.shape
    diff = np.sqrt(n) - int(np.sqrt(n))
    s = np.sqrt(n)
    m = int(s)
    # print 'm', m
    if diff > 1e-6: m += 1
    mosaic = np.zeros((m * w, m * h)).astype(data.dtype)
    for i in range(m):
        for j in range(m):
            if (i * m + j) < n:
                mosaic[i * w:(i + 1) * w, j * h:(j + 1) * h] = data[i * m + j]
    return mosaic


def imsave(a, filename=None, vmin=None, vmax=None, cmap=None):
    """
    imsave(a) converts array a into, and returns a PIL image
    imsave(a, filename) returns the image and also saves it to filename
    imsave(a, ..., vmin=vmin, vmax=vmax) clips the array to values between vmin and vmax.
    imsave(a, ..., cmap=cmap) uses a matplotlib colormap.
    """

    if a.dtype.kind == 'c':
        # Image is complex
        if cmap is not None:
            print('imsave: Ignoring provided cmap - input array is complex')
        i = P1A_to_HSV(a, vmin, vmax)
        im = Image.fromarray(np.uint8(i), mode='RGB')

    else:
        if vmin is None:
            vmin = a.min()
        if vmax is None:
            vmax = a.max()
        im = Image.fromarray((255 * (a.clip(vmin, vmax) - vmin) / (vmax - vmin)).astype('uint8'))
        if cmap is not None:
            r = im.point(lambda x: cmap(x / 255.0)[0] * 255)
            g = im.point(lambda x: cmap(x / 255.0)[1] * 255)
            b = im.point(lambda x: cmap(x / 255.0)[2] * 255)
            im = Image.merge("RGB", (r, g, b))
            # b = (255*(a.clip(vmin,vmax)-vmin)/(vmax-vmin)).astype('uint8')
            # im = Image.fromstring('L', a.shape[-1::-1], b.tostring())

    if filename is not None:
        im.save(filename)
    return im


def plot_complex_multi(x, title='_', figsize=(10, 10), savePath=None, scale=None, show=True):
    n, h, w = x.shape
    rows = int(np.floor(np.sqrt(n)))
    cols = n // rows + 1
    fontprops = fm.FontProperties(size=18)
    fig = plt.figure(dpi=300, constrained_layout=True)
    gs1 = gridspec.GridSpec(rows, cols)
    gs1.update(wspace=0.1, hspace=0.1)
    for r in range(rows):
        for c in range(cols):
            i = cols * r + c
            ax = plt.subplot(gs1[i])
            if i < n:
                imax1 = ax.imshow(imsave(x[i]), interpolation='nearest')
                if scale is not None and i == 0:
                    scalebar = AnchoredSizeBar(ax.transData,
                                               scale[0], scale[1], 'lower right',
                                               pad=0.1,
                                               color='white',
                                               frameon=False,
                                               size_vertical=x.shape[0] / 40,
                                               fontproperties=fontprops)
                    ax.add_artist(scalebar)
            else:
                ax.axis('off')
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_xticks([])
            ax.set_yticks([])

    plt.suptitle(title)
    plt.grid(False)
    fig.set_constrained_layout_pads(w_pad=0.1, h_pad=0.1)
    if savePath is not None:
        fig.savefig(savePath + '.png')
        fig.savefig(savePath + '.pdf')
    if show:
        plt.show()
    return fig


def plotcx(x, title='Image', figsize=(10, 10), savePath=None, scale=None):
    fig, (ax1) = plt.subplots(1, 1, figsize=figsize)
    imax1 = ax1.imshow(imsave(x), interpolation='nearest')
    ax1.set_title(title)
    plt.grid(False)
    fontprops = fm.FontProperties(size=18)
    if scale is not None:
        scalebar = AnchoredSizeBar(ax1.transData,
                                   scale[0], scale[1], 'lower right',
                                   pad=0.1,
                                   color='white',
                                   frameon=False,
                                   size_vertical=x.shape[0] / 40,
                                   fontproperties=fontprops)

        ax1.add_artist(scalebar)
    if savePath is not None:
        fig.savefig(savePath + '.png', dpi=300)
        fig.savefig(savePath + '.pdf', dpi=300)
    plt.show()


"""выводит все изображения, имеющиеся в каталоге, в виде миниатюр на кнопках,
щелчок на которых приводит к выводу полноразмерного изображения; требует
наличия пакета PIL для отображения JPEG-файлов и создания миниатюр; что сделать:
добавить прокрутку, если в окне выводится слишком много миниатюр!
"""
import os
# import sys
import math
from tkinter import *
from PIL import Image
from PIL.ImageTk import PhotoImage


def make_thumbs(imgdir, size=(100, 100), subdir='thumbs'):
    """
    создает миниатюры для всех изображений в каталоге; для каждого изображения
    создается и сохраняется новая миниатюра или загружается существующая;
    при необходимости создает каталог thumb;
    возвращает список кортежей (имя_файла_изображения, объект_миниатюры);
    для получения списка файлов миниатюр вызывающая программа может также
    воспользоваться функцией listdir в каталоге thumb; для неподдерживаемых
    типов файлов может возбуждать исключение IOError, или другое;
    ВНИМАНИЕ: можно было бы проверять время создания файлов;
    :param imgdir:
    :param size:
    :param subdir:
    :return: thumbs:
    """
    thumbdir = os.path.join(imgdir, subdir)
    if not os.path.exists(thumbdir):
        os.mkdir(thumbdir)

    thumbs = []

    for imgfile in os.listdir(imgdir):
        thumbpath = os.path.join(thumbdir, imgfile)
        if os.path.exists(thumbpath):
            thumbobj = Image.open(thumbpath)
            thumbs.append((imgfile, thumbobj))
        else:
            print('making', thumbpath)
            imgpath = os.path.join(imgdir, imgfile)
            try:
                imgobj = Image.open(imgpath)
                imgobj.thumbnail(size, Image.ANTIALIAS)
                imgobj.save(thumbpath)

                thumbs.append((imgfile, imgobj))
            except:
                print('Skiping:', imgpath)
    return thumbs


class ViewOne(Toplevel):
    """
    открывает одно изображение в новом окне; ссылку на объект PhotoImage
    требуется сохранить: изображение будет утрачено при утилизации объекта;
    """
    def __init__(self, imgdir, imgfile):
        Toplevel.__init__(self)
        self.title(imgfile)
        imgpath = os.path.join(imgdir, imgfile)
        imgobj = PhotoImage(file=imgpath)
        Label(self, image=imgobj).pack()
        print(imgpath, imgobj.width(), imgobj.height())
        self.savephoto = imgobj


# def viewer(imgdir, kind=Toplevel, cols=None):
#     """
#     создает окно с миниатюрами для каталога с изображениями: по одной кнопке с
#     миниатюрой для каждого изображения;
#     используйте параметр kind=Tk, чтобы вывести миниатюры в главном окне, или
#     Frame (чтобы прикрепить к фрейму); значение imgfile изменяется в каждой
#     итерации цикла: ссылка на значение должна сохраняться по умолчанию;
#     объекты PhotoImage должны сохраняться: иначе при утилизации изображения
#     будут уничтожены;
#     компонует в ряды фреймов (в противоположность сеткам, фиксированным
#     размерам, холстам);
#     :param imgdir:
#     :param kind:
#     :param cols:
#     :return: win, savephotos:
#     """
#     win = Tk()
#     win.title('Viewer:' + imgdir)
#     quit = Button(win, text='Quit', command=win.quit, bg='beige')
#     quit.pack(fill=X, side=BOTTOM)
#
#     thumbs = make_thumbs(imgdir)
#     if not cols:
#         cols = int(math.ceil(math.sqrt(len(thumbs))))       # фиксированное или N x N
#
#     saved_photos = []
#     while thumbs:
#         thumbsrow, thumbs = thumbs[:cols], thumbs[cols:]
#         row = Frame(win)
#         row.pack(fill=BOTH)
#         for (imgfile, imgobj) in thumbsrow:
#             photo = PhotoImage(imgobj)
#             link = Button(row, image=photo)
#             handler = lambda savefile=imgfile: ViewOne(imgdir, savefile)
#             link.config(command=handler)
#             link.pack(side=LEFT, expand=YES)
#             saved_photos.append(photo)
#
#     return win, saved_photos


def viewer(imgdir, kind=Toplevel, cols=None):
    """
    измененная версия, размещает миниатюры по сетке
    """
    win = kind()
    win.title('Viewer: ' + imgdir)
    thumbs = make_thumbs(imgdir)
    if not cols:
        cols = int(math.ceil(math.sqrt(len(thumbs))))# фиксированное или N x N

    rownum = 0
    saved_photos = []

    while thumbs:
        thumbsrow, thumbs = thumbs[:cols], thumbs[cols:]
        colnum = 0
        for (imgfile, imgobj) in thumbsrow:
            photo = PhotoImage(imgobj)
            link = Button(win, image=photo)
            handler = lambda savefile=imgfile: ViewOne(imgdir, savefile)
            link.config(command=handler)
            link.grid(row=rownum, column=colnum)
            saved_photos.append(photo)
            colnum += 1
        rownum += 1
    Button(win, text='Quit', command=win.quit).grid(columnspan=cols, stick=EW)
    return win, saved_photos


if __name__ == '__main__':
    # imgdir = (len(sys.argv) > 1 and sys.argv[1]) or 'images'
    imgdir = './images/'
    main, save = viewer(imgdir, kind=Tk)
    main.mainloop()






























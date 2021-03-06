from modules.discogs import GetDiscogsData
from modules import db
import json
import os
import sys
import PySimpleGUI as sg
from shutil import copyfile
from PIL import Image, ImageFont, ImageDraw
from pyglet import font


def open_file(*args):
    dialog = sg.tk.Tk()
    dialog.option_add('*foreground', 'black')
    dialog.option_add('*activeForeground', 'black')
    dialog.withdraw()
    f = sg.tkinter.filedialog.askopenfile(parent=dialog, filetypes=args[0])
    return f.name


def open_directory(*args):
    dialog = sg.tk.Tk()
    dialog.option_add('*foreground', 'black')
    dialog.option_add('*activeForeground', 'black')
    dialog.withdraw()
    f = sg.tkinter.filedialog.askdirectory(parent=dialog)
    return f


def save_file(*args):
    dialog = sg.tk.Tk()
    dialog.option_add('*foreground', 'black')
    dialog.option_add('*activeForeground', 'black')
    dialog.withdraw()
    f = sg.tkinter.filedialog.asksaveasfile(parent=dialog, filetypes=args[0], initialdir=args[1])
    return f

def open_project(directory, window):
    with open(directory + "/project.json") as json_file:
        data = json.load(json_file)
        for p in data['project']:
            window.Element("project_name").Update(value=p['name'])
            if p['nr_albums'] == 1:
                window.Element("album_1").Update(value=True)
            if p['nr_albums'] == 2:
                window.Element("album_2").Update(value=True)
        for p in data['albums']:
            window.Element("artist_1").Update(value=p['artist1'])
            window.Element("title_1").Update(value=p['title1'])
            window.Element("artist_2").Update(value=p['artist2'])
            window.Element("title_2").Update(value=p['title2'])
        for p in data['details']:
            if p['dolby'] == '---':
                window.Element("dolbynone").Update(value=True)
            if p['dolby'] == 'dolby-b':
                window.Element("dolbyb").Update(value=True)
            if p['dolby'] == 'dolby-c':
                window.Element("dolbyc").Update(value=True)
            if p['dolby'] == 'dolby-s':
                window.Element("dolbys").Update(value=True)
            window.Element("label").Update(value=p['label'])
            window.Element("code").Update(value=p['code'])
        for p in data['images']:
            try:
                loadimage1(window, directory + "/" + p['image1'])
                loadimage2(window, directory + "/" + p['image2'])
            except:
                pass
        for p in data['titles']:
            f = open(directory + "/" + p['sidea'], "r")
            window.Element("songs_a").Update(value=f.read())
            f.close()
            f = open(directory + "/" + p['sideb'], "r")
            window.Element("songs_b").Update(value=f.read())
            f.close()
            

def save_project(directory, projectname = "", nralbums = 1, artist1 = "", title1 = "", artist2 = "", title2 = "", dolby = "---", label = "", code = "", image1 = "", image2 = "", sidea = "", sideb = ""):
    if image1 != "":
        copyfile(image1, directory + "/image1.png")
    if image2 != "":
        copyfile(image2, directory + "/image2.png")
    f = open(directory + "/sidea.txt", "w")
    f.write(sidea)
    f.close()
    f = open(directory + "/sideb.txt", "w")
    f.write(sideb)
    f.close()
    data = {}
    data['project'] = []
    data['project'].append({
        'name': projectname,
        'nr_albums': nralbums
    })
    data['albums'] = []
    data['albums'].append({
        'artist1': artist1,
        'title1': title1,
        'artist2': artist2,
        'title2': title2
    })
    data['details'] = []
    data['details'].append({
        'dolby': dolby,
        'label': label,
        'code': code
    })
    data['images'] = []
    data['images'].append({
        'image1': "image1.png",
        'image2': "image2.png"
    })
    data['titles'] = []
    data['titles'].append({
        'sidea': "sidea.txt",
        'sideb': "sideb.txt"
    })
    with open(directory + "/project.json", "w") as outfile:
        json.dump(data, outfile)


def print_combine(*args):
    try:
        # nowy obraz
        image_w, image_h = 7016, 4960
        im = Image.new('RGB', (image_w, image_h), (255, 255, 255))
        if args[0] != "":
            cover1 = Image.open(args[0])
            im.paste(cover1, (400, 300))
        if args[1] != "":
            cover2 = Image.open(args[1])
            im.paste(cover2, (2962, 300))
        if os.path.exists("output/"):
            pass
        else:
            os.mkdir("output/")
        filename = save_file(((".jpg","*.jpg"),), "output/")
        im.save(filename, quality=95)
        #todo print support
        '''
        if sys.platform == "linux":
            os.system("pwd")
            os.system("lpr ./print/print.jpg")
        if sys.platform == "win32":
            pass
        if sys.platform == "darwin" or sys.platform == "cygwin":
            sg.popup_error("This system is not supported. Please print file manually from \"print\" directory.")
        '''
    except ValueError:
        pass


def wnd_print_combine():
    img1 = ""
    img2 = ""
    ans = True
    while ans:
        # theme
        sg.SetOptions(font=("Arial", 10), margins=(0, 0))
        sg.theme("Dark")
        # layouts
        logo = [
            [sg.Image("./gfx/cccc.png")]
        ]
        browse = [
            [sg.Input(key="img1", size=(74,1)), sg.Button("Select Cover #1", key="btn_file1")],
            [sg.Input(key="img2", size=(74,1)), sg.Button("Select Cover #2", key="btn_file2")]
        ]
        action = [
            [sg.Button("Combine Covers for print", key="btn_printcombine")]
        ]
        frm_browse = [
            [sg.Frame("Browse files:", browse)]
        ]
        frm_action = [
            [sg.Frame("Actions:", action)]
        ]
        form = [
            [sg.Column(logo)],
            [sg.Column(frm_browse)],
            [sg.Column(frm_action)]
        ]
        window = sg.Window("CCCC " + db.version, form, finalize=True)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                ans = False
                break
            if event == "btn_file1":
                try:
                    img1 = open_file(((".jpg","*.jpg"),))
                    window.Element("img1").Update(value=img1)
                except AttributeError:
                    pass
            if event == "btn_file2":
                try:
                    img2 = open_file(((".jpg","*.jpg"),))
                    window.Element("img2").Update(value=str(img2))
                except AttributeError:
                    pass
            if event == "btn_printcombine":
                print_combine(values["img1"], values["img2"])
        window.close()


def createcover_1(projectname, filebrowse1, artist1, title1, dolby, label, code):
    # dla jednego albumu
    # nowy obraz
    image_w, image_h = 1520, 2410
    im = Image.new('RGB', (image_w, image_h), (255, 255, 255))
    # import coveru oraz resize
    cover1 = Image.open(filebrowse1)
    cover1_w, cover1_h = 1500, 1500
    cover1 = cover1.resize((cover1_w, cover1_h))
    # dolby
    if dolby != "---":
        dolby_img = Image.open("dolby/" + dolby + ".jpg")
        dolby_img_w, dolby_img_h = 531, 72
        dolby_img = dolby_img.resize((dolby_img_w, dolby_img_h))
    # import fontów
    title_font1 = ImageFont.truetype('./fonts/TTWPGOTT.ttf', 90)
    title_font2 = ImageFont.truetype('./fonts/TTWPGOTT.ttf', 75)
    # rysowanie linii marginesów
    draw = ImageDraw.Draw(im)
    draw.line((0, 3, 1520, 3), fill=(0, 0, 0), width=8)
    draw.line((0, 2406, 1520, 2406), fill=(0, 0, 0), width=8)
    # wklejanie coveru do zawartości obrazu
    im.paste(cover1, (10, 60))
    # title - linia #1
    tl1w, tl1h = draw.textsize(artist1, title_font1)
    tl1p = ((image_w - tl1w) / 2, 1700)
    draw.text(tl1p, artist1, font=title_font1, fill=(0, 0, 0, 0), align="center")
    # title - linia #2
    tl2w, tl2h = draw.textsize(title1, title_font1)
    tl2p = ((image_w - tl2w) / 2, 1800)
    draw.text(tl2p, title1, font=title_font1, fill=(0, 0, 0, 0))
    # numer taśmy
    tl4w, tl4h = draw.textsize(label + " - " + code, title_font2)
    tl4p = ((image_w - tl4w) / 2, 2175)
    draw.text(tl4p, label + " - " + code, font=title_font2, fill=(0, 0, 0, 0))
    # znaczek dolby
    #tl5w, tl5h = draw.textsize(dolby, title_font2)
    #tl5p = ((image_w - tl5w) / 2, 2250)
    #draw.text(tl5p, dolby, font=title_font2, fill=(0, 0, 0, 0))
    if dolby != "---":
        im.paste(dolby_img, (int((image_w - dolby_img_w) / 2), 2260))
    # zapis obrazu
    if os.path.exists("covers/" + projectname):
        pass
    else:
        os.mkdir("covers/" + projectname)
        os.mkdir("covers/" + projectname + "/build")
    im.save("covers/" + projectname + '/build/tape_title.jpg', quality=95)


def createcover_2(projectname, filebrowse1, filebrowse2, artist1, title1, artist2, title2, dolby, label, code):
    # nowy obraz
    image_w, image_h = 1520, 2410
    im = Image.new('RGB', (image_w, image_h), (255, 255, 255))
    # import coverów oraz resize
    cover1 = Image.open(filebrowse1)
    cover1_w, cover1_h = 750, 750
    cover1 = cover1.resize((cover1_w, cover1_h))
    cover2 = Image.open(filebrowse2)
    cover2_w, cover2_h = 750, 750
    cover2 = cover2.resize((cover2_w, cover2_h))
    # dolby
    if dolby != "---":
        dolby_img = Image.open("dolby/" + dolby + ".jpg")
        dolby_img_w, dolby_img_h = 531, 72
        dolby_img = dolby_img.resize((dolby_img_w, dolby_img_h))
    # import fontów
    title_font1 = ImageFont.truetype('./fonts/TTWPGOTT.ttf', 90)
    title_font2 = ImageFont.truetype('./fonts/TTWPGOTT.ttf', 75)
    # rysowanie linii marginesów
    draw = ImageDraw.Draw(im)
    draw.line((0, 3, 1520, 3), fill=(0, 0, 0), width=8)
    draw.line((0, 2406, 1520, 2406), fill=(0, 0, 0), width=8)
    # wklejanie coveru do zawartości obrazu
    im.paste(cover1, (385, 60))
    im.paste(cover2, (385, 1050))
    # album 1 - linia #1
    tl1w, tl1h = draw.textsize(artist1, title_font1)
    tl1p = ((image_w-tl1w)/2, 830)
    draw.text(tl1p, artist1, font=title_font1, fill=(0, 0, 0, 0), align="center")
    # album 1 - linia #2
    tl2w, tl2h = draw.textsize(title1, title_font1)
    tl2p = ((image_w - tl2w) / 2, 930)
    draw.text(tl2p, title1, font=title_font1, fill=(0, 0, 0, 0))
    # album 2 - linia #1
    tl3w, tl3h = draw.textsize(artist2, title_font1)
    tl3p = ((image_w - tl3w) / 2, 1820)
    draw.text(tl3p, artist2, font=title_font1, fill=(0, 0, 0, 0))
    # album 2 - linia #2
    tl4w, tl4h = draw.textsize(title2, title_font1)
    tl4p = ((image_w - tl4w) / 2, 1920)
    draw.text(tl4p, title2, font=title_font1, fill=(0, 0, 0, 0))
    # info - linia #1
    tl5w, tl5h = draw.textsize(label + " - " + code, title_font2)
    tl5p = ((image_w - tl5w) / 2, 2175)
    draw.text(tl5p, label + " - " + code, font=title_font2, fill=(0, 0, 0, 0))
    # info - linia #2
    #tl6w, tl6h = draw.textsize(dolby, title_font2)
    #tl6p = ((image_w - tl6w) / 2, 2250)
    #draw.text(tl6p, dolby, font=title_font2, fill=(0, 0, 0, 0))
    if dolby != "---":
        im.paste(dolby_img, (int((image_w - dolby_img_w) / 2), 2260))
    # zapis obrazu
    if os.path.exists("covers/" + projectname):
        pass
    else:
        os.mkdir("covers/" + projectname)
        os.mkdir("covers/" + projectname + "/build")
    im.save("covers/" + projectname + '/build/tape_title.jpg', quality=95)


def createspine_1(projectname, artist1, title1, dolby, label, code):
    # nowy obraz
    image_w, image_h = 2410, 667
    im = Image.new('RGB', (image_w, image_h), (255, 255, 255))
    # dolby
    if dolby != "---":
        dolby_img = Image.open("dolby/" + dolby + ".jpg")
        dolby_img_w, dolby_img_h = 531, 72
        dolby_img = dolby_img.resize((dolby_img_w, dolby_img_h))
    # import fontów
    title_font2 = ImageFont.truetype('./fonts/TTWPGOTT.ttf', 75)
    # rysowanie linii marginesów
    draw = ImageDraw.Draw(im)
    # poziome linie
    draw.line((0, 3, 2410, 3), fill=(0, 0, 0), width=8)
    draw.line((0, 664, 2410, 664), fill=(0, 0, 0), width=8)
    draw.line((0, 374, 2410, 374), fill=(0, 0, 0), width=8)
    # pionowe linie
    draw.line((3, 0, 3, 667), fill=(0, 0, 0), width=8)
    draw.line((2406, 0, 2406, 667), fill=(0, 0, 0), width=8)

    # small title 1 - linia #1
    tl1w, tl1h = draw.textsize(artist1, title_font2)
    tl1p = ((image_w-tl1w)/2, 20)
    draw.text(tl1p, artist1, font=title_font2, fill=(0, 0, 0, 0), align="center")
    # small title 1 - linia #2
    tl2w, tl2h = draw.textsize(title1, title_font2)
    tl2p = ((image_w - tl2w) / 2, 105)
    draw.text(tl2p, title1, font=title_font2, fill=(0, 0, 0, 0))
    # small title 1 - linia #3
    tl3w, tl3h = draw.textsize(label + " - " + code, title_font2)
    tl3p = ((image_w - tl3w) / 2, 190)
    draw.text(tl3p, label + " - " + code, font=title_font2, fill=(0, 0, 0, 0))
    # small title 1 - linia #4
    #tl4w, tl4h = draw.textsize(dolby, title_font2)
    #tl4p = ((image_w - tl4w) / 2, 275)
    #draw.text(tl4p, dolby, font=title_font2, fill=(0, 0, 0, 0))
    if dolby != "---":
        im.paste(dolby_img, (int((image_w - dolby_img_w) / 2), 275))
    # small title 2 - linia #1
    tl1w, tl1h = draw.textsize(artist1, title_font2)
    tl1p = ((image_w - tl1w) / 2, 378+20)
    draw.text(tl1p, artist1, font=title_font2, fill=(0, 0, 0, 0), align="center")
    # small title 2 - linia #2
    tl2w, tl2h = draw.textsize(title1, title_font2)
    tl2p = ((image_w - tl2w) / 2, 378+105)
    draw.text(tl2p, title1, font=title_font2, fill=(0, 0, 0, 0))
    # small title 3 - linia #3
    tl3w, tl3h = draw.textsize(label + " - " + code, title_font2)
    tl3p = ((image_w - tl3w) / 2, 378+190)
    draw.text(tl3p, label + " - " + code, font=title_font2, fill=(0, 0, 0, 0))
    if dolby != "---":
        im.paste(dolby_img, (int((image_w - dolby_img_w)-20), 378+190))
    # zapis obrazu
    if os.path.exists("covers/" + projectname):
        pass
    else:
        os.mkdir("covers/" + projectname)
        os.mkdir("covers/" + projectname + "/build")
    im.save("covers/" + projectname + '/build/tape_spine.jpg', quality=95)


def createspine_2(projectname, artist1, title1, artist2, title2, dolby, label, code):
    # nowy obraz
    image_w, image_h = 2410, 667
    im = Image.new('RGB', (image_w, image_h), (255, 255, 255))
    # dolby
    if dolby != "---":
        dolby_img = Image.open("dolby/" + dolby + ".jpg")
        dolby_img_w, dolby_img_h = 531, 72
        dolby_img = dolby_img.resize((dolby_img_w, dolby_img_h))
    # import fontów
    title_font2 = ImageFont.truetype('./fonts/TTWPGOTT.ttf', 75)
    # rysowanie linii marginesów
    draw = ImageDraw.Draw(im)
    # poziome linie
    draw.line((0, 3, 2410, 3), fill=(0, 0, 0), width=8)
    draw.line((0, 664, 2410, 664), fill=(0, 0, 0), width=8)
    draw.line((0, 374, 2410, 374), fill=(0, 0, 0), width=8)
    # pionowe linie
    draw.line((3, 0, 3, 667), fill=(0, 0, 0), width=8)
    draw.line((2406, 0, 2406, 667), fill=(0, 0, 0), width=8)

    # small title 1 - linia #1
    tl1w, tl1h = draw.textsize(artist1 + " - " + title1, title_font2)
    tl1p = ((image_w-tl1w)/2, 20)
    draw.text(tl1p, artist1 + " - " + title1, font=title_font2, fill=(0, 0, 0, 0), align="center")
    # small title 1 - linia #2
    tl2w, tl2h = draw.textsize(artist2 + " - " + title2, title_font2)
    tl2p = ((image_w - tl2w) / 2, 105)
    draw.text(tl2p, artist2 + " - " + title2, font=title_font2, fill=(0, 0, 0, 0))
    # small title 1 - linia #3
    tl3w, tl3h = draw.textsize(label + " - " + code, title_font2)
    tl3p = ((image_w - tl3w) / 2, 190)
    draw.text(tl3p, label + " - " + code, font=title_font2, fill=(0, 0, 0, 0))
    # small title 1 - linia #4
    #tl4w, tl4h = draw.textsize(dolby, title_font2)
    #tl4p = ((image_w - tl4w) / 2, 275)
    #draw.text(tl4p, dolby, font=title_font2, fill=(0, 0, 0, 0))
    if dolby != "---":
        im.paste(dolby_img, (int((image_w - dolby_img_w) / 2), 275))
    # small title 2 - linia #1
    tl1w, tl1h = draw.textsize(artist1 + " - " + title1, title_font2)
    tl1p = ((image_w - tl1w) / 2, 378+20)
    draw.text(tl1p, artist1 + " - " + title1, font=title_font2, fill=(0, 0, 0, 0), align="center")
    # small title 2 - linia #2
    tl2w, tl2h = draw.textsize(artist2 + " - " + title2, title_font2)
    tl2p = ((image_w - tl2w) / 2, 378+105)
    draw.text(tl2p, artist2 + " - " + title2, font=title_font2, fill=(0, 0, 0, 0))
    # small title 3 - linia #3
    tl3w, tl3h = draw.textsize(label + " - " + code, title_font2)
    tl3p = ((image_w - tl3w) / 2, 378+190)
    draw.text(tl3p, label + " - " + code, font=title_font2, fill=(0, 0, 0, 0))
    # zapis obrazu
    if os.path.exists("covers/" + projectname):
        pass
    else:
        os.mkdir("covers/" + projectname)
        os.mkdir("covers/" + projectname + "/build")
    im.save("covers/" + projectname + '/build/tape_spine.jpg', quality=95)


def createsongs_1(projectname, side_a, side_b):
    # nowy obraz
    image_w, image_h = 2410, 1545
    im = Image.new('RGB', (image_w, image_h), (255, 255, 255))
    # import fontów
    title_font1 = ImageFont.truetype('./fonts/TTWPGOTT.ttf', 70)
    # rysowanie linii marginesów
    draw = ImageDraw.Draw(im)
    # poziome linie
    draw.line((0, 3, 2410, 3), fill=(0, 0, 0), width=8)
    draw.line((0, 1541, 2410, 1541), fill=(0, 0, 0), width=8)
    # pionowe linie
    draw.line((3, 0, 3, 1545), fill=(0, 0, 0), width=8)
    draw.line((2406, 0, 2406, 1545), fill=(0, 0, 0), width=8)
    draw.line((image_w / 2 - 4, 0, image_w / 2 - 4, 1545), fill=(0, 0, 0), width=8)
    height_increment = 70
    side_a = side_a.split("\n")
    side_b = side_b.split("\n")
    for i, txt in enumerate(side_a):
        # song_w, song_h = draw.textsize(side_a_list[i], title_font1)
        song_p = (50, 20 + height_increment * i)
        draw.text(song_p, txt, font=title_font1, fill=(0, 0, 0, 0), align="center")
    # small title 1 - linia #2
    for i, txt in enumerate(side_b):
        # song_w, song_h = draw.textsize(side_a_list[i], title_font1)
        song_p = (1255, 20 + height_increment * i)
        draw.text(song_p, txt, font=title_font1, fill=(0, 0, 0, 0), align="center")
    # zapis obrazu
    if os.path.exists("covers/" + projectname):
        pass
    else:
        os.mkdir("covers/" + projectname)
        os.mkdir("covers/" + projectname + "/build")
    im.save("covers/" + projectname + '/build/tape_songs.jpg', quality=95)


def createsongs_2(projectname, side_a, side_b):
    # nowy obraz
    image_w, image_h = 2410, 1545
    im = Image.new('RGB', (image_w, image_h), (255, 255, 255))
    # import fontów
    title_font1 = ImageFont.truetype('./fonts/TTWPGOTT.ttf', 70)
    # rysowanie linii marginesów
    draw = ImageDraw.Draw(im)
    # poziome linie
    draw.line((0, 3, 2410, 3), fill=(0, 0, 0), width=8)
    draw.line((0, 1541, 2410, 1541), fill=(0, 0, 0), width=8)
    # pionowe linie
    draw.line((3, 0, 3, 1545), fill=(0, 0, 0), width=8)
    draw.line((2406, 0, 2406, 1545), fill=(0, 0, 0), width=8)
    draw.line((image_w / 2 - 4, 0, image_w / 2 - 4, 1545), fill=(0, 0, 0), width=8)
    height_increment = 70
    side_a = side_a.split("\n")
    side_b = side_b.split("\n")
    for i, txt in enumerate(side_a):
        # song_w, song_h = draw.textsize(side_a_list[i], title_font1)
        song_p = (50, 20 + height_increment * i)
        draw.text(song_p, txt, font=title_font1, fill=(0, 0, 0, 0), align="center")
    # small title 1 - linia #2
    for i, txt in enumerate(side_b):
        # song_w, song_h = draw.textsize(side_a_list[i], title_font1)
        song_p = (1255, 20 + height_increment * i)
        draw.text(song_p, txt, font=title_font1, fill=(0, 0, 0, 0), align="center")
    # zapis obrazu
    if os.path.exists("covers/" + projectname):
        pass
    else:
        os.mkdir("covers/" + projectname)
        os.mkdir("covers/" + projectname + "/build")
    im.save("covers/" + projectname + '/build/tape_songs.jpg', quality=95)


def compile(projectname):
    image_w, image_h = 2410, 3733
    im = Image.new('RGB', (image_w, image_h), (255, 255, 255))
    if os.path.exists("covers/" + projectname):
        small_title = Image.open("covers/" + projectname + '/build/tape_spine.jpg')
        title = Image.open("covers/" + projectname + '/build/tape_title.jpg').rotate(270, expand=1)
        songs = Image.open("covers/" + projectname + '/build/tape_songs.jpg')
        im.paste(small_title, (0, 0))
        im.paste(title, (0, 668))
        im.paste(songs, (0, 2188))
        if os.path.exists("covers/" + projectname + "/output"):
            pass
        else:
            os.mkdir("covers/" + projectname + "/output")
        im.save("covers/" + projectname + "/output/" + projectname + "_out.jpg")


def savecover():
    image_w, image_h = 1520, 2410
    im = Image.new('RGB', (image_w, image_h), (255, 255, 255))


def loadimage1(main_window, filepath):
    if os.path.exists("preview/"):
        pass
    else:
        os.mkdir("preview/")
    cover = Image.open(filepath)
    cover = cover.resize((150, 150))
    cover.save("preview/cover1.png")
    main_window.Element("image1").update(filename="preview/cover1.png")

def loadimage2(main_window, filepath):
    if os.path.exists("preview/"):
        pass
    else:
        os.mkdir("preview/")
    cover = Image.open(filepath)
    cover = cover.resize((150, 150))
    cover.save("preview/cover2.png")
    main_window.Element("image2").update(filename="preview/cover2.png")


def test1():
    style = sg.ttk.Style()
    style.theme_use("clam")
    style.configure("TScrolledFrame", foreground="red")
    filename = sg.filedialog.askopenfile("r")
    print(filename)

def discogs_dl(main_window):
    ans = True
    while ans:
        # theme
        sg.SetOptions(font=("Arial", 10), margins=(0, 0))
        sg.theme("Dark")
        # layouts
        discogs = [
            [sg.Text("Discogs release:"), sg.InputText("", size=(10, 1), key="discogs_release"), sg.Button("Download data", size=(18, 1), pad=((4, 4), (0, 4)), key="btn_getdiscogsdata")],
            [sg.Text("Artist:", size=(5, 1)), sg.Button("+ Artist 1", key="btn_addart1", size=(5, 1)),
             sg.Button("+ Artist 2", key="btn_addart2", size=(5, 1))],
            [sg.InputText("", enable_events=True, key="discogs_artist", size=(32, 1))],
            [sg.Text("Title:", size=(5, 1)), sg.Button("+ Title 1", key="btn_addtit1", size=(5, 1)),
             sg.Button("+ Title 2", key="btn_addtit2", size=(5, 1))],
            [sg.InputText("", enable_events=True, key="discogs_title", size=(32, 1))],
            [sg.Listbox([], size=(65, 15), enable_events=True, key="discogs_list")],
            [sg.Button("+ Side A", key="btn_addsidea"), sg.Button("+ Side B", key="btn_addsideb"),
             sg.Checkbox("Add track numbers", key="tracknr"), sg.Text("Track:", size=(5, 1)),
             sg.InputText(1, key="track", size=(2, 1))]
        ]
        frm_discogs = [
            [sg.Frame(title="Discogs", layout=discogs)]
        ]
        gui = [
            [sg.Column(layout=frm_discogs)]
        ]
        window = sg.Window("CCCC - Discogs database", gui, finalize=True, size=(440, 440))
        while True:
            event, values = window.read()
            if event == "btn_getdiscogsdata":
                artists, title, songs = GetDiscogsData(values["discogs_release"])
                artist = ""
                for i, a in enumerate(artists):
                    artist += a
                    if i < len(artists) - 1:
                        artist += ", "
                window.Element("discogs_artist").update(artist)
                window.Element("discogs_title").update(title)
                window.Element("discogs_list").update(songs)
            if event == "btn_addsidea":
                data = values["discogs_list"]
                if values["tracknr"]:
                    main_window.Element("songs_a").update(value=values["track"] + ". " + str(data[0]) + "\n", append=True)
                    window.Element("track").update(value=int(values["track"]) + 1)
                else:
                    main_window.Element("songs_a").update(value=str(data[0]) + "\n", append=True)
            if event == "btn_addsideb":
                data = values["discogs_list"]
                if values["tracknr"]:
                    main_window.Element("songs_b").update(value=values["track"] + ". " + str(data[0]) + "\n", append=True)
                    window.Element("track").update(value=int(values["track"]) + 1)
                else:
                    main_window.Element("songs_b").update(value=str(data[0]) + "\n", append=True)
            if event == "btn_addart1":
                data = values["discogs_artist"]
                main_window.Element("artist_1").update(value=str(data))
            if event == "btn_addtit1":
                data = values["discogs_title"]
                main_window.Element("title_1").update(value=str(data))
            if event == "btn_addart2":
                data = values["discogs_artist"]
                main_window.Element("artist_2").update(value=str(data))
            if event == "btn_addtit2":
                data = values["discogs_title"]
                main_window.Element("title_2").update(value=str(data))
            if event == sg.WIN_CLOSED:
                ans = False
                break

def jcard_creator():
    img1 = ""
    img2 = ""
    #font
    font.add_file('fonts/TTWPGOTT.ttf')
    PolyglOTT = font.load('Truetypewriter PolyglOTT')
    ans = True
    while ans:
        # theme
        sg.SetOptions(font=("Arial", 10), margins=(0, 0))
        sg.theme("Dark")
        # layouts
        logo = [
            [sg.Image("./gfx/cccc.png")]
        ]
        options = [
            [sg.Text("Project name:")],
            [sg.InputText("", size=(20, 1), key="project_name")],
            [sg.Text("Number of albums:")],
            [sg.Radio("1", group_id=1, key="album_1", default=True, size=(5, 1), enable_events=True), sg.Radio("2", group_id=1, key="album_2", size=(5, 1), enable_events=True)],

        ]
        titles = [
            [sg.Text(text="Artist 1:", size=(8, 1)), sg.InputText("", key="artist_1", font=("Truetypewriter PolyglOTT", 12),)],
            [sg.Text(text="Title 1:", size=(8, 1)), sg.InputText("", key="title_1", font=("Truetypewriter PolyglOTT", 12))],
            [sg.Text(text="Artist 2:", size=(8, 1)), sg.InputText("", key="artist_2", disabled=True, font=("Truetypewriter PolyglOTT", 12))],
            [sg.Text(text="Title 2:", size=(8, 1)), sg.InputText("", key="title_2", disabled=True, font=("Truetypewriter PolyglOTT", 12))],
        ]
        details = [
            [sg.Text(text="Dolby:", size=(8, 1)), sg.Radio(text="None", group_id=2, key="dolbynone", enable_events=True, default=True), sg.Radio(text="B", group_id=2, key="dolbyb", enable_events=True), sg.Radio(text="C", group_id=2, key="dolbyc", enable_events=True), sg.Radio(text="S", group_id=2, key="dolbys", enable_events=True)],
            [sg.Text(text="Label:"), sg.InputText("", font=("Truetypewriter PolyglOTT", 12), key="label")],
            [sg.Text(text="Code:"), sg.InputText("", font=("Truetypewriter PolyglOTT", 12), key="code")],
        ]
        songs_a = [
            [sg.Text("Side A")],
            [sg.Multiline("", size=(36, 15), key="songs_a", font=("Truetypewriter PolyglOTT", 12))]
        ]
        songs_b = [
            [sg.Text("Side B")],
            [sg.Multiline("", size=(36, 15), key="songs_b", font=("Truetypewriter PolyglOTT", 12))]
        ]
        songs = [
            [sg.Column(layout=songs_a), sg.Column(layout=songs_b)]
        ]
        action_buttons = [
            [sg.Button("Get data from Discogs", size=(18, 1), pad=((4, 4), (0, 4)), key="btn_discogs"), sg.Button("Save cover", size=(18, 1), pad=((4, 4), (0, 4)), key="btn_savecover"), sg.Button("Combine covers", size=(18, 1), pad=((4, 4), (0, 4)), key="btn_combineprint")],
            [sg.Button("", size=(18, 1), pad=((4, 4), (0, 4)), key="btn_openproject", image_filename="./gfx/directory.png", image_size=(40, 24), image_subsample=2), sg.Button("Save project", size=(18, 1), pad=((4, 4), (0, 4)), key="btn_saveproject")]
        ]
        images_1 = [
            [sg.Image(filename="gfx/default_cassette.png", enable_events=True, key="image1", size=(150,150))],
            [sg.Button("Select Image", key="btn_filebrowse1")]
            #[sg.FileBrowse("Select Image", enable_events=True, key="filebrowse1")]
        ]
        images_2 = [
            [sg.Image(filename="gfx/default_cassette.png", enable_events=True, key="image2", size=(150,150))],
            [sg.Button("Select Image", key="btn_filebrowse2")]
            #[sg.FileBrowse("Select Image", enable_events=True, key="filebrowse2")]
        ]
        images = [
            [sg.Column(layout=images_1), sg.Column(layout=images_2)],
        ]
        frm_action_buttons = [
            [sg.Frame(title="Actions", layout=action_buttons)]
        ]
        frm_options = [
            [sg.Frame(title="Options", layout=options)]
        ]
        frm_titles = [
            [sg.Frame(title="Artists and Titles", layout=titles)]
        ]
        frm_details = [
            [sg.Frame(title="Details", layout=details)]
        ]
        frm_songs = [
            [sg.Frame(title="Songs", layout=songs)]
        ]
        frm_images = [
            [sg.Frame(title="Images", layout=images)]
        ]
        frm_img_btn = [
            [sg.Column(layout=frm_images)],
            [sg.Column(layout=frm_action_buttons)]
        ]
        gui = [
            [sg.Column(layout=logo)],
            [sg.Column(layout=frm_options), sg.Column(layout=frm_titles), sg.Column(layout=frm_details)],
            [sg.Column(layout=frm_songs), sg.Column(layout=frm_img_btn)]
        ]
        window = sg.Window("CCCC " + db.version, gui, finalize=True, size=(960, 570))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                ans = False
                break
            if values["dolbynone"]:
                dolby = "---"
            if values["dolbyb"]:
                dolby = "dolby-b"
            if values["dolbyc"]:
                dolby = "dolby-c"
            if values["dolbys"]:
                dolby = "dolby-s"
            if event == "btn_filebrowse1":
                try:
                    img1 = open_file(((".png","*.png"),))
                    loadimage1(window, img1)
                except AttributeError:
                    pass
            if event == "btn_filebrowse2":
                try:
                    img2 = open_file(((".png","*.png"),))
                    loadimage2(window, img2)
                except AttributeError:
                    pass
            if event == "album_1":
                window.Element("artist_2").update(value="", disabled=True)
                window.Element("title_2").update(value="", disabled=True)
            if event == "album_2":
                window.Element("artist_2").update(disabled=False)
                window.Element("title_2").update(disabled=False)
            if event == "btn_discogs":
                window.Element("btn_discogs").update(disabled=True)
                discogs_dl(window)
                window.Element("btn_discogs").update(disabled=False)
            if event == "btn_addsidea":
                data = values["discogs_list"]
                if values["tracknr"]:
                    window.Element("songs_a").update(value=values["track"] + ". " + str(data[0]) + "\n", append=True)
                    window.Element("track").update(value=int(values["track"]) + 1)
                else:
                    window.Element("songs_a").update(value=str(data[0]) + "\n", append=True)
            if event == "btn_addsideb":
                data = values["discogs_list"]
                if values["tracknr"]:
                    window.Element("songs_b").update(value=values["track"] + ". " + str(data[0]) + "\n", append=True)
                    window.Element("track").update(value=int(values["track"]) + 1)
                else:
                    window.Element("songs_b").update(value=str(data[0]) + "\n", append=True)
            if event == "btn_addart1":
                data = values["discogs_artist"]
                window.Element("artist_1").update(value=str(data))
            if event == "btn_addtit1":
                data = values["discogs_title"]
                window.Element("title_1").update(value=str(data))
            if event == "btn_addart2":
                data = values["discogs_artist"]
                window.Element("artist_2").update(value=str(data))
            if event == "btn_addtit2":
                data = values["discogs_title"]
                window.Element("title_2").update(value=str(data))
            if event == "btn_savecover":
                if values["album_1"]:
                    projectname = values["project_name"]
                    filebrowse1 = img1
                    artist1 = values["artist_1"]
                    title1 = values["title_1"]
                    label = values["label"]
                    code = values["code"]
                    side_a = "A\n------------------------------------\n" + values["songs_a"]
                    side_b = "B\n------------------------------------\n" + values["songs_b"]
                    createcover_1(projectname, filebrowse1, artist1, title1, dolby, label, code)
                    createspine_1(projectname, artist1, title1, dolby, label, code)
                    createsongs_1(projectname, side_a, side_b)
                    compile(projectname)
                if values["album_2"]:
                    projectname = values["project_name"]
                    filebrowse1 = img1
                    filebrowse2 = img2
                    artist1 = values["artist_1"]
                    title1 = values["title_1"]
                    artist2 = values["artist_2"]
                    title2 = values["title_2"]
                    label = values["label"]
                    code = values["code"]
                    side_a = "A\n------------------------------------\n" + values["songs_a"]
                    side_b = "B\n------------------------------------\n" + values["songs_b"]
                    createcover_2(projectname, filebrowse1, filebrowse2, artist1, title1, artist2, title2, dolby, label, code)
                    createspine_2(projectname, artist1, title1, artist2, title2, dolby, label, code)
                    createsongs_2(projectname, side_a, side_b)
                    compile(projectname)
            if event == "btn_saveproject":
                try:
                    directory = open_directory()
                    projectname = values["project_name"]
                    if values["album_1"]:
                        nralbums = 1
                    if values["album_2"]:
                        nralbums = 2
                    filebrowse1 = img1
                    filebrowse2 = img2
                    artist1 = values["artist_1"]
                    title1 = values["title_1"]
                    artist2 = values["artist_2"]
                    title2 = values["title_2"]
                    label = values["label"]
                    code = values["code"]
                    side_a = values["songs_a"]
                    side_b = values["songs_b"]
                    save_project(directory, projectname, nralbums, artist1, title1, artist2, title2, dolby, label, code, filebrowse1, filebrowse2, side_a, side_b)
                except AttributeError:
                    pass
            if event == "btn_openproject":
                try:
                    directory = open_directory()
                    open_project(directory, window)
                except AttributeError:
                    pass
            if event == "btn_combineprint":
                wnd_print_combine()
        window.close()


if __name__ == '__main__':
    if os.path.exists("covers/"):
        pass
    else:
        os.mkdir("covers/")
    db.initialize()
    jcard_creator()

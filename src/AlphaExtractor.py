import glob
import os
import xml.etree.ElementTree as et
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

EXTRACTABLE_DIRS = ["Defs"]
CONFIG_VERSION = 2
EXTRACTOR_VERSION = "0.7.7"
WORD_NEWLINE = '\n'
WORD_BACKSLASH = '\\'


class EntryHint(Entry):
    def __init__(self, master=None, hint="", color='grey'):
        super().__init__(master)

        self.hint = hint
        self.hint_color = color
        self.default_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_hint()

    def put_hint(self):
        self.insert(0, self.hint)
        self['fg'] = self.hint_color

    def foc_in(self, *args):
        if self['fg'] == self.hint_color:
            self.delete('0', 'end')
            self['fg'] = self.default_color

    def get(self):
        tmp = super().get()
        if tmp == self.hint:
            return ""
        else:
            return tmp

    def foc_out(self, *args):
        if not self.get():
            self.put_hint()


class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                      background="#ffffff", relief='solid', borderwidth=1,
                      wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


def loadConfig(fileName='config.dat'):
    with open(fileName, 'r', encoding='UTF8') as fin:
        configs = fin.read().split('\n')

    if CONFIG_VERSION > int(configs[3]):
        raise ()

    modDir = configs[5]
    definedExcludes = configs[7].replace(' ', '').split('/')
    definedIncludes = configs[9].replace(' ', '').split('/')
    exportDir = configs[11]
    exportFile = configs[13]
    isNameTODO = (configs[15] == 'True')
    collisionOption = int(configs[17])

    return modDir, definedExcludes, definedIncludes, exportDir, exportFile, isNameTODO, collisionOption


def writeConfig(new_modDir=None, new_exportDir=None, new_exportFile=None,
                new_isNameTODO=None, new_collisionOption=None, fileName="config.dat"):
    try:
        modDir, definedExcludes, definedIncludes, exportDir, exportFile, isNameTODO, collisionOption = loadConfig()
        if new_modDir: modDir = new_modDir
        if new_exportDir: exportDir = new_exportDir
        if new_exportFile: exportFile = new_exportFile
        if str(new_isNameTODO): isNameTODO = new_isNameTODO
        if new_collisionOption: collisionOption = new_collisionOption
    except Exception:
        modDir = ""
        definedExcludes = []
        definedIncludes = "label/description/customLabel/rulesStrings/slateRef/reportString/jobString/verb/labelNoun/gerund/helpText/letterText/labelFemale/labelPlural/text/labelShort/letterLabel/baseInspectLine/beginLetter/rejectInputMessage/deathMessage/beginLetterLabel/recoveryMessage/endMessage/gerundLabel/pawnLabel/onMapInstruction/labelNounPretty/labelForFullStatList/pawnSingular/pawnsPlural/labelSolidTendedWell/labelTendedWell/labelTendedWellInner/destroyedLabel/permanentLabel/skillLabel/graphLabelY/formatString/meatLabel/headerTip/labelMale/ingestCommandString/ingestReportString/useLabel/descriptionFuture/destroyedOutLabel/leaderTitle/textEnemy/textWillArrive/arrivalTextEnemy/letterLabelEnemy/arrivedLetter/stuffAdjective/textFriendly/arrivalTextFriendly/letterLabelFriendly/name/summary/labelMechanoids/approachingReportString/approachOrderString/fuelGizmoLabel/fuelLabel/outOfFuelMessage/labelSocial/calledOffMessage/finishedMessage/discoverLetterLabel/discoverLetterText/discoveredLetterText/discoveredLetterTitle/instantlyPermanentLabel/letter/adjective/labelFemalePlural/successfullyRemovedHediffMessage/offMessage/ingestReportStringEat/renounceTitleMessage/royalFavorLabel/letterTitle".split(
            '/')
        exportDir = "extracted"
        exportFile = "alpha.xml"
        isNameTODO = "True"
        collisionOption = 0

    configs = f"""Alpha's Extractor Configure file
DO NOT EDIT THIS FILE MANUALLY
Config version [int]
{CONFIG_VERSION}
Mod directory [string]
{modDir}
Excluded tags [string, split with '/']
{'/'.join(definedExcludes)}
Included tags [string, split with '/']
{'/'.join(definedIncludes)}
Export directory [string, split with '/']
{exportDir}
Export filename
{exportFile}
Is Name TODO [Boolean, True/False]
{isNameTODO}
Option file collision  [int, 0:Stop, 1:Skip, 2:Overwrite, 3:Merge, 4:Refer]
{collisionOption}"""

    with open(fileName, 'w', encoding='UTF8') as fin:
        fin.write(configs)


def loadInit(window):
    global modDir, easterEgg
    easterEgg = 0

    frame = Frame(window)
    frame.grid(row=0, column=0, sticky=N + S + E + W)

    for i in range(3):
        Grid.rowconfigure(frame, i, weight=1)
    for i in range(2):
        Grid.columnconfigure(frame, i, weight=1)

    labelText = f"""림월드 모드들이 위치한 폴더를 선택해 주십시오

해당 폴더에는 모드 폴더들이 존재해야 합니다.스팀 창작마당 모드의 경우 기본값은 다음과 같습니다.

[C:/Program Files (x86)/Steam/steamapps/workshop/content/294100]

이 텍스트를 클릭할 경우 위 경로가 적용됩니다.

GUI 첫 배포 버전이므로 현재 Defs만 추출이 가능합니다.
모든 종류의 개선안이나, 버그 제보는 항상 환영합니다.

version = {EXTRACTOR_VERSION}"""

    label = Label(frame, text=labelText)
    label.grid(row=0, column=0, columnspan=4, sticky=N + S + E + W)

    def onClickLabel(event):
        entry.delete(0, END)
        entry.insert(0, "C:/Program Files (x86)/Steam/steamapps/workshop/content/294100")

    label.bind("<Button-1>", onClickLabel)

    entry = Entry(frame)
    entry.insert(0, modDir)
    entry.grid(row=1, column=0, columnspan=3, sticky=E + W)

    def onClick1():
        entry.delete(0, END)
        entry.insert(0, filedialog.askdirectory())

    btn = Button(frame, text="폴더 선택", command=onClick1)
    btn.grid(row=1, column=3)

    def onClick2():
        global modDir, easterEgg
        modDir = entry.get()
        if not modDir:
            messagebox.showerror("경로 선택되지 않음", "모드들이 위치한 폴더를 선택해 주십시오.")
            return
        writeConfig(new_modDir=modDir)
        frame.destroy()
        loadSelectMod(window)

    btn = Button(frame, text="확인", command=onClick2)
    btn.grid(row=2, column=0, columnspan=4)


def loadSelectMod(window):
    global modDir

    frame = Frame(window)
    frame.grid(row=0, column=0, sticky=N + S + E + W)
    for i in range(1):
        Grid.rowconfigure(frame, i, weight=1)
    for i in range(2):
        Grid.columnconfigure(frame, i, weight=1)

    listbox = Listbox(frame)
    modsList = glob.glob(modDir + '/*')

    if not modsList:
        messagebox.showerror("파일/폴더 찾을 수 없음", "해당 폴더에 어떤 파일/폴더도 존재하지 않습니다")
        frame.destroy()
        loadInit(window)
        return

    for i, modPath in enumerate(modsList):
        try:
            listbox.insert(i + 1,
                           f"{int(modPath.split(WORD_BACKSLASH)[-1]):010d} | {et.parse(modPath + '/About/About.xml').getroot().find('name').text}")
        except (FileNotFoundError, ValueError):
            listbox.insert(i + 1, f"0000000000 | {modPath.split(WORD_BACKSLASH)[-1]}")

    def onSelect(evt):
        w = evt.widget
        index = int(w.curselection()[0])

        rightFrame = Frame(frame)
        rightFrame.grid(row=0, column=1, sticky=N + S + E + W)
        for i in range(3):
            Grid.rowconfigure(rightFrame, i, weight=1)
        for i in range(1):
            Grid.columnconfigure(rightFrame, i, weight=1)

        upFrame = Frame(rightFrame)
        upFrame.grid(row=0, column=0, sticky=N + S + E + W)
        dnFrame = Frame(rightFrame)
        dnFrame.grid(row=1, column=0, sticky=N + S + E + W)

        isChecked = IntVar()

        def onCheck():
            dnFrame = Frame(rightFrame)
            dnFrame.grid(row=1, column=0, sticky=N + S + E + W)
            Label(dnFrame, text="추출할 폴더를 선택하세요.").pack()
            extractCheck = [BooleanVar() for _ in versionDir[isChecked.get()]]
            # get Keyed
            try:
                list(et.parse(modsList[index] + '/Languages/English/Keyed').getroot())
            except (FileNotFoundError, PermissionError):
                pass
            ###########
            checkButtons = [Checkbutton(dnFrame, text=extractDir.split("\\")[-1], var=check)
                            for extractDir, check in zip(versionDir[isChecked.get()], extractCheck)]
            for checkButton in checkButtons:
                checkButton.pack()

            def onExtract():
                global goExtractList

                goExtractList = [v for v, b in zip(versionDir[isChecked.get()], extractCheck) if b.get()]
                if not goExtractList:
                    messagebox.showerror("폴더를 선택하세요", "추출할 폴더를 하나 이상 선택하세요.")
                    return
                frame.destroy()
                loadSelectTags(window)

            extractButton = Button(rightFrame, text="추출하기", command=onExtract)
            extractButton.grid(row=2, column=0)

        # get Defs/Patches folders
        try:
            versionList = list(et.parse(modsList[index] + '/LoadFolders.xml').getroot())
            Label(upFrame, text="LoadFolders.xml이 발견되었습니다.\n추출할 버전을 선택하세요.").pack()
            isLoadFoldersExist = True

            versionRadioBtns = [Radiobutton(upFrame, text=version.tag, value=i, variable=isChecked, command=onCheck)
                                for i, version in enumerate(versionList)]
            versionDirs = [[(modsList[index] + "/" + versionDir.text if not versionDir.text == '/' else modsList[index])
                         for versionDir in list(version) if versionDir.text]
                        for version in versionList]
            versionDir = [[os.path.join(eachVersionDir, dir)
                           for eachVersionDir in eachVersion
                           for dir in os.listdir(eachVersionDir)
                           if os.path.isdir(os.path.join(eachVersionDir, dir)) and dir in EXTRACTABLE_DIRS]
                          for eachVersion in versionDirs]

        except FileNotFoundError:
            isLoadFoldersExist = False
            Label(upFrame,
                  text="LoadFolders.xml을 발견하지 못했습니다.\n폴더명 기반으로 추측되었습니다.\n추출할 버전을 선택하세요.").pack()
            versionsPath = [name
                            for name in os.listdir(modsList[index])
                            if os.path.isdir(os.path.join(modsList[index], name))]

            versionList = []
            isModNoVersion = False
            for item in versionsPath:
                tmp = item.split('\\')[-1]
                if tmp in EXTRACTABLE_DIRS:
                    isModNoVersion = True
                if "1." in tmp:
                    versionList.append(tmp)
            if isModNoVersion:
                versionList.insert(0, "default")

            versionRadioBtns = [Radiobutton(upFrame, text=version, value=i, variable=isChecked, command=onCheck)
                                for i, version in enumerate(versionList)]

            versionDirs = [os.path.join(modsList[index], version)
                        if not version == 'default' else modsList[index]
                        for version in versionList]
            versionDir = [[os.path.join(atVer, dir)
                           for dir in os.listdir(atVer)
                           if os.path.isdir(os.path.join(atVer, dir)) and dir in EXTRACTABLE_DIRS]
                          for atVer in versionDirs]
        ###################################

        for btn in versionRadioBtns:
            btn.deselect()
            btn.pack()

        isChecked.set(0)

    listbox.bind('<<ListboxSelect>>', onSelect)
    listbox.grid(row=0, column=0, sticky=N + S + E + W)


def parse_recursive(parent, className, tag, lastTag=None):
    if list(parent):
        tags = [child.tag == 'li' for child in list(parent)]
        texts = [child.text for child in list(parent)]
        if all(tags) and all(texts) and tags and texts:
            yield className, lastTag, tag, texts
        else:
            num_list = 0
            for child in list(parent):
                if child.tag == 'li':
                    yield from parse_recursive(child, className, tag + '.' + str(num_list), str(num_list))
                    num_list += 1
                else:
                    yield from parse_recursive(child, className, tag + '.' + child.tag, child.tag)
    else:
        yield className, lastTag, tag, (parent.text if not parent.text is None else "ERROR:{$BLANK TEXT}")

def extractDefs(root):
    if 'value' != root.tag and 'Defs' != root.tag:
        raise ValueError("첫 태그가 Defs가 아닙니다. 오류를 발생시킨 모드 이름과 파일명을 Alpha에게 제보해주세요.")

    for item in list(root):
        try:
            if item.attrib['Abstract'].lower() == 'true':
                continue
        except Exception:
            pass

        try:
            defName = item.find('defName').text
        except Exception:
            continue

        className = item.tag
        if className == 'Def':
            try:
                className = item.attrib['Class']
            except Exception:
                raise ValueError("Def임에도 불구하고 클래스 이름이 없습니다. 오류를 발생시킨 모드 이름과 파일명을 Alpha에게 제보해주세요.")

        yield from parse_recursive(item, className, defName)


def loadSelectTags(window):
    global goExtractList, excludes, defaults, includes, excludeHide, defaultHide, includeHide, dict_class

    frame = Frame(window)
    frame.grid(row=0, column=0, sticky=N + S + E + W)

    Grid.rowconfigure(frame, 0, weight=1)  # label
    Grid.rowconfigure(frame, 1, weight=9)  # list
    Grid.rowconfigure(frame, 2, weight=1)  # moveButton
    Grid.rowconfigure(frame, 3, weight=1)  # search
    Grid.rowconfigure(frame, 4, weight=1)  # extract
    for i in range(3):
        Grid.columnconfigure(frame, i, weight=1)

    dict_tags_text = {}

    for goExtract in goExtractList:
        GoExtractLists = glob.glob(goExtract + "/**/*.xml", recursive=True)
        if goExtract.split('\\')[-1] == 'Defs':
            for path in GoExtractLists:
                try:
                    extracts = extractDefs(et.parse(path).getroot())
                except ValueError as e:
                    messagebox.showerror("에러 발생", str(e) + "\n파일명: " + path)
                    return

                for className, lastTag, tag, text in extracts:
                    try:
                        dict_class[className].append((lastTag, tag, text))
                    except KeyError:
                        dict_class[className] = [(lastTag, tag, text)]
                    if type(text) == list:
                        text = WORD_NEWLINE.join(text)
                    try:
                        dict_tags_text[lastTag].append(text)
                    except KeyError:
                        dict_tags_text[lastTag] = [text]
        else:
            messagebox.showerror("에러 발생", "Patches 등 Defs 이외의 모든 폴더는 아직 추출할 수 없습니다.\n자동으로 제외합니다.")
    if dict_tags_text == {}:
        messagebox.showerror("에러 발생", "추출 가능한 xml가 존재하지 않거나, 찾을 수 없습니다. 프로그램을 종료합니다.")
        window.destroy()

    def showTexts(evt):
        w = evt.widget
        tag = w.get(int(w.curselection()[0]))
        # messagebox.showinfo(tag,'\n'.join(dict_tags_text[tag]))
        dialog = Toplevel(window)
        dialog.title(tag)
        text = Text(dialog)
        text.insert(1.0, '\n'.join(sorted(list(set(dict_tags_text[tag])))))
        text.configure(state='disabled')
        text.bind("<Escape>", lambda x: dialog.destroy())
        text.bind("<q>", lambda x: moveTag(tag, 0, diag=dialog))
        text.bind("<w>", lambda x: moveTag(tag, 1, diag=dialog))
        text.bind("<e>", lambda x: moveTag(tag, 2, diag=dialog))
        text.focus_set()
        Grid.rowconfigure(dialog, 0, weight=1)
        Grid.columnconfigure(dialog, 0, weight=1)
        text.grid(row=0, column=0, sticky=N + S + E + W)

    excludes = []
    defaults = sorted(dict_tags_text.keys())
    includes = []

    while True:
        candidate = defaults.pop(0)
        try:
            int(candidate)
            excludes.append(candidate)
        except Exception:
            defaults.insert(0, candidate)
            break

    for _ in range(len(defaults)):
        candidate = defaults.pop(0)
        if candidate in definedExcludes:
            excludes.append(candidate)
        elif candidate in definedIncludes:
            includes.append(candidate)
        else:
            defaults.append(candidate)

    Label(frame, text="추출 제외 태그").grid(row=0, column=0, sticky=N + S + E + W)
    excludeVar = StringVar(value=excludes)
    excludeList = Listbox(frame, listvariable=excludeVar)
    excludeList.grid(row=1, column=0, sticky=N + S + E + W)
    excludeList.bind("<w>", lambda x: moveTag(excludeList.get(excludeList.curselection()[0]), 1))
    excludeList.bind("<e>", lambda x: moveTag(excludeList.get(excludeList.curselection()[0]), 2))

    Label(frame, text="미분류 태그\n(추출 제외)").grid(row=0, column=1, sticky=N + S + E + W)
    defaultVar = StringVar(value=defaults)
    defaultList = Listbox(frame, listvariable=defaultVar)
    defaultList.grid(row=1, column=1, sticky=N + S + E + W)
    defaultList.bind("<q>", lambda x: moveTag(defaultList.get(defaultList.curselection()[0]), 0))
    defaultList.bind("<e>", lambda x: moveTag(defaultList.get(defaultList.curselection()[0]), 2))

    Label(frame, text="추출 대상 태그").grid(row=0, column=2, sticky=N + S + E + W)
    includeVar = StringVar(value=includes)
    includeList = Listbox(frame, listvariable=includeVar)
    includeList.grid(row=1, column=2, sticky=N + S + E + W)
    includeList.bind("<q>", lambda x: moveTag(includeList.get(includeList.curselection()[0]), 0))
    includeList.bind("<w>", lambda x: moveTag(includeList.get(includeList.curselection()[0]), 1))

    def moveTag(tag, destination, diag=None):
        if diag: diag.destroy()
        try:
            toMove = defaults.pop(defaults.index(tag))
            if destination == 1: return
            if defaultList.get(END) == toMove:
                defaultList.activate(defaultList.size() - 2)
                defaultList.selection_set(defaultList.size() - 2)
        except ValueError:
            try:
                toMove = excludes.pop(excludes.index(tag))
                if destination == 0: return
                if excludeList.get(END) == toMove:
                    excludeList.activate(excludeList.size() - 2)
                    excludeList.selection_set(excludeList.size() - 2)
            except ValueError:
                try:
                    toMove = includes.pop(includes.index(tag))
                    if destination == 2: return
                    if includeList.get(END) == toMove:
                        includeList.activate(includeList.size() - 2)
                        includeList.selection_set(includeList.size() - 2)
                except ValueError:
                    return

        [excludes, defaults, includes][destination].append(toMove)

        excludeVar.set(sorted(excludes))
        defaultVar.set(sorted(defaults))
        includeVar.set(sorted(includes))

        if destination == 0:
            for i, v in enumerate(excludeList.get(0, END)):
                if v == toMove:
                    break
            excludeList.see(i)
        elif destination == 0:
            for i, v in enumerate(defaultList.get(0, END)):
                if v == toMove:
                    break
            defaultList.see(i)
        elif destination == 0:
            for i, v in enumerate(includeList.get(0, END)):
                if v == toMove:
                    break
            includeList.see(i)

    excludeList.bind('<Double-Button-1>', showTexts)
    defaultList.bind('<Double-Button-1>', showTexts)
    includeList.bind('<Double-Button-1>', showTexts)

    def onSelect(evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)

    Label(frame, text="[Q]를 입력해 추출 제외").grid(row=2, column=0)
    Label(frame, text="[W]를 입력해 분류 취소").grid(row=2, column=1)
    Label(frame, text="[E]를 입력해 추출 추가").grid(row=2, column=2)

    searchTag = EntryHint(frame, "[태그 필터]")
    searchTag.grid(row=3, column=0, sticky=E + W)
    searchText = EntryHint(frame, "[원본 텍스트 필터]")
    searchText.grid(row=3, column=1, columnspan=2, sticky=E + W)

    dictTextTag = {}
    for tag, texts in dict_tags_text.items():
        for text in texts:
            try:
                dictTextTag[text].append(tag)
            except KeyError:
                dictTextTag[text] = [tag]

    def onSearch(evt):
        global excludes, defaults, includes, excludeHide, defaultHide, includeHide
        tagSearch = searchTag.get()
        tagFlag = (tagSearch != "")
        textSearch = searchText.get()
        textFlag = (textSearch != "")

        excludes = excludes + excludeHide
        defaults = defaults + defaultHide
        includes = includes + includeHide

        filteredTags = []
        if textFlag:
            for tags in [dictTextTag[text] for text in dictTextTag.keys() if textSearch in text]:
                filteredTags.extend(tags)
            if tagFlag:
                filteredTags = [tag for tag in list(set(filteredTags)) if tagSearch in tag]
        elif tagFlag:
            filteredTags = [tag for tag in dict_tags_text.keys() if tagSearch in tag]

        if textFlag or tagFlag:
            excludeIntersect = list(set(excludes) & set(filteredTags))
            excludeHide = [tag for tag in excludes if not tag in excludeIntersect]
            excludes = excludeIntersect
            defaultIntersect = list(set(defaults) & set(filteredTags))
            defaultHide = [tag for tag in defaults if not tag in defaultIntersect]
            defaults = defaultIntersect
            includeIntersect = list(set(includes) & set(filteredTags))
            includeHide = [tag for tag in includes if not tag in includeIntersect]
            includes = includeIntersect
        else:
            excludeHide = []
            defaultHide = []
            includeHide = []

        excludeVar.set(sorted(excludes))
        defaultVar.set(sorted(defaults))
        includeVar.set(sorted(includes))

    searchTag.bind("<KeyRelease>", onSearch)
    searchText.bind("<KeyRelease>", onSearch)

    def finishTag():
        frame.destroy()
        loadSelectExport(window)

    Button(frame, text="태그 선택 완료", command=finishTag).grid(row=4, column=1)


def loadSelectExport(window):
    global includes

    frame = Frame(window)
    frame.grid(row=0, column=0, sticky=N + S + E + W)

    for i in range(8):
        Grid.rowconfigure(frame, i, weight=1)
    for i in range(1):
        Grid.columnconfigure(frame, i, weight=1)

    varDirName = StringVar(value=exportDir)
    varFileName = StringVar(value=exportFile)
    varIsNameTODO = BooleanVar(value=isNameTODO)
    varCollisionOption = IntVar(value=collisionOption)

    Label(frame, text="결과 폴더 이름 지정").grid(row=0, column=0)
    Entry(frame, textvariable=varDirName).grid(row=1, column=0, sticky=E + W)

    Label(frame, text="결과 파일 이름 지정, [.xml]을 끝에 붙일 것").grid(row=2, column=0)
    Entry(frame, textvariable=varFileName).grid(row=3, column=0, sticky=E + W)

    Label(frame, text="번역해야 할 부분의 텍스트 지정").grid(row=4, column=0)
    row5Frame = Frame(frame)
    row5Frame.grid(row=5, column=0)
    Radiobutton(row5Frame, text="TODO", value=True, variable=varIsNameTODO).grid(row=0, column=0)
    Radiobutton(row5Frame, text="원문", value=False, variable=varIsNameTODO).grid(row=0, column=1)

    Label(frame, text="결과 폴더와 파일명이 일치할 경우 파일의 작업 방법").grid(row=6, column=0)
    row7Frame = Frame(frame)
    row7Frame.grid(row=7, column=0)
    radioButtons = []
    btnTexts = ["중단하기", "덮어쓰기", "병합하기", "참조하기"]
    tooltips = ["파일 충돌이 발생할 경우, 파일 출력을 중단하고 알림을 표시합니다. 이 경우, 파일 충돌이 발생할 때까지 작성된 파일은 남아 있음에 유의하십시오.",
                "파일 충돌이 발생할 경우, 해당 파일을 내용을 삭제하고 새로 작성합니다. 이 경우, 기존 파일을 복구할 수 없으므로 사전 백업이 권장됩니다.",
                "파일 충돌이 발생할 경우, 해당 파일에 새로운 태그들을 추가해 병합합니다. 추출기가 추출하지 않았지만 존재했던 내용은 파일의 하단에 출력됩니다.",
                "파일 충돌이 발생할 경우, 해당 파일의 내용을 새로 작성하되, 기존 파일에 같은 태그가 있을 경우 해당 내용을 보존합니다. 추출기가 추출하지 않았지만 존재했던 내용은 버려집니다."]
    for i, (text, tooltip) in enumerate(zip(btnTexts, tooltips)):
        tmp = Radiobutton(row7Frame, text=text, value=i, variable=varCollisionOption)
        CreateToolTip(tmp, tooltip)
        tmp.grid(row=0, column=i)

    def exportXml():
        savedList = []
        for className, values in dict_class.items():
            isThereNoIncludes = True
            for lastTag, _, _ in values:  # check existence of include tag
                if lastTag in includes:
                    isThereNoIncludes = False
                    break
            if isThereNoIncludes:
                continue  # pass the class

            filename = varDirName.get() + '/DefInjected/' + className + '/' + varFileName.get()
            Path('/'.join((filename).split('/')[:-1])).mkdir(parents=True, exist_ok=True)

            if varCollisionOption.get() == 0:  # collision -> stop
                try:
                    with open(filename, 'r', encoding='UTF8') as fin:
                        messagebox.showerror("파일 충돌 발견됨",
                                             f"다음 폴더의 파일이 존재하여 작업을 중단하였습니다.\n{className}\n\n이미 저장된 파일의 폴더 리스트는 아래와 같습니다.\n{WORD_NEWLINE.join(savedList)}")
                        return
                except FileNotFoundError:
                    pass

            residueList = ["\n\n  <!-- 알파의 추출기는 추출하지 않았지만 이미 존재했던 노드들 -->\n\n"]
            alreadyDefinedDict = {}
            if varCollisionOption.get() > 1:  # collision -> merge/refer
                try:
                    for node in list(et.parse(filename).getroot()):
                        if list(node):
                            alreadyDefinedDict[node.tag] = [li.text for li in list(node)]
                        else:
                            alreadyDefinedDict[node.tag] = node.text
                except FileNotFoundError:
                    pass

            writingTextList = []
            for lastTag, tag, text in values:
                if lastTag in includes:
                    if type(text) == list:
                        try:
                            for i, v in enumerate(alreadyDefinedDict[tag]):
                                text[i] = alreadyDefinedDict[tag][i]
                            del alreadyDefinedDict[tag]
                        except:
                            pass
                        writingTextList.append(f"  <!-- ALPHA:LIST TYPE EXTRACTS -->\n  <{tag}>\n{WORD_NEWLINE.join([f'    <!-- {text_i} -->{WORD_NEWLINE}    <li>TODO</li>' for text_i in text])}\n  </{tag}>"
                                               if varIsNameTODO.get()
                                               else f"  <{tag}>\n{WORD_NEWLINE.join([f'    <li>{text_i}</li>' for text_i in text])}\n  </{tag}>")
                    else:
                        try:
                            writingTextList.append(f"  <!-- {text} -->\n  <{tag}>{alreadyDefinedDict[tag]}</{tag}>"
                                                   if varIsNameTODO.get()
                                                   else f"  <{tag}>{alreadyDefinedDict[tag]}</{tag}>")
                            del alreadyDefinedDict[tag]
                        except KeyError:
                            writingTextList.append(f"  <!-- {text} -->\n  <{tag}>TODO</{tag}>"
                                                   if varIsNameTODO.get()
                                                   else f"  <{tag}>{text}</{tag}>")

            with open(filename, 'w', encoding='UTF8') as fin:
                fin.write("""<?xml version="1.0" encoding="utf-8"?>\n<LanguageData>\n""")
                fin.write('\n'.join(writingTextList))
                if varCollisionOption.get() == 3 and len(residueList) > 1:  # collision -> refer
                    fin.write('\n'.join(residueList))
                fin.write("\n</LanguageData>")

            savedList.append(className)

        writeConfig(new_exportDir=varDirName.get(), new_exportFile=varFileName.get(),
                    new_isNameTODO=varIsNameTODO.get(), new_collisionOption=varCollisionOption.get())

        messagebox.showinfo("퍼일 저장 완료",
                            "작업이 완료되었습니다.\n새로 작성되거나 변경된 파일의 폴더 리스트는 아래와 같습니다.\n{}".format("\n".join(savedList)))

    Button(frame, text="추출하기", command=exportXml).grid(row=8, column=0)


if __name__ == '__main__':
    easterEgg = 0

    goExtractList = []

    excludes = []
    defaults = []
    includes = []

    excludeHide = []
    defaultHide = []
    includeHide = []

    dict_class = {}

    window = Tk()
    window.title("Alpha의 림월드 모드 언어 추출기")
    window.geometry("640x400+100+100")
    Grid.rowconfigure(window, 0, weight=1)
    Grid.columnconfigure(window, 0, weight=1)

    try:
        modDir, definedExcludes, definedIncludes, exportDir, exportFile, isNameTODO, collisionOption = loadConfig()
    except Exception:
        writeConfig()
        modDir, definedExcludes, definedIncludes, exportDir, exportFile, isNameTODO, collisionOption = loadConfig()

    loadInit(window)

    window.mainloop()

import math
import random
import IlnessBase
import copy
import pdb
import datetime

from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '500')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout 
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

fps = 60

class FullApp(FloatLayout):

    def __init__(self, **kwargs):
        super(FullApp, self).__init__(**kwargs)
        
        self.username = 'Sample User'
        self.notes = []#{'type':'request','undertype':'ser','state':'inprogress','name':'Dup Anal','idnum':int(random.random()*10000),'date':'23:40 17.03.2017'}]
        self.state = "loading"
        global loadingscreen
        loadingscreen = LoadingScreen()
        self.add_widget(loadingscreen)


    def AppLoop(self,dt):
        Window.size = (random.random()*0.0000000000001+300,random.random()*0.0000000000001+500)

        if(self.state == "loading"):
            Clock.schedule_once(self.children[0].updateSmallLoadingText, len(self.children[0].SmallLoadingTexts[self.children[0].SmallCurrentLoadingText])*self.children[0].SmallTextRatio)
        
        elif(self.state == 'IlnessSearch'):
            global ilnesssearch
            for i in range(len(ilnesssearch.QuestionList)):
                if (ilnesssearch.QuestionList[i].chagingopacity != 0):
                    ilnesssearch.QuestionList[i].opacity += ilnesssearch.QuestionList[i].opacitypace*ilnesssearch.QuestionList[i].chagingopacity
                    if(ilnesssearch.QuestionList[i].opacity >= 1):
                        ilnesssearch.QuestionList[i].opacity = 1
                        ilnesssearch.QuestionList[i].chagingopacity = 0
                    if(ilnesssearch.QuestionList[i].opacity <= 0):
                        ilnesssearch.QuestionList[i].opacity = 0
                        ilnesssearch.QuestionList[i].chagingopacity = 0
                        ilnesssearch.HitList.append(ilnesssearch.QuestionList[i].CurNum)

            for i in ilnesssearch.HitList: 
                SentencedToDeathNum = ilnesssearch.get_by_CurNum(i)                                  
                for j in range(SentencedToDeathNum,len(ilnesssearch.QuestionList)):
                    ilnesssearch.QuestionList[j].rect.pos = [ilnesssearch.QuestionList[j].rect.pos[0],ilnesssearch.QuestionList[j].rect.pos[1]+ilnesssearch.spacing[1] + ilnesssearch.unitheight]       
                    ilnesssearch.QuestionList[j].bluelinerect.pos = (ilnesssearch.QuestionList[j].bluelinerect.pos[0],ilnesssearch.QuestionList[j].bluelinerect.pos[1]+ilnesssearch.spacing[1] + ilnesssearch.unitheight)  
               
                ilnesssearch.remove_widget(ilnesssearch.QuestionList[SentencedToDeathNum])
                ilnesssearch.QuestionList.pop(SentencedToDeathNum)
                ilnesssearch.HitList.remove(i)
                break

            Clock.schedule_once(self.AppLoop,1/fps)

        elif(self.state == 'menu'):
            Clock.schedule_once(self.AppLoop,1/fps)  

        elif(self.state == 'lit'):
            Clock.schedule_once(self.AppLoop,1/fps)

        elif(self.state == 'medicine'):
            if(len(medicine.active_checkboxes) > 0):
                medicine.SomeWidget.opacity=1
            else:
                medicine.SomeWidget.opacity=0
            Clock.schedule_once(self.AppLoop,1/fps)
    

    def clear(self):
        self.clear_widgets()

    def create_service(self):
        global service
        self.clear()
        service = Service()
        fullapp.add_widget(service)
        fullapp.state = 'service'

    def create_literature(self):
        self.clear()
        global literature 
        literature = Literature()
        fullapp.add_widget(literature)
        fullapp.state = 'lit'

    def create_medicine(self):
        self.clear()
        global medicine
        medicine = Medicine()
        fullapp.add_widget(medicine)
        fullapp.state = 'medicine'

    def create_search(self):
        self.clear()
        global ilnesssearch
        ilnesssearch = IlnessSearch()
        scrollview = ScrollView()
        scrollview.add_widget(ilnesssearch)
        BackForScroll = Widget()
        WhiteWidget = Widget()
        FrontForScroll = Widget(size=(fullapp.size[0],fullapp.size[1]*0.236))

        WhiteWidget.canvas.add(Color(1,1,1))
        Whiterect = Rectangle(size=fullapp.size,pos=fullapp.pos)
        WhiteWidget.canvas.add(Whiterect)
        WhiteWidget.opacity = 0.5
        FrontForScroll.canvas.clear()
        FrontForScroll.canvas.add(Color(1,1,1))
        rect = Rectangle(size=fullapp.size,pos=fullapp.pos,source='MainBackground.png')
        BackForScroll.canvas.add(rect)
        BackForScroll.add_widget(WhiteWidget)
        rect = Rectangle(size=FrontForScroll.size,pos=fullapp.pos,source='FrontForScroll.png')
        FrontForScroll.canvas.add(rect)
        ilnesssearch.MenuButton = MenuButton()
    
        fullapp.add_widget(BackForScroll)
        fullapp.add_widget(scrollview)
        fullapp.add_widget(FrontForScroll)
        fullapp.add_widget(ilnesssearch.MenuButton)
        fullapp.add_widget(Widget(size=(100,100),size_hint=(None,None),pos=(100,100)))
        ilnesssearch.add_unit(0)
        fullapp.state = "IlnessSearch"

    def create_menu(self):
        self.clear()
        global menu
        menu = Menu()
        fullapp.add_widget(menu)

    def get_user_name(self):
        return self.username 

class LoadingScreen(Widget):
    SmallLoadingTexts = ['__pycache__','Sprites.zip','150994_blog-6481.jpg','IlnessBase.py','kredit_test_finlajn_karta','tutorial.kv','Preloader_2.gif','complete!']
    SmallCurrentLoadingText = 0
    SmallTextRatio = 0.026

    def updateSmallLoadingText(self,dt):
        if(self.SmallCurrentLoadingText == len(self.SmallLoadingTexts)-1):
            self.ids['SmallFakeText'].text = ""
            loginpopup = LoginPopup()
            global fullapp
            loginpopup.height = fullapp.height * 0.5
            loginpopup.width = fullapp.width * 0.8
            loginpopup.pos = ((fullapp.width-loginpopup.width)/2,(fullapp.height-loginpopup.height)/2)
            self.parent.add_widget(loginpopup)
            self.parent.state = "LoginPopup"

        else:
            self.SmallCurrentLoadingText += 1
            self.ids['SmallFakeText'].text = self.SmallLoadingTexts[self.SmallCurrentLoadingText]
            Clock.schedule_once(self.parent.AppLoop, len(self.SmallLoadingTexts[self.SmallCurrentLoadingText])*self.SmallTextRatio)

class LoginPopup(Popup):
    def __init__(self,**kwargs):
        super(LoginPopup, self).__init__(**kwargs)
    
    def OnButton(self,instance,input):
        global fullapp
        fullapp.remove_widget(loadingscreen)
        fullapp.username = input[0] if(fullapp.state == 'menu' or input[0] != '') else fullapp.username

        fullapp.create_search()
        fullapp.create_medicine()
        fullapp.create_menu()
        Clock.schedule_once(fullapp.AppLoop,1/fps)

class MenuButton(Button):
    def __init__(self, **kwargs):
        super(MenuButton,self).__init__(**kwargs)
        global fullapp
        self.size_hint = (None,None)
        self.size = (fullapp.size[0]*0.4,fullapp.size[1]*0.2)
        self.background_color = (1,1,1,0)
        self.on_press = self.return_menu
        self.pos = (fullapp.size[0]*0.3,0)

    def return_menu(self):
        fullapp.create_menu()

class IlnessSearch(StackLayout):

    def __init__(self, **kwargs):
        super(IlnessSearch, self).__init__(**kwargs)

        self.CurrentQuestionId = 0
        self.INNERPROGRESS = False
        self.size_hint = (None,None)
        self.size = (Window.size[0],10000)
        self.unitwidth = 0.95 * Window.size[0]
        self.unitheight = 0.2 * Window.size[1]
        self.spacing = Window.size[1]*0.02
        self.padding = [7,30,7,10]
        self.toppadding = Window.size[1]*0.03
        self.unitSize = [self.unitwidth,self.unitheight]
        self.QuestionList = list()
        self.QuestionCounter = 0
        self.HitList = []
    
    def add_unit(self,num):
        print('fffffffffff')
        self.QuestionList.append(BoxLayout())
        self.QuestionList[-1].orientation = 'vertical'
        self.QuestionList[-1].size_hint = (None,None)
        self.QuestionList[-1].size = self.unitSize
        self.QuestionList[-1].center_x = self.center_x
        self.QuestionList[-1].canvas.add(Color(0.5,0.5,0.5))
        self.QuestionList[-1].rect = Rectangle(size=self.unitSize,pos=(self.padding[0],self.top-self.padding[1]-len(self.QuestionList)*self.unitheight-(len(self.QuestionList)-1)*self.spacing[1]))
        self.QuestionList[-1].canvas.add(self.QuestionList[-1].rect)
        self.QuestionList[-1].opacity = 0.01
        self.QuestionList[-1].chagingopacity = 1
        self.QuestionList[-1].opacitypace = 2/fps

        BaseElement = self.BaseSearch(num)
        CurNum = str(self.QuestionCounter)
        self.QuestionList[-1].CurNum = self.QuestionCounter
        self.QuestionList[-1].IdInBase = num
        self.QuestionCounter += 1
        TextNumberLabel = Label()
        TextNumberLabel.italic = True
        TextNumberLabel.markup = True
        TextNumberLabel.text = str("[color=292929]Question  [/color]" + CurNum + ".") if BaseElement['isQuest'] else str("Diag")
        TextNumberLabel.color = (0,0,0,0.2) if BaseElement['isQuest'] else (0.5,0,0.08,0.6)
        TextNumberLabel.bold = False if BaseElement['isQuest'] else True
        TextNumberLabel.font_size = Window.size[1]*0.025
        self.QuestionList[-1].TextNumberLabel = TextNumberLabel
        self.QuestionList[-1].add_widget(TextNumberLabel)

        QuestLabel = Label()
        QuestLabel.text = self.BaseSearch(num)['text'] if BaseElement['isQuest'] else '                                                              '+self.BaseSearch(num)['text']
        QuestLabel.color = (1,1,1,0.9)
        QuestLabel.font_size = Window.size[1]*0.03
        QuestLabel.text_size = (self.unitwidth*0.9,None)
        QuestLabel.size_hint_y = 0.9 if BaseElement['isQuest'] else 0.1
        QuestLabel.bold = False if BaseElement['isQuest'] else True
        self.QuestionList[-1].QuestLabel = QuestLabel
        self.QuestionList[-1].add_widget(QuestLabel)

        JustBlueLine = Widget()
        JustBlueLine.size_hint_y = 1 if BaseElement['isQuest'] else 1
        self.QuestionList[-1].bluelinerect = Rectangle(size=(self.unitwidth*0.98,self.unitheight*0.025),pos=(self.padding[0]+self.unitwidth*0.01,self.QuestionList[-1].rect.pos[1]+self.unitheight*0.28))
        JustBlueLine.canvas.add(Color(0.26, 0.63, 0.75))
        JustBlueLine.canvas.add(self.QuestionList[-1].bluelinerect)
        self.QuestionList[-1].JustBlueLine = JustBlueLine
        self.QuestionList[-1].add_widget(JustBlueLine)

        FakeWidget = Widget(size_hint_y = 0.5)
        self.QuestionList[-1].add_widget(FakeWidget)


        if(BaseElement['isQuest'] == True):
            CheckBoxGroup=BoxLayout(size_hint_y=1.4)
            CheckBoxGroup.orientation = "horizontal"
            CheckBoxGroup.id = "checkgroup"
            CheckBoxGroup.IdInBase = num
            CheckBoxYes = CheckBox(group="ilness"+CurNum)
            CheckBoxYes.bind(active=self.MakeChoice)
            CheckBoxYes.type = 'yes'
            CheckBoxNo = CheckBox(group="ilness"+CurNum)
            CheckBoxNo.bind(active=self.MakeChoice)
            CheckBoxNo.type = 'no'
            CheckBoxNotStated = CheckBox(group="ilness"+CurNum)
            CheckBoxNotStated.bind(active=self.MakeChoice)
            CheckBoxNotStated.type = 'notstated'
            CheckBoxFlaseWidget = Widget()  
            CheckBoxGroup.add_widget(CheckBoxYes)
            CheckBoxGroup.add_widget(Label(text="Yes.",color = (1,1,1,0.6),font_size=Window.size[1]*0.026,bold=True,halign='left'))
            CheckBoxGroup.add_widget(copy.copy(CheckBoxFlaseWidget))
            CheckBoxGroup.add_widget(CheckBoxNo)
            CheckBoxGroup.add_widget(Label(text="No.",color = (1,1,1,0.6),font_size=Window.size[1]*0.026,bold=True))
            CheckBoxGroup.add_widget(copy.copy(CheckBoxFlaseWidget))
            CheckBoxGroup.add_widget(CheckBoxNotStated)
            CheckBoxGroup.add_widget(Label(text="NaN",color = (1,1,1,0.5),font_size=Window.size[1]*0.026,bold=False,size_hint_x=2))
            CheckBoxGroup.add_widget(Widget(size_hint_x=0.4))
            self.QuestionList[-1].add_widget(CheckBoxGroup)

        else:
            a = self.unitSize
            ButtonGroup = BoxLayout(orientation='horizontal',spacing=self.unitwidth*0.1,padding=(a[0]*0.05,a[1]*0.05,a[0]*0.05,a[1]*0.05))
            BackToMenu = Button()
            BackToMenu.text = "main"
            BackToMenu.color = (0,0,0,1)
            BackToMenu.font_size = fullapp.size[1]*0.025
            BackToMenu.italic = True
            BackToMenu.on_press = self.MenuButton.return_menu
            RestartSearch = Button()
            RestartSearch.text = 'exit'
            RestartSearch.color = (0,0,0,1)
            RestartSearch.font_size = fullapp.size[1]*0.025
            RestartSearch.italic = True
            RestartSearch.on_press = self.restart

            ButtonGroup.add_widget(BackToMenu)
            ButtonGroup.add_widget(RestartSearch)
            self.QuestionList[-1].add_widget(ButtonGroup)

        self.add_widget(self.QuestionList[-1])

    def return_menu(self):
        fullapp.create_menu()
    def restart(self):
        fullapp.create_search()

    def delete_unit(self,numer):
        self.QuestionList[numer].chagingopacity = -1

    def MakeChoice(self,instance,value):
        instancenum = int(instance.group[6:])
        global ilnesssearch
        for i in range(len(ilnesssearch.QuestionList)):
            try:
                if(ilnesssearch.QuestionList[i].CurNum == instancenum): 
                    CurBaseElement = ilnesssearch.BaseSearch(ilnesssearch.QuestionList[i].children[get_by_id(ilnesssearch.QuestionList[i],'checkgroup')].IdInBase)       
                    if(value == False):
                        ilnesssearch.QuestionList[i].TextNumberLabel.color = ilnesssearch.QuestionList[i].TextNumberLabelold
                        ilnesssearch.QuestionList[i].QuestLabel.color = ilnesssearch.QuestionList[i].QuestLabelold
                        CurCheckGroup = self.QuestionList[self.get_by_CurNum(instancenum)].children[get_by_id(self.QuestionList[self.get_by_CurNum(instancenum)],'checkgroup')]
                        SentencedToDeathList = list(CurBaseElement['neibs'])
                        while(len(SentencedToDeathList) != 0):
                            for i in ilnesssearch.QuestionList:
                                if(i.IdInBase == SentencedToDeathList[0]):
                                    self.delete_unit(self.get_by_CurNum(i.CurNum))
                                    if(self.BaseSearch(i.IdInBase)['isQuest'] == True):
                                        SentencedToDeathList.extend(self.BaseSearch(i.IdInBase)['neibs'])
                            SentencedToDeathList.pop(0)

                    else:
                        ilnesssearch.QuestionList[i].TextNumberLabelold = ilnesssearch.QuestionList[i].TextNumberLabel.color
                        ilnesssearch.QuestionList[i].QuestLabelold = ilnesssearch.QuestionList[i].QuestLabel.color
                        ilnesssearch.QuestionList[i].QuestLabel.color = (0.62,1,0.40,0.4)
                        if(instance.type == "yes"):
                            neibs_for_adding = [copy.copy(CurBaseElement['neibs'][0])]
                            for i in ilnesssearch.QuestionList:
                                if(ilnesssearch.BaseSearch(i.IdInBase)['id'] in neibs_for_adding):
                                    neibs_for_adding.remove(ilnesssearch.BaseSearch(i.IdInBase)['id'])
                                    #i.chagingopacity = 0
                                    #i.opacity = 1
                                    SentencedToDeathList = [copy.copy(CurBaseElement['neibs'][0])]
                                    while(len(SentencedToDeathList) != 0):
                                        #print(SentencedToDeathList)
                                        for j in ilnesssearch.QuestionList:
                                            if(j.IdInBase == SentencedToDeathList[0]):
                                                j.chagingopacity = 0
                                                j.opacity = 1
                                                if(self.BaseSearch(i.IdInBase)['isQuest'] == True):
                                                    SentencedToDeathList.extend(self.BaseSearch(i.IdInBase)['neibs'])
                                        SentencedToDeathList.pop(0)

                            for i in neibs_for_adding:
                                ilnesssearch.add_unit(i)
                        elif(instance.type == 'no'):
                            #ilnesssearch.add_unit(CurBaseElement['neibs'][1])
                            neibs_for_adding = [copy.copy(CurBaseElement['neibs'][1])]
                            print(neibs_for_adding)
                            for i in ilnesssearch.QuestionList:
                                if(ilnesssearch.BaseSearch(i.IdInBase)['id'] in neibs_for_adding):
                                    neibs_for_adding.remove(ilnesssearch.BaseSearch(i.IdInBase)['id'])
                                    SentencedToDeathList = [copy.copy(CurBaseElement['neibs'][1])]
                                    while(len(SentencedToDeathList) != 0):
                                        #print(SentencedToDeathList)
                                        for j in ilnesssearch.QuestionList:
                                            if(j.IdInBase == SentencedToDeathList[0]):
                                                j.chagingopacity = 0
                                                j.opacity = 1
                                                if(self.BaseSearch(i.IdInBase)['isQuest'] == True):
                                                    SentencedToDeathList.extend(self.BaseSearch(i.IdInBase)['neibs'])
                                        SentencedToDeathList.pop(0)

                            for i in neibs_for_adding:
                                ilnesssearch.add_unit(i)

                        elif(instance.type == 'notstated'):
                            neibs_for_adding = copy.copy(CurBaseElement['neibs'])
                            for i in ilnesssearch.QuestionList:
                                if(ilnesssearch.BaseSearch(i.IdInBase)['id'] in neibs_for_adding):
                                    neibs_for_adding.remove(ilnesssearch.BaseSearch(i.IdInBase)['id'])
                                    i.chagingopacity = 0
                                    i.opacity = 1
                                    SentencedToDeathList = list(CurBaseElement['neibs'])
                                    while(len(SentencedToDeathList) != 0):
                                        #print(SentencedToDeathList)
                                        for j in ilnesssearch.QuestionList:
                                            if(j.IdInBase == SentencedToDeathList[0]):
                                                j.chagingopacity = 0
                                                j.opacity = 1
                                                if(self.BaseSearch(i.IdInBase)['isQuest'] == True):
                                                    SentencedToDeathList.extend(self.BaseSearch(i.IdInBase)['neibs'])
                                        SentencedToDeathList.pop(0)

                            for i in neibs_for_adding:
                                ilnesssearch.add_unit(i)
            except:
                pass

    def BaseSearch(self,num):
        for i in IlnessBase.Base:
            if(i['id'] == num):
                return i
        return False

    def get_by_CurNum(self,num):
        for i in range(len(ilnesssearch.QuestionList)):
            if(ilnesssearch.QuestionList[i].CurNum == num):
                return i

def get_by_id(widget,id):
    for i in range(len(widget.children)):
        if(widget.children[i].id==id):
            return i

class Menu(FloatLayout):
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        global fullapp
        self.size = fullapp.size
        self.canvas.add(Color(1,1,1))
        LoginField = Widget()
        LoginField.orientation = 'vertical'
        LoginField.size = (Window.size[0]*0.7,Window.size[1]*0.23)
        LoginField.pos = (Window.size[0]*0.327,Window.size[1]*0.793)
        rect = Rectangle(size = LoginField.size,source = 'LoginWindow.png',pos = LoginField.pos)
        LoginField.canvas.add(rect)

        SomeLabel = Label(text='acc',color=(0,0,0,0.85),font_size=Window.size[1]*0.03,bold=True)
        SomeLabel.pos = (Window.size[0]*0.5,Window.size[1]*0.865)
        NickNameButton = Button(color=(0,0,0,1),font_size=Window.size[1]*0.034,bold=True)
        NickNameButton.pos = (Window.size[0]*0.4,Window.size[1]*0.88)
        NickNameButton.size = (Window.size[0]*0.55,Window.size[1]*0.064)
        NickNameButton.text = fullapp.get_user_name()
        NickNameButton.on_press = self.change_user
        NickNameButton.background_color = (0,0,0,0)

        LoginButton = Button(text = 'Pushers',color=(0.48,0.14,0.165,1),font_size=Window.size[1]*0.03,italic=True)
        LoginButton.background_color = (0,0,0,0)
        LoginButton.pos = (Window.size[0]*0.5,Window.size[1]*0.82)
        LoginButton.size = (Window.size[0]*0.38,Window.size[1]*0.064)
        LoginButton.on_press = self.notify

        LoginField.add_widget(SomeLabel)
        LoginField.add_widget(NickNameButton)
        LoginField.add_widget(LoginButton)
        self.LoginField = LoginField
        self.add_widget(LoginField) 

    def change_user(self):
        global fullapp
        loginpopupmenu = LoginPopup()
        loginpopupmenu.height = fullapp.height * 0.5
        loginpopupmenu.width = fullapp.width * 0.8
        loginpopupmenu.pos = ((fullapp.width-loginpopupmenu.width)/2,(fullapp.height-loginpopupmenu.height)/2)
        self.LoginPopup = loginpopupmenu
        self.add_widget(self.LoginPopup)

    def notify(self):
        def exit(instance):
            self.remove_widget(NotePopup)

        self.scrollsize = fullapp.size[0]*0.8,fullapp.size[1]*0.6
        self.scrollpos = fullapp.size[0]*0.095,fullapp.size[1]*0.185
        self.size_of_note = (self.scrollsize[0],fullapp.size[1]*0.25)

        NotePopup = Popup(size_hint=(None,None),size=(fullapp.size[0]*0.9,fullapp.size[1]*0.8))
        NotePopup.pos = (fullapp.size[0]/2 - NotePopup.size[0]/2,fullapp.size[1]/2 - NotePopup.size[1]/2)
        NotePopup.title = 'view pushers.'
        NotePopup.title_align = 'center'
        NotePopup.separator_color = (0.3,0.3,1,1)
        NotePopup.title_size = fullapp.size[1]*0.03

        NoteScroll = ScrollView()
        NoteScroll.size_hint = (None,None)
        NoteScroll.size = self.scrollsize
        NoteScroll.pos =self.scrollpos

        NoteBox = Widget()
        NoteBox.size_of_note = self.size_of_note
        NoteBox.spacing = fullapp.size[1]*0.006
        NoteBox.size = (self.scrollsize[0],(NoteBox.spacing+NoteBox.size_of_note[1])*len(fullapp.notes)-NoteBox.spacing)
        NoteBox.size_hint_y = None

        for i in range(len(fullapp.notes)):
            b = Button(size=self.size_of_note,pos=(-2,i*(NoteBox.spacing+NoteBox.size_of_note[1])))
            
            if(fullapp.notes[i]['type'] == 'request'):
                b.add_widget(Label(markup=True,text='[color=cccccc]'+'ok request number '+ '[b][/color]' + str(fullapp.notes[i]['idnum']) + '[/b]',font_size=fullapp.size[1]*0.03,color=(1,1,1,1),pos=(fullapp.size[0]*0.19,fullapp.size[1]*0.126+i*(NoteBox.spacing+NoteBox.size_of_note[1]))))
                if(fullapp.notes[i]['undertype']=='med'):
                    preparate =  IlnessBase.Medicine[fullapp.notes[i]['idinIlnessBase']]
                    print(preparate)
                    b.add_widget(Label(text_size=(self.size_of_note[0]*0.97,self.size_of_note[1]*0.7),markup=True,text='to adding preparate '+ '[b][i]' + preparate[:preparate.find(':')]\
                         + '[/b][/i]'+' seems ' + '[b][i]' + preparate[preparate.find(':')+1:] + '[/b][/i]'+' by systemATX.',font_size=fullapp.size[1]*0.03,color=(1,1,1,1),pos=(fullapp.size[0]*0.244,fullapp.size[1]*0.086+i*(NoteBox.spacing+NoteBox.size_of_note[1]))))
                    
                    if(fullapp.notes[i]['state']=='inprogress'):
                        b.add_widget(Label(text='[color=cccccc]Poss: [/color][b][color=adaddf]cheking[/color][b]',font_size=fullapp.size[1]*0.03,markup=True,pos=(fullapp.size[0]*0.184,-fullapp.size[1]*0.046+i*(NoteBox.spacing+NoteBox.size_of_note[1]))))

                    b.add_widget(Label(text='[color=353535]from '+ fullapp.notes[i]['date'],markup=True,font_size=fullapp.size[1]*0.025,pos=(fullapp.size[0]*0.384,-fullapp.size[1]*0.076+i*(NoteBox.spacing+NoteBox.size_of_note[1]))))
                
                elif(fullapp.notes[i]['undertype']=='ser'):
                    service =  fullapp.notes[i]['name']
                    print(service)
                    b.add_widget(Label(text_size=(self.size_of_note[0],self.size_of_note[1]*0.7),markup=True,text='To add new usluga '+ '[b][i]' + service\
                         + '[/b][/i]'+ '[/b][/i]'+'.   Check info to usluga.',font_size=fullapp.size[1]*0.03,color=(1,1,1,1),pos=(fullapp.size[0]*0.244,fullapp.size[1]*0.056+i*(NoteBox.spacing+NoteBox.size_of_note[1]))))
                    
                    if(fullapp.notes[i]['state']=='inprogress'):
                        b.add_widget(Label(text='[color=cccccc]Statust: [/color][b][color=adaddf]checking[/color][b]',font_size=fullapp.size[1]*0.03,markup=True,pos=(fullapp.size[0]*0.184,-fullapp.size[1]*0.046+i*(NoteBox.spacing+NoteBox.size_of_note[1]))))

                    b.add_widget(Label(text='[color=353535]from '+ fullapp.notes[i]['date'],markup=True,font_size=fullapp.size[1]*0.025,pos=(fullapp.size[0]*0.384,-fullapp.size[1]*0.076+i*(NoteBox.spacing+NoteBox.size_of_note[1]))))
            
            NoteBox.add_widget(b)

        DefendWidget = Widget(size=fullapp.size,pos=fullapp.pos,size_hint=(None,None))
        NoteScroll.add_widget(NoteBox)
        DefendWidget.add_widget(NoteScroll)
        DefendWidget.add_widget(Button(size_hint=(None,None),pos=(fullapp.size[0]*0.11,fullapp.size[1]*0.13),size=(25,25),background_normal='47.png',on_press=exit))
        if(len(fullapp.notes)==0):
            DefendWidget.add_widget(Label(text='Non pushers',pos=(self.scrollpos[0]+self.scrollsize[0]/3.6,self.scrollpos[1]+self.scrollsize[1]/2),font_size=fullapp.size[1]*0.04))
        else:
            DefendWidget.add_widget(Label(text_size=(fullapp.size[0]*0.7,100),text='[color=010101]view in [b] http://www.sechenovclinic.ru/[/color][/b]',font_size=fullapp.size[1]*0.02,pos=(self.scrollpos[0]+self.scrollsize[0]/2.7,self.scrollpos[1]-fullapp.size[1]*0.047),markup=True))
        NotePopup.add_widget(DefendWidget)
        self.add_widget(NotePopup)

    def on_service(self):
        fullapp.create_service()

    def on_lit(self):
        fullapp.create_literature()

    def on_med(self):
        fullapp.create_medicine()

    def on_search(self):
        fullapp.create_search()

class ScrollableLabel(ScrollView):
    pass

class Literature(FloatLayout):
    def __init__(self, **kwargs):
        super(Literature, self).__init__(**kwargs)

        global fullapp,LitScroll
        self.canvas.add(Rectangle(size=fullapp.size,pos=fullapp.pos,source="MainBackgroundWhiter.png"))
        self.add_widget(MenuButton())
        rect = Rectangle(size=(fullapp.size[0],fullapp.size[1]*0.236),pos=fullapp.pos,source='FrontForScroll.png')
        self.canvas.add(rect)

        self.scrollsize = fullapp.size[0]*0.86,fullapp.size[1]*0.6
        self.scrollpos = fullapp.size[0]*0.07,fullapp.size[1]*0.27
        self.libra = IlnessBase.Literature
        self.opened_divisions = [0 for i in range(len(self.libra.keys())+6)]

        LitScroll = ScrollView()
        LitScroll.size_hint = (None,None)
        LitScroll.pos = self.scrollpos
        LitScroll.size = self.scrollsize
        LitScroll.add_widget(self.create_literature())
        self.add_widget(LitScroll)
        self.add_widget(Label(text = '[color=000033]'+'litra.'+'[/color]',bold= True,font_size = fullapp.size[1]*0.038,pos=(0,fullapp.size[1]*0.44),markup = True))#,pos = (fullapp.size[0]*0.3,fullapp.size[1]*0.8)))


    def create_literature(self):
        global fullapp,butsize,chartsize,spacing
        butsize = (self.scrollsize[0],fullapp.size[1]*0.1)
        spacing = fullapp.size[1]*0.03
        chartsize = (fullapp.size[0]*0.68,fullapp.size[1]*0.1)
        symbols_to_fill = 50
        
        image = Widget()
        image.size = (fullapp.size[0]*0.68,self.find_height(len(self.opened_divisions))+self.find_chartsize(self.opened_divisions[-1])[1]*self.opened_divisions[-1])
        image.size_hint_y = None

        for i in range(len(self.opened_divisions)):

            CurBaseElement = copy.copy(IlnessBase.Literature[IlnessBase.LiteratureKeys[i]])
            CurSource = 'ButtonForLiterature.png' if (self.opened_divisions[i] == 0) else 'ButtonForLiteratureClicked.png'
            image.canvas.add(Rectangle(size = butsize,pos = (0,image.size[1] - self.find_height(i+1)),source = CurSource))
            label = Label(text = '[color=ffffff]'+str(IlnessBase.LiteratureKeys[i])+'[/color]', markup = True, bold =True, italic = True, font_size = fullapp.size[1]*0.04)
            label.text_size=butsize
            label.halign = 'left'
            label.pos = (fullapp.size[0]*0.32,image.size[1] - self.find_height(i+1) - fullapp.size[1]*0.02)
            image.add_widget(label)

            button = Button(size = butsize,pos = (0,image.size[1] - self.find_height(i+1)),background_color = (1,1,1,0))
            button.num = i
            button.bind(on_press = self.on_button)
            image.add_widget(button)

            if(self.opened_divisions[i] == 1):
                rectpos =  (fullapp.size[0]*0.13,image.size[1] - self.find_height(i+1) - self.find_chartsize(i)[1])
                image.canvas.add(Rectangle(size = self.find_chartsize(i),pos = rectpos,source = 'GreySquare.png'))
                for j in range(len(CurBaseElement)):
                    if(len(CurBaseElement[j]) < symbols_to_fill/1.4):
                        CurBaseElement[j] = CurBaseElement[j][:CurBaseElement[j].find(':')] + ':' +' '*20 + CurBaseElement[j][CurBaseElement[j].find(':')+1:]

                    ChartLabel = Label(text='* ' + CurBaseElement[j][:CurBaseElement[j].find(':')] + '[i]'+CurBaseElement[j][CurBaseElement[j].find(':'):] + '[/i]',
                        text_size = (chartsize[0]*1,chartsize[1]),font_size=chartsize[1]/3.36,markup = True,color = (0.17,0.17,0.17,1),
                        pos = (chartsize[0]/2-fullapp.size[0]*0.017,image.size[1] - self.find_height(i+1)-chartsize[1]*(j+1.4)))
                    image.add_widget(ChartLabel)
        return image

    def find_chartsize(self,num):
        print(len(IlnessBase.Literature[IlnessBase.LiteratureKeys[num]]))
        return (chartsize[0],chartsize[1]*(-1)+chartsize[1]*(len(IlnessBase.Literature[IlnessBase.LiteratureKeys[num]])+1))

    def find_height(self,num):
        result = 0
        for i in range(num):
            result += butsize[1]
            result += spacing if i > 0 else 0
            if (i > 0 and self.opened_divisions[i-1] == 1):
                result += self.find_chartsize(i-1)[1]
            print(i,self.opened_divisions[i])

        return result

    def on_button(self,instance):
        literature.opened_divisions[instance.num] = not literature.opened_divisions[instance.num]
        LitScroll.remove_widget(LitScroll.children[0])
        LitScroll.add_widget(self.create_literature())

class Service(FloatLayout):
    def __init__(self,**kwargs):
        super(Service,self).__init__(**kwargs)
        widget = Widget()
        rect = Rectangle(size=fullapp.size,pos=fullapp.pos,source="MainBackgroundWhiter.png")
        widget.canvas.add(rect)
        self.add_widget(widget)
        self.add_widget(MenuButton())
        rect = Rectangle(size=(fullapp.size[0],fullapp.size[1]*0.236),pos=fullapp.pos,source='FrontForScroll.png')
        self.canvas.add(rect)

        leftedge = fullapp.size[0]*0.1
        self.add_widget(Label(size_hint=(None,None),text='[color=00002c]Search in spis:[/color]',markup=True,halign='center',font_size=fullapp.size[1]*0.045,text_size=(fullapp.size[0]*0.9,fullapp.size[1]*0.2),pos=(fullapp.size[0]*0.33,fullapp.size[1]*0.87)))
        analisys = Button(size_hint=(None,None),background_normal= 'BlueButton.png',background_down = 'BlueButtonDark.png',pos=(leftedge,fullapp.size[1]*0.7),size=(fullapp.size[0]-leftedge*2,fullapp.size[1]*0.1), text='[b][color=1f1f1f]Dup anal',markup=True,font_size=fullapp.size[1]*0.04)
        analisys.bind(on_press=self.on_choose)
        self.add_widget(analisys)
        research = Button(size_hint=(None,None),background_normal= 'BlueButton.png',background_down = 'BlueButtonDark.png',pos=(leftedge,fullapp.size[1]*0.55),size=(fullapp.size[0]-leftedge*2,fullapp.size[1]*0.1), text='[b][color=1f1f1f]Prof obsledov',markup=True,font_size=fullapp.size[1]*0.04)
        research.bind(on_press=self.on_choose)
        self.add_widget(research)
        cons = Button(size_hint=(None,None),background_normal= 'BlueButton.png',background_down = 'BlueButtonDark.png',pos=(leftedge,fullapp.size[1]*0.4),size=(fullapp.size[0]-leftedge*2,fullapp.size[1]*0.1), text='[b][color=1f1f1f]Consalting',markup=True,font_size=fullapp.size[1]*0.04)
        cons.bind(on_press=self.on_choose)
        self.add_widget(cons)

    def on_choose(self,instance):
        self.add_widget(self.create_Popup(instance))

    def create_Popup(self,instance):
        def close(instance):
            self.remove_widget(nowPopup)

        date = datetime.datetime.now()
        strdate = ''
        if(date.hour<10):
            strdate = '0'+str(date.hour)+':'
        else:
            strdate = str(date.hour)+":"
        if(date.minute<10):
            strdate += '0'+str(date.minute)+' '
        else:
            strdate += str(date.minute)+" "
        if(date.day<10):
            strdate += '0'+str(date.day)+'.'
        else:
            strdate += str(date.day)+"."
        if(date.month<10):
            strdate += '0'+str(date.month)+'.'
        else:
            strdate += str(date.month)+"."
        strdate+=str(date.year)

        instancetext = instance.text[17:]
        fullapp.notes.append({'type':'request','undertype':'ser','state':'inprogress','name':instancetext,'idnum':int(random.random()*10000),'date':strdate})
        nowPopup = Popup(size_hint = (None,None),size = (fullapp.size[0]*0.94,fullapp.size[1]*0.45),pos = (fullapp.size[0]*0.03,fullapp.size[1]*0.3))
        nowPopupContent = Widget(size_hint=(None,None),pos=fullapp.pos,size=fullapp.size)
        nowPopupContent.add_widget(Button(pos=nowPopup.pos,size=nowPopup.size,background_color=(1,1,1,0),on_press=close))
        nowPopup.title = 'Requaets is dowload.'
        nowPopup.title_align = 'center'
        nowPopup.title_size = fullapp.size[1]*0.035
        nowLabel = Label(markup=True,font_size=fullapp.size[1]*0.03,text_size=(nowPopup.size[0]*0.9,nowPopup.size[1]-nowPopup.title_size),size_hint=(None,None),pos=(nowPopup.pos[0]+nowPopup.size[0]/3.2,nowPopup.pos[1]+nowPopup.size[1]/2.5-nowPopup.title_size*1.5))
        nowLabel.text = '[color=a9a9a9]' + ' ' + '[/color][i]' + instancetext  + '[/color][/i][color=a9a9a9]' + '  ' + '[i]' + '' \
            + '[/i]' + ' ' + '[i]' + 'Pushers.' + '[/i]' 
        nowPopupContent.add_widget(nowLabel)
        nowPopup.add_widget(nowPopupContent)
        return nowPopup

class Medicine(FloatLayout):

    def __init__(self,**kwargs):
        super(Medicine,self).__init__(**kwargs)
        self.active_checkboxes = []
        self.checkboxeslist = []
        self.scrollsize = fullapp.size[0]*0.86,fullapp.size[1]*0.57
        self.scrollpos = fullapp.size[0]*0.07,fullapp.size[1]*0.34

        self.canvas.add(Rectangle(size=fullapp.size,pos=fullapp.pos,source="MainBackgroundWhiter.png"))
        self.add_widget(MenuButton())
        rect = Rectangle(size=(fullapp.size[0],fullapp.size[1]*0.236),pos=fullapp.pos,source='FrontForScroll.png')
        self.canvas.add(rect)
        self.canvas.add(Color(0.5,0.5,0.5,1))
        self.canvas.add(Rectangle(size=self.scrollsize,pos=self.scrollpos))

        MedScroll = ScrollView()
        MedScroll.size_hint = (None,None)
        MedScroll.size = self.scrollsize
        MedScroll.pos = self.scrollpos

        MedBox = Widget()
        MedBox.size_of_drug = (self.scrollsize[0],fullapp.size[1]*0.1)
        MedBox.spacing = fullapp.size[1]*0.01
        MedBox.size = (self.scrollsize[0],(MedBox.spacing+MedBox.size_of_drug[1])*len(IlnessBase.Medicine)-MedBox.spacing)
        MedBox.size_hint_y = None

        for i in range(len(IlnessBase.Medicine)):
            text = Label(color=(1,1,1,1),markup=True)
            text.text = IlnessBase.Medicine[i][:IlnessBase.Medicine[i].find(':')] + '  ' + '[i][size=11][color=272727]' + 'ATX num ' + IlnessBase.Medicine[i][IlnessBase.Medicine[i].find(':')+1:] + '[/i][/size][/color]'
            text.text_size = MedBox.size_of_drug
            text.text_size[0] -= MedBox.size_of_drug[1]
            text.halign = 'left'
            text.valign = 'middle'
            text.pos = (MedBox.size_of_drug[0]/4.3,i*(MedBox.spacing+MedBox.size_of_drug[1])-MedBox.size_of_drug[1]/2)
            b = Button(size=MedBox.size_of_drug,pos=(0,i*(MedBox.spacing+MedBox.size_of_drug[1])))
            b.bind(on_press=self.on_button)
            b.add_widget(text)
            checkbox = CheckBox(size=(MedBox.size_of_drug[1],MedBox.size_of_drug[1]),pos = (MedBox.size_of_drug[0]-MedBox.size_of_drug[1],i*(MedBox.spacing+MedBox.size_of_drug[1])))
            checkbox.num = i
            checkbox.bind(active=self.on_checkbox)
            b.add_widget(checkbox)
            self.checkboxeslist.append(checkbox)
            b.ATXNum = IlnessBase.Medicine[i][IlnessBase.Medicine[i].find(':')+1:]
            MedBox.add_widget(b)

        TopLabel = Label(bold=True,size_hint=(None,None),text='check prep:',font_size=fullapp.size[1]*0.036,color = (0,0,0,1),pos = (fullapp.size[0]*0.34,fullapp.size[1]*0.85))
        
        self.SomeWidget = Widget(pos=(0,0),size_hint=(None,None),size = fullapp.size)
        CancelButton = Button(text = 'exit',font_size=fullapp.size[1]*0.022,size_hint=(None,None),size=(MedBox.size_of_drug[0]/2.01,fullapp.size[1]*0.05),
            pos = (self.scrollpos[0],self.scrollpos[1]-fullapp.size[1]*0.05-1),background_color = (0.3,0.3,0.9,1),on_press=self.on_cancel)
        OkButton = Button(text = 'chose',font_size=fullapp.size[1]*0.022,size_hint=(None,None),size=(MedBox.size_of_drug[0]/2.01,fullapp.size[1]*0.05),
            pos = (self.scrollpos[0]+MedBox.size_of_drug[0]/2+1,self.scrollpos[1]-fullapp.size[1]*0.05-1),background_color = (0.3,0.3,0.9,1),on_press=self.on_choose)
        
        self.SomeWidget.add_widget(CancelButton)
        self.SomeWidget.add_widget(OkButton)
        self.SomeWidget.opacity=0

        MedScroll.add_widget(MedBox)
        self.add_widget(self.SomeWidget)
        self.add_widget(MedScroll)
        self.add_widget(TopLabel)

    def on_button(self,instance):
        self.add_widget(self.create_Popup([instance.ATXNum]*1))

    def on_cancel(self,instance):
        self.active_checkboxes = []
        for i in self.checkboxeslist:
            i.active = False

    def on_choose(self,instance):      
        list = []
        for i in self.active_checkboxes:
            list.append(IlnessBase.Medicine[i][IlnessBase.Medicine[i].find(':')+1:])
        self.add_widget(self.create_Popup(list))
        self.on_cancel(Button())

    def on_checkbox(self,instance,value):
        if(value):
            self.active_checkboxes.append(instance.num)
        else:
            try:
                self.active_checkboxes.remove(instance.num)
            except:
                pass

    def create_Popup(self,list):
        def close(instance):
            self.remove_widget(nowPopup)
        nowPopup = Popup(size_hint = (None,None),size = (fullapp.size[0]*0.94,fullapp.size[1]*0.45),pos = (fullapp.size[0]*0.03,fullapp.size[1]*0.3))
        nowPopupContent = Widget(size_hint=(None,None),pos=fullapp.pos,size=fullapp.size)
        nowPopupContent.add_widget(Button(pos=nowPopup.pos,size=nowPopup.size,background_color=(1,1,1,0),on_press=close))
        nowPopup.title = '.'
        nowPopup.title_align = 'center'
        nowPopup.title_size = fullapp.size[1]*0.035
        str_of_nums = ''
        for i in list:
            str_of_nums = str_of_nums + str(i) + ', '
        str_of_nums = str_of_nums[:len(str_of_nums)-2]
        nowLabel = Label(markup=True,font_size=fullapp.size[1]*0.03,text_size=(nowPopup.size[0]*0.9,nowPopup.size[1]-nowPopup.title_size),size_hint=(None,None),pos=(nowPopup.pos[0]+nowPopup.size[0]/3.2,nowPopup.pos[1]+nowPopup.size[1]/2-nowPopup.title_size*1.5))
        nowLabel.text = '[color=a9a9a9]' + ' (ATX NUM ' + '[color=ffffff][i]' + str_of_nums  + '[/i][/color]' + ')  ' + '[i]' + '' \
            + '[/i]' + '  ' + '[i]' + '.' + '[/i]' 
        nowPopupContent.add_widget(nowLabel)
        nowPopup.add_widget(nowPopupContent)
        for i in list:
            for j in range(len(IlnessBase.Medicine)):
                if(i in IlnessBase.Medicine[j]):
                    k = j
            date = datetime.datetime.now()
            strdate = ''
            if(date.hour<10):
                strdate = '0'+str(date.hour)+':'
            else:
                strdate = str(date.hour)+":"
            if(date.minute<10):
                strdate += '0'+str(date.minute)+' '
            else:
                strdate += str(date.minute)+" "
            if(date.day<10):
                strdate += '0'+str(date.day)+'.'
            else:
                strdate += str(date.day)+"."
            if(date.month<10):
                strdate += '0'+str(date.month)+'.'
            else:
                strdate += str(date.month)+"."
            strdate+=str(date.year)
            fullapp.notes.append({'type':'request','undertype':'med','state':'inprogress','idinIlnessBase':k,'idnum':int(random.random()*10000),'date':strdate})
        return nowPopup


class TutorialApp(App):
    def build(self):
        global fullapp
        fullapp = FullApp()
        Clock.schedule_once(fullapp.AppLoop,0.0001)

        return fullapp

if __name__ == "__main__":
    TutorialApp().run()

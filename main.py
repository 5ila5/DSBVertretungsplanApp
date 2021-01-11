import kivy
import getDSB
import threading
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.properties import DictProperty
from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.utils import escape_markup
from kivy.uix.recycleview.datamodel import RecycleDataModelBehavior
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
import os.path
import time
from os import path
from pathlib import Path
from kivy.clock import mainthread
from functools import partial
from plyer import notification




from bs4 import BeautifulSoup
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
#from kivy.uix.listview import ListItemButton
from kivy.uix.recycleview import RecycleView
#from kivy.uix. import RecycleView
from kivy.clock import Clock


try:
    from plyer import vibrator
except:
    print("not Imported")

#try:

def startService():
    try:
        print("service Try begin")
        SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
            packagename=u'org.silas.dsbnews',
            servicename=u'Myservice'
        )
        #SERVICE_NAME= 'DSB_News.ServicegetUpdates'
        from jnius import autoclass
        print("Service Name")
        print(SERVICE_NAME)
        service = autoclass(SERVICE_NAME)
        print("After 'Service' Declaration")

        mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
        argument = ''
        service.start(mActivity, argument)
        print("END OF INIT SERVICE")

        """
        package_name = 'net.saband.myapp'
        service_name = 'ENTRYPOINT_TO_PY'
        service = autoclass('{}.Service{}'.format(package_name, service_name))
        mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        service.start(mActivity, '')"""

        '''from jnius import autoclass
        
    
        service = autoclass('your.package.domain.package.DSB_News.ServiceMyservice')
        mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        argument = ''
        service.start(mActivity, argument)
        # Context is a normal java class in the Android API
        Context = autoclass('android.content.Context')'''
    except Exception as e:
        print("Service not started"+str(e))
    try:
        from os import environ
        argument = environ.get('PYTHON_SERVICE_ARGUMENT', '')
        print(argument)
    except Exception as e:
        print("Fail2:"+str(e))
startService()
def Vibrate():
    try:
        from jnius import autoclass,cast

    # PythonActivity is provided by the Kivy bootstrap app in python-for-android
        print("Vibrate Start")
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        print("1")
        # The PythonActivity stores a reference to the currently running activity
        # We need this to access the vibrator service
        activity = PythonActivity.mActivity
        print("2")
        # This is almost identical to the java code for the vibrator
        Context = autoclass('android.content.Context')
        print("3")
        vibrator_service = activity.getSystemService(Context.VIBRATOR_SERVICE)
        print("4")
        vibrator = cast("android.os.Vibrator", vibrator_service)
        print("5")

        vibration_effect = autoclass("android.os.VibrationEffect")
        print("6")

        #vibrator.vibrate(10000)
        vibrator.vibrate(vibration_effect.createOneShot(2000, 150))
        print("end of Vibrate")
    except Exception as e:
        print("Not Vibrated")
        print(str(e))

#Vibrate()
#Window.size =(1000,700)
Builder.load_file("start.kv")
configPath = "config.json"

class Login(Screen):
    Window.size
    ben = StringProperty()
    pw = StringProperty()
    knopf = ObjectProperty()
    kl= StringProperty()

    def anmPopUp(self):
        if self.ben == "" and self.pw == "":
            popup = Popup(title='fehler', content = Label(text='Es wurde nichts eingegeben'), size_hint=(None, None), size=(400, 400) )
            popup.open()
        else:

            login = True
            if login:
                self.knopf.background_color = [0., 1., 0., 1.]
                conf = {
                "benutzer" : self.ben,
                "passwort" : self.pw,
                "klassen" : self.kl
                }
                with open(configPath, "r", encoding="utf-8") as confFile:
                    if not confFile.read() == json.dumps(conf):
                        for file in os.listdir("Tables"):
                            if not file[-4:] == ".txt":
                                os.remove("Tables/"+file)
                with open(configPath, "w", encoding="utf-8") as confFile:
                    confFile.write(json.dumps(conf))
                threading.Thread(target=DSBgetMethod).start()
                return True
            else:
                self.knopf.background_color = [1., 0., 0., 1.]
                return False

    def insertFromConf(self):
        if not path.exists("config.json"):
            open(configPath, "w")
        with open(configPath, "r", encoding="utf-8") as confFile:
            conf = json.loads(confFile.read())



        self.ben= conf["benutzer"]
        self.pw= conf["passwort"]
        self.kl= conf ["klassen"]
        print(self.knopf)
        #print(conf["benutzer"])
        #print(conf["passwort"])
        #print(conf["klassen"])
        #return self.anmPopUp()
    def on_enter(self, *args):
        #print("enter")
        self.insertFromConf()


class uebersicht(Screen):
    Window.size
    fbox = ObjectProperty()
    bLay = ObjectProperty()
    tab1 = ObjectProperty()
    tab2 = ObjectProperty()

    #@mainthread
    def __init__(self,gesTab=False, **kwargs):
        super(uebersicht, self).__init__(**kwargs)
        self.gesTab = gesTab

        self.tab1.disabled = True
        #Clock.schedule_interval(self.on_enter, 30)
                #self.ids.BL.add_widget(button)
                #pass
    def on_enter(self,newContent=True,*args):

        #Vibrate()
        print(self.bLay)
        if self.gesTab:
            if newContent:
                #Clock.schedule_once(DSBWhol)
                threading.Thread(target=DSBWhol).start()
            self.tab1.disabled= False
            self.tab2.disabled = True
        else:
            self.tab2.disabled= False
            self.tab1.disabled = True

        self.bLay.clear_widgets()
        i = 0
        for datei in sorted(Path("Tables").iterdir(), key=os.path.getmtime, reverse=True):
            datei= str(datei.name)
            if datei[-5:].lower() == ".html" and ((self.gesTab and datei[:6] == "Total_")or (not self.gesTab and not datei[:6] == "Total_")):
                datei = datei[:-5]

                button = MenuButton(text=datei.replace("Total_",""))
                #buttoncallback = lambda: print(g.text)
                #button.bind(on_press=buttoncallback)
                button.bind(on_release=partial(self.wechsel, datei))
                #state = wechsel
                self.bLay.add_widget(button)



    def wechsel(self, text,button):
        print(text)
        print("button")
        print(button)
        table = Table(name=text,tableName=text)
        sm.add_widget(table)
        sm.current = text
        sm.transition.direction = "left"
        #print(test)
        startService()


    def refresh(self,*args):
        if self.gesTab:
            getDSB.getContent(total=True)
        else:
            getDSB.getContent()
        self.on_enter(newContent=False)

class PresenzeScreen(Screen):
    def switch(self):
        self.parent.current = 'presenze'

class Table (Screen):

    recycleV = ObjectProperty()
    name = StringProperty()
    gridLay = ObjectProperty()
    rowcount = NumericProperty(2)
    colcount = NumericProperty(2)
    data_items = ListProperty()

    def __init__(self,tableName="", **kwargs):
        super(Table, self).__init__(**kwargs)
        self.gridLay.bind(minimum_height=self.gridLay.setter('height'))
        print("GUTEN TAG")
        print(self.name)
        self.name = tableName
        print(self.name)
        self.ids.headerLable.text = tableName
        with open("Tables/"+tableName+".html", "r", encoding='utf-8') as datei:

            soup = BeautifulSoup(datei.read(),features="html.parser")
            table=soup.find("table")
            print(table.findChildren("tr")[0])
            anzTr = 0
            #print(table)

            self.colcount = len(table.findChildren("tr")[0].findChildren("td"))

            for tr in table.findChildren("tr"):
                #print(tr)
                anzTr += 1
                self.rowcount = anzTr
                anzTd = 0

                for tr in tr.findChildren("th"):
                    label = TableLable(text=tr.text)
                    label.legende = True
                    self.gridLay.add_widget(label)
                    anzTd +=1

                for td in tr.findChildren("td"):
                    #label = TableLable()#text=td.text) #,background_color=[105, 106, 188, 1])
                    #label.texts =td.text
                    #print(label.texts)
                    #print(self.recycleV)
                    #if anzTr % 2 == 0:
                    #    self.data_items.append({'text': td.text, 'background_color': (0.980392156862745, 0.827450980392157, 0.650980392156863, 1)})

                    #else:
                    #    self.data_items.append({'text': td.text, 'background_color': (0.992156862745098, 0.925490196078431, 0.850980392156863, 1)})
                    #td.replace("<s>","[s]").replace("</s>","[/s]")
                    try:
                        td.s.insert(0,"[s]")
                        td.s.insert(2,"[/s]")
                    except Exception as e:
                        print(str(e))
                        pass

                    label = TableLable(text=td.text,markup=True)#.text)
                    #label = TableLable(text=td.text,color=[0,0,0,1])
                    #if anzTr %2 == 1:
                        #label.firstColor = False
                    #label.bind(text=td.text)
                    #label.texts = str(td.text)
                    #label.rgba = [.5, 1, .2, 1]
                    # fad3a6
                    # fdecd9
                    self.gridLay.add_widget(label)
                    anzTd +=1
                #print(anzTd)
            # here I expect textinputs id but got empty dict

            #print(self.gridLay)

            print(anzTd)
            print(anzTr)
            self.colcount = anzTd
            self.rowcount = anzTr

    def resize(self, *args):
        #print(self.goto_node(self.colcount*self.rowcount))

        print("resize")
        max = [0]
        curr = 0
        x = 0
        max[0]=0
        for child in self.gridLay.children:

            if max[curr] < child.texture_size[1]:
                max[curr] = child.texture_size[1]
            x+= 1
            print(x)
            if x >= self.colcount:
                curr+=1
                max.append(0)
                x = 0
        print("max"+str(max))
        print("elf.colcount"+str(self.colcount))
        x = 0
        curr = 0
        fCol = True
        for child in self.gridLay.children:

            child.maxheight = max[curr]
            child.firstColor = fCol
            x+=1
            if curr == self.rowcount:
                child.legende = True
            if x >= self.colcount:
                curr+=1
                x=0
                fCol = not fCol
            child.background()
            child.allowSize=True




    def on_enter(self, *args):
        print(len(self.ids.grid.children))
        print("HALLLLOOOOO123")
        self.resize()
        #Clock.schedule_once(self.resize)
        #Clock.schedule_interval(self.resize, 0.5)

    def vollerPlan(self):
        DSBWhol()
        text = "Total_"+self.name
        table = Table(name=text, tableName=text)
        sm.add_widget(table)
        sm.current = text


    def delete(self):
        print("HIER")
        print(self.ids.grid.children)
        sm.remove_widget(self)

class TableLable(Label):
    allowSize = False
    maxheight = NumericProperty(20)
    firstColor = BooleanProperty(True)
    legende = BooleanProperty(False)
    bColor = DictProperty()
    texts = StringProperty()
    #def on_size(self,*args):
    #    print(args)
    #    print("HALLLO BITTE")
    def on_size(self, *args):
        print(args)
        if (self.allowSize):
            self.background()
    def background(self, *args):
        print("On SIze")
        self.canvas.before.clear()
        with self.canvas.before:
            if self.firstColor:
                Color(
                0.980392156862745,
                0.827450980392157,
                0.650980392156863
                )
            else:
                Color(0.992156862745098, 0.925490196078431, 0.850980392156863)
            if self.legende:
                Color(0., 0., 0.)
                self.color =(1,1,1,1)
            self.size[1] = self.maxheight
            Rectangle(pos=self.pos, size=self.size)
            print(self.size)
    def __init__(self, **kwargs):
        super(TableLable, self).__init__(**kwargs)
        #self.on_size()
    #def __init__(self, text="old",**kwargs):
    #    super(TableLable, self).__init__(**kwargs)
    #    #print("InitTest")
    #    self.texts = text
        #print(self.texts)


class MenuButton(Button):
    pass
    #def on_size(self,*args):
    #    self.texture_update()


class RV(RecycleView):
    grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        print("child1")
        #self.data = [{'text': str(x),'background_color':(x/255,0.827450980392157,0.650980392156863,1)} for x in range(300)]
        for x in range(50):
            self.data.append({'text': str(x),'background_color':(x/255,0.827450980392157,0.650980392156863,1)})
        x = 0
        #for child in self.grid.children:
        #    if x%2 == 0:
        #        child.firstColor = False
        #        child.bColor = (0.992156862745098, 0.925490196078431, 0.850980392156863,1)
        #    x+=1
        #    print(child)
        #    print("child3")
        #print("child2")
class Test(Screen):
    pass

def DSBWhol(*args):
    getDSB.getContent(total = True)
    uebersichtTab2.on_enter(newContent=False)

def DSBgetMethod(*args):
    print("DSBgetMethod")
    getDSB.getContent()
    uebersichtTab1.on_enter(newContent=False)

test = Test()
#test.add_widget(TableLable(text="Hallo"))
#test.add_widget(RV())

sm = ScreenManager()
#sm.add_widget(test)
uebersichtTab1 =uebersicht(name='lockedArea')
loginScreen = Login(name='login')
sm.add_widget(uebersichtTab1)
sm.add_widget(loginScreen)


uebersichtTab2=uebersicht(name='gesTabel',gesTab=True)
sm.add_widget(uebersichtTab2)

sm.add_widget(PresenzeScreen(name='Presenze'))


#Window.clearcolor = 0.992156862745098, 0.925490196078431, 0.850980392156863,1
#Window.clearcolor = 1, 1, 1,1
Window.shape_color_key = 1,1,1,1


class DSBApp(App):
    def build(self):
        '''try:
            vibrator.vibrate(10)
        except:
            print("run this bock if there was error in earlier block")
        '''
        print("test")
        #return RV()
        #Clock.schedule_interval(getDSB.getContent, 60)
        print("after")

        print("before")
        return sm #Login() #Login() #Button(text="test")


#print("hi")
if __name__ == "__main__":
    print("hi2")
    threading.Thread(target=DSBgetMethod).start()
    DSBApp().run()


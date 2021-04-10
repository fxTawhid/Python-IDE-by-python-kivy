from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.codeinput import CodeInput
from kivy.uix.splitter import Splitter
from kivymd.uix.screen import Screen
import ctypes
import os
from kivy.uix.button import Button
from tkinter.filedialog import Directory, askopenfile, test
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivymd.uix.button import MDRectangleFlatButton as Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
ctypes.windll.shcore.SetProcessDpiAwareness(1)#if on pc?
VERTICAL = "vertical"

li = []
def newprint(query):
    global li 
    li.append(str(query))
filepath = ""
class MyAPP(MDApp):
    def build(self):
        #main widget
        self.wm = ScreenManager()
        logsc = Screen()
        logstate = BoxLayout(orientation=VERTICAL)
        lab = Label(text="Welcome to PyIDEkv" ,color="blue")
        but = Button(text = "Start" ,on_press=lambda x:self.change("main"))
        but.size_hint=1,1
        logstate.add_widget(lab)
        logstate.add_widget(but)
        logsc.add_widget(logstate)

        logsc.name = "login"
        testscreen = Screen()
        testscreen.name = "main"
        box = BoxLayout()
        box.orientation = VERTICAL
        global p,l, codeout
        p = Popup()
        p.title = "Choose your file!"
        self.x = FileChooserIconView()
        anlay = BoxLayout()
        anlay.add_widget(self.x)
        anolay = BoxLayout()
        anolay.size_hint=0.5,0.5
        anlay.orientation= VERTICAL
        anolay.add_widget(Button(text="Open", on_press=self.op))
        anolay.add_widget(Button(text="Cancel", on_press=lambda instance:p.dismiss()))
        anlay.add_widget(anolay)
        
        p.add_widget(anlay)
        toolwid = BoxLayout()
        toolwid.size_hint = 1, 0.3
        btn = Button(text="Open", on_press=lambda instance:p.open())
        btn.size_hint = 0.25, 1
        toolwid.add_widget(btn)
        btn2 = Button(text="Save", on_press=self.save)
        btn2.size_hint = 0.25,1
        toolwid.add_widget(btn2)
        btn3 = Button(text="Run", on_press=lambda ins:self.executor())
        btn3.size_hint = 0.25,1
        toolwid.add_widget(btn3)
        box.add_widget(toolwid)
        #code widget
        s = Splitter()
        s.max_size = 100000
        s.min_size = 0
        s.sizable_from = "bottom"
        l = CodeInput()
        s.add_widget(l)
        box.add_widget(s)
        codeout = CodeInput()
        codeout.readonly = True
        codeout.multiline = True
        box.add_widget(codeout)
        testscreen.add_widget(box)
        self.wm.add_widget(logsc)
        self.wm.add_widget(testscreen)
        
        #return style
        
        return self.wm
    def op(self, instance):
        global filepath
        selection = self.x.selection[-1]
        filepath = selection
        with open(selection,"r",encoding="utf-8") as fp:
            tex = fp.read()
            l.text = tex

            
        p.dismiss()
    def save(self, instance):
        if filepath ==  "":
            p = Popup(title="Warning")
            p.size_hint = 0.5,0.5
            lay = BoxLayout(orientation=VERTICAL)
            lay.add_widget(Label(text="Please Open A file first!"))
            lay.add_widget(Button(text="Ok", on_press=lambda instance: p.dismiss()))
            p.add_widget(lay)
            p.open()
        else:
            code = l.text
            with open(filepath,"w") as fp:
                fp.write(code)
                p = Popup(title="Success")
                p.size_hint = 0.5,0.5
                lay = BoxLayout(orientation=VERTICAL)
                lay.add_widget(Label(text="File Saved!"))
                lay.add_widget(Button(text="Ok", on_press=lambda instance: p.dismiss()))
                p.add_widget(lay)
                p.open()

    def runP(self, instance):
"""if you want to use python to execute code!"""
        if filepath == "lol":
            p = Popup(title="Warning")
            p.size_hint = 0.5,0.5
            lay = BoxLayout(orientation=VERTICAL)
            lay.add_widget(Label(text="Please Open A file first!"))
            lay.add_widget(Button(text="Ok", on_press=lambda instance: p.dismiss()))
            p.add_widget(lay)
            p.open()
        else:
            path = filepath
            try:
                result = os.popen(f"py {path}")
            except Exception as e:
                result = repr(e)
            codeout.text = result
    def change(self,x):
        self.wm.current = x

    def executor(self):
        global li, codeout
        try:
            inp= l.text.replace("print","newprint")
            exec(inp,globals())
            codeout.text = str("\n".join(li))
            li = []
        except Exception as e:
            
            codeout.text= str(repr(e))
        
        
app = MyAPP()
app.run()

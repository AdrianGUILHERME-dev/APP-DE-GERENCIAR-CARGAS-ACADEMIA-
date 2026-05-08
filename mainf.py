from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import sqlite3
import json
from kivy.clock import Clock

class MainApp (App):
    def build(self):
        self.treino = {'DOM':['a'],'SEG':['b'],'TER':['c'],'QUA':['d'],'QUI':['e'],'SEX':['f'],'SAB':['g']}
        self.input=[]
        return Gerenciador()

    def exibirtreino(self, x, y, largura, altura):

        layoutlistascroll= ScrollView(
                           size_hint=(largura, altura),
                           pos_hint={'center_x':x, 'center_y':y},
        )

        layoutlistabox= BoxLayout(
                        orientation='horizontal',
                        size_hint=(largura + 1, altura )
        )
        layoutlistascroll.add_widget(layoutlistabox)

        for dia in self.treino.keys():
            treinostr=''
            if len(self.treino[dia])>0:
                for exercicio in self.treino[dia]:
                    treinostr+=exercicio + '\n'
                Coluna=Label(text=dia+ '\n' + exercicio)
                layoutlistabox.add_widget(Coluna)

        return layoutlistascroll

    def TextInput (self):
        pass

class TelaInicial(Screen):

    #Método para aguardar um tempo antes de adicionar a lista na tela!
    ##def on_enter(self):
    ##    Clock.schedule_once(self.carregar_treino, 0.1)
    ##
    #O parâmetro dt está aqui pois o Clock.schedule_once carrega o tempo para a funcção executada
    ##def carregar_treino(self, dt):
    ##   appinstancia = App.get_running_app()
    ##                                            #x  #y  #Largura #Altura
    ##    listaemscroll = appinstancia.exibirtreino(.6, .2, .6, .6)
    ##    self.ids.layoutinicial.add_widget(listaemscroll)
    pass

class TelaConfig(Screen):
    def on_enter(self):
        def carregar_treino(self, dt):
            appinstancia = App.get_running_app()
            listaemscroll = appinstancia.exibirtreino(.2, .5, .6, .6) # x  #y  #Largura #Altura
            self.ids.layoutconfig.add_widget(listaemscroll)
    pass

class TelaAnotar(Screen):
    pass

class TelaEvo(Screen):
    pass

class Gerenciador(ScreenManager):
    pass


if __name__ == '__main__':
    app = MainApp()
    app.run()

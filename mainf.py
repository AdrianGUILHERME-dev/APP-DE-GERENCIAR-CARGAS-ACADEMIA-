from importlib.metadata import pass_none
from json import JSONDecodeError
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import sqlite3
import json
from kivy.clock import Clock
from datetime import datetime
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown


class MainApp (App):
    def build(self):

        self.treino = {'SEG':[],'TER':[],'QUA':[],'QUI':[],'SEX':[],'SAB':[],'DOM':[]}
        self.input=[]
        self.diaatual=datetime.now().strftime("%Y-%m-%d")
        #Recebe dia da semana atual correspondente a dada de self.diaatual
        self.diadasemana=list(self.treino.keys())[datetime.now().weekday()]

        return Gerenciador()

    def exibirtreino(self, x, y, largura, altura):

        with open('exercicios_base.json','r', encoding="utf-8") as exercicios_base:
            exercicios_disponiveis=json.load(exercicios_base)
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
            layout_coluna_box = BoxLayout(orientation='vertical')
            layoutlistabox.add_widget(layout_coluna_box)
            Dia= Label(text=f'{dia}')
            layout_coluna_box.add_widget(Dia)
            for x in range(0,6):
                try:
                    entrada= DropDown(text=f'{self.treino[dia][x]}')
                    layout_coluna_box.add_widget(entrada)
                except IndexError:
                    entrada = DropDown(text='')
                    layout_coluna_box.add_widget(entrada)
                for exercicio in exercicios_disponiveis[exercicios]:
                    opcoesdisponiveis= Button(text=f'{exercicio}'
                                              on_release=(pass)
                    )


        return layoutlistascroll


    def guardartreino(self,*args):
        #Escreve a lista atual
        with open("treinoatual.json", "w", encoding="utf-8") as treino:
            json.dump(self.treino, treino, indent=4, ensure_ascii=False)

    def lertreino(self):
        #Tenta ler o documento treinoatual.json
        try:
            with open("treinoatual.json", "r", encoding="utf-8") as treino:
                self.treino= json.load(treino)
        #Se o caso não exista, cria um usando o "w" da função with open()
        except (FileNotFoundError,JSONDecodeError):
            with open("treinoatual.json", "w", encoding="utf-8") as treino:
                json.dump(self.treino, treino, indent=4, ensure_ascii=False)

    def limpartreino(self):
        self.treino = {'SEG':[],'TER':[],'QUA':[],'QUI':[],'SEX':[],'SAB':[],'DOM':[]}
        self.guardartreino()
        self.exibirtreino()

    def guardarcargas(self):
        with sqlite3.connect('treinoatual.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS cargas
                            ( id INTEGER PRIMARY KEY AUTOINCREMENT, 
                              exercicio TEXT NOT NULL,
                              carga(Kg) FLOAT, 
                              data TEXT NOT NULL)'''
            )
            treino_do_dia = self.treino[self.diadasemana]
            for input in self.input:
                cursor.execute(f'''INSERT INTO cargas VALUES
                                   ({treino_do_dia[self.input.index(input)]},
                                    {input},
                                    {self.diaatual}
                                    '''
                )



    def lercargas(self):
        pass

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
        app = App.get_running_app()
        app.lertreino()
        listaemscroll = app.exibirtreino(.5, .5, .5, .8) # x  #y  #Largura #Altura
        self.ids.layoutconfig.add_widget(listaemscroll)

    pass

class TelaAnotar(Screen):
    def on_enter(self):
        app=App.get_running_app()
        app.lertreino()
        layout_coluna_texto= BoxLayout(orientation='vertical',
                                       size_hint=(0.1,0.1),
                                       pos_hint={'center_x':.3, 'center_y':.5}
                                       )
        self.ids.layoutanotar.add_widget(layout_coluna_texto)
        layout_coluna_input= BoxLayout(orientation='vertical',
                                       size_hint=(0.2, 0.1),
                                       pos_hint={'center_x': .5, 'center_y': .5}
                                       )
        self.ids.layoutanotar.add_widget(layout_coluna_input)

        if len(app.treino[app.diadasemana]) > 0:
            for exercicio in app.treino[app.diadasemana]:
                Colunaexercicios= Label(text=exercicio)
                layout_coluna_texto.add_widget(Colunaexercicios)
                Colunainputs= TextInput(text='')
                layout_coluna_input.add_widget(Colunainputs)
        else:
            Aviso= Label(text='HOJE É DIA DE DESCANSO, VOLTE AMANHÃ!\n (Atenção:'
                                  'caso não seja dia de descanso, por favor verifique'
                                  'o treino cadastrado nas configurações)'
                             )
            self.ids.layoutanotar.add_widget(Aviso)

        pass

class TelaEvo(Screen):
    pass

class Gerenciador(ScreenManager):
    pass


if __name__ == '__main__':
    app = MainApp()
    app.run()

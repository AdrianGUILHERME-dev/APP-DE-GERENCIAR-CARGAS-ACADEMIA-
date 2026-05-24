from asyncio.windows_events import NULL
from json import JSONDecodeError
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import sqlite3
import json
from kivy.clock import Clock
from datetime import datetime
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
import matplotlib.pyplot as plt
import numpy as np



class MainApp (App):
    def build(self):

        self.treino = {'SEG':[],'TER':[],'QUA':[],'QUI':[],'SEX':[],'SAB':[],'DOM':[]}
        self.cargas={}
        self.dataatual=datetime.now().strftime("%Y-%m-%d")
        #Recebe dia da semana atual correspondente a dada de self.dataatual
        self.diadasemana=list(self.treino.keys())[datetime.now().weekday()]
        self.layoutscroll=ScrollView()
        self.identificadores={}

        with sqlite3.connect('bancodedados.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS cargas
                                        ( id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                          exercicio TEXT NOT NULL,
                                          carga_Kg FLOAT, 
                                          data TEXT NOT NULL)''')
            cursor.execute('''SELECT data FROM cargas WHERE data = ? ''', (self.dataatual,))
            self.datas=cursor.fetchall()


        return Gerenciador()



    def telaatual(self):
        tela_atual = self.root.current_screen
        return tela_atual

    def exibirtreino(self):
        # .4, .45, .65, .8
        with open('exercicios_base.json', 'r', encoding="utf-8") as exercicios_base:
            exerciciosbase = json.load(exercicios_base)
            chaveexercicios = list(exerciciosbase.keys())
            exerciciosbase[chaveexercicios[0]].sort()

        self.layoutscroll = ScrollView(
            size_hint=(.65, .8),
            pos_hint={'center_x': .4, 'center_y': .45},
        )

        layouthorizontalpai = BoxLayout(
            orientation='horizontal',
            size_hint_x=None,
            width=2000
        )
        self.layoutscroll.add_widget(layouthorizontalpai)

        dropdown = DropDown()

        apagaropcao = BotaoRetangular(text='', height=44, size_hint_y=None)
        apagaropcao.bind(on_release=lambda instance: dropdown.select(instance.text))
        dropdown.add_widget(apagaropcao)

        for exercicio in exerciciosbase[chaveexercicios[0]]:
            opcoesdisponiveis = BotaoRetangular(text=f'{exercicio}', height=44, size_hint_y=None)
            opcoesdisponiveis.bind(on_release=lambda instance: dropdown.select(instance.text))
            dropdown.add_widget(opcoesdisponiveis)

        for dia in self.treino.keys():
            layoutverticalfilho = BoxLayout(orientation='vertical')
            layouthorizontalpai.add_widget(layoutverticalfilho)
            Diatexto = Label(text=f'{dia}')
            layoutverticalfilho.add_widget(Diatexto)
            for x in range(0, 6):
                try:
                    textobotao = f'{self.treino[dia][x]}'
                except IndexError:
                    textobotao = ''

                botaopai = BotaoRetangular(text=f'{textobotao}')
                botaopai.id=f"{dia}"+f"{x}"
                layoutverticalfilho.add_widget(botaopai)
                self.identificadores[botaopai.id]=botaopai

                botaopai.bind(on_release=lambda btn: self.abrir_dropdown_para_botao(btn, dropdown))

        return self.layoutscroll

    def abrir_dropdown_para_botao(self, botao, objeto_dropdown):
        # 1. Limpa qualquer bind anterior do dropdown para não acumular
        objeto_dropdown.unbind(
            on_select=objeto_dropdown.callback_atual if hasattr(objeto_dropdown, 'callback_atual') else lambda *x: None)

        # 2. Cria a função que vai atualizar o botão específico que foi clicado
        def atualizar_texto(instance, texto_selecionado):
            botao.text = texto_selecionado
            #Recupera dia e posição na tabela através do id de cada botão.
            #E adiciona na lista de treino.
            self.receberinput(botao)
        # 3. Salva a referência para podermos limpar no próximo clique
        objeto_dropdown.callback_atual = atualizar_texto

        # 4. Associa o evento e abre o menu na posição do botão
        objeto_dropdown.bind(on_select=atualizar_texto)
        objeto_dropdown.open(botao)


    def receberinput(self, instance):
        textobotao=instance.text
        if textobotao != '':
            try:
                self.treino[instance.id[:3]][int(instance.id[4])]=textobotao
            except IndexError:
                self.treino[instance.id[:3]].append(textobotao)

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
        for botao in self.identificadores.values():
            botao.text=''
        self.guardartreino()

    def guardarcargas(self, *args):
        with sqlite3.connect('bancodedados.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS cargas
                            ( id INTEGER PRIMARY KEY AUTOINCREMENT, 
                              exercicio TEXT NOT NULL,
                              carga_Kg FLOAT, 
                              data TEXT NOT NULL)'''
            )

            for exercicio, carga in self.cargas.items():

                cursor.execute('''INSERT INTO cargas (exercicio, carga_Kg, data) 
                                          VALUES (?, ?, ?)''',
                               (exercicio, carga, self.dataatual))


    def pop_up_confirmacao(self, *args):

        layoutconfirmacaoscroll = ScrollView()
        layoutconfirmacaobox1 = BoxLayout(orientation='vertical',
                                         size_hint_y=None
                                         )


        layoutconfirmacaobox1.bind(minimum_height=layoutconfirmacaobox1.setter('height'))
        layoutconfirmacaoscroll.add_widget(layoutconfirmacaobox1)

        for exercicio, carga in self.cargas.items():
            label=Label(text=f'{exercicio}: {carga} Kg',
                        size_hint_y=None,
                        height=40)
            layoutconfirmacaobox1.add_widget(label)

        pop_up= Popup(title='CONFIRMAÇÃO:',
                      content=layoutconfirmacaoscroll,
                      size_hint=(0.5,0.5),
                      )
        botaosalvar = BotaoArredondado(text='SALVAR',
                                       size_hint_y=None,
                                       height=50
                                       )
        botaosalvar.bind(on_release=self.guardarcargas)
        botaosalvar.bind(on_release=pop_up.dismiss)
        layoutconfirmacaobox1.add_widget(botaosalvar)

        pop_up.open()

    def lercargas(self):
        pass

    def TextInput (self):
        pass

class TelaInicial(Screen):
    pass

class TelaConfig(Screen):
    def on_enter(self):
        app = App.get_running_app()
        self.ids.layoutconfig.remove_widget(app.layoutscroll)
        app.lertreino()
        listaemscroll = app.exibirtreino()
        self.ids.layoutconfig.add_widget(listaemscroll)

    pass

class TelaAnotar(Screen):
    def on_enter(self):

        self.aviso=Label()
        self.carga={}
        app=App.get_running_app()
        app.lertreino()
        diccarga = {}


        if len(app.treino[app.diadasemana]) > 0 and len(app.datas) == 0:

            for exercicio in app.treino[app.diadasemana]:

                Colunaexercicios= Label(text=exercicio,
                                        size_hint_y=None,
                                        height=50
                                        )
                self.ids.boxtexto.add_widget(Colunaexercicios)
                caixainput= TextInput(text='',
                                        size_hint_y=None,
                                        height=50
                                        )
                diccarga[exercicio]=caixainput
                self.ids.boxentrada.add_widget(caixainput)

            def pre_salvamento(*args):
                for exercicio in app.treino[app.diadasemana]:
                    if diccarga[exercicio].text != '':
                        app.cargas[exercicio] = float(diccarga[exercicio].text)
                    else:
                        app.cargas[exercicio] = 0
                app.pop_up_confirmacao()

            botao_salvar= BotaoArredondado(text='OK',
                                           size_hint=(.2,.15),
                                           pos_hint={'x':0.77,'y':0.75}
                                           )
            botao_salvar.bind(on_release= pre_salvamento)

            self.ids.layoutanotar.add_widget(botao_salvar)
        elif len(app.datas) > 0:
            self.aviso = Label(text='VOCÊ JÁ INSERIU AS CARGAS DE HOJE,\n'
                                    'VOLTE AMANHÃ PARA CONTINUAR'
                                    'A REGISTRAR SEU PROGRESSO!')
            self.ids.layoutanotar.add_widget(self.aviso)

        else:
            self.aviso= Label(text='HOJE É DIA DE DESCANSO, VOLTE AMANHÃ!\n (Atenção:'
                                  'caso não seja dia de descanso, por favor verifique'
                                  'o treino cadastrado nas configurações)'
                             )
            self.ids.layoutanotar.add_widget(self.aviso)

        pass

    def on_leave(self):
        self.ids.layoutanotar.remove_widget(self.aviso)
        self.ids.boxtexto.clear_widgets()
        self.ids.boxentrada.clear_widgets()

class TelaEvo(Screen):
    def on_enter(self):
        self.dados=np.empty(shape=2)
        layoutatual=self.ids.layoutevo
        dropdown = DropDown()
        with open("exercicios_base.json", "r", encoding="utf-8") as exercicios_txt:
            exercicios=json.load(exercicios_txt)
            exercicios[list(exercicios.keys())[0]].sort()

            for exercicio in exercicios[list(exercicios.keys())[0]]:
                botao= BotaoRetangular(text=exercicio, size_hint_y=None, height=40)
                dropdown.add_widget(botao)
                botao.bind(on_release=lambda instance: dropdown.select(instance.text))
                botao.bind(on_release=self.pegardados)

        botaopai= BotaoRetangular(text='',
                                   size_hint=(.4,.10),
                                   pos_hint={'center_x':0.50,'center_y':0.85}
                                   )
        self.ids.layoutevo.add_widget(botaopai)
        botaopai.bind(on_release= dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(botaopai, 'text', x))

        botaodografico= BotaoArredondado(text='GERAR GRÁFICO',
                                         size_hint=(.4,.10),
                                         pos_hint={'center_x':0.80,'center_y':0.85}
                                         )
        botaodografico.bind(on_release=self.gerargrafico)
        self.ids.layoutevo.add_widget(botaodografico)




        pass

    def pegardados(self, botao):

        exercicio = botao.text
        with sqlite3.connect('bancodedados.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT carga_Kg, data FROM cargas 
                              WHERE exercicio= ? ORDER BY data ASC''', ( exercicio,))
            dados=cursor.fetchall()
            cargas=np.array([float(x[0]) for x in dados])
            datas=np.array([x[1] for x in dados])
            self.dados=[datas, cargas]

    def gerargrafico(self, *args):
        print("Datas:", self.dados[0])
        print("Cargas:", self.dados[1])
        fig, ax=plt.subplots()
        ax.plot(self.dados[0],self.dados[1])
        plt.show()


class Gerenciador(ScreenManager):
    pass

######################################### BOTÕES PERSONALIZADOS ############################################
class BotaoArredondado(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 1. Configurações básicas de transparência
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''

        # 2. Desenho do fundo arredondado
        with self.canvas.before:
            Color(0.10, 0.10, 0.10, 1)  # A cor que você definiu
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[15, ]  # Arredondamento dos cantos
            )

        # 3. Vínculo crucial: se o botão mudar de lugar ou tamanho, redesenha o fundo
        self.bind(pos=self.atualizar_canvas, size=self.atualizar_canvas)

    def atualizar_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class BotaoRetangular(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''

        with self.canvas.before:
            Color(0.10, 0.10, 0.10, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

            # Use um cinza um pouco mais claro (0.3) para testar se aparece,
            # depois você volta para o 0.05 se preferir.
            Color(0.08, 0.08, 0.08, 1)
            self.linha_borda = Line(rectangle=(self.x, self.y, self.width, self.height), width=1.2)

        self.bind(pos=self.atualizar_canvas, size=self.atualizar_canvas)

    def atualizar_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        # CORREÇÃO: O nome deve ser EXATAMENTE o mesmo que você criou no __init__
        self.linha_borda.rectangle = (self.x, self.y, self.width, self.height)

############################################################################################################



if __name__ == '__main__':
    app = MainApp()
    app.run()

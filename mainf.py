from asyncio.windows_events import NULL
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
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle




class MainApp (App):
    def build(self):

        self.treino = {'SEG':[],'TER':[],'QUA':[],'QUI':[],'SEX':[],'SAB':[],'DOM':[]}
        self.input=[]
        self.diaatual=datetime.now().strftime("%Y-%m-%d")
        #Recebe dia da semana atual correspondente a dada de self.diaatual
        self.diadasemana=list(self.treino.keys())[datetime.now().weekday()]
        self.layoutscroll=ScrollView()
        self.identificadores={}

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
        self.ids.layoutconfig.remove_widget(app.layoutscroll)
        app.lertreino()
        listaemscroll = app.exibirtreino() # x  #y  #Largura #Altura
        self.ids.layoutconfig.add_widget(listaemscroll)

    pass

class TelaAnotar(Screen):
    def on_enter(self):

        self.aviso=Label()

        app=App.get_running_app()
        app.lertreino()


        if len(app.treino[app.diadasemana]) > 0:
            c=0
            for exercicio in app.treino[app.diadasemana]:
                c=c+1
                Colunaexercicios= Label(text=exercicio,
                                        size_hint_y=None,
                                        height=50
                                        )
                self.ids.boxtexto.add_widget(Colunaexercicios)
                Colunainputs= TextInput(text='',
                                        size_hint_y=None,
                                        height=50
                                        )
                self.ids.boxentrada.add_widget(Colunainputs)
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
    pass


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

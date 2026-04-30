from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.scrollview import ScrollView
import datetime

#NOTA: Os {atributos nome_do_widget.id = "Alguma coisa"} são identificadores de cada widget criado dentro de um 'for'.

Window.clearcolor = get_color_from_hex('#363636')

class MainApp(App):
    def build(self):
        self.treino= {'DOM':[],'SEG':[],'TER':[],'QUA':[],'QUI':[],'SEX':[],'SAB':[]}
        self.opcoes= ['Mudar/Adicionar treino', 'Treino atual']
        self.layoutp= FloatLayout()
        self.inputs= []
        self.layoutlista=BoxLayout()

        self.tela_inicial()

        return self.layoutp

#CRIAÇÃO DE TELA INICIAL{
    def tela_inicial(self, *args):
        self.layoutp.clear_widgets()

        titulo= Label(text="Organizador de treino ultra-master",
                       size_hint=(0.2, 0.2),
                       pos_hint={'center_x': 0.5, 'center_y': 0.98}
                       )
        self.layoutp.add_widget(titulo)

        self.abadeopc= BoxLayout(orientation='vertical',
                                  size_hint=(0.6, 0.6),
                                  pos_hint={'center_x': 0.1, 'center_y': 0.5}
                                  )
        self.layoutp.add_widget(self.abadeopc)

        for opcao in self.opcoes:
            buttons = Button(text=opcao,
                             size_hint=(0.8, 0.2),
                             pos_hint={'center_x': 0.5, 'center_y': 0.5}
                             )
            buttons.bind(on_press=self.on_press_button)
            # esse 'buttons.bind' já trata cada botão isoladamente.
            self.abadeopc.add_widget(buttons)

        self.exibirlista(0.7,0.8, 0.6, 0.4)

        return self.layoutp
#}

    #Função de cada botão
    def on_press_button(self, instance):

    #CRIAÇÃO PÁGINA 1
        if instance.text == 'Mudar/Adicionar treino':
            self.layoutp.clear_widgets()

            titulo1= Label(text='ABA DE MODIFICAÇÃO DO TREINO',
                           pos_hint={'center_x':0.5, 'center_y':0.97}
                           )
            self.layoutp.add_widget(titulo1)

            layoutscroll= ScrollView(size_hint=(0.7,0.7))
            self.layoutp.add_widget(layoutscroll)

            layoutbase= FloatLayout()
            layoutscroll.add_widget(layoutbase)

            layoutdias = BoxLayout(orientation='horizontal',
                                   size_hint=(0.9, 0.1),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.85}
                                   )
            layoutbase.add_widget(layoutdias)

            layoutentradas= BoxLayout(orientation='vertical')
            layoutbase.add_widget(layoutentradas)

            for dia in self.treino.keys():
                colunanomes= Label(text=dia)
                layoutdias.add_widget(colunanomes)
                layoutcolunas= BoxLayout(orientation='vertical')
                layoutentradas.add_widget(layoutcolunas)

                for x in range(len(self.treino[dia])):
                    caixadeentrada= Label(text=self.treino[dia][x])
                    layoutcolunas.add_widget(caixadeentrada)
                for x in range(6-len(self.treino[dia])):
                    caixadeentrada = Label(text='',size_hint=(0.02,0.02))
                    layoutcolunas.add_widget(caixadeentrada)

        #BOTÃO VOLTAR NO CANTO ESQUERDO{
            botaovoltar= Button(text='<--',
                                size_hint=(0.1,0.1),
                                pos_hint={'center_x': 0.05, 'center_y': 0.95}
                                )
            botaovoltar.bind(on_press=self.tela_inicial)
            self.layoutp.add_widget(botaovoltar)
        #}
            ##############################################
            #CRIAR BOTÃO PARA LIMPAR LISTAS DE EXERCICIO#
            ##############################################



            return self.layoutp


    #CRIAÇÃO DE PÁGINA 2
        elif instance.text == 'Treino atual':
            self.layoutp.clear_widgets()

            for exercicio in self.treino:
                continue

            return self.layoutp

#MODIFICAÇÃO DE LISTA{
    def modlista (self, instance):

        if instance.text == '+':

            #Compara o texto de cada caixa de entrada com os dias de self.treino
            for input in self.inputs:
                for dia in self.treino.keys():
                    if len(self.treino[dia])<8:
                        if input.text != '':
                            if input.id == dia and input.id == instance.id:
                                self.treino[dia].append(input.text)
                                input.text = ''
                    else:
                        continue




        elif instance.text == 'C':
             m=1
#}

#EXIBE PEQUENA TABELA COM TREINO SEMANAL ( POSIÇÃO E PROPORÇÕES AJUSTÁVEIS ){
    def exibirlista(self, x, y, largura, altura):

        self.layoutp.remove_widget(self.layoutlista)
        self.layoutlista=BoxLayout(orientation='vertical',
                              size_hint=(largura, altura),
                              pos_hint={'center_x': x, 'center_y': y}
                              )
        self.layoutp.add_widget(self.layoutlista)

        layoutlistaint= BoxLayout(orientation='horizontal'
                                  )
        self.layoutlista.add_widget(layoutlistaint)


        for dia in self.treino.keys():
            treinostr=''
            for exercicio in self.treino[dia]:
                treinostr+=exercicio+'\n'
            coluna= Label(text=dia + '\n' + treinostr)
            layoutlistaint.add_widget(coluna)
#}

if __name__ == '__main__':
    MainApp().run()

import threading
from concurrent.futures import thread
from idlelib import window
from info import Ui_InfoWindow
import numpy
import self as self
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QWidget, QPushButton, QMessageBox
from datetime import datetime, timedelta, date
import time
import datetime as dt
import threading as th
from PyQt5.QtWidgets import *
from interface import *
from backup_db import *
import pymysql
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
import sys
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import random
import serial
import PID

teste_conexao = 0
botao_info = False
auto_update_graph=False
tendencias=0
config_pid_lamp=False
config_pid_banho=False
verify_pid_lamp=False
target_lamp=0
target_banho=0
pid_lamp=0
verify_pir1=False
verify_pir2=False
presenca=False
verify_lamp_economic=False
time_last=datetime.now()
time_last2=datetime.now()


#Variável usada para conferência da mudança de hora para realização do backup
hora_inicial=datetime.now()
hora_inicial = hora_inicial.replace(minute=00,second=00,microsecond=00)
#Conexao com a porta SERIAL
serial_port = serial.Serial('COM8', baudrate = 9600, writeTimeout = 0)

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Apresenta Aba aberta
        print(self.get_tab())

        # Funcao Data Atual
        self.minha_data()

        # Funcao Botao Teste
        self.ui.btn_teste.clicked.connect(self.teste_btn)

        # Funcoes Botao SAIR
        self.ui.btn_sair.clicked.connect(self.sair)
        self.ui.btn_sair2.clicked.connect(self.sair)

        # Apresenta Consumo
        self.consumo_mensal()
        print("Iniciando Software")
        time.sleep(4)

        # Apresenta Grafico
        self.seta_data_grafico()
        self.update_graph()
        self.select_dia_graph_mac()

        # Abre Janela de INFO
        self.ui.btn_info.clicked.connect(self.openWindow)

        # Funcoes das Select BOX
        self.ui.comboBox.currentIndexChanged.connect(self.update_graph)
        self.ui.comboBox_Dia.currentIndexChanged.connect(self.update_graph)
        self.ui.comboBox_Mes.currentIndexChanged.connect(self.update_graph)
        self.ui.comboBox_Ano.currentIndexChanged.connect(self.update_graph)

        #Configurações
        self.set_configs_user()

        # Funcoes de Botoes e Slider de Iluminacao e Temperatura//Aba QUARTO
        self.ui.horizontalSlider.valueChanged.connect(self.change_slider_ilum)
        self.ui.horizontalSlider.sliderReleased.connect(self.update_intensidade_iluminacao)
        #self.ui.horizontalSlider.bind("<ButtonRelease-1>", self.update_intensidade_iluminacao)
        self.ui.btn_on_ilum.clicked.connect(self.btn_on_lamp)
        self.ui.btn_off_ilum.clicked.connect(self.btn_off_lamp)
        self.ui.btn_temp.clicked.connect(self.update_temp)
        self.ui.btn_temp_agua_economic.clicked.connect(self.update_temp_banho_economic)
        self.ui.btn_temp_agua_normal.clicked.connect(self.update_temp_banho_normal)
        self.ui.btn_temp_mais.clicked.connect(self.update_temp_ar_mais)
        self.ui.btn_temp_menos.clicked.connect(self.update_temp_ar_menos)
        self.ui.btn_vol_mais.clicked.connect(self.update_volume_mais)
        self.ui.btn_vol_menos.clicked.connect(self.update_volume_menos)
        self.ui.btn_canal_mais.clicked.connect(self.update_canal_mais)
        self.ui.btn_canal_menos.clicked.connect(self.update_canal_menos)
        self.ui.btn_modo_ar.clicked.connect(self.update_modo_ar)
        self.ui.btn_power_ar.clicked.connect(self.update_power_ar)
        self.ui.btn_power_tv.clicked.connect(self.update_power_tv)

        # Funcao Backup/Restaurar
        #       self.backup()
        self.ui.btn_backup.clicked.connect(self.backup)
        self.ui.btn_restaurar.clicked.connect(self.restaurar)

        # Funcao CheckBoxs
        self.ui.check_Aprendizagem.stateChanged.connect(self.update_Aprendizagem)
        self.ui.check_Economia.stateChanged.connect(self.update_Economia)
        self.ui.check_Controle.stateChanged.connect(self.update_Controle)
        self.ui.btn_tendencia.clicked.connect(self.update_Tendencia)



        #Chama agente gerente
        self.agente_gerente()

    # FUNÇÕES DO SISTEMA
    def minha_data(self):

        data_atual = datetime.now()
        data_em_texto = data_atual.strftime('%d/%m/%Y')
        horas_em_texto = data_atual.strftime('%Hh:%Mmin:%Ss')
        saida = "Agora é " + horas_em_texto + " do dia: " + data_em_texto
        self.ui.data.setText(saida)

        # t = threading.Timer(1, self.minha_data)
        # t.start()


        # if data_em_texto=='30/01/2020':
        #   self.ui.label_3.setText("Hoje é dia:"+data_em_texto)

    def get_tab(self):

        currentWidget = self.ui.tabWidget.currentIndex()
        if currentWidget == 0:
            aba = 'Consumo'
        elif currentWidget == 1:
            aba = 'Configuração'
        elif currentWidget == 2:
            aba = 'Comandos'
        elif currentWidget == 3:
            aba = 'Aprendizagem'
        return aba

    def teste_btn(self):
        #valor=self.medicao_potencia()
        self.ui.label_3.setText("Botão Pressionado")

    def sair(self):
        window.destroy()
        sys.exit(app.exec_())

    def history(self):
        # Variaveis Globais para a Função
        global potencia_dia
        global dias_do_mes

        potencia_dia = 0
        # Captura os valores das ComboBoxs
        selecao = self.ui.comboBox.currentText()
        selecao_dia = self.ui.comboBox_Dia.currentText()
        selecao_mes = self.ui.comboBox_Mes.currentText()
        selecao_ano = self.ui.comboBox_Ano.currentText()

        i = 0
        # Abrimos uma conexão com o banco de dados:
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')

            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando de Acordo com o tipo da ComboBox:
            cursor.execute(
                "SELECT * FROM medicao  WHERE DAY(horario) = %s AND MONTH(horario) = %s AND YEAR(horario) = %s ORDER BY horario DESC ",
                (selecao_dia, selecao_mes, selecao_ano))

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                res = np.array([[0] * 5] * cursor.rowcount, dtype=np.int64)

                for linha in resultado:
                    res[i][0] = linha[0]
                    res[i][2] = linha[2]
                    res[i][3] = linha[3]
                    res[i][4] = linha[4]

                    # Classifica o Eixo por Dia
                    data = linha[1].strftime('%H')
                    res[i][1] = data
                    # Identifica a quantidade de Dias Diferentes no Mês
                    p = 1
                    for x in range(0, cursor.rowcount - 1):
                        if res[x][1] != res[x + 1][1]:
                            p = p + 1

                    # Cria Eixos do tamanho adequado
                    eixo_x_hora = np.zeros((1, p))
                    eixo_y_hora = np.zeros((1, p))

                    n = 0
                    horas_do_dia = np.zeros((1, p))
                    horas_do_dia[0][n] = res[0][1]
                    potencia_dia = np.zeros((1, p))
                    # Atribuiu os valores dos dias no Eixo X
                    for x in range(0, cursor.rowcount - 1):
                        if res[x][1] != res[x + 1][1]:
                            horas_do_dia[0][n + 1] = res[x + 1][1]
                            n = n + 1
                    n = 0
                    potencia_dia[0][0] = res[0][4]
                    # Atribui os valores das Potencias no Eixo Y
                    for x in range(0, cursor.rowcount - 1):
                        if res[x][1] == res[x + 1][1]:
                            potencia_dia[0][n] = potencia_dia[0][n] + res[x + 1][4]
                        elif res[x][1] != res[x + 1][1]:
                            n = n + 1
                            potencia_dia[0][n] = res[x + 1][4]
                    for x in range(0, p):
                        eixo_y_hora[0][x] = round((potencia_dia[0][x])/3600000,4) # Conversão para  kWh
                        eixo_x_hora[0][x] = horas_do_dia[0][x]

                    i = 1 + i
                # Conta a quantidade de valores do Vetor
                posicao1 = len(eixo_x_hora[0])
                hora = True

            # Caso nao haja registro de horario
            else:
                print("Não há Registros Diário.")
                hora = False

            # Executa o SELECT por Mes
            cursor.execute(
                "SELECT * FROM medicao  WHERE MONTH(horario) = %s AND YEAR(horario) = %s ORDER BY horario DESC ",
                (selecao_mes, selecao_ano))

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                i = 0
                res = np.array([[0] * 5] * cursor.rowcount, dtype=np.int64)

                for linha in resultado:
                    res[i][0] = linha[0]
                    res[i][2] = linha[2]
                    res[i][3] = linha[3]
                    res[i][4] = linha[4]

                    # Classifica o Eixo por Dia
                    data = linha[1].strftime('%d')
                    res[i][1] = data
                    # Identifica a quantidade de Dias Diferentes no Mês
                    p = 1
                    for x in range(0, i ):
                        if res[x][1] != res[x + 1][1]:
                            p = p + 1
                    # Cria Eixos do tamanho adequado
                    eixo_x_dia = np.zeros((1, p))
                    eixo_y_dia = np.zeros((1, p))

                    n = 0
                    dias_do_mes = np.zeros((1, p))
                    dias_do_mes[0][n] = res[0][1]

                    potencia_dia = np.zeros((1, p))
                    # Atribuiu os valores dos dias no Eixo X
                    for x in range(0, i):
                        if res[x][1] != res[x + 1][1]:
                            dias_do_mes[0][n + 1] = res[x + 1][1]
                            n = n + 1
                    n = 0

                    potencia_dia[0][0] = res[0][4]
                    # Atribui os valores das Potencias no Eixo Y
                    for x in range(0, i):
                        if res[x][1] == res[x + 1][1]:
                            potencia_dia[0][n] = potencia_dia[0][n] + res[x + 1][4]

                        elif res[x][1] != res[x + 1][1]:
                            n = n + 1
                            potencia_dia[0][n] = res[x + 1][4]

                    # Correcao do BUG Mensal
                    # if i != 0:
                    #     potencia_dia[0][n] = potencia_dia[0][n] + res[i][4]

                    for x in range(0, p):
                        eixo_y_dia[0][x] = round((potencia_dia[0][x])/3600000,4)
                        eixo_x_dia[0][x] = dias_do_mes[0][x]
                    i = 1 + i

                # Conta a quantidade de valores do Vetor
                posicao2 = len(eixo_x_dia[0])
                dia = True

            # Se nao houver registro diario
            else:
                print("Não há Registros Mensais.")
                dia = False

            # SELECT por ANO
            cursor.execute("SELECT * FROM medicao  WHERE YEAR(horario) = %s ORDER BY horario DESC ", selecao_ano)
            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                i = 0
                res = np.array([[0] * 5] * cursor.rowcount, dtype=np.int64)

                for linha in resultado:
                    res[i][0] = linha[0]
                    res[i][2] = linha[2]
                    res[i][3] = linha[3]
                    res[i][4] = linha[4]

                    data = linha[1].strftime('%m')
                    res[i][1] = data
                    # Identifica a quantidade de Dias Diferentes no Mês
                    p = 1
                    for x in range(0, i - 1):
                        if res[x][1] != res[x + 1][1]:
                            p = p + 1
                    # Cria Eixos do tamanho adequado
                    eixo_x_mes = np.zeros((1, p))
                    eixo_y_mes = np.zeros((1, p))

                    n = 0
                    mes_do_ano = np.zeros((1, p))
                    mes_do_ano[0][n] = res[0][1]

                    potencia_mes = np.zeros((1, p))
                    # Atribuiu os valores dos dias no Eixo X
                    for x in range(0, i - 1):
                        if res[x][1] != res[x + 1][1]:
                            mes_do_ano[0][n + 1] = res[x + 1][1]
                            n = n + 1
                    n = 0

                    potencia_mes[0][0] = res[0][4]
                    # Atribui os valores das Potencias no Eixo Y
                    for x in range(0, i - 1):
                        if res[x][1] == res[x + 1][1]:
                            potencia_mes[0][n] = potencia_mes[0][n] + res[x + 1][4]
                        elif res[x][1] != res[x + 1][1]:
                            n = n + 1
                            potencia_mes[0][n] = res[x + 1][4]
                    potencia_mes[0][n] = potencia_mes[0][n] + res[i][4]
                    i = 1 + i

                    for x in range(0, p):
                        eixo_y_mes[0][x] = round((potencia_mes[0][x])/3600000,4)
                        eixo_x_mes[0][x] = mes_do_ano[0][x]
                # Conta a quantidade de valores do Vetor
                posicao3 = len(eixo_x_mes[0])
                mes = True
            # Se não houver registro mensal
            else:
                print("Não Há Registros Anuais.")
                mes = False
            conexao.close()

            # IFS para escrever os valores ABA DIARIA
            if hora == True:
                for x in range(0, posicao1):
                    if eixo_x_hora[0][x] == 1:
                        self.ui2.txt_hora_1.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 2:
                        self.ui2.txt_hora_2.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 3:
                        self.ui2.txt_hora_3.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 4:
                        self.ui2.txt_hora_4.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 5:
                        self.ui2.txt_hora_5.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 6:
                        self.ui2.txt_hora_6.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 7:
                        self.ui2.txt_hora_7.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 8:
                        self.ui2.txt_hora_8.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 9:
                        self.ui2.txt_hora_9.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 10:
                        self.ui2.txt_hora_10.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 11:
                        self.ui2.txt_hora_11.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 12:
                        self.ui2.txt_hora_12.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 13:
                        self.ui2.txt_hora_13.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 14:
                        self.ui2.txt_hora_14.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 15:
                        self.ui2.txt_hora_15.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 16:
                        self.ui2.txt_hora_16.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 17:
                        self.ui2.txt_hora_17.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 18:
                        self.ui2.txt_hora_18.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 19:
                        self.ui2.txt_hora_19.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 20:
                        self.ui2.txt_hora_20.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 21:
                        self.ui2.txt_hora_21.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 22:
                        self.ui2.txt_hora_22.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 23:
                        self.ui2.txt_hora_23.setText(str(eixo_y_hora[0][x]))
                    if eixo_x_hora[0][x] == 00:
                        self.ui2.txt_hora_24.setText(str(eixo_y_hora[0][x]))

            # IFS para escrever os valores ABA MENSAL
            if dia == True:
                for x in range(0, posicao2):
                    if eixo_x_dia[0][x] == 1:
                        self.ui2.txt_dia_1.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 2:
                        self.ui2.txt_dia_2.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 3:
                        self.ui2.txt_dia_3.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 4:
                        self.ui2.txt_dia_4.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 5:
                        self.ui2.txt_dia_5.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 6:
                        self.ui2.txt_dia_6.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 7:
                        self.ui2.txt_dia_7.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 8:
                        self.ui2.txt_dia_8.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 9:
                        self.ui2.txt_dia_9.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 10:
                        self.ui2.txt_dia_10.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 11:
                        self.ui2.txt_dia_11.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 12:
                        self.ui2.txt_dia_12.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 13:
                        self.ui2.txt_dia_13.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 14:
                        self.ui2.txt_dia_14.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 15:
                        self.ui2.txt_dia_15.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 16:
                        self.ui2.txt_dia_16.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 17:
                        self.ui2.txt_dia_17.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 18:
                        self.ui2.txt_dia_18.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 19:
                        self.ui2.txt_dia_19.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 20:
                        self.ui2.txt_dia_20.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 21:
                        self.ui2.txt_dia_21.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 22:
                        self.ui2.txt_dia_22.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 23:
                        self.ui2.txt_dia_23.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 24:
                        self.ui2.txt_dia_24.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 25:
                        self.ui2.txt_dia_25.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 26:
                        self.ui2.txt_dia_26.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 27:
                        self.ui2.txt_dia_27.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 28:
                        self.ui2.txt_dia_28.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 29:
                        self.ui2.txt_dia_29.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 30:
                        self.ui2.txt_dia_30.setText(str(eixo_y_dia[0][x]))
                    if eixo_x_dia[0][x] == 31:
                        self.ui2.txt_dia_31.setText(str(eixo_y_dia[0][x]))

            # IFS para escrever os valores ABA ANUAL
            if mes == True:
                for x in range(0, posicao3):
                    if eixo_x_mes[0][x] == 1:
                        self.ui2.txt_mes_1.setText(str(eixo_y_mes[0][x]))
                    if eixo_x_mes[0][x] == 2:
                        self.ui2.txt_mes_2.setText(str(eixo_y_mes[0][x]))
                    if eixo_x_mes[0][x] == 3:
                        self.ui2.txt_mes_3.setText(str(eixo_y_mes[0][x]))
                    if eixo_x_mes[0][x] == 4:
                        self.ui2.txt_mes_4.setText(str(eixo_y_mes[0][x]))
                    if eixo_x_mes[0][x] == 5:
                        self.ui2.txt_mes_5.setText(str(eixo_y_mes[0][x]))
                    if eixo_x_mes[0][x] == 6:
                        self.ui2.txt_mes_6.setText(str(eixo_y_mes[0][x]))
                    if eixo_x_mes[0][x] == 7:
                        self.ui2.txt_mes_7.setText(str(eixo_y_mes[0][x]))
                    if eixo_x_mes[0][x] == 8:
                        self.ui2.txt_mes_8.setText(str(eixo_y_mes[0][x]))
                    if eixo_x_mes[0][x] == 9:
                        self.ui2.txt_mes_9.setText(str(eixo_y_mes[0][x]))
                    if eixo_x_mes[0][x] == 10:
                        self.ui2.txt_mes_10.setText(str(eixo_y_mes[0][x]))
                    if eixo_x_mes[0][x] == 11:
                        self.ui2.txt_mes_11.setText(str(eixo_y_mes[0][x]))
                    if eixo_x_mes[0][x] == 12:
                        self.ui2.txt_mes_12.setText(str(eixo_y_mes[0][x]))

        # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:

            print("Error while connecting to MySQL", e)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText(".::Erro de Conexão com o Banco de Dados::.")
            msg.setInformativeText("Falha na Comunicação com o Servidor!")
            msg.setWindowTitle("Erro na Inicialização")
            msg.setDetailedText(
                "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

    def openWindow(self):
        btn_info = 1
        self.window = QtWidgets.QMainWindow()
        self.ui2 = Ui_InfoWindow()
        self.ui2.setupUi(self.window)
        self.window.setWindowTitle('Histórico de Consumo')

        wRectangle = self.window.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        wRectangle.moveCenter(centerPoint)
        self.window.move(wRectangle.topLeft())
        self.window.show()
        selecao = self.ui.comboBox.currentText()
        if selecao == 'Diário':
            aba = 0
        elif selecao == 'Mensal':
            aba = 1
        elif selecao == 'Anual':
            aba = 2

        self.ui2.tabWidget2.setCurrentIndex(aba)

        self.history()

    def consumo_mensal(self):
        global teste_conexao


        data_atual = datetime.now()
        mes = int(data_atual.strftime('%m'))
        i = 0
        # Abrimos uma conexão com o banco de dados:
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')

            # Cria um cursor:
            cursor = conexao.cursor()

            # Executa o comando:
            cursor.execute("SELECT * FROM medicao  WHERE MONTH(horario) = %s ORDER BY horario DESC ", mes)

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                print("Numero de Registros: ", cursor.rowcount)
                res = np.array([[0] * 5] * cursor.rowcount,dtype=np.float64)
                # print(res, "\n")
                # print("\nDados:")
                for linha in resultado:
                    # print("Id = ", linha[0])
                    # print("Horário = ", linha[1])
                    # print("Corrente   = ", linha[2])
                    # print("Tensão  = ", linha[3])
                    # print("Potência  = ", linha[4], "\n")
                    data = linha[1].strftime('%d%m%Y%H%M%S')
                    valor = int(data)

                    res[i][0] = linha[0]
                    res[i][1] = valor
                    res[i][2] = linha[2]
                    res[i][3] = linha[3]
                    res[i][4] = linha[4]

                    i = i + 1

                # Somatorio do Consumo Total
                consumo_total = 0
                for x in range(0, i):
                    consumo_total = consumo_total + res[x][4]
                consumo_total=(consumo_total)/3600000 #Dividindo por 3600000 para conversão para kWh
                # Atualização dos Valores da Interface
                self.ui.consumo_instantaneo.setText(str(res[0][4]))
                self.ui.consumo_mensal.setText(str(round(consumo_total,4)))
            else:
                print("Dados Insuficientes no Banco de Dados")
            # Finaliza a conexão
            conexao.close()
            teste_conexao = 0

            # Threading para Consultas do BD
            # s = threading.Timer(15, self.consumo_mensal)
            # s.start()

        # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText(
                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

            # s = threading.Timer(15, self.consumo_mensal)
            # s.start()

    def seta_data_grafico(self):
        # Variáveis setadas como Globais para usar no decorrer da função
        global data_atual
        global dia
        global mes
        global ano
        # Identifica a data atual
        data_atual = datetime.now()
        dia = int(data_atual.strftime('%d'))
        mes = int(data_atual.strftime('%m'))
        ano = int(data_atual.strftime('%Y'))

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')

            # Cria um cursor:
            cursor = conexao.cursor()
            # Recupera o Ultimo e o Primeiro Ano do BD para setar no ComboBox
            cursor.execute("SELECT horario FROM medicao  ORDER BY horario DESC LIMIT 1")
            # Recupera o resultado:
            resultado = cursor.fetchall()

            if cursor.rowcount > 0:
                for linha in resultado:
                    ultimo_ano = int(linha[0].strftime('%Y'))
            cursor.execute("SELECT horario FROM medicao  ORDER BY horario ASC LIMIT 1")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    primeiro_ano = int(linha[0].strftime('%Y'))
            else:
                print("Dados Insuficientes no Banco de Dados")

            # Finaliza a conexão
            conexao.close()

        # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            print("Error while connecting to MySQL", e)
        # Escreve na ComboBox o Primeiro e Ultimo Ano
        for x in range(ultimo_ano, primeiro_ano - 1, -1):
            self.ui.comboBox_Ano.addItem(str(x))

        # Escreve nas ComboBoxs as datas Atuais
        self.ui.comboBox_Mes.setCurrentText(str(mes))
        self.ui.comboBox_Dia.setCurrentText(str(dia))
        self.ui.comboBox_Ano.setCurrentText(str(ano))

    def update_graph(self):
        # Variaveis Globais para a Função
        global potencia_dia
        global dias_do_mes
        global botao_info
        global auto_update_graph
        potencia_dia = 0

        # Captura os valores das ComboBoxs
        selecao = self.ui.comboBox.currentText()
        selecao_dia = self.ui.comboBox_Dia.currentText()
        selecao_mes = self.ui.comboBox_Mes.currentText()
        selecao_ano = self.ui.comboBox_Ano.currentText()

        i = 0
        # Abrimos uma conexão com o banco de dados:
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')

            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando de Acordo com o tipo da ComboBox:
            if selecao == 'Diário':
                cursor.execute(
                    "SELECT * FROM medicao  WHERE DAY(horario) = %s AND MONTH(horario) = %s AND YEAR(horario) = %s ORDER BY horario DESC ",
                    (selecao_dia, selecao_mes, selecao_ano))
            elif selecao == 'Mensal':
                cursor.execute(
                    "SELECT * FROM medicao  WHERE MONTH(horario) = %s AND YEAR(horario) = %s ORDER BY horario DESC ",
                    (selecao_mes, selecao_ano))
            elif selecao == 'Anual':
                cursor.execute("SELECT * FROM medicao  WHERE YEAR(horario) = %s ORDER BY horario DESC ", selecao_ano)

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                res = np.array([[0] * 5] * cursor.rowcount, dtype=np.int64)
                for linha in resultado:
                    res[i][0] = linha[0]
                    res[i][2] = linha[2]
                    res[i][3] = linha[3]
                    res[i][4] = linha[4]
                    # Caso selecao em Diario
                    if selecao == 'Diário':
                        # Classifica o Eixo por Dia
                        data = linha[1].strftime('%H')
                        res[i][1] = data
                        # Identifica a quantidade de Dias Diferentes no Mês
                        p = 1
                        for x in range(0, cursor.rowcount - 1):
                            if res[x][1] != res[x + 1][1]:
                                p = p + 1

                        # Cria Eixos do tamanho adequado
                        eixo_x = np.zeros((1, p))
                        eixo_y = np.zeros((1, p))

                        n = 0
                        horas_do_dia = np.zeros((1, p))
                        horas_do_dia[0][n] = res[0][1]
                        potencia_dia = np.zeros((1, p))
                        # Atribuiu os valores dos dias no Eixo X
                        for x in range(0, cursor.rowcount - 1):
                            if res[x][1] != res[x + 1][1]:
                                horas_do_dia[0][n + 1] = res[x + 1][1]
                                n = n + 1
                        n = 0

                        # Atribui os valores das Potencias no Eixo Y
                        potencia_dia[0][0] = res[0][4]
                        for x in range(0, cursor.rowcount - 1):
                            if res[x][1] == res[x + 1][1]:
                                potencia_dia[0][n] = potencia_dia[0][n] + res[x + 1][4]
                            elif res[x][1] != res[x + 1][1]:
                                n = n + 1
                                potencia_dia[0][n] = res[x + 1][4]


                    # Caso selecao em Mes
                    elif selecao == 'Mensal':
                        # Classifica o Eixo por Dia
                        data = linha[1].strftime('%d')
                        res[i][1] = data
                        # Identifica a quantidade de Dias Diferentes no Mês
                        p = 1
                        for x in range(0, i):
                            if res[x][1] != res[x + 1][1]:
                                p = p + 1
                        # Cria Eixos do tamanho adequado
                        eixo_x = np.zeros((1, p))
                        eixo_y = np.zeros((1, p))

                        n = 0
                        dias_do_mes = np.zeros((1, p))
                        dias_do_mes[0][n] = res[0][1]

                        potencia_dia = np.zeros((1, p))
                        # Atribuiu os valores dos dias no Eixo X
                        for x in range(0, i):
                            if res[x][1] != res[x + 1][1]:
                                dias_do_mes[0][n + 1] = res[x + 1][1]
                                n = n + 1
                        n = 0
                        # Atribui os valores das Potencias no Eixo Y
                        potencia_dia[0][0] = res[0][4]
                        for x in range(0, i):
                            if res[x][1] == res[x + 1][1]:
                                potencia_dia[0][n] = potencia_dia[0][n] + res[x + 1][4]
                            elif res[x][1] != res[x + 1][1]:
                                n = n + 1
                                potencia_dia[0][n] = res[x + 1][4]
                        # Correcao do BUG mensal
                        # if i != 0:
                        #     potencia_dia[0][n] = potencia_dia[0][n] + res[i][4]

                    # Caso selecao em Ano
                    elif selecao == 'Anual':
                        # Classifica o Eixo por Dia
                        data = linha[1].strftime('%m')
                        res[i][1] = data
                        # Identifica a quantidade de Dias Diferentes no Mês
                        p = 1
                        for x in range(0, i - 1):
                            if res[x][1] != res[x + 1][1]:
                                p = p + 1
                        # Cria Eixos do tamanho adequado
                        eixo_x = np.zeros((1, p))
                        eixo_y = np.zeros((1, p))

                        n = 0
                        mes_do_ano = np.zeros((1, p))
                        mes_do_ano[0][n] = res[0][1]

                        potencia_mes = np.zeros((1, p))
                        # Atribuiu os valores dos dias no Eixo X
                        for x in range(0, i - 1):
                            if res[x][1] != res[x + 1][1]:
                                mes_do_ano[0][n + 1] = res[x + 1][1]
                                n = n + 1
                        n = 0

                        # Atribui os valores das Potencias no Eixo Y
                        potencia_mes[0][0] = res[0][4]
                        for x in range(0, i - 1):
                            if res[x][1] == res[x + 1][1]:
                                potencia_mes[0][n] = potencia_mes[0][n] + res[x + 1][4]
                            elif res[x][1] != res[x + 1][1]:
                                n = n + 1
                                potencia_mes[0][n] = res[x + 1][4]
                        potencia_mes[0][n] = potencia_mes[0][n] + res[i][4]
                    i = 1 + i

                # Cria um Interrupt caso seja selecionado Diário, para recarregar a cada hora.
                if selecao == 'Diário':
                    for x in range(0, p):
                        eixo_y[0][x] = potencia_dia[0][x]/3600000
                        eixo_x[0][x] = horas_do_dia[0][x]
                    # u = threading.Timer(3600, self.update_graph)
                    # u.start()
                # Atribui as variáveis nos eixos para Apresentar
                if selecao == 'Mensal':
                    for x in range(0, p):
                        eixo_y[0][x] = potencia_dia[0][x]/3600000
                        eixo_x[0][x] = dias_do_mes[0][x]
                # Atribui as variáveis nos eixos para Apresentar
                if selecao == 'Anual':
                    for x in range(0, p):
                        eixo_y[0][x] = potencia_mes[0][x]/3600000
                        eixo_x[0][x] = mes_do_ano[0][x]

                # Cria os Graficos
                self.ui.MplWidget.canvas.axes.clear()
                # Bolas
                self.ui.MplWidget.canvas.axes.plot(eixo_x[0], eixo_y[0], 'or', linewidth=8)
                # Linhas
                self.ui.MplWidget.canvas.axes.plot(eixo_x[0], eixo_y[0], 'r', linewidth=3)
                # Barras
                self.ui.MplWidget.canvas.axes.bar(eixo_x[0], eixo_y[0])
                # Apresenta os valores nos eixos
                for p in self.ui.MplWidget.canvas.axes.patches:
                    self.ui.MplWidget.canvas.axes.annotate("%.4f" % p.get_height(),
                                                           (p.get_x() + p.get_width() / 2., p.get_height()),
                                                           ha='center', va='center', fontsize=11, color='gray',
                                                           xytext=(0, 20),
                                                           textcoords='offset points')
                # Seta os limites do Eixo Y para os valores nas barras nao Ultrapassar o Grafico

                self.ui.MplWidget.canvas.axes.set_ylim(0, max(eixo_y[0]) + 0.15 * max(eixo_y[0]))
                self.ui.MplWidget.canvas.axes.legend(['Consumo Diário'], loc='upper right')
                self.ui.MplWidget.canvas.axes.set_xticks(eixo_x[0])
                self.ui.MplWidget.canvas.axes.set_title('Gráficos do Consumo')
                self.ui.MplWidget.canvas.axes.set_ylabel('Potência [kWh]')
                # Classifica as unidades dos eixos de acordo com as selecoes
                if selecao == 'Diário':
                    self.ui.MplWidget.canvas.axes.legend(['Consumo Diário'], loc='upper right')
                    self.ui.MplWidget.canvas.axes.set_xlabel('Tempo [Hora]')
                elif selecao == 'Mensal':
                    self.ui.MplWidget.canvas.axes.legend(['Consumo Mensal'], loc='upper right')
                    self.ui.MplWidget.canvas.axes.set_xlabel('Tempo [Dia]')
                elif selecao == 'Anual':
                    self.ui.MplWidget.canvas.axes.legend(['Consumo Anual'], loc='upper right')
                    self.ui.MplWidget.canvas.axes.set_xlabel('Tempo [Mês]')

                self.ui.MplWidget.canvas.axes.grid()
                self.ui.MplWidget.canvas.draw()

                # Habilita Botao Info
                self.ui.btn_info.setEnabled(True)
                botao_info = True
                #Variavel para correção do BUG janela de data errada
                auto_update_graph=False
                return eixo_x, eixo_y, selecao
            # Apresenta as mensagens de erro caso as datas não forem encontradas
            else:
                # Variavel para correção do BUG janela de data errada
                auto_update_graph = True

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Data!::.")
                msg.setInformativeText("A Data Selecionada não possui Registros.")
                msg.setWindowTitle("Data Indisponível")
                msg.setDetailedText(
                        "Por favor, altere a Data Selecionada\nConfira se o Dia selecionado corresponde corretamente ao mês escolhido.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                # Desabilita Botao para evitar erro.
                self.ui.btn_info.setEnabled(False)
                botao_info = True


            # Finaliza a conexão
            conexao.close()


        # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            print("Error while connecting to MySQL", e)

    def backup(self):
        ano_atual = datetime.now().year
        mes_atual = datetime.now().month
        dia_atual = datetime.now().day
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute(
                "SELECT date_backup FROM configuracao_user  WHERE id=1")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    date_backup = linha[0]
            # Se o mês atual for diferente do ultimo mes da condensação, significa que se passou 1 mês e é hora de executar novamente,
            if dia_atual != date_backup.day:
                saida = backup()
                self.ui.textBrowser.append(saida)

                # Atualização da data atual para comparação
                data_atual = datetime.now()
                # Atualização da data atual no BD
                cursor.execute("UPDATE configuracao_user SET date_agrupamento_medicoes=%s WHERE id=1", data_atual)

                conexao.close()
        except pymysql.err.OperationalError as e:
            print("Error while connecting to MySQL", e)

    def restaurar(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText(".::Não é Possível fazer a Restauração::.")
        msg.setInformativeText("")
        msg.setWindowTitle("Restauração")
        msg.setDetailedText(
            "Para Restaurar o último Backup,\nContacte o engenheiro responsável para fazê-lo manualmente.")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

    def agrupamento_medicoes(self):
        print("Verificando mudança de Horário")
        global hora_inicial
        global teste_conexao
        #Capta a hora atual e zera os minutos e segundos
        time_now=datetime.now().replace(minute=00,second=00,microsecond=00)
        #Capta horário que o programa se iniciou
        ano = hora_inicial.year
        mes=hora_inicial.month
        dia=hora_inicial.day
        hora=hora_inicial.hour
        microsec=hora_inicial.microsecond
        #Se a hora for diferente da hora inicial, faz a condensação das medições da hora que passou
        if time_now != hora_inicial:

            print("Realizando Condensação dos registros de medições")

            try:
                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
                # Executa o comando:
                cursor.execute("SELECT * FROM medicao  WHERE YEAR(horario) = %s AND MONTH(horario) = %s AND DAY(horario) = %s AND HOUR(horario) = %s ORDER BY horario DESC ", (ano,mes,dia,hora))
                # Recupera o resultado:
                resultado = cursor.fetchall()
                if cursor.rowcount > 0:
                    print("Quantidade de medições: ", cursor.rowcount)
                    res = np.array([[0] * 5] * cursor.rowcount,dtype=np.float)
                    i=0
                    for linha in resultado:
                        data = linha[1]

                        res[i][0] = linha[0]
                        #res[i][1] = valor
                        res[i][2] = linha[2]
                        res[i][3] = linha[3]
                        res[i][4] = linha[4]

                        i+=1

                    #print(res)
                    corrente=0
                    tensao=0
                    potencia=0
                    #Somatorio de todas as medições
                    for x in range(0, cursor.rowcount):
                        corrente=res[x][2]+corrente
                        tensao = res[x][3] + tensao
                        potencia=res[x][4] + potencia
                    #Modificação dos horários de registros, para retirar os minutos e segundos
                    newdate = data.replace(minute=00,second=00)
                    #Media das correntes e tensões
                    corrente=round(corrente/cursor.rowcount,3)
                    tensao = round(tensao / cursor.rowcount,3)
                    print("\nCorrente media:{}A, Tensão Media:{}V, Potencia Média:{}kWh\n".format(corrente,tensao,potencia))

                    cursor.execute("DELETE FROM medicao WHERE YEAR(horario) = %s AND MONTH(horario) = %s AND DAY(horario) = %s AND HOUR(horario) = %s ORDER BY horario DESC ", (ano,mes,dia,hora))
                    print("Medições não condensadas, DELETADAS")

                    cursor.execute("INSERT INTO medicao (horario,corrente,tensao,potencia) VALUES(%s,%s,%s,%s)",(newdate,float(corrente),float(tensao),float(potencia)))
                    print("Potência Condensada, registrada\n")

                    conexao.close()
                    #Atribui uma nova hora para comparação
                    hora_inicial = datetime.now().replace(minute=00,second=00,microsecond=00)
                else:
                    print("Dados Insuficientes no Banco de Dados")
                    # Finaliza a conexão
                    conexao.close()
                    teste_conexao = 0
            except pymysql.err.OperationalError as e:
                if teste_conexao == 0:
                    print("Error while connecting to MySQL", e)

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)

                    msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                    msg.setInformativeText("Falha na Comunicação com o Servidor!")
                    msg.setWindowTitle("Erro na Inicialização")
                    msg.setDetailedText(
                        "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.exec_()
                    teste_conexao = 1

    def agrupamento_medicoes_diario(self):
        ano_atual=datetime.now().year
        mes_atual=datetime.now().month
        dia_atual=datetime.now().day
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute(
                "SELECT date_agrupamento_medicoes, agrupamento_medicoes FROM configuracao_user  WHERE id=1")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    date_agrupamentos = linha[0]
                    status_agrupamento=linha[1]
            #Se o mês atual for diferente do ultimo mes da condensação, significa que se passou 1 mês e é hora de executar novamente,
            if dia_atual!=date_agrupamentos.day:
                cursor.execute(
                    "SELECT * FROM medicao  WHERE YEAR(horario) = %s AND MONTH(horario) = %s AND DAY(horario) = %s ORDER BY horario DESC ",
                    (date_agrupamentos.year, date_agrupamentos.month, date_agrupamentos.day))
                # Recupera o resultado:
                resultado = cursor.fetchall()
                if cursor.rowcount > 0:
                    #print("Quantidade de medições: ", cursor.rowcount)
                    res = np.array([[0] * 5] * cursor.rowcount,dtype='<U22')

                    i = 0
                    for linha in resultado:
                        data = linha[1]

                        res[i][0] = linha[0]
                        res[i][1] = linha[1]
                        res[i][2] = linha[2]
                        res[i][3] = linha[3]
                        res[i][4] = linha[4]

                        i += 1
                    #Criação do vetor agrupamento para
                    agrupamentos = np.array([[0] * 5] , dtype='<U22')
                    #Atribui o primeiro resultado do BD ao vetor
                    agrupamentos[0]=res[0]
                    #Atribui o ID 0
                    agrupamentos[0][0]=0

                    n=0
                    for x in range(0, cursor.rowcount):
                        #Trava para impedir o erro de Index
                        if x+1<cursor.rowcount:
                            #Criação de objetos datas
                            data_obj_1 = datetime.strptime(res[x][1], '%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                            data_obj_2 = datetime.strptime(res[x+1][1], '%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                            #Comparações. Caso a hora das duas datas sejam as mesmas, elas se agrupam
                            if data_obj_1.hour==data_obj_2.hour:
                                agrupamentos[n][4]=float(agrupamentos[n][4])+float(res[x+1][4])
                            #Se nao, ha o aumento do vetor agrupamentos e a atribuiçao da nova medida
                            else:
                                agrupamentos = np.resize(agrupamentos, (len(agrupamentos) + 1, 5))
                                agrupamentos[n+1]=res[x+1]
                                agrupamentos[n+1][0]=n+1
                                n+=1

                    #Delete no BD, as medidas que foram agrupadas
                    for x in range(0,cursor.rowcount):
                        id=res[x][0]
                        cursor.execute("DELETE FROM medicao WHERE  id = %s ",id)
                    print("\nMedições não condensadas, DELETADAS\n")
                    #Inserção do novo agrupamento novamente no BD
                    for x in range(0,n+1):
                        newdate=datetime.strptime(agrupamentos[x][1], '%Y-%m-%d %H:%M:%S')
                        corrente=agrupamentos[x][2]
                        tensao=agrupamentos[x][3]
                        potencia=agrupamentos[x][4]
                        cursor.execute("INSERT INTO medicao (horario,corrente,tensao,potencia) VALUES(%s,%s,%s,%s)",
                                       (newdate, float(corrente), float(tensao), float(potencia)))
                    print("Potência Condensada, registrada\n")

                    #Atualização da data atual para comparação
                    data_atual = datetime.now()
                    #Atualização da data atual no BD
                    cursor.execute("UPDATE configuracao_user SET date_agrupamento_medicoes=%s WHERE id=1", data_atual)

                    conexao.close()
        except pymysql.err.OperationalError as e:
            print("Error while connecting to MySQL", e)

    def change_slider_ilum(self):
        valor = self.ui.horizontalSlider.value()
        self.ui.label_10.setText(str(valor))

    def update_intensidade_iluminacao(self):
        valor = self.ui.horizontalSlider.value()
        self.lamp_control(valor)

        teste_conexao = 0
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("UPDATE configuracao_user SET intensidade_iluminacao=%s WHERE id=1", valor)
            conexao.close()

        # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText(
                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def btn_on_lamp(self):
        #Atualiza estado do Check Controle
        self.ui.check_Controle.setCheckState(False)
        self.update_Controle()
        #Atualiza estado da Lâmpada
        self.update_estado_iluminacao_on()

    def btn_off_lamp(self):
        #Desabilita o Check Control
        self.ui.check_Controle.setCheckState(False)
        self.update_Controle()
        #Atualiza estado da Lâmpada
        self.update_estado_iluminacao_off()

    def update_estado_iluminacao_on(self):

        controle=self.check_controle()
        if controle==False:
            valor = self.ui.horizontalSlider.value()
            self.lamp_control(valor)
            self.ui.horizontalSlider.setEnabled(True)

        teste_conexao = 0


        self.ui.btn_on_ilum.setEnabled(False)
        self.ui.btn_off_ilum.setEnabled(True)
        self.ui.txt_state_lamp.setText("Ligada")

        data_atual = datetime.now()
        data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')
        # Ação e Valor que recebe
        acao = "Iluminacao"
        valor = True

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("UPDATE configuracao_user SET estado_iluminacao=%s WHERE id=1", valor)

            cursor.execute("INSERT INTO historico_acoes (acao,valor,horario) VALUES(%s,%s,%s)", (acao, valor, data_db))
            conexao.close()

            # msg = QMessageBox()
            # msg.setIcon(QMessageBox.Information)
            #
            # msg.setText(".::Dado Salvo com Sucesso::.")
            # msg.setInformativeText("Sua Iluminação foi Ligada!")
            # msg.setWindowTitle("Sucesso!")
            #
            # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # msg.exec_()
        # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText(
                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def update_estado_iluminacao_off(self):
        global verify_lamp_economic
        verify_lamp_economic = False
        valor = self.ui.horizontalSlider.value()
        self.lamp_control(0)
        teste_conexao = 0
        self.ui.horizontalSlider.setEnabled(False)
        self.ui.btn_off_ilum.setEnabled(False)
        self.ui.btn_on_ilum.setEnabled(True)
        self.ui.txt_state_lamp.setText("Desligada")

        data_atual = datetime.now()
        data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')
        # Ação e Valor que recebe
        acao = "Iluminacao"
        valor = False

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("UPDATE configuracao_user SET estado_iluminacao=%s WHERE id=1", valor)
            conexao.close()

            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("INSERT INTO historico_acoes (acao,valor,horario) VALUES(%s,%s,%s)", (acao, valor, data_db))
            conexao.close()

            # msg = QMessageBox()
            # msg.setIcon(QMessageBox.Information)
            #
            # msg.setText(".::Dado Salvo com Sucesso::.")
            # msg.setInformativeText("Sua Iluminação foi Desligada!")
            # msg.setWindowTitle("Sucesso!")
            #
            # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # msg.exec_()

        # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText(
                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def update_temp(self):
        valor = self.ui.txt_temp.toPlainText()
        if valor=="":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText(".::Erro de Valor::.")
            msg.setInformativeText("Falha na Comunicação com o Servidor!")
            msg.setWindowTitle("Erro na Inicialização")
            msg.setDetailedText(
                "A temperatura não pode ser vazia!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
        else:
            teste_conexao = 0

            try:
                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')

                # Cria um cursor:
                cursor = conexao.cursor()

                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET temperatura=%s WHERE id=1", valor)
                conexao.close()

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText(".::Dado Salvo com Sucesso::.")
                msg.setInformativeText("Sua Temperatura foi Alterada!")
                msg.setWindowTitle("Sucesso!")

                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

            # Caso a Conexão dê errado:
            except pymysql.err.OperationalError as e:
                if teste_conexao == 0:
                    print("Error while connecting to MySQL", e)

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)

                    msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                    msg.setInformativeText("Falha na Comunicação com o Servidor!")
                    msg.setWindowTitle("Erro na Inicialização")
                    msg.setDetailedText(
                        "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.exec_()
                    teste_conexao = 1

    def update_temp_banho_economic(self):
        valor = self.ui.txt_temp_agua_economic.toPlainText()
        try:
            #Variável CHECK NAN......Não retirar!
            check_nan=int(valor)

            teste_conexao = 0

            try:
                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')

                # Cria um cursor:
                cursor = conexao.cursor()

                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET temp_banho_economic=%s WHERE id=1", valor)
                conexao.close()

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText(".::Dado Salvo com Sucesso::.")
                msg.setInformativeText("Sua Temperatura do Banho Econômico foi Alterada!")
                msg.setWindowTitle("Sucesso!")

                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

            # Caso a Conexão dê errado:
            except pymysql.err.OperationalError as e:
                if teste_conexao == 0:
                    print("Error while connecting to MySQL", e)

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)

                    msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                    msg.setInformativeText("Falha na Comunicação com o Servidor!")
                    msg.setWindowTitle("Erro na Inicialização")
                    msg.setDetailedText(
                        "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.exec_()
                    teste_conexao = 1

        except:
            self.ui.txt_temp_agua_economic.setText("")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText(".::Erro de Valor::.")
            msg.setInformativeText("Falha na Comunicação com o Servidor!")
            msg.setWindowTitle("Erro na Inicialização")
            msg.setDetailedText(
                "A temperatura deve ser um número inteiro!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

    def update_temp_banho_normal(self):
        valor = self.ui.txt_temp_agua_normal.toPlainText()
        try:
            #Variável CHECK NAN......Não retirar!
            check_nan=int(valor)

            teste_conexao = 0

            try:
                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')

                # Cria um cursor:
                cursor = conexao.cursor()

                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET temp_banho_normal=%s WHERE id=1", valor)
                conexao.close()

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)

                msg.setText(".::Dado Salvo com Sucesso::.")
                msg.setInformativeText("Sua Temperatura do Banho Normal foi Alterada!")
                msg.setWindowTitle("Sucesso!")

                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

            # Caso a Conexão dê errado:
            except pymysql.err.OperationalError as e:
                if teste_conexao == 0:
                    print("Error while connecting to MySQL", e)

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)

                    msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                    msg.setInformativeText("Falha na Comunicação com o Servidor!")
                    msg.setWindowTitle("Erro na Inicialização")
                    msg.setDetailedText(
                        "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.exec_()
                    teste_conexao = 1

        except:
            self.ui.txt_temp_agua_normal.setText("")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText(".::Erro de Valor::.")
            msg.setInformativeText("Falha na Comunicação com o Servidor!")
            msg.setWindowTitle("Erro na Inicialização")
            msg.setDetailedText(
                "A temperatura deve ser um número inteiro!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

    def update_temp_ar_mais(self):

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT ar_condicionado FROM configuracao_user  WHERE id=1")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    ar_ligado = linha[0]
            if ar_ligado == False:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Error::.")
                msg.setInformativeText("O Ar Condicionado se Encontra Desligado")
                msg.setWindowTitle("Ar Desligado")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

                conexao.close()
            else:
                self.temp_mais_ar()

                valor = int(self.ui.text_temp_ar.text()) + 1
                self.ui.text_temp_ar.setText(str(valor))
                teste_conexao = 0
                data_atual = datetime.now()
                data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')
                # Ação e Valor que recebe
                acao = "Temperatura-Ar-Mais"

                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET temp_ar=%s WHERE id=1", valor)
                valor = True

                #Verifica Acionamento da aprendizagem
                aprendizagem = self.check_aprendizagem()
                if aprendizagem == True:
                    cursor.execute("INSERT INTO historico_acoes (acao,valor,horario) VALUES(%s,%s,%s)",
                                   (acao, valor, data_db))
                conexao.close()

            # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText("Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def update_temp_ar_menos(self):

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT ar_condicionado FROM configuracao_user  WHERE id=1")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    ar_ligado = linha[0]
            if ar_ligado == False:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Error::.")
                msg.setInformativeText("O Ar Condicionado se Encontra Desligado")
                msg.setWindowTitle("Ar Desligado")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

                conexao.close()
            else:
                self.temp_menos_ar()
                valor = int(self.ui.text_temp_ar.text()) - 1
                self.ui.text_temp_ar.setText(str(valor))
                teste_conexao = 0

                data_atual = datetime.now()
                data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')
                # Ação e Valor que recebe
                acao = "Temperatura-Ar-Menos"

                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET temp_ar=%s WHERE id=1", valor)

                valor = False

                # Verifica Acionamento da aprendizagem
                aprendizagem = self.check_aprendizagem()
                if aprendizagem == True:
                    # Executa o comando:
                    cursor.execute("INSERT INTO historico_acoes (acao,valor,horario) VALUES(%s,%s,%s)",
                                   (acao, valor, data_db))
                conexao.close()



            # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText("Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def update_volume_mais(self):

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT televisao FROM configuracao_user  WHERE id=1")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    tv_ligada = linha[0]
            if tv_ligada == False:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Error::.")
                msg.setInformativeText("A Televisão se Encontra Desligada")
                msg.setWindowTitle("TV Desligada")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

                conexao.close()
            else:
                self.vol_mais_tv()
                valor = int(self.ui.text_vol.text()) + 1
                self.ui.text_vol.setText(str(valor))
                teste_conexao = 0

                data_atual = datetime.now()
                data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')
                # Ação e Valor que recebe
                acao = "Volume-Tv"

                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET volume_tv=%s WHERE id=1", valor)

                valor = True

                # Executa o comando:
                cursor.execute("INSERT INTO historico_acoes (acao,valor,horario) VALUES(%s,%s,%s)",
                               (acao, valor, data_db))
                conexao.close()

            # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText("Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def update_volume_menos(self):

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT televisao FROM configuracao_user  WHERE id=1")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    tv_ligada = linha[0]
            if tv_ligada == False:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Error::.")
                msg.setInformativeText("A Televisão se Encontra Desligada")
                msg.setWindowTitle("TV Desligada")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

                conexao.close()
            else:
                self.vol_menos_tv()
                valor = int(self.ui.text_vol.text()) - 1
                self.ui.text_vol.setText(str(valor))
                teste_conexao = 0

                data_atual = datetime.now()
                data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')
                # Ação e Valor que recebe
                acao = "Volume-Tv"

                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET volume_tv=%s WHERE id=1", valor)

                valor = False

                # Executa o comando:
                cursor.execute("INSERT INTO historico_acoes (acao,valor,horario) VALUES(%s,%s,%s)",
                               (acao, valor, data_db))
                conexao.close()

            # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText("Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def update_canal_mais(self):

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT televisao FROM configuracao_user  WHERE id=1")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    tv_ligada = linha[0]
            if tv_ligada == False:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Error::.")
                msg.setInformativeText("A Televisão se Encontra Desligada")
                msg.setWindowTitle("TV Desligada")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

                conexao.close()
            else:
                self.canal_mais_tv()
                valor = int(self.ui.text_canal.text()) + 1
                self.ui.text_canal.setText(str(valor))
                teste_conexao = 0

                data_atual = datetime.now()
                data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')
                # Ação e Valor que recebe
                acao = "Canal-Tv"

                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET canais_tv=%s WHERE id=1", valor)

                valor = True

                # Executa o comando:
                cursor.execute("INSERT INTO historico_acoes (acao,valor,horario) VALUES(%s,%s,%s)",
                               (acao, valor, data_db))
                conexao.close()

            # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText("Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def update_canal_menos(self):

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT televisao FROM configuracao_user  WHERE id=1")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    tv_ligada = linha[0]
            if tv_ligada == False:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Error::.")
                msg.setInformativeText("A Televisão se Encontra Desligada")
                msg.setWindowTitle("TV Desligada")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

                conexao.close()
            else:
                self.canal_menos_tv()
                valor = int(self.ui.text_canal.text()) - 1
                self.ui.text_canal.setText(str(valor))
                teste_conexao = 0

                data_atual = datetime.now()
                data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')
                # Ação e Valor que recebe
                acao = "Canal-Tv"

                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET canais_tv=%s WHERE id=1", valor)

                valor = False

                # Executa o comando:
                cursor.execute("INSERT INTO historico_acoes (acao,valor,horario) VALUES(%s,%s,%s)",
                               (acao, valor, data_db))
                conexao.close()

            # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText("Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def update_modo_ar(self):

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT ar_condicionado FROM configuracao_user  WHERE id=1")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    ar_ligado = linha[0]
            if ar_ligado == False:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Error::.")
                msg.setInformativeText("O Ar Condicionado se Encontra Desligado")
                msg.setWindowTitle("Ar Desligado")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

                conexao.close()
            else:
                self.modo_ar()
                # Valor False=Normal | True=Turbo
                data_atual = datetime.now()
                data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')

                acao = "Modo-Ar"

                valor = self.ui.text_modo_ar.text()
                if valor == "Normal":
                    valor = True
                    self.ui.text_modo_ar.setText("Turbo")
                elif valor == "Turbo":
                    valor = False
                    self.ui.text_modo_ar.setText("Normal")
                teste_conexao = 0

                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET modo_ar=%s WHERE id=1", valor)

                # Verifica Acionamento da aprendizagem
                aprendizagem = self.check_aprendizagem()
                if aprendizagem == True:
                    # Executa o comando:
                    cursor.execute("INSERT INTO historico_acoes (acao,valor,horario) VALUES(%s,%s,%s)",
                                   (acao, valor, data_db))
                conexao.close()


            # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText("Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def update_power_ar(self):
        self.power_off_ar()
        valor = self.ui.btn_power_ar.text()
        data_atual = datetime.now()
        data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')

        if valor == 'Ligar':
            valor = True
            acao = "Power-Ar-On"
            self.ui.btn_power_ar.setText("Desligar")
        elif valor == 'Desligar':
            valor = False
            acao = "Power-Ar-Off"
            self.ui.btn_power_ar.setText("Ligar")
        teste_conexao = 0

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("UPDATE configuracao_user SET ar_condicionado=%s WHERE id=1", valor)

            # Verifica Acionamento da aprendizagem
            aprendizagem = self.check_aprendizagem()
            if aprendizagem == True:
                # Executa o comando:
                cursor.execute("INSERT INTO historico_acoes (acao,valor,horario) VALUES(%s,%s,%s)", (acao, valor, data_db))
            conexao.close()

        # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText(
                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def update_power_tv(self):

        self.power_off_tv()
        valor = self.ui.btn_power_tv.text()
        data_atual = datetime.now()
        data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')

        acao = "Power-Tv"
        if valor == 'Ligar':
            valor = True
            self.ui.btn_power_tv.setText("Desligar")
        elif valor == 'Desligar':
            valor = False
            self.ui.btn_power_tv.setText("Ligar")
        teste_conexao = 0

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("UPDATE configuracao_user SET televisao=%s WHERE id=1", valor)
            # Executa o comando:
            cursor.execute("INSERT INTO historico_acoes (acao,valor,horario) VALUES(%s,%s,%s)", (acao, valor, data_db))
            conexao.close()

        # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText(
                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def update_Aprendizagem(self):
        valor = self.ui.check_Aprendizagem.checkState()

        teste_conexao = 0
        if valor == 1 or valor == 2:
            valor = True
        elif valor == 0:
            valor = False
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')

            # Cria um cursor:
            cursor = conexao.cursor()

            # Executa o comando:
            cursor.execute("UPDATE configuracao_user SET aprendizagem=%s WHERE id=1", valor)
            conexao.close()
            # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText(
                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

        aprendizagem=self.check_aprendizagem()
        if aprendizagem==True:
            self.machine_learning()

    def update_Economia(self):
        global verify_lamp_economic
        valor = self.ui.check_Economia.checkState()
        teste_conexao = 0
        if valor == 1 or valor == 2:
            valor = True
            verify_lamp_economic=False
        elif valor == 0:
            valor = False
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')

            # Cria um cursor:
            cursor = conexao.cursor()

            # Executa o comando:
            cursor.execute("UPDATE configuracao_user SET economia=%s WHERE id=1", valor)
            conexao.close()
        # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText(
                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def update_Controle(self):
        valor = self.ui.check_Controle.checkState()

        teste_conexao = 0

        if valor == 1 or valor == 2:
            valor = True
        elif valor == 0:
            valor = False

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')

            # Cria um cursor:
            cursor = conexao.cursor()

            # Executa o comando:
            cursor.execute("UPDATE configuracao_user SET controle=%s WHERE id=1", valor)
            conexao.close()
        # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText(
                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

        if valor == True:
            print("Modo Controle Habilitado")
            self.check_tendencias()
            self.auto_tendencias()
        else:
            print("Modo Controle Desabilitado")

    def update_Tendencia(self):
        valor = self.ui.txt_tendencia.text()
        teste_conexao = 0
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')

            # Cria um cursor:
            cursor = conexao.cursor()

            # Executa o comando:
            cursor.execute("UPDATE configuracao_user SET tendencia=%s WHERE id=1", valor)
            conexao.close()

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText(".::Dado Salvo com Sucesso::.")
            msg.setInformativeText("Sua Tendência foi Alterada!")
            msg.setWindowTitle("Sucesso!")

            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

            # Chama Machine Learn
            self.machine_learning()

        # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText(
                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def set_configs_user(self):

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute(
                "SELECT intensidade_iluminacao, temperatura, aprendizagem, economia, controle,ar_condicionado, televisao, temp_banho_economic,temp_ar,modo_ar,volume_tv,canais_tv, tendencia,estado_iluminacao,lux,temp_banho_normal FROM configuracao_user  WHERE id=1")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    valor_ilum = linha[0]
                    valor_temp = linha[1]
                    valor_aprendizagem = linha[2]
                    valor_economia = linha[3]
                    valor_controle = linha[4]
                    valor_ar = linha[5]
                    valor_televisao = linha[6]
                    valor_temp_banho_economic = linha[7]
                    valor_temp_ar = linha[8]
                    valor_modo_ar = linha[9]
                    valor_volume_tv = linha[10]
                    valor_canais_tv = linha[11]
                    tendencia=linha[12]
                    estado_iluminacao=linha[13]
                    lux=linha[14]
                    valor_temp_banho_normal=linha[15]

                self.ui.horizontalSlider.setValue(valor_ilum)
                self.ui.label_10.setText(str(valor_ilum))
                if estado_iluminacao==True:
                    self.ui.horizontalSlider.setEnabled(True)
                    self.ui.btn_on_ilum.setEnabled(False)
                    self.ui.txt_state_lamp.setText("Ligada")
                else:
                    self.ui.horizontalSlider.setEnabled(False)
                    self.ui.btn_off_ilum.setEnabled(False)
                    self.ui.txt_state_lamp.setText("Desligada")

                self.ui.txt_temp.setText(str(valor_temp))
                self.ui.check_Aprendizagem.setCheckState(valor_aprendizagem)
                self.ui.check_Economia.setCheckState(valor_economia)
                self.ui.check_Controle.setCheckState(valor_controle)
                self.ui.txt_temp_agua_economic.setText(str(valor_temp_banho_economic))
                self.ui.text_temp_ar.setText(str(valor_temp_ar))
                self.ui.text_vol.setText(str(valor_volume_tv))
                self.ui.text_canal.setText(str(valor_canais_tv))
                self.ui.txt_tendencia.setText(str(tendencia))
                self.ui.txt_temp_agua_normal.setText(str(valor_temp_banho_normal))

                if valor_ar == True:
                    self.ui.btn_power_ar.setText("Desligar")
                else:
                    self.ui.btn_power_ar.setText("Ligar")
                if valor_televisao == True:
                    self.ui.btn_power_tv.setText("Desligar")
                else:
                    self.ui.btn_power_tv.setText("Ligar")
                if valor_modo_ar == True:
                    self.ui.text_modo_ar.setText("Turbo")
                else:
                    self.ui.text_modo_ar.setText("Normal")
            else:
                print("Dados Insuficientes no Banco de Dados")

            # Finaliza a conexão
            conexao.close()


        except pymysql.err.OperationalError as e:
            print("Error while connecting to MySQL", e)

    def machine_learning(self):
        aprendizagem = self.check_aprendizagem()
        if aprendizagem == True:

            self.machine_learning_temperatura_ar_mais()
            self.machine_learning_temperatura_ar_menos()
            self.machine_learning_power_ar_off()
            self.machine_learning_power_ar_on()
            self.select_graph_update_mac()

        controle= self.check_controle()
        if controle == True:
            self.check_tendencias()

    def machine_learning_temperatura_ar_mais(self):
        #Variaveis de Configuração
        qq = 0
        sair = 0
        taxa_tendencia=0.5
        temperatura_ar_mais = 0
        n_temperatura_ar_mais = 0
        quantidade_grupos_temperatura_ar_mais = 0

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT acao,valor,horario FROM historico_acoes ORDER BY TIME(horario) ASC")
            #cursor.execute("SELECT acao,valor,horario FROM historico_acoes ORDER BY horario ASC")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                mac_acao = np.array([[0] * 3] * cursor.rowcount, dtype='<U19')
                for linha in resultado:
                    mac_acao[qq][0] = linha[0]
                    mac_acao[qq][1] = linha[1]
                    mac_acao[qq][2] = linha[2]
                    #Verifica a categoria da Função atual
                    if mac_acao[qq][0] == 'Temperatura-Ar-Mais':
                        temperatura_ar_mais = temperatura_ar_mais + 1
                    #Contador de resultados
                    qq = qq + 1
            #criação do vetorcom a quantidade de resultados
            mac_temperatura_ar_mais = np.array([[0] * 3] * temperatura_ar_mais, dtype='<U19')

            #Conta a quantidade de resultados, e atribui ao novo vetor
            for x in range(0, cursor.rowcount):
                if mac_acao[x][0] == 'Temperatura-Ar-Mais':
                    mac_temperatura_ar_mais[n_temperatura_ar_mais] = mac_acao[x]
                    n_temperatura_ar_mais = n_temperatura_ar_mais + 1

            ##ESTATISTICA TEMPERATURA AR
            # for x in range(0,n_temperatura_ar_mais):  #Apresenta todos os valores recuperados do BD. IMPORTANTE PARA CONFERENCIA
            #     print(mac_temperatura_ar_mais[x][2])

            # Criação dos Eixos E Vetor do dia do grupo
            eixo_x_temperatura_ar_mais = np.zeros((1, 1), dtype='<U19')
            eixo_y_temperatura_ar_mais = np.zeros((1, 1))
            dia_do_grupo_temperatura_ar_mais=np.zeros((1, 1),dtype='i4') #Torna o vetor, inteiro

            # Criação da data inicial
            data_obj = datetime.strptime(mac_temperatura_ar_mais[0][2], '%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
            horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
            data_horario_inicio = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO
            data_comparativa_1 = (data_horario_inicio + (timedelta(minutes=15)))  # Data inicial + 15min
            dia_comparativo=(data_obj).weekday() #Dia da semana da data comparativa
            dia_atual=dia_comparativo   #Dia da semana para comparação inicial

            # Contador do Loop
            nn = 0
            # Seto o primeiro valor do Eixo X e do Dia do Grupo 1
            eixo_x_temperatura_ar_mais[0][0] = data_comparativa_1
            dia_do_grupo_temperatura_ar_mais[0][0]=dia_comparativo

            # Loop Comparativo
            while sair == 0:
                # Se for a 1ª vez do loop, não incrementa os eixos
                if nn != 0:
                    # Incremento o vetor X com 1 posição a mais
                    eixo_x_temperatura_ar_mais = np.resize(eixo_x_temperatura_ar_mais, (1, len(eixo_x_temperatura_ar_mais[0]) + 1))
                    # Atribuo o valor para a posição Criada
                    eixo_x_temperatura_ar_mais[0][quantidade_grupos_temperatura_ar_mais] = data_comparativa_1

                    # Incremento o vetor dia_do_Grupo com 1 posição a mais
                    dia_do_grupo_temperatura_ar_mais = np.resize(dia_do_grupo_temperatura_ar_mais, (1, len(dia_do_grupo_temperatura_ar_mais[0]) + 1))
                    # Atribuo o valor para a posição Criada
                    dia_do_grupo_temperatura_ar_mais[0][quantidade_grupos_temperatura_ar_mais] = dia_comparativo

                    # Crio o vetor auxiliar para Incrementar Eixo Y
                    eixo_y_aux_temperatura_ar_mais = eixo_y_temperatura_ar_mais[:]
                    # Incremento Eixo Y
                    eixo_y_temperatura_ar_mais = np.zeros((1, len(eixo_y_temperatura_ar_mais[0]) + 1))
                    # Loop para atribuir respectivos valores do Eixo Y
                    for jj in range(0, len(eixo_y_aux_temperatura_ar_mais[0])):
                        eixo_y_temperatura_ar_mais[0][jj] = eixo_y_aux_temperatura_ar_mais[0][jj]

                # Loop Comparativo entre datas
                while data_horario_inicio <= data_comparativa_1 and nn < (n_temperatura_ar_mais - 1) and dia_atual==dia_comparativo:
                #while data_horario_inicio <= data_comparativa_1 and nn < ( n_temperatura_ar_mais - 1):
                    # Se tiver dentro dos 15min, Incrementa o valor do eixo Y
                    eixo_y_temperatura_ar_mais[0][quantidade_grupos_temperatura_ar_mais] = eixo_y_temperatura_ar_mais[0][quantidade_grupos_temperatura_ar_mais] + 1
                    nn = nn + 1
                    # Capto a nova Data, e deixo pronto pra nova passagem do loop
                    data_obj = datetime.strptime(mac_temperatura_ar_mais[nn][2],'%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
                    data_horario_inicio = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO
                    #Data em dia da Semana
                    dia_atual = (data_obj).weekday()

                # Quando sai do Loop, um novo grupo de datas é formado.
                quantidade_grupos_temperatura_ar_mais = quantidade_grupos_temperatura_ar_mais + 1

                # Se a contagem não for a ultima, atribuo um novo valor pra ultima data
                if nn != n_temperatura_ar_mais - 1:
                    data_comparativa_1 = (data_horario_inicio + timedelta(minutes=15))
                    dia_comparativo=(data_obj).weekday()
                # Se a contagem for a ultima, ele atribui a saida do loop geral
                if (nn == (n_temperatura_ar_mais - 1)):
                    sair = 1

            # Apos sair o loop, ele compara a ultima data (que não é comparada com o loop anterior)
            if data_horario_inicio <= data_comparativa_1 and dia_atual == dia_comparativo:
            #if data_horario_inicio <= data_comparativa_1:
                # Se for o mesmo intervalo de 15min, atribui o valor para o Eixo Y
                eixo_y_temperatura_ar_mais[0][quantidade_grupos_temperatura_ar_mais - 1] = eixo_y_temperatura_ar_mais[0][quantidade_grupos_temperatura_ar_mais - 1] + 1
            else:
                # Senao, cria um novo grupo, um novo Eixo X
                quantidade_grupos_temperatura_ar_mais = quantidade_grupos_temperatura_ar_mais + 1
                eixo_x_temperatura_ar_mais = np.resize(eixo_x_temperatura_ar_mais, (1, len(eixo_x_temperatura_ar_mais[0]) + 1))
                eixo_x_temperatura_ar_mais[0][quantidade_grupos_temperatura_ar_mais - 1] = data_comparativa_1

                # Incremento o vetor dia_doGrupo com 1 posição a mais
                dia_do_grupo_temperatura_ar_mais = np.resize(dia_do_grupo_temperatura_ar_mais, (1, len(dia_do_grupo_temperatura_ar_mais[0]) + 1))
                # Atribuo o valor para a posição Criada
                dia_do_grupo_temperatura_ar_mais[0][quantidade_grupos_temperatura_ar_mais-1] = dia_atual

                # Cria um novo valor pro Eixo Y, e atribui os valores antigos pro novo Eixo Y
                eixo_y_aux_temperatura_ar_mais = eixo_y_temperatura_ar_mais[:]
                eixo_y_temperatura_ar_mais = np.zeros((1, len(eixo_y_temperatura_ar_mais[0]) + 1))
                for jj in range(0, len(eixo_y_aux_temperatura_ar_mais[0])):
                    eixo_y_temperatura_ar_mais[0][jj] = eixo_y_aux_temperatura_ar_mais[0][jj]

                # Atribui novos valores pros eixos X e Y
                eixo_x_temperatura_ar_mais[0][quantidade_grupos_temperatura_ar_mais - 1] = data_horario_inicio
                eixo_y_temperatura_ar_mais[0][quantidade_grupos_temperatura_ar_mais - 1] = eixo_y_temperatura_ar_mais[0][ quantidade_grupos_temperatura_ar_mais - 1] + 1

            # Apresenta os Vetores
            # Grupos Misturados separados pelos dias das semanas a cada 15min.
            # print(eixo_x_temperatura_ar_mais)
            # print(eixo_y_temperatura_ar_mais)
            # print(dia_do_grupo_temperatura_ar_mais)

            ################# Aqui ocorre o agrupamento dos dias IGUAIS a cada 15min ####################
            #Criação do Vetor que ira receber os valores
            eixo_x_agrupado_temperatura_ar_mais=np.zeros((1, 3), dtype='<U19')
            n=0
            #For que ira rodar por todos os valores baixados do BD
            for kkk in range(0,7):
                for x in range(0, len(eixo_x_temperatura_ar_mais[0])):
                    #Aqui verifica qual dia da semana é.
                    if dia_do_grupo_temperatura_ar_mais[0][x] == kkk:
                        #Se for a primeira rodada no For:
                        if n==0:
                            eixo_x_agrupado_temperatura_ar_mais[n][0]=eixo_x_temperatura_ar_mais[0][x]
                            eixo_x_agrupado_temperatura_ar_mais[n][1]=eixo_y_temperatura_ar_mais[0][x]
                            eixo_x_agrupado_temperatura_ar_mais[n][2]=dia_do_grupo_temperatura_ar_mais[0][x]
                            n=1
                        else:
                            #Aumento o tamanho da minha matrix,e acrescenta os valores
                            eixo_x_agrupado_temperatura_ar_mais = np.resize(eixo_x_agrupado_temperatura_ar_mais, (len(eixo_x_agrupado_temperatura_ar_mais) + 1, 3))
                            eixo_x_agrupado_temperatura_ar_mais[n][0] = eixo_x_temperatura_ar_mais[0][x]
                            eixo_x_agrupado_temperatura_ar_mais[n][1] = eixo_y_temperatura_ar_mais[0][x]
                            eixo_x_agrupado_temperatura_ar_mais[n][2] = dia_do_grupo_temperatura_ar_mais[0][x]
                            n=n+1

            #Criação dos vetores RESULTADO
            vetor_x_temperatura_ar_mais = np.zeros((1, 1), dtype='<U19')
            vetor_y_temperatura_ar_mais = np.zeros((1, 1))
            vetor_z_temperatura_ar_mais = np.zeros((1, 1), dtype='<U19')
            n = 0
            #For que roda no tamanho da matrix ordenada
            for x in range(0,len(eixo_x_agrupado_temperatura_ar_mais)):
                if n==0:
                    vetor_x_temperatura_ar_mais[0][0]=eixo_x_agrupado_temperatura_ar_mais[0][0]
                    vetor_y_temperatura_ar_mais[0][0]=eixo_x_agrupado_temperatura_ar_mais[0][1]
                    vetor_z_temperatura_ar_mais[0][0]=eixo_x_agrupado_temperatura_ar_mais[0][2]
                    n=1
                else:
                    #Criacao das datas para comparativo e AGRUPAR os horarios dos mesmos 15min
                    data_obj = datetime.strptime(vetor_x_temperatura_ar_mais[0][n-1],'%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
                    data_horario_inicio = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO
                    data_comparativa_1 = (data_horario_inicio - (timedelta(minutes=15)))  # Data inicial + 15min
                    data_comparativa_2=data_horario_inicio
                    dia_comparativo = vetor_z_temperatura_ar_mais[0][n-1]


                    data_obj2 = datetime.strptime(eixo_x_agrupado_temperatura_ar_mais[x][0],'%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    horario2 = (data_obj2).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
                    minha_data_horario2 = datetime.strptime(horario2, '%H:%M:%S')  # Converto novamente para OBJETO
                    data_horario2=(minha_data_horario2 - (timedelta(minutes=15)))
                    dia_atual = eixo_x_agrupado_temperatura_ar_mais[x][2]
                    ##Trava para caso o vetor acabe apenas com 1 contagem na ultima casa, neste caso, a datação dela deve ser diferente para comparação.
                    if (x == (len(eixo_x_agrupado_temperatura_ar_mais) - 1)) and (eixo_x_agrupado_temperatura_ar_mais[x][1] == '1.0'):
                        data_horario2 = (minha_data_horario2)

                    #Se o horario atual estiver entre os 15min do horario do grupo e se for do mesmo dia, soma o valor de quantidades
                    if data_horario2>data_comparativa_1 and data_horario2<data_comparativa_2 and dia_atual==dia_comparativo:
                        vetor_y_temperatura_ar_mais[0][n-1]=vetor_y_temperatura_ar_mais[0][n-1]+float(eixo_x_agrupado_temperatura_ar_mais[x][1])
                    #Se nao, aumento os vetores, e acrescento como um outro grupo
                    else:
                        # Incremento o vetor X com 1 posição a mais
                        vetor_x_temperatura_ar_mais = np.resize(vetor_x_temperatura_ar_mais,(1,len(vetor_x_temperatura_ar_mais[0])+1))
                        vetor_y_temperatura_ar_mais = np.resize(vetor_y_temperatura_ar_mais,(1, len(vetor_y_temperatura_ar_mais[0]) + 1))
                        vetor_z_temperatura_ar_mais = np.resize(vetor_z_temperatura_ar_mais,(1, len(vetor_z_temperatura_ar_mais[0]) + 1))
                        #Acrescento valores
                        vetor_x_temperatura_ar_mais[0][n] = eixo_x_agrupado_temperatura_ar_mais[x][0]
                        vetor_y_temperatura_ar_mais[0][n] = eixo_x_agrupado_temperatura_ar_mais[x][1]
                        vetor_z_temperatura_ar_mais[0][n]=eixo_x_agrupado_temperatura_ar_mais[x][2]
                        n=n+1

            #Apresentação dos valores AGRUPADOS E ORDENADOS
            # print(vetor_x_temperatura_ar_mais)
            # print(vetor_y_temperatura_ar_mais)
            # print(vetor_z_temperatura_ar_mais)


            #Parametros de Configuração para Estatísticas
            somatorio_temperatura_ar_mais=0
            qtd_somatorio_temperatura_ar_mais=0

            # Capto o Valor da Taxa de Tendencia do BD
            # Executa o comando:
            cursor.execute("SELECT tendencia FROM configuracao_user  WHERE id=1")
            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    taxa_tendencia = linha[0] / 100
            else:
                print("Dados Insuficientes no Banco de Dados")
                # Finaliza a conexão

            #Loop para saber qual o total dos valores da ação
            for n in range(0, len(eixo_x_temperatura_ar_mais[0])):
                somatorio_temperatura_ar_mais=somatorio_temperatura_ar_mais+eixo_y_temperatura_ar_mais[0][n]
            #Loop para saber quantos valores estão acima da Taxa de Tendencia
            for nn in range(0, len(vetor_x_temperatura_ar_mais[0])):
                if (float(vetor_y_temperatura_ar_mais[0][nn]) / somatorio_temperatura_ar_mais) >= taxa_tendencia:
                    qtd_somatorio_temperatura_ar_mais=qtd_somatorio_temperatura_ar_mais+1

            #Proteção para nao criar o vetor e nao tentar inserir no BD se nao existir Tendencias.
            if qtd_somatorio_temperatura_ar_mais>0:
                k=0
                #Criaçcao do Vetor
                tendencia_temperatura_ar_mais = np.zeros((qtd_somatorio_temperatura_ar_mais, 4), dtype='<U19')
                vetor_x_temperatura_ar_mais_tendencia=np.zeros((1, qtd_somatorio_temperatura_ar_mais), dtype='<U19')
                vetor_y_temperatura_ar_mais_tendencia = np.zeros((1, qtd_somatorio_temperatura_ar_mais))
                vetor_z_temperatura_ar_mais_tendencia = np.zeros((1, qtd_somatorio_temperatura_ar_mais), dtype='<U19')
                #Loop para procurar novamente valores acima da Taxa de Tendencia
                for nn in range(0, len(vetor_x_temperatura_ar_mais[0])):
                    #Condicação que compara cada valor com a Taxa de Tendencia
                    if (float(vetor_y_temperatura_ar_mais[0][nn]) / somatorio_temperatura_ar_mais) >= taxa_tendencia:
                        #Atribuições do Vetor
                        tendencia_temperatura_ar_mais[k][0]="Temperatura-Ar-Mais"
                        tendencia_temperatura_ar_mais[k][1]=vetor_x_temperatura_ar_mais[0][nn]
                        tendencia_temperatura_ar_mais[k][2]=vetor_z_temperatura_ar_mais[0][nn]
                        tendencia_temperatura_ar_mais[k][3]=vetor_y_temperatura_ar_mais[0][nn]
                        # Atribui Vetor de Tendencia que vai para o gráfico
                        vetor_x_temperatura_ar_mais_tendencia[0][k] = vetor_x_temperatura_ar_mais[0][nn]
                        vetor_y_temperatura_ar_mais_tendencia[0][k] = vetor_y_temperatura_ar_mais[0][nn]
                        vetor_z_temperatura_ar_mais_tendencia[0][k] = vetor_z_temperatura_ar_mais[0][nn]
                        k=k+1

                ##########Inserção no BD#############
                #DELETA VALORES DO BD PREVIAMENTE CONFIGURADOS
                cursor.execute("DELETE FROM tendencias WHERE acao='Temperatura-Ar-Mais'")
                #LOOP PARA INSERIR TODOS AS LINHAS DA MATRIZ
                for nn in range(0, len(tendencia_temperatura_ar_mais)):
                    # Executa o comando:
                    cursor.execute("INSERT INTO tendencias (acao,horario,dia,valor) VALUES(%s,%s,%s,%s)",(tendencia_temperatura_ar_mais[nn][0], tendencia_temperatura_ar_mais[nn][1], tendencia_temperatura_ar_mais[nn][2], tendencia_temperatura_ar_mais[nn][3]))
                conexao.close()
                print("Nova Tendência Registrada!")

            #CASO NAO HAJA TENDENCIA
            else:
                print("Não há tendência")
                #DELETA VALORES DO BD PREVIAMENTE CONFIGURADOS
                cursor.execute("DELETE FROM tendencias WHERE acao='Temperatura-Ar-Mais'")
                conexao.close()
                # Cria o vetor com 1 posição
                vetor_x_temperatura_ar_mais_tendencia = np.zeros((1, 1), dtype='<U22')
                vetor_y_temperatura_ar_mais_tendencia = np.zeros((1, 1))
                vetor_z_temperatura_ar_mais_tendencia = np.zeros((1, 1), dtype='<U22')
                vetor_x_temperatura_ar_mais_tendencia[0][0] = "0"
                vetor_y_temperatura_ar_mais_tendencia[0][0] = 0
                vetor_z_temperatura_ar_mais_tendencia[0][0] = 0

            self.update_graph_machine_learning(vetor_x_temperatura_ar_mais[0], vetor_y_temperatura_ar_mais[0], vetor_z_temperatura_ar_mais[0],vetor_x_temperatura_ar_mais_tendencia[0],vetor_y_temperatura_ar_mais_tendencia[0],vetor_z_temperatura_ar_mais_tendencia[0])
        except pymysql.err.OperationalError as e:
            print("Error while connecting to MySQL", e)

    def machine_learning_temperatura_ar_menos(self):
        #Variaveis de Configuração
        qq = 0
        sair = 0
        taxa_tendencia=0.5
        temperatura_ar_menos = 0
        n_temperatura_ar_menos = 0
        quantidade_grupos_temperatura_ar_menos = 0

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT acao,valor,horario FROM historico_acoes ORDER BY TIME(horario) ASC")
            #cursor.execute("SELECT acao,valor,horario FROM historico_acoes ORDER BY horario ASC")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                mac_acao = np.array([[0] * 3] * cursor.rowcount, dtype='<U22')
                for linha in resultado:
                    mac_acao[qq][0] = linha[0]
                    mac_acao[qq][1] = linha[1]
                    mac_acao[qq][2] = linha[2]
                    #Verifica a categoria da Função atual
                    if mac_acao[qq][0] == 'Temperatura-Ar-Menos':
                        temperatura_ar_menos = temperatura_ar_menos + 1
                    #Contador de resultados
                    qq = qq + 1
            #criação do vetorcom a quantidade de resultados
            mac_temperatura_ar_menos = np.array([[0] * 3] * temperatura_ar_menos, dtype='<U22')

            #Conta a quantidade de resultados, e atribui ao novo vetor
            for x in range(0, cursor.rowcount):
                if mac_acao[x][0] == 'Temperatura-Ar-Menos':
                    mac_temperatura_ar_menos[n_temperatura_ar_menos] = mac_acao[x]
                    n_temperatura_ar_menos = n_temperatura_ar_menos + 1

            ##ESTATISTICA TEMPERATURA AR
            # for x in range(0,n_temperatura_ar_menos):  #Apresenta todos os valores recuperados do BD. IMPORTANTE PARA CONFERENCIA
            #     print(mac_temperatura_ar_menos[x][2])

            # Criação dos Eixos E Vetor do dia do grupo
            eixo_x_temperatura_ar_menos = np.zeros((1, 1), dtype='<U22')
            eixo_y_temperatura_ar_menos = np.zeros((1, 1))
            dia_do_grupo_temperatura_ar_menos=np.zeros((1, 1),dtype='i4') #Torna o vetor, inteiro

            # Criação da data inicial
            data_obj = datetime.strptime(mac_temperatura_ar_menos[0][2], '%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
            horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
            data_horario_inicio = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO
            data_comparativa_1 = (data_horario_inicio + (timedelta(minutes=15)))  # Data inicial + 15min
            dia_comparativo=(data_obj).weekday() #Dia da semana da data comparativa
            dia_atual=dia_comparativo   #Dia da semana para comparação inicial

            # Contador do Loop
            nn = 0
            # Seto o primeiro valor do Eixo X e do Dia do Grupo 1
            eixo_x_temperatura_ar_menos[0][0] = data_comparativa_1
            dia_do_grupo_temperatura_ar_menos[0][0]=dia_comparativo

            # Loop Comparativo
            while sair == 0:
                # Se for a 1ª vez do loop, não incrementa os eixos
                if nn != 0:
                    # Incremento o vetor X com 1 posição a mais
                    eixo_x_temperatura_ar_menos = np.resize(eixo_x_temperatura_ar_menos, (1, len(eixo_x_temperatura_ar_menos[0]) + 1))
                    # Atribuo o valor para a posição Criada
                    eixo_x_temperatura_ar_menos[0][quantidade_grupos_temperatura_ar_menos] = data_comparativa_1

                    # Incremento o vetor dia_do_Grupo com 1 posição a mais
                    dia_do_grupo_temperatura_ar_menos = np.resize(dia_do_grupo_temperatura_ar_menos, (1, len(dia_do_grupo_temperatura_ar_menos[0]) + 1))
                    # Atribuo o valor para a posição Criada
                    dia_do_grupo_temperatura_ar_menos[0][quantidade_grupos_temperatura_ar_menos] = dia_comparativo

                    # Crio o vetor auxiliar para Incrementar Eixo Y
                    eixo_y_aux_temperatura_ar_menos = eixo_y_temperatura_ar_menos[:]
                    # Incremento Eixo Y
                    eixo_y_temperatura_ar_menos = np.zeros((1, len(eixo_y_temperatura_ar_menos[0]) + 1))
                    # Loop para atribuir respectivos valores do Eixo Y
                    for jj in range(0, len(eixo_y_aux_temperatura_ar_menos[0])):
                        eixo_y_temperatura_ar_menos[0][jj] = eixo_y_aux_temperatura_ar_menos[0][jj]

                # Loop Comparativo entre datas
                while data_horario_inicio <= data_comparativa_1 and nn < (n_temperatura_ar_menos - 1) and dia_atual==dia_comparativo:
                #while data_horario_inicio <= data_comparativa_1 and nn < ( n_temperatura_ar_menos - 1):
                    # Se tiver dentro dos 15min, Incrementa o valor do eixo Y
                    eixo_y_temperatura_ar_menos[0][quantidade_grupos_temperatura_ar_menos] = eixo_y_temperatura_ar_menos[0][quantidade_grupos_temperatura_ar_menos] + 1
                    nn = nn + 1
                    # Capto a nova Data, e deixo pronto pra nova passagem do loop
                    data_obj = datetime.strptime(mac_temperatura_ar_menos[nn][2],'%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
                    data_horario_inicio = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO
                    #Data em dia da Semana
                    dia_atual = (data_obj).weekday()

                # Quando sai do Loop, um novo grupo de datas é formado.
                quantidade_grupos_temperatura_ar_menos = quantidade_grupos_temperatura_ar_menos + 1

                # Se a contagem não for a ultima, atribuo um novo valor pra ultima data
                if nn != n_temperatura_ar_menos - 1:
                    data_comparativa_1 = (data_horario_inicio + timedelta(minutes=15))
                    dia_comparativo=(data_obj).weekday()
                # Se a contagem for a ultima, ele atribui a saida do loop geral
                if (nn == (n_temperatura_ar_menos - 1)):
                    sair = 1

            # Apos sair o loop, ele compara a ultima data (que não é comparada com o loop anterior)
            if data_horario_inicio <= data_comparativa_1 and dia_atual == dia_comparativo:
            #if data_horario_inicio <= data_comparativa_1:
                # Se for o mesmo intervalo de 15min, atribui o valor para o Eixo Y
                eixo_y_temperatura_ar_menos[0][quantidade_grupos_temperatura_ar_menos - 1] = eixo_y_temperatura_ar_menos[0][quantidade_grupos_temperatura_ar_menos - 1] + 1
            else:
                # Senao, cria um novo grupo, um novo Eixo X
                quantidade_grupos_temperatura_ar_menos = quantidade_grupos_temperatura_ar_menos + 1
                eixo_x_temperatura_ar_menos = np.resize(eixo_x_temperatura_ar_menos, (1, len(eixo_x_temperatura_ar_menos[0]) + 1))
                eixo_x_temperatura_ar_menos[0][quantidade_grupos_temperatura_ar_menos - 1] = data_comparativa_1

                # Incremento o vetor dia_doGrupo com 1 posição a mais
                dia_do_grupo_temperatura_ar_menos = np.resize(dia_do_grupo_temperatura_ar_menos, (1, len(dia_do_grupo_temperatura_ar_menos[0]) + 1))
                # Atribuo o valor para a posição Criada
                dia_do_grupo_temperatura_ar_menos[0][quantidade_grupos_temperatura_ar_menos-1] = dia_atual

                # Cria um novo valor pro Eixo Y, e atribui os valores antigos pro novo Eixo Y
                eixo_y_aux_temperatura_ar_menos = eixo_y_temperatura_ar_menos[:]
                eixo_y_temperatura_ar_menos = np.zeros((1, len(eixo_y_temperatura_ar_menos[0]) + 1))
                for jj in range(0, len(eixo_y_aux_temperatura_ar_menos[0])):
                    eixo_y_temperatura_ar_menos[0][jj] = eixo_y_aux_temperatura_ar_menos[0][jj]

                # Atribui novos valores pros eixos X e Y
                eixo_x_temperatura_ar_menos[0][quantidade_grupos_temperatura_ar_menos - 1] = data_horario_inicio
                eixo_y_temperatura_ar_menos[0][quantidade_grupos_temperatura_ar_menos - 1] = eixo_y_temperatura_ar_menos[0][ quantidade_grupos_temperatura_ar_menos - 1] + 1

            # Apresenta os Vetores
            # Grupos Misturados separados pelos dias das semanas a cada 15min.
            # print(eixo_x_temperatura_ar_menos)
            # print(eixo_y_temperatura_ar_menos)
            # print(dia_do_grupo_temperatura_ar_menos)

            ################# Aqui ocorre o agrupamento dos dias IGUAIS a cada 15min ####################
            #Criação do Vetor que ira receber os valores
            eixo_x_agrupado_temperatura_ar_menos=np.zeros((1, 3), dtype='<U22')
            n=0
            #For que ira rodar por todos os valores baixados do BD
            for kkk in range(0,7):
                for x in range(0, len(eixo_x_temperatura_ar_menos[0])):
                    #Aqui verifica qual dia da semana é.
                    if dia_do_grupo_temperatura_ar_menos[0][x] == kkk:
                        #Se for a primeira rodada no For:
                        if n==0:
                            eixo_x_agrupado_temperatura_ar_menos[n][0]=eixo_x_temperatura_ar_menos[0][x]
                            eixo_x_agrupado_temperatura_ar_menos[n][1]=eixo_y_temperatura_ar_menos[0][x]
                            eixo_x_agrupado_temperatura_ar_menos[n][2]=dia_do_grupo_temperatura_ar_menos[0][x]
                            n=1
                        else:
                            #Aumento o tamanho da minha matrix,e acrescenta os valores
                            eixo_x_agrupado_temperatura_ar_menos = np.resize(eixo_x_agrupado_temperatura_ar_menos, (len(eixo_x_agrupado_temperatura_ar_menos) + 1, 3))
                            eixo_x_agrupado_temperatura_ar_menos[n][0] = eixo_x_temperatura_ar_menos[0][x]
                            eixo_x_agrupado_temperatura_ar_menos[n][1] = eixo_y_temperatura_ar_menos[0][x]
                            eixo_x_agrupado_temperatura_ar_menos[n][2] = dia_do_grupo_temperatura_ar_menos[0][x]
                            n=n+1
            #Criação dos vetores RESULTADO
            vetor_x_temperatura_ar_menos = np.zeros((1, 1), dtype='<U22')
            vetor_y_temperatura_ar_menos = np.zeros((1, 1))
            vetor_z_temperatura_ar_menos = np.zeros((1, 1), dtype='<U22')
            n = 0
            #For que roda no tamanho da matrix ordenada
            for x in range(0,len(eixo_x_agrupado_temperatura_ar_menos)):
                if n==0:
                    vetor_x_temperatura_ar_menos[0][0]=eixo_x_agrupado_temperatura_ar_menos[0][0]
                    vetor_y_temperatura_ar_menos[0][0]=eixo_x_agrupado_temperatura_ar_menos[0][1]
                    vetor_z_temperatura_ar_menos[0][0]=eixo_x_agrupado_temperatura_ar_menos[0][2]
                    n=1
                else:
                    #Criacao das datas para comparativo e AGRUPAR os horarios dos mesmos 15min
                    data_obj = datetime.strptime(vetor_x_temperatura_ar_menos[0][n-1],'%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
                    data_horario_inicio = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO
                    data_comparativa_1 = (data_horario_inicio - (timedelta(minutes=15)))  # Data inicial + 15min
                    data_comparativa_2=data_horario_inicio
                    dia_comparativo = vetor_z_temperatura_ar_menos[0][n-1]


                    data_obj2 = datetime.strptime(eixo_x_agrupado_temperatura_ar_menos[x][0],'%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    horario2 = (data_obj2).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
                    minha_data_horario2 = datetime.strptime(horario2, '%H:%M:%S')  # Converto novamente para OBJETO
                    data_horario2 = (minha_data_horario2 - (timedelta(minutes=15)))
                    dia_atual = eixo_x_agrupado_temperatura_ar_menos[x][2]

                    ##Trava para caso o vetor acabe apenas com 1 contagem na ultima casa, neste caso, a datação dela deve ser diferente para comparação.
                    if (x == (len(eixo_x_agrupado_temperatura_ar_menos)-1)) and (eixo_x_agrupado_temperatura_ar_menos[x][1]=='1.0'):
                        data_horario2 = (minha_data_horario2 )


                    #Se o horario atual estiver entre os 15min do horario do grupo e se for do mesmo dia, soma o valor de quantidades
                    if data_horario2>data_comparativa_1 and data_horario2<data_comparativa_2 and dia_atual==dia_comparativo:
                        vetor_y_temperatura_ar_menos[0][n-1]=vetor_y_temperatura_ar_menos[0][n-1]+float(eixo_x_agrupado_temperatura_ar_menos[x][1])
                    #Se nao, aumento os vetores, e acrescento como um outro grupo
                    else:
                        # Incremento o vetor X com 1 posição a mais
                        vetor_x_temperatura_ar_menos = np.resize(vetor_x_temperatura_ar_menos,(1,len(vetor_x_temperatura_ar_menos[0])+1))
                        vetor_y_temperatura_ar_menos = np.resize(vetor_y_temperatura_ar_menos,(1, len(vetor_y_temperatura_ar_menos[0]) + 1))
                        vetor_z_temperatura_ar_menos = np.resize(vetor_z_temperatura_ar_menos,(1, len(vetor_z_temperatura_ar_menos[0]) + 1))
                        #Acrescento valores
                        vetor_x_temperatura_ar_menos[0][n] = eixo_x_agrupado_temperatura_ar_menos[x][0]
                        vetor_y_temperatura_ar_menos[0][n] = eixo_x_agrupado_temperatura_ar_menos[x][1]
                        vetor_z_temperatura_ar_menos[0][n]=eixo_x_agrupado_temperatura_ar_menos[x][2]
                        n=n+1

            #Apresentação dos valores AGRUPADOS E ORDENADOS
            # print(vetor_x_temperatura_ar_menos)
            # print(vetor_y_temperatura_ar_menos)
            # print(vetor_z_temperatura_ar_menos)


            #Parametros de Configuração para Estatísticas
            somatorio_temperatura_ar_menos=0
            qtd_somatorio_temperatura_ar_menos=0

            # Capto o Valor da Taxa de Tendencia do BD
            # Executa o comando:
            cursor.execute("SELECT tendencia FROM configuracao_user  WHERE id=1")
            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    taxa_tendencia = linha[0] / 100
            else:
                print("Dados Insuficientes no Banco de Dados")
                # Finaliza a conexão

            #Loop para saber qual o total dos valores da ação
            for n in range(0, len(eixo_x_temperatura_ar_menos[0])):
                somatorio_temperatura_ar_menos=somatorio_temperatura_ar_menos+eixo_y_temperatura_ar_menos[0][n]
            #Loop para saber quantos valores estão acima da Taxa de Tendencia
            for nn in range(0, len(vetor_x_temperatura_ar_menos[0])):
                if (float(vetor_y_temperatura_ar_menos[0][nn]) / somatorio_temperatura_ar_menos) >= taxa_tendencia:
                    qtd_somatorio_temperatura_ar_menos=qtd_somatorio_temperatura_ar_menos+1

            #Proteção para nao criar o vetor e nao tentar inserir no BD se nao existir Tendencias.
            if qtd_somatorio_temperatura_ar_menos>0:
                k=0
                #Criaçcao do Vetor
                tendencia_temperatura_ar_menos = np.zeros((qtd_somatorio_temperatura_ar_menos, 4), dtype='<U22')
                vetor_x_temperatura_ar_menos_tendencia= np.zeros((1, qtd_somatorio_temperatura_ar_menos), dtype='<U22')
                vetor_y_temperatura_ar_menos_tendencia = np.zeros((1, qtd_somatorio_temperatura_ar_menos))
                vetor_z_temperatura_ar_menos_tendencia = np.zeros((1, qtd_somatorio_temperatura_ar_menos), dtype='<U22')
                #Loop para procurar novamente valores acima da Taxa de Tendencia
                for nn in range(0, len(vetor_x_temperatura_ar_menos[0])):
                    #Condicação que compara cada valor com a Taxa de Tendencia
                    if (float(vetor_y_temperatura_ar_menos[0][nn]) / somatorio_temperatura_ar_menos) >= taxa_tendencia:
                        #Atribuições do Vetor
                        tendencia_temperatura_ar_menos[k][0]="Temperatura-Ar-Menos"
                        tendencia_temperatura_ar_menos[k][1]=vetor_x_temperatura_ar_menos[0][nn]
                        tendencia_temperatura_ar_menos[k][2]=vetor_z_temperatura_ar_menos[0][nn]
                        tendencia_temperatura_ar_menos[k][3]=vetor_y_temperatura_ar_menos[0][nn]
                        vetor_x_temperatura_ar_menos_tendencia[0][k]=vetor_x_temperatura_ar_menos[0][nn]
                        vetor_y_temperatura_ar_menos_tendencia[0][k]=vetor_y_temperatura_ar_menos[0][nn]
                        vetor_z_temperatura_ar_menos_tendencia[0][k]=vetor_z_temperatura_ar_menos[0][nn]
                        k=k+1

                ##########Inserção no BD#############
                #DELETA VALORES DO BD PREVIAMENTE CONFIGURADOS
                cursor.execute("DELETE FROM tendencias WHERE acao='Temperatura-Ar-Menos'")
                #LOOP PARA INSERIR TODOS AS LINHAS DA MATRIZ
                for nn in range(0, len(tendencia_temperatura_ar_menos)):
                    # Executa o comando:
                    cursor.execute("INSERT INTO tendencias (acao,horario,dia,valor) VALUES(%s,%s,%s,%s)",(tendencia_temperatura_ar_menos[nn][0], tendencia_temperatura_ar_menos[nn][1], tendencia_temperatura_ar_menos[nn][2], tendencia_temperatura_ar_menos[nn][3]))
                conexao.close()
                print("Nova Tendência Registrada!")

            #CASO NAO HAJA TENDENCIA
            else:
                print("Não há tendência")
                #DELETA VALORES DO BD PREVIAMENTE CONFIGURADOS
                cursor.execute("DELETE FROM tendencias WHERE acao='Temperatura-Ar-Menos'")
                conexao.close()
                # Cria o vetor com 1 posição
                vetor_x_temperatura_ar_menos_tendencia = np.zeros((1, 1), dtype='<U22')
                vetor_y_temperatura_ar_menos_tendencia = np.zeros((1, 1))
                vetor_z_temperatura_ar_menos_tendencia = np.zeros((1, 1), dtype='<U22')
                vetor_x_temperatura_ar_menos_tendencia[0][0] = "0"
                vetor_y_temperatura_ar_menos_tendencia[0][0] = 0
                vetor_z_temperatura_ar_menos_tendencia[0][0] = 0

            self.update_graph_machine_learning(vetor_x_temperatura_ar_menos[0], vetor_y_temperatura_ar_menos[0], vetor_z_temperatura_ar_menos[0],vetor_x_temperatura_ar_menos_tendencia[0],vetor_y_temperatura_ar_menos_tendencia[0],vetor_z_temperatura_ar_menos_tendencia[0])
        except pymysql.err.OperationalError as e:
            print("Error while connecting to MySQL", e)

    def machine_learning_power_ar_on(self):
        # Variaveis de Configuração
        qq = 0
        sair = 0
        taxa_tendencia = 0.5
        power_ar_on = 0
        n_power_ar_on = 0
        quantidade_grupos_power_ar_on = 0

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT acao,valor,horario FROM historico_acoes ORDER BY TIME(horario) ASC")
            # cursor.execute("SELECT acao,valor,horario FROM historico_acoes ORDER BY horario ASC")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                mac_acao = np.array([[0] * 3] * cursor.rowcount, dtype='<U22')
                for linha in resultado:
                    mac_acao[qq][0] = linha[0]
                    mac_acao[qq][1] = linha[1]
                    mac_acao[qq][2] = linha[2]
                    # Verifica a categoria da Função atual
                    if mac_acao[qq][0] == 'Power-Ar-On':
                        power_ar_on = power_ar_on + 1
                    # Contador de resultados
                    qq = qq + 1
            # criação do vetorcom a quantidade de resultados
            mac_power_ar_on = np.array([[0] * 3] * power_ar_on, dtype='<U22')

            # Conta a quantidade de resultados, e atribui ao novo vetor
            for x in range(0, cursor.rowcount):
                if mac_acao[x][0] == 'Power-Ar-On':
                    mac_power_ar_on[n_power_ar_on] = mac_acao[x]
                    n_power_ar_on = n_power_ar_on + 1

            ##ESTATISTICA POWER AR Off
            # for x in range(0,n_power_ar_on):  #Apresenta todos os valores recuperados do BD. IMPORTANTE PARA CONFERENCIA
            #     print(mac_power_ar_on[x][2])

            # Criação dos Eixos E Vetor do dia do grupo
            eixo_x_power_ar_on = np.zeros((1, 1), dtype='<U22')
            eixo_y_power_ar_on = np.zeros((1, 1))
            dia_do_grupo_power_ar_on = np.zeros((1, 1), dtype='i4')  # Torna o vetor, inteiro

            # Criação da data inicial
            data_obj = datetime.strptime(mac_power_ar_on[0][2], '%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
            horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
            data_horario_inicio = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO
            data_comparativa_1 = (data_horario_inicio + (timedelta(minutes=15)))  # Data inicial + 15min
            dia_comparativo = (data_obj).weekday()  # Dia da semana da data comparativa
            dia_atual = dia_comparativo  # Dia da semana para comparação inicial

            # Contador do Loop
            nn = 0
            # Seto o primeiro valor do Eixo X e do Dia do Grupo 1
            eixo_x_power_ar_on[0][0] = data_comparativa_1
            dia_do_grupo_power_ar_on[0][0] = dia_comparativo

            # Loop Comparativo
            while sair == 0:
                # Se for a 1ª vez do loop, não incrementa os eixos
                if nn != 0:
                    # Incremento o vetor X com 1 posição a mais
                    eixo_x_power_ar_on = np.resize(eixo_x_power_ar_on, (1, len(eixo_x_power_ar_on[0]) + 1))
                    # Atribuo o valor para a posição Criada
                    eixo_x_power_ar_on[0][quantidade_grupos_power_ar_on] = data_comparativa_1

                    # Incremento o vetor dia_do_Grupo com 1 posição a mais
                    dia_do_grupo_power_ar_on = np.resize(dia_do_grupo_power_ar_on,
                                                          (1, len(dia_do_grupo_power_ar_on[0]) + 1))
                    # Atribuo o valor para a posição Criada
                    dia_do_grupo_power_ar_on[0][quantidade_grupos_power_ar_on] = dia_comparativo

                    # Crio o vetor auxiliar para Incrementar Eixo Y
                    eixo_y_aux_power_ar_on = eixo_y_power_ar_on[:]
                    # Incremento Eixo Y
                    eixo_y_power_ar_on = np.zeros((1, len(eixo_y_power_ar_on[0]) + 1))
                    # Loop para atribuir respectivos valores do Eixo Y
                    for jj in range(0, len(eixo_y_aux_power_ar_on[0])):
                        eixo_y_power_ar_on[0][jj] = eixo_y_aux_power_ar_on[0][jj]

                # Loop Comparativo entre datas
                while data_horario_inicio <= data_comparativa_1 and nn < (
                        n_power_ar_on - 1) and dia_atual == dia_comparativo:
                    # while data_horario_inicio <= data_comparativa_1 and nn < ( n_power_ar_on - 1):
                    # Se tiver dentro dos 15min, Incrementa o valor do eixo Y
                    eixo_y_power_ar_on[0][quantidade_grupos_power_ar_on] = eixo_y_power_ar_on[0][
                                                                                 quantidade_grupos_power_ar_on] + 1
                    nn = nn + 1
                    # Capto a nova Data, e deixo pronto pra nova passagem do loop
                    data_obj = datetime.strptime(mac_power_ar_on[nn][2],
                                                 '%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
                    data_horario_inicio = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO
                    # Data em dia da Semana
                    dia_atual = (data_obj).weekday()

                # Quando sai do Loop, um novo grupo de datas é formado.
                quantidade_grupos_power_ar_on = quantidade_grupos_power_ar_on + 1

                # Se a contagem não for a ultima, atribuo um novo valor pra ultima data
                if nn != n_power_ar_on - 1:
                    data_comparativa_1 = (data_horario_inicio + timedelta(minutes=15))
                    dia_comparativo = (data_obj).weekday()
                # Se a contagem for a ultima, ele atribui a saida do loop geral
                if (nn == (n_power_ar_on - 1)):
                    sair = 1

            # Apos sair o loop, ele compara a ultima data (que não é comparada com o loop anterior)
            if data_horario_inicio <= data_comparativa_1 and dia_atual == dia_comparativo:
                # if data_horario_inicio <= data_comparativa_1:
                # Se for o mesmo intervalo de 15min, atribui o valor para o Eixo Y
                eixo_y_power_ar_on[0][quantidade_grupos_power_ar_on - 1] = eixo_y_power_ar_on[0][
                                                                                 quantidade_grupos_power_ar_on - 1] + 1
            else:
                # Senao, cria um novo grupo, um novo Eixo X
                quantidade_grupos_power_ar_on = quantidade_grupos_power_ar_on + 1
                eixo_x_power_ar_on = np.resize(eixo_x_power_ar_on, (1, len(eixo_x_power_ar_on[0]) + 1))
                eixo_x_power_ar_on[0][quantidade_grupos_power_ar_on - 1] = data_comparativa_1

                # Incremento o vetor dia_doGrupo com 1 posição a mais
                dia_do_grupo_power_ar_on = np.resize(dia_do_grupo_power_ar_on,
                                                      (1, len(dia_do_grupo_power_ar_on[0]) + 1))
                # Atribuo o valor para a posição Criada
                dia_do_grupo_power_ar_on[0][quantidade_grupos_power_ar_on - 1] = dia_atual

                # Cria um novo valor pro Eixo Y, e atribui os valores antigos pro novo Eixo Y
                eixo_y_aux_power_ar_on = eixo_y_power_ar_on[:]
                eixo_y_power_ar_on = np.zeros((1, len(eixo_y_power_ar_on[0]) + 1))
                for jj in range(0, len(eixo_y_aux_power_ar_on[0])):
                    eixo_y_power_ar_on[0][jj] = eixo_y_aux_power_ar_on[0][jj]

                # Atribui novos valores pros eixos X e Y
                eixo_x_power_ar_on[0][quantidade_grupos_power_ar_on - 1] = data_horario_inicio
                eixo_y_power_ar_on[0][quantidade_grupos_power_ar_on - 1] = eixo_y_power_ar_on[0][
                                                                                 quantidade_grupos_power_ar_on - 1] + 1

            # Apresenta os Vetores
            # Grupos Misturados separados pelos dias das semanas a cada 15min.
            # print(eixo_x_power_ar_on)
            # print(eixo_y_power_ar_on)
            # print(dia_do_grupo_power_ar_on)

            ################# Aqui ocorre o agrupamento dos dias IGUAIS a cada 15min ####################
            # Criação do Vetor que ira receber os valores
            eixo_x_agrupado_power_ar_on = np.zeros((1, 3), dtype='<U22')
            n = 0
            # For que ira rodar por todos os valores baixados do BD
            for kkk in range(0, 7):
                for x in range(0, len(eixo_x_power_ar_on[0])):
                    # Aqui verifica qual dia da semana é.
                    if dia_do_grupo_power_ar_on[0][x] == kkk:
                        # Se for a primeira rodada no For:
                        if n == 0:
                            eixo_x_agrupado_power_ar_on[n][0] = eixo_x_power_ar_on[0][x]
                            eixo_x_agrupado_power_ar_on[n][1] = eixo_y_power_ar_on[0][x]
                            eixo_x_agrupado_power_ar_on[n][2] = dia_do_grupo_power_ar_on[0][x]
                            n = 1
                        else:
                            # Aumento o tamanho da minha matrix,e acrescenta os valores
                            eixo_x_agrupado_power_ar_on = np.resize(eixo_x_agrupado_power_ar_on,
                                                                     (len(eixo_x_agrupado_power_ar_on) + 1, 3))
                            eixo_x_agrupado_power_ar_on[n][0] = eixo_x_power_ar_on[0][x]
                            eixo_x_agrupado_power_ar_on[n][1] = eixo_y_power_ar_on[0][x]
                            eixo_x_agrupado_power_ar_on[n][2] = dia_do_grupo_power_ar_on[0][x]
                            n = n + 1
            # Criação dos vetores RESULTADO
            vetor_x_power_ar_on = np.zeros((1, 1), dtype='<U22')
            vetor_y_power_ar_on = np.zeros((1, 1))
            vetor_z_power_ar_on = np.zeros((1, 1), dtype='<U22')
            n = 0
            # For que roda no tamanho da matrix ordenada
            for x in range(0, len(eixo_x_agrupado_power_ar_on)):
                if n == 0:
                    vetor_x_power_ar_on[0][0] = eixo_x_agrupado_power_ar_on[0][0]
                    vetor_y_power_ar_on[0][0] = eixo_x_agrupado_power_ar_on[0][1]
                    vetor_z_power_ar_on[0][0] = eixo_x_agrupado_power_ar_on[0][2]
                    n = 1
                else:
                    # Criacao das datas para comparativo e AGRUPAR os horarios dos mesmos 15min
                    data_obj = datetime.strptime(vetor_x_power_ar_on[0][n - 1],
                                                 '%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
                    data_horario_inicio = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO
                    data_comparativa_1 = (data_horario_inicio - (timedelta(minutes=15)))  # Data inicial + 15min
                    data_comparativa_2 = data_horario_inicio
                    dia_comparativo = vetor_z_power_ar_on[0][n - 1]

                    data_obj2 = datetime.strptime(eixo_x_agrupado_power_ar_on[x][0],
                                                  '%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    horario2 = (data_obj2).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
                    minha_data_horario2 = datetime.strptime(horario2, '%H:%M:%S')  # Converto novamente para OBJETO
                    data_horario2 = (minha_data_horario2 - (timedelta(minutes=15)))
                    dia_atual = eixo_x_agrupado_power_ar_on[x][2]

                    ##Trava para caso o vetor acabe apenas com 1 contagem na ultima casa, neste caso, a datação dela deve ser diferente para comparação.
                    if (x == (len(eixo_x_agrupado_power_ar_on) - 1)) and (eixo_x_agrupado_power_ar_on[x][1] == '1.0'):
                        data_horario2 = (minha_data_horario2)

                    # Se o horario atual estiver entre os 15min do horario do grupo e se for do mesmo dia, soma o valor de quantidades
                    if data_horario2 > data_comparativa_1 and data_horario2 < data_comparativa_2 and dia_atual == dia_comparativo:
                        vetor_y_power_ar_on[0][n - 1] = vetor_y_power_ar_on[0][n - 1] + float(
                            eixo_x_agrupado_power_ar_on[x][1])
                    # Se nao, aumento os vetores, e acrescento como um outro grupo
                    else:
                        # Incremento o vetor X com 1 posição a mais
                        vetor_x_power_ar_on = np.resize(vetor_x_power_ar_on, (1, len(vetor_x_power_ar_on[0]) + 1))
                        vetor_y_power_ar_on = np.resize(vetor_y_power_ar_on, (1, len(vetor_y_power_ar_on[0]) + 1))
                        vetor_z_power_ar_on = np.resize(vetor_z_power_ar_on, (1, len(vetor_z_power_ar_on[0]) + 1))
                        # Acrescento valores
                        vetor_x_power_ar_on[0][n] = eixo_x_agrupado_power_ar_on[x][0]
                        vetor_y_power_ar_on[0][n] = eixo_x_agrupado_power_ar_on[x][1]
                        vetor_z_power_ar_on[0][n] = eixo_x_agrupado_power_ar_on[x][2]
                        n = n + 1

            # Apresentação dos valores AGRUPADOS E ORDENADOS
            # print(vetor_x_power_ar_on)
            # print(vetor_y_power_ar_on)
            # print(vetor_z_power_ar_on)

            # Parametros de Configuração para Estatísticas
            somatorio_power_ar_on = 0
            qtd_somatorio_power_ar_on = 0

            # Capto o Valor da Taxa de Tendencia do BD
            # Executa o comando:
            cursor.execute("SELECT tendencia FROM configuracao_user  WHERE id=1")
            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    taxa_tendencia = linha[0] / 100
            else:
                print("Dados Insuficientes no Banco de Dados")
                # Finaliza a conexão

            # Loop para saber qual o total dos valores da ação
            for n in range(0, len(eixo_x_power_ar_on[0])):
                somatorio_power_ar_on = somatorio_power_ar_on + eixo_y_power_ar_on[0][n]
            # Loop para saber quantos valores estão acima da Taxa de Tendencia
            for nn in range(0, len(vetor_x_power_ar_on[0])):
                if (float(vetor_y_power_ar_on[0][nn]) / somatorio_power_ar_on) >= taxa_tendencia:
                    qtd_somatorio_power_ar_on = qtd_somatorio_power_ar_on + 1

            # Proteção para nao criar o vetor e nao tentar inserir no BD se nao existir Tendencias.
            if qtd_somatorio_power_ar_on > 0:

                k = 0
                # Criaçcao do Vetor
                tendencia_power_ar_on = np.zeros((qtd_somatorio_power_ar_on, 4), dtype='<U22')
                vetor_x_power_ar_on_tendencia = np.zeros((1, qtd_somatorio_power_ar_on), dtype='<U22')
                vetor_y_power_ar_on_tendencia = np.zeros((1, qtd_somatorio_power_ar_on))
                vetor_z_power_ar_on_tendencia = np.zeros((1, qtd_somatorio_power_ar_on), dtype='<U22')
                # Loop para procurar novamente valores acima da Taxa de Tendencia
                for nn in range(0, len(vetor_x_power_ar_on[0])):
                    # Condicação que compara cada valor com a Taxa de Tendencia
                    if (float(vetor_y_power_ar_on[0][nn]) / somatorio_power_ar_on) >= taxa_tendencia:
                        # Atribuições do Vetor
                        tendencia_power_ar_on[k][0] = "Power-Ar-On"
                        tendencia_power_ar_on[k][1] = vetor_x_power_ar_on[0][nn]
                        tendencia_power_ar_on[k][2] = vetor_z_power_ar_on[0][nn]
                        tendencia_power_ar_on[k][3] = vetor_y_power_ar_on[0][nn]
                        # Atribui Vetor de Tendencia que vai para o gráfico
                        vetor_x_power_ar_on_tendencia[0][k] = vetor_x_power_ar_on[0][nn]
                        vetor_y_power_ar_on_tendencia[0][k] = vetor_y_power_ar_on[0][nn]
                        vetor_z_power_ar_on_tendencia[0][k] = vetor_z_power_ar_on[0][nn]
                        k = k + 1

                ##########Inserção no BD#############
                # DELETA VALORES DO BD PREVIAMENTE CONFIGURADOS
                cursor.execute("DELETE FROM tendencias WHERE acao='Power-Ar-On'")
                # LOOP PARA INSERIR TODOS AS LINHAS DA MATRIZ
                for nn in range(0, len(tendencia_power_ar_on)):
                    # Executa o comando:
                    cursor.execute("INSERT INTO tendencias (acao,horario,dia,valor) VALUES(%s,%s,%s,%s)", (tendencia_power_ar_on[nn][0], tendencia_power_ar_on[nn][1], tendencia_power_ar_on[nn][2],tendencia_power_ar_on[nn][3]))
                conexao.close()
                print("Nova Tendência Registrada!")

            # CASO NAO HAJA TENDENCIA
            else:
                print("Não há tendência")
                # DELETA VALORES DO BD PREVIAMENTE CONFIGURADOS
                cursor.execute("DELETE FROM tendencias WHERE acao='Power-Ar-On'")
                conexao.close()
                #Cria o vetor com 1 posição
                vetor_x_power_ar_on_tendencia = np.zeros((1, 1), dtype='<U22')
                vetor_y_power_ar_on_tendencia = np.zeros((1, 1))
                vetor_z_power_ar_on_tendencia = np.zeros((1, 1), dtype='<U22')
                vetor_x_power_ar_on_tendencia[0][0] = "0"
                vetor_y_power_ar_on_tendencia[0][0] = 0
                vetor_z_power_ar_on_tendencia[0][0] = 0

            self.update_graph_machine_learning(vetor_x_power_ar_on[0], vetor_y_power_ar_on[0],
                                               vetor_z_power_ar_on[0], vetor_x_power_ar_on_tendencia[0],
                                               vetor_y_power_ar_on_tendencia[0], vetor_z_power_ar_on_tendencia[0])
        except pymysql.err.OperationalError as e:
            print("Error while connecting to MySQL", e)

    def machine_learning_power_ar_off(self):
        #Variaveis de Configuração
        qq = 0
        sair = 0
        taxa_tendencia=0.5
        power_ar_off = 0
        n_power_ar_off = 0
        quantidade_grupos_power_ar_off = 0

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT acao,valor,horario FROM historico_acoes ORDER BY TIME(horario) ASC")
            #cursor.execute("SELECT acao,valor,horario FROM historico_acoes ORDER BY horario ASC")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                mac_acao = np.array([[0] * 3] * cursor.rowcount, dtype='<U22')
                for linha in resultado:
                    mac_acao[qq][0] = linha[0]
                    mac_acao[qq][1] = linha[1]
                    mac_acao[qq][2] = linha[2]
                    #Verifica a categoria da Função atual
                    if mac_acao[qq][0] == 'Power-Ar-Off':
                        power_ar_off = power_ar_off + 1
                    #Contador de resultados
                    qq = qq + 1
            #criação do vetorcom a quantidade de resultados
            mac_power_ar_off = np.array([[0] * 3] * power_ar_off, dtype='<U22')

            #Conta a quantidade de resultados, e atribui ao novo vetor
            for x in range(0, cursor.rowcount):
                if mac_acao[x][0] == 'Power-Ar-Off':
                    mac_power_ar_off[n_power_ar_off] = mac_acao[x]
                    n_power_ar_off = n_power_ar_off + 1

            ##ESTATISTICA POWER AR Off
            # for x in range(0,n_power_ar_off):  #Apresenta todos os valores recuperados do BD. IMPORTANTE PARA CONFERENCIA
            #     print(mac_power_ar_off[x][2])

            # Criação dos Eixos E Vetor do dia do grupo
            eixo_x_power_ar_off = np.zeros((1, 1), dtype='<U22')
            eixo_y_power_ar_off = np.zeros((1, 1))
            dia_do_grupo_power_ar_off=np.zeros((1, 1),dtype='i4') #Torna o vetor, inteiro

            # Criação da data inicial
            data_obj = datetime.strptime(mac_power_ar_off[0][2], '%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
            horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
            data_horario_inicio = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO
            data_comparativa_1 = (data_horario_inicio + (timedelta(minutes=15)))  # Data inicial + 15min
            dia_comparativo=(data_obj).weekday() #Dia da semana da data comparativa
            dia_atual=dia_comparativo   #Dia da semana para comparação inicial

            # Contador do Loop
            nn = 0
            # Seto o primeiro valor do Eixo X e do Dia do Grupo 1
            eixo_x_power_ar_off[0][0] = data_comparativa_1
            dia_do_grupo_power_ar_off[0][0]=dia_comparativo

            # Loop Comparativo
            while sair == 0:
                # Se for a 1ª vez do loop, não incrementa os eixos
                if nn != 0:
                    # Incremento o vetor X com 1 posição a mais
                    eixo_x_power_ar_off = np.resize(eixo_x_power_ar_off, (1, len(eixo_x_power_ar_off[0]) + 1))
                    # Atribuo o valor para a posição Criada
                    eixo_x_power_ar_off[0][quantidade_grupos_power_ar_off] = data_comparativa_1

                    # Incremento o vetor dia_do_Grupo com 1 posição a mais
                    dia_do_grupo_power_ar_off = np.resize(dia_do_grupo_power_ar_off, (1, len(dia_do_grupo_power_ar_off[0]) + 1))
                    # Atribuo o valor para a posição Criada
                    dia_do_grupo_power_ar_off[0][quantidade_grupos_power_ar_off] = dia_comparativo

                    # Crio o vetor auxiliar para Incrementar Eixo Y
                    eixo_y_aux_power_ar_off = eixo_y_power_ar_off[:]
                    # Incremento Eixo Y
                    eixo_y_power_ar_off = np.zeros((1, len(eixo_y_power_ar_off[0]) + 1))
                    # Loop para atribuir respectivos valores do Eixo Y
                    for jj in range(0, len(eixo_y_aux_power_ar_off[0])):
                        eixo_y_power_ar_off[0][jj] = eixo_y_aux_power_ar_off[0][jj]

                # Loop Comparativo entre datas
                while data_horario_inicio <= data_comparativa_1 and nn < (n_power_ar_off - 1) and dia_atual==dia_comparativo:
                #while data_horario_inicio <= data_comparativa_1 and nn < ( n_power_ar_off - 1):
                    # Se tiver dentro dos 15min, Incrementa o valor do eixo Y
                    eixo_y_power_ar_off[0][quantidade_grupos_power_ar_off] = eixo_y_power_ar_off[0][quantidade_grupos_power_ar_off] + 1
                    nn = nn + 1
                    # Capto a nova Data, e deixo pronto pra nova passagem do loop
                    data_obj = datetime.strptime(mac_power_ar_off[nn][2],'%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
                    data_horario_inicio = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO
                    #Data em dia da Semana
                    dia_atual = (data_obj).weekday()

                # Quando sai do Loop, um novo grupo de datas é formado.
                quantidade_grupos_power_ar_off = quantidade_grupos_power_ar_off + 1

                # Se a contagem não for a ultima, atribuo um novo valor pra ultima data
                if nn != n_power_ar_off - 1:
                    data_comparativa_1 = (data_horario_inicio + timedelta(minutes=15))
                    dia_comparativo=(data_obj).weekday()
                # Se a contagem for a ultima, ele atribui a saida do loop geral
                if (nn == (n_power_ar_off - 1)):
                    sair = 1

            # Apos sair o loop, ele compara a ultima data (que não é comparada com o loop anterior)
            if data_horario_inicio <= data_comparativa_1 and dia_atual == dia_comparativo:
            #if data_horario_inicio <= data_comparativa_1:
                # Se for o mesmo intervalo de 15min, atribui o valor para o Eixo Y
                eixo_y_power_ar_off[0][quantidade_grupos_power_ar_off - 1] = eixo_y_power_ar_off[0][quantidade_grupos_power_ar_off - 1] + 1
            else:
                # Senao, cria um novo grupo, um novo Eixo X
                quantidade_grupos_power_ar_off = quantidade_grupos_power_ar_off + 1
                eixo_x_power_ar_off = np.resize(eixo_x_power_ar_off, (1, len(eixo_x_power_ar_off[0]) + 1))
                eixo_x_power_ar_off[0][quantidade_grupos_power_ar_off - 1] = data_comparativa_1

                # Incremento o vetor dia_doGrupo com 1 posição a mais
                dia_do_grupo_power_ar_off = np.resize(dia_do_grupo_power_ar_off, (1, len(dia_do_grupo_power_ar_off[0]) + 1))
                # Atribuo o valor para a posição Criada
                dia_do_grupo_power_ar_off[0][quantidade_grupos_power_ar_off-1] = dia_atual

                # Cria um novo valor pro Eixo Y, e atribui os valores antigos pro novo Eixo Y
                eixo_y_aux_power_ar_off = eixo_y_power_ar_off[:]
                eixo_y_power_ar_off = np.zeros((1, len(eixo_y_power_ar_off[0]) + 1))
                for jj in range(0, len(eixo_y_aux_power_ar_off[0])):
                    eixo_y_power_ar_off[0][jj] = eixo_y_aux_power_ar_off[0][jj]

                # Atribui novos valores pros eixos X e Y
                eixo_x_power_ar_off[0][quantidade_grupos_power_ar_off - 1] = data_horario_inicio
                eixo_y_power_ar_off[0][quantidade_grupos_power_ar_off - 1] = eixo_y_power_ar_off[0][ quantidade_grupos_power_ar_off - 1] + 1

            # Apresenta os Vetores
            # Grupos Misturados separados pelos dias das semanas a cada 15min.
            # print(eixo_x_power_ar_off)
            # print(eixo_y_power_ar_off)
            # print(dia_do_grupo_power_ar_off)

            ################# Aqui ocorre o agrupamento dos dias IGUAIS a cada 15min ####################
            #Criação do Vetor que ira receber os valores
            eixo_x_agrupado_power_ar_off=np.zeros((1, 3), dtype='<U22')
            n=0
            #For que ira rodar por todos os valores baixados do BD
            for kkk in range(0,7):
                for x in range(0, len(eixo_x_power_ar_off[0])):
                    #Aqui verifica qual dia da semana é.
                    if dia_do_grupo_power_ar_off[0][x] == kkk:
                        #Se for a primeira rodada no For:
                        if n==0:
                            eixo_x_agrupado_power_ar_off[n][0]=eixo_x_power_ar_off[0][x]
                            eixo_x_agrupado_power_ar_off[n][1]=eixo_y_power_ar_off[0][x]
                            eixo_x_agrupado_power_ar_off[n][2]=dia_do_grupo_power_ar_off[0][x]
                            n=1
                        else:
                            #Aumento o tamanho da minha matrix,e acrescenta os valores
                            eixo_x_agrupado_power_ar_off = np.resize(eixo_x_agrupado_power_ar_off, (len(eixo_x_agrupado_power_ar_off) + 1, 3))
                            eixo_x_agrupado_power_ar_off[n][0] = eixo_x_power_ar_off[0][x]
                            eixo_x_agrupado_power_ar_off[n][1] = eixo_y_power_ar_off[0][x]
                            eixo_x_agrupado_power_ar_off[n][2] = dia_do_grupo_power_ar_off[0][x]
                            n=n+1
            #Criação dos vetores RESULTADO
            vetor_x_power_ar_off = np.zeros((1, 1), dtype='<U22')
            vetor_y_power_ar_off = np.zeros((1, 1))
            vetor_z_power_ar_off = np.zeros((1, 1), dtype='<U22')
            n = 0
            #For que roda no tamanho da matrix ordenada
            for x in range(0,len(eixo_x_agrupado_power_ar_off)):
                if n==0:
                    vetor_x_power_ar_off[0][0]=eixo_x_agrupado_power_ar_off[0][0]
                    vetor_y_power_ar_off[0][0]=eixo_x_agrupado_power_ar_off[0][1]
                    vetor_z_power_ar_off[0][0]=eixo_x_agrupado_power_ar_off[0][2]
                    n=1
                else:
                    #Criacao das datas para comparativo e AGRUPAR os horarios dos mesmos 15min
                    data_obj = datetime.strptime(vetor_x_power_ar_off[0][n-1],'%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
                    data_horario_inicio = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO
                    data_comparativa_1 = (data_horario_inicio - (timedelta(minutes=15)))  # Data inicial + 15min
                    data_comparativa_2=data_horario_inicio
                    dia_comparativo = vetor_z_power_ar_off[0][n-1]


                    data_obj2 = datetime.strptime(eixo_x_agrupado_power_ar_off[x][0],'%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    horario2 = (data_obj2).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
                    minha_data_horario2 = datetime.strptime(horario2, '%H:%M:%S')  # Converto novamente para OBJETO
                    data_horario2 = (minha_data_horario2 - (timedelta(minutes=15)))
                    dia_atual = eixo_x_agrupado_power_ar_off[x][2]

                    ##Trava para caso o vetor acabe apenas com 1 contagem na ultima casa, neste caso, a datação dela deve ser diferente para comparação.
                    if (x == (len(eixo_x_agrupado_power_ar_off)-1)) and (eixo_x_agrupado_power_ar_off[x][1]=='1.0'):
                        data_horario2 = (minha_data_horario2 )


                    #Se o horario atual estiver entre os 15min do horario do grupo e se for do mesmo dia, soma o valor de quantidades
                    if data_horario2>data_comparativa_1 and data_horario2<data_comparativa_2 and dia_atual==dia_comparativo:
                        vetor_y_power_ar_off[0][n-1]=vetor_y_power_ar_off[0][n-1]+float(eixo_x_agrupado_power_ar_off[x][1])
                    #Se nao, aumento os vetores, e acrescento como um outro grupo
                    else:
                        # Incremento o vetor X com 1 posição a mais
                        vetor_x_power_ar_off = np.resize(vetor_x_power_ar_off,(1,len(vetor_x_power_ar_off[0])+1))
                        vetor_y_power_ar_off = np.resize(vetor_y_power_ar_off,(1, len(vetor_y_power_ar_off[0]) + 1))
                        vetor_z_power_ar_off = np.resize(vetor_z_power_ar_off,(1, len(vetor_z_power_ar_off[0]) + 1))
                        #Acrescento valores
                        vetor_x_power_ar_off[0][n] = eixo_x_agrupado_power_ar_off[x][0]
                        vetor_y_power_ar_off[0][n] = eixo_x_agrupado_power_ar_off[x][1]
                        vetor_z_power_ar_off[0][n]=eixo_x_agrupado_power_ar_off[x][2]
                        n=n+1

            #Apresentação dos valores AGRUPADOS E ORDENADOS
            # print(vetor_x_power_ar_off)
            # print(vetor_y_power_ar_off)
            # print(vetor_z_power_ar_off)


            #Parametros de Configuração para Estatísticas
            somatorio_power_ar_off=0
            qtd_somatorio_power_ar_off=0

            # Capto o Valor da Taxa de Tendencia do BD
            # Executa o comando:
            cursor.execute("SELECT tendencia FROM configuracao_user  WHERE id=1")
            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    taxa_tendencia = linha[0] / 100
            else:
                print("Dados Insuficientes no Banco de Dados")
                # Finaliza a conexão

            #Loop para saber qual o total dos valores da ação
            for n in range(0, len(eixo_x_power_ar_off[0])):
                somatorio_power_ar_off=somatorio_power_ar_off+eixo_y_power_ar_off[0][n]
            #Loop para saber quantos valores estão acima da Taxa de Tendencia
            for nn in range(0, len(vetor_x_power_ar_off[0])):
                if (float(vetor_y_power_ar_off[0][nn]) / somatorio_power_ar_off) >= taxa_tendencia:
                    qtd_somatorio_power_ar_off=qtd_somatorio_power_ar_off+1

            #Proteção para nao criar o vetor e nao tentar inserir no BD se nao existir Tendencias.
            if qtd_somatorio_power_ar_off>0:
                k=0
                #Criaçcao do Vetor
                tendencia_power_ar_off = np.zeros((qtd_somatorio_power_ar_off, 4), dtype='<U22')
                vetor_x_power_ar_off_tendencia = np.zeros((1, qtd_somatorio_power_ar_off), dtype='<U22')
                vetor_y_power_ar_off_tendencia = np.zeros((1, qtd_somatorio_power_ar_off))
                vetor_z_power_ar_off_tendencia = np.zeros((1, qtd_somatorio_power_ar_off), dtype='<U22')
                #Loop para procurar novamente valores acima da Taxa de Tendencia
                for nn in range(0, len(vetor_x_power_ar_off[0])):
                    #Condicação que compara cada valor com a Taxa de Tendencia
                    if (float(vetor_y_power_ar_off[0][nn]) / somatorio_power_ar_off) >= taxa_tendencia:
                        #Atribuições do Vetor
                        tendencia_power_ar_off[k][0]="Power-Ar-Off"
                        tendencia_power_ar_off[k][1]=vetor_x_power_ar_off[0][nn]
                        tendencia_power_ar_off[k][2]=vetor_z_power_ar_off[0][nn]
                        tendencia_power_ar_off[k][3]=vetor_y_power_ar_off[0][nn]
                        #Atribui Vetor de Tendencia que vai para o gráfico
                        vetor_x_power_ar_off_tendencia[0][k]=vetor_x_power_ar_off[0][nn]
                        vetor_y_power_ar_off_tendencia[0][k] = vetor_y_power_ar_off[0][nn]
                        vetor_z_power_ar_off_tendencia[0][k] = vetor_z_power_ar_off[0][nn]
                        k=k+1

                ##########Inserção no BD#############
                #DELETA VALORES DO BD PREVIAMENTE CONFIGURADOS
                cursor.execute("DELETE FROM tendencias WHERE acao='Power-Ar-Off'")
                #LOOP PARA INSERIR TODOS AS LINHAS DA MATRIZ
                for nn in range(0, len(tendencia_power_ar_off)):
                    # Executa o comando:
                    cursor.execute("INSERT INTO tendencias (acao,horario,dia,valor) VALUES(%s,%s,%s,%s)",(tendencia_power_ar_off[nn][0], tendencia_power_ar_off[nn][1], tendencia_power_ar_off[nn][2], tendencia_power_ar_off[nn][3]))
                conexao.close()
                print("Nova Tendência Registrada!")

            #CASO NAO HAJA TENDENCIA
            else:
                print("Não há tendência")
                #DELETA VALORES DO BD PREVIAMENTE CONFIGURADOS
                cursor.execute("DELETE FROM tendencias WHERE acao='Power-Ar-Off'")
                conexao.close()
                # Cria o vetor com 1 posição
                vetor_x_power_ar_off_tendencia = np.zeros((1, 1), dtype='<U22')
                vetor_y_power_ar_off_tendencia = np.zeros((1, 1))
                vetor_z_power_ar_off_tendencia = np.zeros((1, 1), dtype='<U22')
                vetor_x_power_ar_off_tendencia[0][0] = "0"
                vetor_y_power_ar_off_tendencia[0][0] = 0
                vetor_z_power_ar_off_tendencia[0][0] = 0

            self.update_graph_machine_learning(vetor_x_power_ar_off[0],vetor_y_power_ar_off[0],vetor_z_power_ar_off[0],vetor_x_power_ar_off_tendencia[0],vetor_y_power_ar_off_tendencia[0],vetor_z_power_ar_off_tendencia[0])
        except pymysql.err.OperationalError as e:
            print("Error while connecting to MySQL", e)

    def select_dia_graph_mac(self):
        data_atual = datetime.now()
        dia = data_atual.weekday()

        if dia==0:
            self.ui.comboBox_Dia_2.setCurrentText("Segunda")
        elif dia==1:
            self.ui.comboBox_Dia_2.setCurrentText("Terça")
        elif dia==2:
            self.ui.comboBox_Dia_2.setCurrentText("Quarta")
        elif dia==3:
            self.ui.comboBox_Dia_2.setCurrentText("Quinta")
        elif dia==4:
            self.ui.comboBox_Dia_2.setCurrentText("Sexta")
        elif dia==5:
            self.ui.comboBox_Dia_2.setCurrentText("Sábado")
        elif dia==6:
            self.ui.comboBox_Dia_2.setCurrentText("Domingo")

        self.ui.comboBox_3.currentIndexChanged.connect(self.select_graph_update_mac)
        self.ui.comboBox_Dia_2.currentIndexChanged.connect(self.select_graph_update_mac)
        self.ui.comboBox_2.currentIndexChanged.connect(self.select_graph_update_mac)

    def select_graph_update_mac(self):
        select_modo=self.ui.comboBox_3.currentText()
        if select_modo=="Ar Condicionado ON":
            self.machine_learning_power_ar_on()
        elif select_modo=="Ar Condicionado OFF":
            self.machine_learning_power_ar_off()
        elif select_modo=="Temperatura +":
            self.machine_learning_temperatura_ar_mais()
        elif select_modo=="Temperatura -":
            self.machine_learning_temperatura_ar_menos()

    def update_graph_machine_learning(self, eixo_x, eixo_y, eixo_z, eixo_x_tendencia, eixo_y_tendencia, eixo_z_tendencia):
        #Variaveis de Configurações Iniciais
        qtd_dias=0
        qtd_dias_tendencia=0
        n=0
        m=0
        #Pego o valor das caixas de Seleção
        select_modo_exibicao=self.ui.comboBox_2.currentText()
        select_dia = self.ui.comboBox_Dia_2.currentText()

        #Criação dos vetores do tamanho da entrada na Função
        novo_eixo_x_aux = np.zeros((1, len(eixo_x)), dtype='<U22')
        novo_eixo_y_aux = np.zeros((1, len(eixo_x)))
        novo_eixo_z_aux = np.zeros((1, len(eixo_x)))

        #Execução, caso selecionado modo GERAL
        if select_modo_exibicao=="Geral":
            n=1
            #Criação de vetor auxiliar para mudança de data
            novo_eixo_x_aux_data = np.zeros((1, len(eixo_x)), dtype='<U22')
            for x in range(0,len(eixo_x)):
                #Mudança de Data
                data_obj = datetime.strptime(eixo_x[x], '%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                novo_eixo_x_aux_data[0][x] = (data_obj).strftime('%H:%M')
                #Atribuições dos valores ao vetor
                novo_eixo_y_aux[0][x] = eixo_y[x]
                novo_eixo_z_aux[0][x] = eixo_z[x]
            #Transformação da Matriz, para vetor do gráfico
            novo_eixo_x = np.squeeze(np.asarray(novo_eixo_x_aux_data))
            novo_eixo_y = np.squeeze(np.asarray(novo_eixo_y_aux))
            #Caso nao haja tendencia, Também executa para eixo Z
            if eixo_x_tendencia[0][0] == "0":
                novo_eixo_z = np.squeeze(np.asarray(novo_eixo_z_aux))
            #Caso Haja tendencia
            if eixo_x_tendencia[0][0] != "0":
                #Criação dos vetores da Tendencia
                novo_eixo_x_aux_tendencia = np.zeros((1, len(eixo_x_tendencia)), dtype='<U22')
                novo_eixo_z_aux_tendencia = np.zeros((1, len(eixo_x_tendencia)))
                for x in range(0,len(eixo_x_tendencia)):
                    #Mudança de Data
                    data_obj = datetime.strptime(eixo_x_tendencia[x], '%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    novo_eixo_x_aux_tendencia[0][x]=(data_obj).strftime('%H:%M')
                    #Atribuição dos valores de Z
                    novo_eixo_z_aux_tendencia[0][x]=float(eixo_z_tendencia[x])
                #Concatenção dos valores de Z do vetor e do Vetor Tendencia, para nomeação quando plotar o grafico
                novo_eixo_z=np.concatenate((novo_eixo_z_aux,novo_eixo_z_aux_tendencia),axis=1)
                #Conversão das Matrizes para Vetores
                novo_eixo_x_tendencia = np.squeeze(np.asarray(novo_eixo_x_aux_tendencia))
                novo_eixo_z_tendencia = np.squeeze(np.asarray(novo_eixo_z))
                novo_eixo_y_tendencia=eixo_y_tendencia
        #Caso Seleção seja Diária
        else:
            #Atribuição do dia da semana
            if select_dia=="Segunda":
                dia=0
            elif select_dia=="Terça":
                dia=1
            elif select_dia=="Quarta":
                dia=2
            elif select_dia=="Quinta":
                dia=3
            elif select_dia=="Sexta":
                dia=4
            elif select_dia=="Sábado":
                dia=5
            elif select_dia=="Domingo":
                dia=6

            for x in range(0, len(eixo_z)):
                #Somatorio da quantidade de resultados
                if int(eixo_z[x])==dia:
                    qtd_dias=qtd_dias+1
            #Caso seja diferente de zero, cria os vetores dos respectivos tamanhos
            if qtd_dias!=0:
                novo_eixo_x_aux = np.zeros((1, qtd_dias), dtype='<U22')
                novo_eixo_y_aux = np.zeros((1, qtd_dias))
                novo_eixo_z_aux = np.zeros((1, qtd_dias))
            else:
                #Se for zero, crio vetor com 1 posição para evitar erro
                novo_eixo_x_aux = np.zeros((1, 1), dtype='<U22')
                novo_eixo_y_aux = np.zeros((1, 1))
                novo_eixo_z_aux = np.zeros((1, 1))

            for x in range(0, len(eixo_z)):
                #Verificação se há grafico no dia selecionado
                if int(eixo_z[x])==dia:
                    #Condiguração da Data e Atribuição dos vetores
                    data_obj = datetime.strptime(eixo_x[x], '%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    novo_eixo_x_aux[0][n] = (data_obj).strftime('%H:%M')
                    novo_eixo_y_aux[0][n] = eixo_y[x]
                    novo_eixo_z_aux[0][n] = eixo_z[x]
                    n = n + 1
            #Se não houver Dados no dia, Atribuo valores Default para evitar erro
            if n==0:
                novo_eixo_x_aux[0][0] = "0"
                novo_eixo_y_aux[0][0] = 0
                novo_eixo_z_aux[0][0] = 0
                novo_eixo_x = np.squeeze(np.asarray(novo_eixo_x_aux))
                novo_eixo_y = np.squeeze(np.asarray(novo_eixo_y_aux))
                novo_eixo_z = np.squeeze(np.asarray(novo_eixo_z_aux))
            #Se houver 1 valor, atribuo o unico valor ao vetor
            elif n==1:
                novo_eixo_x = [novo_eixo_x_aux[0][0]]
                novo_eixo_y = [novo_eixo_y_aux[0][0]]
                novo_eixo_z = [novo_eixo_z_aux[0][0]]
            #Caso haja varios valores, há a conversão da Matriz, para Vetor
            else:
                novo_eixo_x = np.squeeze(np.asarray(novo_eixo_x_aux))
                novo_eixo_y = np.squeeze(np.asarray(novo_eixo_y_aux))
                novo_eixo_z = np.squeeze(np.asarray(novo_eixo_z_aux))

##################Caso haja TENDENCIA, repete-se o mesmo procedimento
            if eixo_x_tendencia[0][0] != "0":
                for x in range(0, len(eixo_z_tendencia)):
                    if int(eixo_z_tendencia[x]) == dia:
                        qtd_dias_tendencia = qtd_dias_tendencia + 1

                if qtd_dias_tendencia != 0:
                    novo_eixo_x_aux_tendencia = np.zeros((1, qtd_dias_tendencia), dtype='<U22')
                    novo_eixo_y_aux_tendencia = np.zeros((1, qtd_dias_tendencia))
                    novo_eixo_z_aux_tendencia = np.zeros((1, qtd_dias_tendencia))
                else:
                    novo_eixo_x_aux_tendencia = np.zeros((1, 1), dtype='<U22')
                    novo_eixo_y_aux_tendencia = np.zeros((1, 1))
                    novo_eixo_z_aux_tendencia = np.zeros((1, 1))

                for x in range(0, len(eixo_z_tendencia)):
                    if int(eixo_z_tendencia[x]) == dia:
                        data_obj = datetime.strptime(eixo_x_tendencia[x], '%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                        novo_eixo_x_aux_tendencia[0][m] = (data_obj).strftime('%H:%M')
                        novo_eixo_y_aux_tendencia[0][m] = eixo_y_tendencia[x]
                        novo_eixo_z_aux_tendencia[0][m] = eixo_z_tendencia[x]
                        m = m + 1
                if m == 0:
                    novo_eixo_x_aux_tendencia[0][0] = "0"
                    novo_eixo_y_aux_tendencia[0][0] = 0
                    novo_eixo_z_aux_tendencia[0][0] = 0
                    novo_eixo_x_tendencia = np.squeeze(np.asarray(novo_eixo_x_aux_tendencia))
                    novo_eixo_y_tendencia = np.squeeze(np.asarray(novo_eixo_y_aux_tendencia))
                    novo_eixo_z_tendencia = np.squeeze(np.asarray(novo_eixo_z_aux_tendencia))

                elif m == 1:
                    novo_eixo_x_tendencia = [novo_eixo_x_aux_tendencia[0][0]]
                    novo_eixo_y_tendencia = [novo_eixo_y_aux_tendencia[0][0]]
                    novo_eixo_z_tendencia = [novo_eixo_z_aux_tendencia[0][0]]
                else:
                    novo_eixo_x_tendencia = np.squeeze(np.asarray(novo_eixo_x_aux_tendencia))
                    novo_eixo_y_tendencia = np.squeeze(np.asarray(novo_eixo_y_aux_tendencia))
                    novo_eixo_z_tendencia = np.squeeze(np.asarray(novo_eixo_z_aux_tendencia))
        # Cria os Graficos
        self.ui.MplWidget_2.canvas.axes.clear()
        # Linhas
        self.ui.MplWidget_2.canvas.axes.plot(novo_eixo_x, novo_eixo_y, 'pink', linewidth=3)
        # Bolas
        self.ui.MplWidget_2.canvas.axes.plot(novo_eixo_x, novo_eixo_y, 'or', linewidth=8)
        # Barras Gerais
        self.ui.MplWidget_2.canvas.axes.bar(novo_eixo_x, novo_eixo_y)
        #Verificação para Barras de Tendencia
        if eixo_x_tendencia[0][0]!="0" and select_modo_exibicao != "Geral":
            if novo_eixo_y_aux_tendencia[0][0]!=0.0:
                self.ui.MplWidget_2.canvas.axes.bar(novo_eixo_x_tendencia, novo_eixo_y_tendencia, color='r')
        if eixo_x_tendencia[0][0] != "0" and select_modo_exibicao == "Geral":
            self.ui.MplWidget_2.canvas.axes.bar(novo_eixo_x_tendencia, novo_eixo_y_tendencia, color='r')
        # Apresenta os valores nos eixos
        for p in self.ui.MplWidget_2.canvas.axes.patches:
            self.ui.MplWidget_2.canvas.axes.annotate(p.get_height(),(p.get_x() + p.get_width() / 2., p.get_height()),ha='center', va='center', fontsize=11, color='gray',xytext=(0, 20),textcoords='offset points')
        #Apresenta NOMES DOS DIAS nas Barras
        if select_modo_exibicao == "Geral":
            l = 0
            if eixo_x_tendencia[0][0] != "0":
                for p in (self.ui.MplWidget_2.canvas.axes.patches):
                    if novo_eixo_z_tendencia[l] == 0:
                        dia = "Seg"
                    elif novo_eixo_z_tendencia[l] == 1:
                        dia = "Ter"
                    elif novo_eixo_z_tendencia[l] == 2:
                        dia = "Qua"
                    elif novo_eixo_z_tendencia[l] == 3:
                        dia = "Qui"
                    elif novo_eixo_z_tendencia[l] == 4:
                        dia = "Sex"
                    elif novo_eixo_z_tendencia[l] == 5:
                        dia = "Sáb"
                    elif novo_eixo_z_tendencia[l] == 6:
                        dia = "Dom"
                    self.ui.MplWidget_2.canvas.axes.annotate(dia, (p.get_x() + p.get_width() / 2., p.get_height()),ha='center', va='center', fontsize=11, color='white',xytext=(0, -15), textcoords='offset points', rotation=90)
                    l = l + 1
            #Caso Seleção seja Diária
            else:
                for p in (self.ui.MplWidget_2.canvas.axes.patches):
                    if novo_eixo_z[l]==0:
                        dia="Seg"
                    elif novo_eixo_z[l]==1:
                        dia="Ter"
                    elif novo_eixo_z[l]==2:
                        dia="Qua"
                    elif novo_eixo_z[l]==3:
                        dia="Qui"
                    elif novo_eixo_z[l]==4:
                        dia="Sex"
                    elif novo_eixo_z[l]==5:
                        dia="Sáb"
                    elif novo_eixo_z[l]==6:
                        dia="Dom"
                    self.ui.MplWidget_2.canvas.axes.annotate(dia,(p.get_x() + p.get_width() / 2., p.get_height()),ha='center', va='center', fontsize=11, color='white',xytext=(0, -15),textcoords='offset points', rotation=90)
                    l=l+1
        # Seta os limites do Eixo Y para os valores nas barras nao Ultrapassar o Grafico
        if n!=0:
            self.ui.MplWidget_2.canvas.axes.set_ylim(0, max((novo_eixo_y)) + 0.15 * max((novo_eixo_y)))
        self.ui.MplWidget_2.canvas.axes.legend(['Padrões do Usuário'], loc='upper right')
        self.ui.MplWidget_2.canvas.axes.set_xticks(novo_eixo_x)
        #Configuração para Titulo do Gráfico Personalizado
        if select_modo_exibicao == "Geral":
            titulo = "Gráfico de Tendências - Geral"
            self.ui.MplWidget_2.canvas.axes.set_title(titulo)
        else:
            if dia == 0:
                titulo = "Gráfico de Tendências - Segunda"
            elif dia == 1:
                titulo = "Gráfico de Tendências - Terça"
            elif dia == 2:
                titulo = "Gráfico de Tendências - Quarta"
            elif dia == 3:
                titulo = "Gráfico de Tendências - Quinta"
            elif dia == 4:
                titulo = "Gráfico de Tendências - Sexta"
            elif dia == 5:
                titulo = "Gráfico de Tendências - Sábado"
            elif dia == 6:
                titulo = "Gráfico de Tendências - Domingo"
        self.ui.MplWidget_2.canvas.axes.set_title(titulo)
        # Classifica as unidades dos eixos de acordo com as selecoes
        self.ui.MplWidget_2.canvas.axes.set_ylabel('Recorrência')
        self.ui.MplWidget_2.canvas.axes.set_xlabel('Horário')
        self.ui.MplWidget_2.canvas.axes.grid()
        self.ui.MplWidget_2.canvas.draw()

    def controle(self):
        controle = self.check_controle()
        if controle == True:
            self.auto_tendencias()


    #Funções dos Agentes
    #Controle Lâmpada
    def lamp_control(self, input):
        dados="p,{}".format(input)
        serial_port.write(dados.encode('utf-8'))
        serial_port.flush()
        data = serial_port.readline().decode('utf-8').replace('\r\n', '')
        print(data)

        #serial_port.close()

    #Temperatura e Umidade
    def temp_umid(self):
        serial_port.write(b't')
        serial_port.flush()
        data1 = serial_port.readline().decode('utf-8').replace('\r\n', '')
        data2 = serial_port.readline().decode('utf-8').replace('\r\n', '')
        return (data1, data2)
        #serial_port.close()

    # Temperatura e Umidade
    def temp_agua(self):
        serial_port.write(b'a')
        serial_port.flush()
        data1 = serial_port.readline().decode('utf-8').replace('\r\n', '')
        return (data1)
        # serial_port.close()

    #Intensidade Luminosa
    def luximetro(self):
        serial_port.write(b'l')
        serial_port.flush()
        data = serial_port.readline().decode('utf-8').replace('\r\n', '').replace(',', '.')
        return (data)
        #serial_port.close()

    # Sensores de Movimento
    def pir1(self):
        serial_port.write(b'm')
        serial_port.flush()
        data = serial_port.readline().decode('utf-8').replace('\r\n', '').replace(',', '.')
        return (data)
            # serial_port.close()
    def pir2(self):
        #Registrar esse comando no Arduino quando instalar o segundo sensor
        serial_port.write(b'm2')
        serial_port.flush()
        data = serial_port.readline().decode('utf-8').replace('\r\n', '').replace(',', '.')
        return (data)
            # serial_port.close()

    #Controle TV
    def power_off_tv(self):
        serial_port.write(b's,2,99,3450,1700,450,400,450,1250,450,450,400,450,450,400,450,400,450,450,400,450,400,450,450,400,450,400,450,450,400,450,450,1250,450,450,400,450,450,400,450,400,450,400,450,450,400,450,450,400,450,400,450,1300,450,400,450,400,450,400,450,450,400,450,450,400,450,400,450,450,400,1300,450,400,450,1300,400,1300,450,1300,400,1300,450,400,450,400,450,1300,450,400,450,1300,400,1300,450,1250,450,1300,450,400,450,1300,400')
        serial_port.flush()
        return("Comando Enviado para TV")
        #serial_port.close()

    def canal_mais_tv(self):
        serial_port.write(b's,2,99,3450,1650,450,450,450,1250,450,400,450,450,400,450,450,400,450,400,450,450,400,450,450,400,450,400,450,400,450,450,400,1300,450,400,450,450,400,450,450,400,450,400,450,400,450,450,400,450,450,400,450,1300,400,450,450,400,450,400,450,400,450,450,400,450,450,400,450,400,450,450,400,450,450,1250,450,400,450,1300,450,1250,450,450,400,450,450,400,450,400,450,1300,400,450,450,1250,450,1300,450,400,450,1250,450')
        serial_port.flush()
        return("Comando Enviado para TV")
        #serial_port.close()

    def canal_menos_tv(self):
        serial_port.write(b's,2,99,3450,1650,450,450,450,1250,450,400,450,450,400,450,450,400,450,400,450,400,450,450,400,450,450,400,450,400,450,450,400,1300,450,400,450,400,450,450,400,450,450,400,450,400,450,450,400,450,450,400,450,1250,450,450,450,400,450,400,450,450,400,450,400,450,450,400,450,400,450,1300,450,400,450,1250,450,450,400,1300,450,1300,400,450,450,400,450,1250,450,450,400,1300,450,400,450,1300,450,1250,450,400,450,1300,450')
        serial_port.flush()
        return("Comando Enviado para TV")
        #serial_port.close()

    def vol_mais_tv(self):
        serial_port.write(b's,2,99,3450,1700,450,400,500,1250,450,400,450,400,450,400,500,400,450,400,450,400,450,400,450,450,450,400,450,400,450,400,500,1250,450,400,450,400,450,400,500,400,400,450,450,400,450,400,500,350,500,400,450,1250,450,400,450,450,450,400,450,400,450,400,500,350,500,400,450,400,450,400,450,400,500,400,450,400,450,400,450,1250,500,400,450,400,450,400,450,400,500,400,450,400,450,400,450,1250,500,400,450,1250,450')
        serial_port.flush()
        return("Comando Enviado para TV")
        #serial_port.close()

    def vol_menos_tv(self):
        serial_port.write(b's,2,99,3450,1700,450,400,500,1250,450,400,450,400,500,350,500,400,450,400,450,400,450,400,500,400,450,400,450,400,450,400,500,1250,450,400,450,400,450,400,500,400,450,400,450,400,450,400,500,350,500,400,450,1250,450,400,450,450,400,450,450,400,450,400,500,350,500,400,450,400,450,1250,500,400,450,400,450,400,450,400,450,1300,450,400,450,400,450,1300,450,400,450,400,450,400,450,400,500,1250,450,400,450,1300,450')
        serial_port.flush()
        return("Comando Enviado para TV")
        #serial_port.close()

    #Controle AR
    def power_off_ar(self):
        #Mudar o Codigo do Comando
        serial_port.write(b's,2,99,3450,1650,450,450,450,1250,450,400,450,450,400,450,450,400,450,400,450,450,400,450,450,400,450,400,450,400,450,450,400,1300,450,400,450,450,400,450,450,400,450,400,450,400,450,450,400,450,450,400,450,1300,400,450,450,400,450,400,450,400,450,450,400,450,450,400,450,400,450,450,400,450,450,1250,450,400,450,1300,450,1250,450,450,400,450,450,400,450,400,450,1300,400,450,450,1250,450,1300,450,400,450,1250,450')
        serial_port.flush()
        return("Comando Enviado para o AR")
        #serial_port.close()

    def temp_mais_ar(self):
        #Mudar o Codigo do Comando
        serial_port.write(b's,2,99,3450,1650,450,450,450,1250,450,400,450,450,400,450,450,400,450,400,450,450,400,450,450,400,450,400,450,400,450,450,400,1300,450,400,450,450,400,450,450,400,450,400,450,400,450,450,400,450,450,400,450,1300,400,450,450,400,450,400,450,400,450,450,400,450,450,400,450,400,450,450,400,450,450,1250,450,400,450,1300,450,1250,450,450,400,450,450,400,450,400,450,1300,400,450,450,1250,450,1300,450,400,450,1250,450')
        serial_port.flush()
        return("Comando Enviado para o AR")
        #serial_port.close()

    def temp_menos_ar(self):
        #Mudar o Codigo do Comando
        serial_port.write(b's,2,99,3450,1650,450,450,450,1250,450,400,450,450,400,450,450,400,450,400,450,450,400,450,450,400,450,400,450,400,450,450,400,1300,450,400,450,450,400,450,450,400,450,400,450,400,450,450,400,450,450,400,450,1300,400,450,450,400,450,400,450,400,450,450,400,450,450,400,450,400,450,450,400,450,450,1250,450,400,450,1300,450,1250,450,450,400,450,450,400,450,400,450,1300,400,450,450,1250,450,1300,450,400,450,1250,450')
        serial_port.flush()
        return("Comando Enviado para o AR")
        #serial_port.close()

    def modo_ar(self):
        #Mudar o Codigo do Comando
        serial_port.write(b's,2,99,3450,1650,450,450,450,1250,450,400,450,450,400,450,450,400,450,400,450,450,400,450,450,400,450,400,450,400,450,450,400,1300,450,400,450,450,400,450,450,400,450,400,450,400,450,450,400,450,450,400,450,1300,400,450,450,400,450,400,450,400,450,450,400,450,450,400,450,400,450,450,400,450,450,1250,450,400,450,1300,450,1250,450,450,400,450,450,400,450,400,450,1300,400,450,450,1250,450,1300,450,400,450,1250,450')
        serial_port.flush()
        return("Comando Enviado para o AR")
        #serial_port.close()


    #Apresentação de Parâmetros na interface
    def apresenta_parametros(self):
        global presenca
        umidade,temperatura=self.temp_umid()
        lux=self.luximetro()
        self.ui.txt_temp_amb.setText(temperatura + "ºC")
        self.ui.txt_umid.setText(umidade + "%")
        self.ui.txt_lux.setText(lux)

        if presenca==True:
            self.ui.txt_presenca.setText("Há alguém no cômodo!")
        else:
            self.ui.txt_presenca.setText("Não há presença no cômodo!")
        # tt = threading.Timer(1, self.apresenta_parametros)
        # tt.start()

    #Automação e Controle
    def check_aprendizagem(self):
        #Checagem para chamar Machine Learning
        teste_conexao = 0
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT aprendizagem FROM configuracao_user  WHERE id=1")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    aprendizagem = linha[0]

            if aprendizagem==True:
                self.ui.txt_modo_aprendizagem.setText("Modo Aprendizagem Habilitado")
            else:
                self.ui.txt_modo_aprendizagem.setText("Modo Aprendizagem Desabilitado")

            return aprendizagem


        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText(
                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def check_controle(self):
        #Checagem para chamar Machine Learning
        teste_conexao = 0
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT controle FROM configuracao_user  WHERE id=1")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    controle = linha[0]

            if controle==True:
                self.ui.txt_modo_aprendizagem.setText("Modo Controle Habilitado")
            else:
                self.ui.txt_modo_aprendizagem.setText("Modo Controle Desabilitado")
            return controle


        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText(
                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def check_economia(self):
        #Checagem para chamar Machine Learning
        teste_conexao = 0
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT economia FROM configuracao_user  WHERE id=1")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                for linha in resultado:
                    economia = linha[0]

            if economia==True:
                self.ui.txt_modo_aprendizagem.setText("Modo Economia Habilitado")
            else:
                self.ui.txt_modo_aprendizagem.setText("Modo Economia Desabilitado")
            return economia


        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText(
                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def check_tendencias(self):
        # Checagem para chamar Machine Learning
        global tendencias
        teste_conexao = 0
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT * FROM tendencias")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            i=0
            res = np.array([[0] * 5] * cursor.rowcount, dtype='<U22')
            if cursor.rowcount > 0:
                for linha in resultado:
                    res[i][0] = linha[0]
                    res[i][1]=linha[1]
                    res[i][2]=linha[2]
                    res[i][3]=linha[3]
                    res[i][4]=linha[4]

                    i+=1

            tendencias = np.array([[0] * 3] * cursor.rowcount, dtype='<U22')

            for x in range(0,cursor.rowcount):
                tendencias[x][0]=res[x][2]
                tendencias[x][1]=res[x][1]
                tendencias[x][2]=res[x][3]

            #Chama a função Auto_tendencias para executar as tarefas
            #self.auto_tendencias()

        except pymysql.err.OperationalError as e:
            if teste_conexao == 0:
                print("Error while connecting to MySQL", e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText(
                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao = 1

    def check_pir1(self):
        #Função para Presença IN
        global verify_pir1
        global presenca
        global time_last
        global time_last2
        #Variavel de verificação se é o primeiro loop
        loop1=False
        #Pega o horário atual para verificar se passaram 5s do PIR2
        real_time=datetime.now()
        #Se houver presença e se tiver passado mais de 10s do horário PIR2
        if presenca==False and real_time-time_last2>timedelta(seconds=10):
            #Se não tiver terminado a ultima verificação, nao começa uma nova
            if verify_pir1==False:
                #Capta valor do sensor 1
                pir1 = self.pir1()
                #Se for captado
                if pir1=="1":
                    #Seta como inciado o processo
                    verify_pir1 = True
                    ##Trocar pelo comando do sensor
                    #pir2=.self.pir2()
                    pir2="1"
                    #Se o sensor 2 estiver acionado
                    if pir2=="1":
                        #Há presença no comodo
                        presenca=True
                        #Se o loop ocorrer, seta o novo horario
                        if loop1==False:
                            time_last=datetime.now()
                            loop1=True
                #Finaliza o loop
                verify_pir1=False
                loop1=False

    def check_pir2(self):
        #Função para Presença OUT
        #VERIFICAR CODIGO CORRIGIDO ACIMA
        global verify_pir2
        global presenca
        global time_last
        global time_last2
        loop1=True
        time_atual=datetime.now()
        if presenca==True and time_atual-time_last>timedelta(seconds=10):
            if verify_pir2==False:
                ##Trocar pelo comando do sensor
                #pir2 = self.pir2()
                pir2="1"
                pir1=self.pir1()
                #if pir2=="1":
                if pir1=="1":
                    verify_pir2 = True
                    pir1=self.pir1()
                    if pir1=="1":
                        presenca=False
                        if loop1 ==True:
                            time_last2=datetime.now()
                            loop1=False

                verify_pir2=False
                loop1=True

    def auto_tendencias(self):
        #Pegando a hora atual
        data_atual=datetime.now()
        horario_atual = (data_atual).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
        data_atual = datetime.strptime(horario_atual, '%H:%M:%S')  # Converto novamente para OBJETO

        print("Verificando atividades agendadas e a próxima verificação é em:{}".format((data_atual + (timedelta(minutes=5)))))

        #Pegando o numero do dia
        dia_da_semana=datetime.now().weekday()
        #For para conferir cada uma das tendencias e ver se está no horário de acionar
        for x in range(0,len(tendencias)-1):
            data_obj = datetime.strptime(tendencias[x][0], '%Y-%m-%d %H:%M:%S')
            horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
            data_obj = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO
            dia_tendencia=int(tendencias[x][2])
            #Soma 5min à hora do sistema, para verificar se está no range
            data_comparativa=(data_atual + (timedelta(minutes=5)))
            #Se a tendencia é maior que a hora atual e menor ou igual a hora daqui 5min


            if data_atual<=data_obj<=data_comparativa and dia_da_semana==dia_tendencia:
                #Atribui a ação
                acao=tendencias[x][1]
                #Verifica a ação e entra em cada uma das funções
                if acao == "Power-Ar-On":
                    #Pega o valor do botao para conferir se ja esta ligado
                    valor = self.ui.btn_power_ar.text()
                    if valor == 'Ligar':
                        #Executa a ação
                        self.power_off_ar
                        #Valor que vai para o UPDATE
                        valor = True
                        #Atualiza o campo de texto
                        self.ui.btn_power_ar.setText("Desligar")
                        teste_conexao = 0
                        try:
                            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                            # Cria um cursor:
                            cursor = conexao.cursor()
                            # Executa o comando:
                            cursor.execute("UPDATE configuracao_user SET ar_condicionado=%s WHERE id=1", valor)
                            conexao.close()
                        except pymysql.err.OperationalError as e:
                            if teste_conexao == 0:
                                print("Error while connecting to MySQL", e)

                                msg = QMessageBox()
                                msg.setIcon(QMessageBox.Critical)

                                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                                msg.setWindowTitle("Erro em executar a ação:", acao)
                                msg.setDetailedText(
                                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                                msg.exec_()
                                teste_conexao = 1
                        print("A ação {} foi executada!".format(acao))
                    else:
                        # Caso o ar já esteja ligado
                        print("O Ar já se encontra Ligado!")
##################EXECUTA O MESMO CODIGO ACIMA. VERIFICAR COMENTÁRIOS#########################
                elif acao=="Power-Ar-Off":
                    valor = self.ui.btn_power_ar.text()
                    if valor == 'Desligar':
                        self.power_off_ar()
                        valor = False
                        self.ui.btn_power_ar.setText("Ligar")
                        teste_conexao = 0
                        try:
                            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                            # Cria um cursor:
                            cursor = conexao.cursor()
                            # Executa o comando:
                            cursor.execute("UPDATE configuracao_user SET ar_condicionado=%s WHERE id=1", valor)
                            conexao.close()
                        except pymysql.err.OperationalError as e:
                            if teste_conexao == 0:
                                print("Error while connecting to MySQL", e)

                                msg = QMessageBox()
                                msg.setIcon(QMessageBox.Critical)

                                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                                msg.setWindowTitle("Erro em executar a ação:", acao)
                                msg.setDetailedText(
                                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                                msg.exec_()
                                teste_conexao = 1
                        print("A ação {} foi executada!".format(acao))
                    else:
                        print("O Ar já se encontra Desligado!")

                elif acao=="Temperatura-Ar-Mais":
                    valor = self.ui.btn_power_ar.text()
                    if valor == 'Desligar':
                        self.temp_mais_ar()
                        valor = int(self.ui.text_temp_ar.text()) + 1
                        self.ui.text_temp_ar.setText(str(valor))
                        teste_conexao = 0
                        try:
                            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                            # Cria um cursor:
                            cursor = conexao.cursor()
                            # Executa o comando:
                            cursor.execute("UPDATE configuracao_user SET temp_ar=%s WHERE id=1", valor)
                            conexao.close()
                        except pymysql.err.OperationalError as e:
                            if teste_conexao == 0:
                                print("Error while connecting to MySQL", e)

                                msg = QMessageBox()
                                msg.setIcon(QMessageBox.Critical)

                                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                                msg.setWindowTitle("Erro em executar a ação:", acao)
                                msg.setDetailedText(
                                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                                msg.exec_()
                                teste_conexao = 1
                        print("A ação {} foi executada!".format(acao))
                    else:
                        print("O Ar se encontra Desligado!")

                elif acao=="Temperatura-Ar-Menos":
                    valor = self.ui.btn_power_ar.text()
                    if valor == 'Desligar':
                        self.temp_menos_ar()
                        valor = int(self.ui.text_temp_ar.text()) - 1
                        self.ui.text_temp_ar.setText(str(valor))
                        teste_conexao = 0
                        try:
                            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                            # Cria um cursor:
                            cursor = conexao.cursor()
                            # Executa o comando:
                            cursor.execute("UPDATE configuracao_user SET temp_ar=%s WHERE id=1", valor)
                            conexao.close()
                        except pymysql.err.OperationalError as e:
                            if teste_conexao == 0:
                                print("Error while connecting to MySQL", e)

                                msg = QMessageBox()
                                msg.setIcon(QMessageBox.Critical)

                                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                                msg.setWindowTitle("Erro em executar a ação:", acao)
                                msg.setDetailedText(
                                    "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                                msg.exec_()
                                teste_conexao = 1
                        print("A ação {} foi executada!".format(acao))
                    else:
                        print("O Ar se encontra Desligado!")

    def auto_iluminacao(self):
        global verify_pid_lamp
        global target_lamp
        global verify_lamp_economic
        #Verifica Check Controle e Economia
        controle=self.check_controle()
        economia=self.check_economia()
        #Se os dois estiverem setados
        if controle==True and economia==True:
            try:
                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
                # Executa o comando:
                cursor.execute("SELECT lux FROM configuracao_user  WHERE id=1")

                # Recupera o resultado:
                resultado = cursor.fetchall()
                if cursor.rowcount > 0:
                    for linha in resultado:
                        lux = linha[0]
                    #Seto a intensidade luminosa
                    target_lamp = lux
                    #Seta Verify PID para cancelar a configuração inicial
                    verify_pid_lamp = True
                    #Envia o comando
                    self.configuracao_pid("Iluminação", lux)

            except pymysql.err.OperationalError as e:
                print("Error while connecting to MySQL", e)
        elif controle == True and economia == False and verify_lamp_economic==False:
            verify_pid_lamp = True
            # Envia o comando
            self.lamp_control(100)
            self.update_estado_iluminacao_on()
            verify_lamp_economic=True

    #Configuração PID
    def configuracao_pid(self,modo,target):
        global config_pid_banho
        global config_pid_lamp
        global pid_lamp
        global verify_pid_lamp
        #Setando variaveis PID
        kp=1.4
        ki=0.4
        kd=0.0
        #Se modo Iluminação
        if modo=="Iluminação":
            #Se não tiver configurado
            if config_pid_lamp == False:
                #Seta parametros
                pid_lamp = PID.PID(kp, ki, kd)
                pid_lamp.SetPoint = target
                pid_lamp.setSampleTime(1)
                config_pid_lamp = True
                print("PID Configurado")
            #Se já houver sido configurado, seta parâmetros e executa o Update
            pid_lamp.SetPoint = target
            pid_lamp.setKp(kp)
            pid_lamp.setKi(ki)
            pid_lamp.setKd(kd)
            lux= self.luximetro()
            pid_lamp.update(float(lux))
            targetPwm = pid_lamp.output
        #Se for Controle da agua do Chuveiro
        else:
            if config_pid_banho == False:
                pid_banho = PID.PID(kp, ki, kd)
                pid_banho.SetPoint = target
                pid_banho.setSampleTime(1)
                config_pid_banho = True
                print("PID Configurado")
            #Se já houver sido configurado
            pid_banho.SetPoint = target
            pid_banho.setKp(kp)
            pid_banho.setKi(ki)
            pid_banho.setKd(kd)
            temp = self.temp_agua()
            pid_banho.update(float(temp))
            targetPwm = pid_banho.output

        #Seta o valor PWM
        targetPwm = max(min(int(targetPwm), 100), 0)

        if modo == "Iluminação":
            #Seta o PWM para lâmpada
            self.lamp_control(targetPwm)
            #Capta se a Lâmpada estava desligada
            state_lamp=self.ui.txt_state_lamp.text()
            print("SET: %.1f LUX | ATUAL: %.1f LUX | PWM: %s %%" % (float(target), float(lux), float(targetPwm)))
            #Se o PID já tiver sido configurado, e a lâmpada estava desligada, atualiza a Lâmpada
            if verify_pid_lamp==True and state_lamp=="Desligada":
                self.update_estado_iluminacao_on()
        else:
            print("SET: %.1f LUX | ATUAL: %.1f LUX | PWM: %s %%" % (float(target), float(temp), float(targetPwm)))

        # Desabilita configuração inicial
        verify_pid_lamp = True

    def verify_pid_lamp(self):
        global target_lamp
        global verify_pid_lamp
        global presenca

        if presenca==True:
            self.ui.txt_presenca.setText("Há alguém no cômodo!")
        else:
            self.ui.txt_presenca.setText("Não há presença no cômodo!")


        # Checa a presença ou não de presença
        self.check_pir1()
        self.check_pir2()
        # GET controle e economia
        controle = self.check_controle()
        # Se controle estiver habilitado
        if controle == True:
            # Se houver Presença, Box Economia estiver setado Executa a automação
            if presenca == True and verify_pid_lamp == True:
                self.auto_iluminacao()
            if presenca==False and verify_pid_lamp == True:
                #Esse IF garante que a lâmpada só vai executar o desligamento, se estiver ligada anteriormente
                if self.ui.txt_state_lamp.text()=="Ligada":
                    self.update_estado_iluminacao_off()

        # Configuração inicial
        if verify_pid_lamp == False and controle == True:
            self.configuracao_pid("Iluminação", target_lamp)

    #Threads
    def action_1_second(self):
        self.minha_data()


        clock_1_sec = threading.Timer(1, self.action_1_second)
        clock_1_sec.start()
    def action_5_seconds(self):
        self.apresenta_parametros()
        self.verify_pid_lamp()

        clock_5_sec = threading.Timer(5, self.action_5_seconds)
        clock_5_sec.start()
    def action_15_seconds(self):
        global auto_update_graph
        self.consumo_mensal()

        # Variavel para correção do BUG janela de data errada
        if auto_update_graph==False:
            selecao = self.ui.comboBox.currentText()
            if selecao == 'Diário':
                #Atualiza Gráficos a cada 15s
                self.update_graph()

        clock_15_sec = threading.Timer(15, self.action_15_seconds)
        clock_15_sec.start()
    def action_5_minutes(self):
        self.controle()
        clock_5_min = threading.Timer(300, self.action_5_minutes)
        clock_5_min.start()
    def action_15_minutes(self):
        self.agrupamento_medicoes()
        try:
            clock_15_min = threading.Timer(400, self.action_15_minutes)
            clock_15_min.start()
        except:
            clock_15_min = threading.Timer(400, self.action_15_minutes)
            clock_15_min.start()
    def action_1_hour(self):
        self.machine_learning()
        self.seta_data_grafico()

        # Recorrencia a cada 15min
        loop_mac = threading.Timer(3600, self.action_1_hour)
        loop_mac.start()
    def action_1_day(self):
        self.agrupamento_medicoes_diario()
        #self.backup()

        vv = threading.Timer(3600, self.action_1_day)
        vv.start()

    #Agentes
    def agente_recepcao(self, modo):
        if modo=="temp_amb":
            umidade,temperatura=self.temp_umid()
            return temperatura,umidade
        elif modo=="lux":
            lux=self.luximetro()
            return lux
        elif modo=="temp_agua":
            temp_agua=self.temp_agua()
            return temp_agua

    def agente_gerente(self):
        self.action_1_second()
        self.action_5_seconds()
        self.action_15_seconds()
        self.action_15_minutes()
        self.action_1_hour()
        self.action_5_minutes()
        self.action_1_day()

        #self.agrupamento_medicoes_mensal()

        #return
#####Backup está fazendo sempre que inicia o programa


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.setWindowTitle('AutoHome')
    myapp.show()

    qtRectangle = myapp.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    myapp.move(qtRectangle.topLeft())

    sys.exit(app.exec_())

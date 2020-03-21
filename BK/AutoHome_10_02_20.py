import threading
from idlelib import window
from info import Ui_InfoWindow
import numpy
import self as self
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QWidget, QPushButton, QMessageBox
from datetime import datetime, timedelta, date
import datetime as dt
import threading as th
import time
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

teste_conexao = 0
botao_info = False


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

        # Apresenta Grafico
        self.seta_data_grafico()
        self.update_graph()

        # Abre Janela de INFO
        self.ui.btn_info.clicked.connect(self.openWindow)

        # Funcoes das Select BOX
        self.ui.comboBox.currentIndexChanged.connect(self.update_graph)
        self.ui.comboBox_Dia.currentIndexChanged.connect(self.update_graph)
        self.ui.comboBox_Mes.currentIndexChanged.connect(self.update_graph)
        self.ui.comboBox_Ano.currentIndexChanged.connect(self.update_graph)

        # Funcoes de Botoes e Slider de Iluminacao e Temperatura//Aba QUARTO
        self.ui.horizontalSlider.valueChanged.connect(self.update_intensidade_iluminacao)
        self.ui.btn_on_ilum.clicked.connect(self.update_estado_iluminacao_on)
        self.ui.btn_off_ilum.clicked.connect(self.update_estado_iluminacao_off)
        self.set_configs_user()
        self.ui.btn_temp.clicked.connect(self.update_temp)
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

        # Chama Machine Learn
        self.machine_learn_acao()

    # FUNÇÕES DO SISTEMA
    def minha_data(self):

        data_atual = datetime.now()
        data_em_texto = data_atual.strftime('%d/%m/%Y')
        horas_em_texto = data_atual.strftime('%Hh:%Mmin:%Ss')
        saida = "Agora é " + horas_em_texto + " do dia: " + data_em_texto
        self.ui.data.setText(saida)
        t = threading.Timer(1, self.minha_data)
        t.start()

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
        return aba

    def teste_btn(self):
        self.ui.label_3.setText("Pressionado!")

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
                        eixo_y_hora[0][x] = potencia_dia[0][x]
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
                    for x in range(0, i - 1):
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
                    for x in range(0, i - 1):
                        if res[x][1] != res[x + 1][1]:
                            dias_do_mes[0][n + 1] = res[x + 1][1]
                            n = n + 1
                    n = 0

                    potencia_dia[0][0] = res[0][4]
                    # Atribui os valores das Potencias no Eixo Y
                    for x in range(0, i - 1):
                        if res[x][1] == res[x + 1][1]:
                            potencia_dia[0][n] = potencia_dia[0][n] + res[x + 1][4]

                        elif res[x][1] != res[x + 1][1]:
                            n = n + 1
                            potencia_dia[0][n] = res[x + 1][4]

                    # Correcao do BUG Mensal
                    if i != 0:
                        potencia_dia[0][n] = potencia_dia[0][n] + res[i][4]

                    for x in range(0, p):
                        eixo_y_dia[0][x] = potencia_dia[0][x]
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
                        eixo_y_mes[0][x] = potencia_mes[0][x]
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
                        self.ui2.txt_hora_12.setText(str(eixo_y_hora[0][x]))
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
                res = np.array([[0] * 5] * cursor.rowcount, dtype=np.int64)
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

                # Atualização dos Valores da Interface
                self.ui.consumo_instantaneo.setText(str(res[0][4]))
                self.ui.consumo_mensal.setText(str(consumo_total))
            else:
                print("Dados Insuficientes no Banco de Dados")
            # Finaliza a conexão
            conexao.close()
            teste_conexao = 0

            # Threading para Consultas do BD
            s = threading.Timer(15, self.consumo_mensal)
            s.start()

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

            s = threading.Timer(15, self.consumo_mensal)
            s.start()
        return

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

        return

    def update_graph(self):
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
                        for x in range(0, i - 1):
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
                        for x in range(0, i - 1):
                            if res[x][1] != res[x + 1][1]:
                                dias_do_mes[0][n + 1] = res[x + 1][1]
                                n = n + 1
                        n = 0
                        # Atribui os valores das Potencias no Eixo Y
                        potencia_dia[0][0] = res[0][4]
                        for x in range(0, i - 1):
                            if res[x][1] == res[x + 1][1]:
                                potencia_dia[0][n] = potencia_dia[0][n] + res[x + 1][4]
                            elif res[x][1] != res[x + 1][1]:
                                n = n + 1
                                potencia_dia[0][n] = res[x + 1][4]
                        # Correcao do BUG mensal
                        if i != 0:
                            potencia_dia[0][n] = potencia_dia[0][n] + res[i][4]

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
                        eixo_y[0][x] = potencia_dia[0][x]
                        eixo_x[0][x] = horas_do_dia[0][x]
                    u = threading.Timer(3600, self.update_graph)
                    u.start()
                # Atribui as variáveis nos eixos para Apresentar
                if selecao == 'Mensal':
                    for x in range(0, p):
                        eixo_y[0][x] = potencia_dia[0][x]
                        eixo_x[0][x] = dias_do_mes[0][x]
                # Atribui as variáveis nos eixos para Apresentar
                if selecao == 'Anual':
                    for x in range(0, p):
                        eixo_y[0][x] = potencia_mes[0][x]
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
                    self.ui.MplWidget.canvas.axes.annotate("%.2f" % p.get_height(),
                                                           (p.get_x() + p.get_width() / 2., p.get_height()),
                                                           ha='center', va='center', fontsize=11, color='gray',
                                                           xytext=(0, 20),
                                                           textcoords='offset points')
                # Seta os limites do Eixo Y para os valores nas barras nao Ultrapassar o Grafico
                self.ui.MplWidget.canvas.axes.set_ylim(0, max(eixo_y[0]) + 0.15 * max(eixo_y[0]))
                self.ui.MplWidget.canvas.axes.legend(['Consumo Diário'], loc='upper right')
                self.ui.MplWidget.canvas.axes.set_xticks(eixo_x[0])
                self.ui.MplWidget.canvas.axes.set_title('Gráficos do Consumo')
                self.ui.MplWidget.canvas.axes.set_ylabel('Potência [W]')
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

                return eixo_x, eixo_y, selecao
            # Apresenta as mensagens de erro caso as datas não forem encontradas
            else:

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

        # return

        # EXECUTA JANELA

    def backup(self):

        saida = backup()

        self.ui.textBrowser.append(saida)

        vv = threading.Timer(3600, self.backup)
        vv.start()

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

    def update_intensidade_iluminacao(self):
        valor = self.ui.horizontalSlider.value()
        self.ui.label_10.setText(str(valor))
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

    def update_estado_iluminacao_on(self):
        teste_conexao = 0

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
            conexao.close()

            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("INSERT INTO historico_acoes (acao,valor,horario) VALUES(%s,%s,%s)", (acao, valor, data_db))
            conexao.close()

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText(".::Dado Salvo com Sucesso::.")
            msg.setInformativeText("Sua Iluminação foi Ligada!")
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

    def update_estado_iluminacao_off(self):
        teste_conexao = 0

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

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText(".::Dado Salvo com Sucesso::.")
            msg.setInformativeText("Sua Iluminação foi Desligada!")
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

    def update_temp(self):
        valor = self.ui.txt_temp.toPlainText()
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

    def update_temp_banho(self):
        valor = self.ui.txt_temp_agua.toPlainText()
        teste_conexao = 0

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')

            # Cria um cursor:
            cursor = conexao.cursor()

            # Executa o comando:
            cursor.execute("UPDATE configuracao_user SET temp_banho=%s WHERE id=1", valor)
            conexao.close()

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText(".::Dado Salvo com Sucesso::.")
            msg.setInformativeText("Sua Temperatura do Banho foi Alterada!")
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

    def update_temp_ar_mais(self):

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
        else:

            valor = int(self.ui.text_temp_ar.text()) + 1
            self.ui.text_temp_ar.setText(str(valor))
            teste_conexao = 0

            data_atual = datetime.now()
            data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')
            # Ação e Valor que recebe
            acao = "Temperatura-Ar"

            try:
                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET temp_ar=%s WHERE id=1", valor)
                conexao.close()

                valor = True

                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
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
                    msg.setDetailedText(
                        "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.exec_()
                    teste_conexao = 1

    def update_temp_ar_menos(self):
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
        else:

            valor = int(self.ui.text_temp_ar.text()) - 1
            self.ui.text_temp_ar.setText(str(valor))
            teste_conexao = 0

            data_atual = datetime.now()
            data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')
            # Ação e Valor que recebe
            acao = "Temperatura-Ar"

            try:
                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET temp_ar=%s WHERE id=1", valor)
                conexao.close()

                valor = False

                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
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
                    msg.setDetailedText(
                        "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.exec_()
                    teste_conexao = 1

    def update_volume_mais(self):
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
        else:

            valor = int(self.ui.text_vol.text()) + 1
            self.ui.text_vol.setText(str(valor))
            teste_conexao = 0

            data_atual = datetime.now()
            data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')
            # Ação e Valor que recebe
            acao = "Volume-Tv"

            try:
                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET volume_tv=%s WHERE id=1", valor)
                conexao.close()

                valor = True

                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
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
                    msg.setDetailedText(
                        "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.exec_()
                    teste_conexao = 1

    def update_volume_menos(self):
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
        else:
            valor = int(self.ui.text_vol.text()) - 1
            self.ui.text_vol.setText(str(valor))
            teste_conexao = 0

            data_atual = datetime.now()
            data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')
            # Ação e Valor que recebe
            acao = "Volume-Tv"

            try:
                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET volume_tv=%s WHERE id=1", valor)
                conexao.close()

                valor = False

                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
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
                    msg.setDetailedText(
                        "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.exec_()
                    teste_conexao = 1

    def update_canal_mais(self):
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
        else:
            valor = int(self.ui.text_canal.text()) + 1
            self.ui.text_canal.setText(str(valor))
            teste_conexao = 0

            data_atual = datetime.now()
            data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')
            # Ação e Valor que recebe
            acao = "Canal-Tv"

            try:
                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET canais_tv=%s WHERE id=1", valor)
                conexao.close()

                valor = True

                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
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
                    msg.setDetailedText(
                        "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.exec_()
                    teste_conexao = 1

    def update_canal_menos(self):
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
        else:
            valor = int(self.ui.text_canal.text()) - 1
            self.ui.text_canal.setText(str(valor))
            teste_conexao = 0

            data_atual = datetime.now()
            data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')
            # Ação e Valor que recebe
            acao = "Canal-Tv"

            try:
                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET canais_tv=%s WHERE id=1", valor)
                conexao.close()

                valor = False

                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
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
                    msg.setDetailedText(
                        "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.exec_()
                    teste_conexao = 1

    def update_modo_ar(self):
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
        else:

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

            try:
                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
                # Executa o comando:
                cursor.execute("UPDATE configuracao_user SET modo_ar=%s WHERE id=1", valor)
                conexao.close()

                conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                # Cria um cursor:
                cursor = conexao.cursor()
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
                    msg.setDetailedText(
                        "Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    msg.exec_()
                    teste_conexao = 1

    def update_power_ar(self):
        valor = self.ui.btn_power_ar.text()
        data_atual = datetime.now()
        data_db = data_atual.strftime('%Y/%m/%d %H:%M:%S')

        acao = "Power-Ar"

        if valor == 'Ligar':
            valor = True
            self.ui.btn_power_ar.setText("Desligar")
        elif valor == 'Desligar':
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

            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
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
            conexao.close()

            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
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

    def update_Economia(self):
        valor = self.ui.check_Economia.checkState()

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

    def set_configs_user(self):
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute(
                "SELECT intensidade_iluminacao, temperatura, aprendizagem, economia, controle,ar_condicionado, televisao, temp_banho,temp_ar,modo_ar,volume_tv,canais_tv FROM configuracao_user  WHERE id=1")

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
                    valor_temp_banho = linha[7]
                    valor_temp_ar = linha[8]
                    valor_modo_ar = linha[9]
                    valor_volume_tv = linha[10]
                    valor_canais_tv = linha[11]

                self.ui.horizontalSlider.setValue(valor_ilum)
                self.ui.txt_temp.setText(str(valor_temp))
                self.ui.check_Aprendizagem.setCheckState(valor_aprendizagem)
                self.ui.check_Economia.setCheckState(valor_economia)
                self.ui.check_Controle.setCheckState(valor_controle)
                self.ui.txt_temp_agua.setText(str(valor_temp_banho))
                self.ui.text_temp_ar.setText(str(valor_temp_ar))
                self.ui.text_vol.setText(str(valor_volume_tv))
                self.ui.text_canal.setText(str(valor_canais_tv))

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

    def machine_learn_acao(self):
        #Variaveis de Configuração
        qq = 0
        iluminacao = 0
        n_iluminacao = 0
        power_tv = 0
        n_power_tv = 0
        power_ar = 0
        n_power_ar = 0
        canal_tv = 0
        n_canal_tv = 0
        volume_tv = 0
        n_volume_tv = 0
        modo_ar = 0
        n_modo_ar = 0
        temperatura_ar = 0
        n_temperatura_ar = 0
        quantidade_grupos_temperatura_ar = 0
        sair = 0
        taxa_tendencia=0.5

        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando:
            cursor.execute("SELECT acao,valor,horario FROM historico_acoes ORDER BY TIME(horario) ASC")

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                mac_acao = np.array([[0] * 3] * cursor.rowcount, dtype='<U19')
                for linha in resultado:
                    mac_acao[qq][0] = linha[0]
                    mac_acao[qq][1] = linha[1]
                    mac_acao[qq][2] = linha[2]
                    data_obj = datetime.strptime(mac_acao[qq][2],'%Y-%m-%d %H:%M:%S')  # Converte String para objeto Data.


                    if mac_acao[qq][0] == 'Iluminacao':
                        iluminacao = iluminacao + 1
                    elif mac_acao[qq][0] == 'Power-Tv':
                        power_tv = power_tv + 1
                    elif mac_acao[qq][0] == 'Power-Ar':
                        power_ar = power_ar + 1
                    elif mac_acao[qq][0] == 'Canal-Tv':
                        canal_tv = canal_tv + 1
                    elif mac_acao[qq][0] == 'Volume-Tv':
                        volume_tv = volume_tv + 1
                    elif mac_acao[qq][0] == 'Modo-Ar':
                        modo_ar = modo_ar + 1
                    elif mac_acao[qq][0] == 'Temperatura-Ar':
                        temperatura_ar = temperatura_ar + 1

                    qq = qq + 1
            mac_iluminacao = np.array([[0] * 3] * iluminacao, dtype='<U19')
            mac_power_tv = np.array([[0] * 3] * power_tv, dtype='<U19')
            mac_power_ar = np.array([[0] * 3] * power_ar, dtype='<U19')
            mac_canal_tv = np.array([[0] * 3] * canal_tv, dtype='<U19')
            mac_volume_tv = np.array([[0] * 3] * volume_tv, dtype='<U19')
            mac_modo_ar = np.array([[0] * 3] * modo_ar, dtype='<U19')
            mac_temperatura_ar = np.array([[0] * 3] * temperatura_ar, dtype='<U19')

            for x in range(0, cursor.rowcount):
                if mac_acao[x][0] == 'Iluminacao':
                    mac_iluminacao[n_iluminacao] = mac_acao[x]
                    n_iluminacao = n_iluminacao + 1
                elif mac_acao[x][0] == 'Power-Tv':
                    mac_power_tv[n_power_tv] = mac_acao[x]
                    n_power_tv = n_power_tv + 1
                elif mac_acao[x][0] == 'Power-Ar':
                    mac_power_ar[n_power_ar] = mac_acao[x]
                    n_power_ar = n_power_ar + 1
                elif mac_acao[x][0] == 'Canal-Tv':
                    mac_canal_tv[n_canal_tv] = mac_acao[x]
                    n_canal_tv = n_canal_tv + 1
                elif mac_acao[x][0] == 'Volume-Tv':
                    mac_volume_tv[n_volume_tv] = mac_acao[x]
                    n_volume_tv = n_volume_tv + 1
                elif mac_acao[x][0] == 'Modo-Ar':
                    mac_modo_ar[n_modo_ar] = mac_acao[x]
                    n_modo_ar = n_modo_ar + 1
                elif mac_acao[x][0] == 'Temperatura-Ar':
                    mac_temperatura_ar[n_temperatura_ar] = mac_acao[x]
                    n_temperatura_ar = n_temperatura_ar + 1

            ##ESTATISTICA TEMPERATURA AR

            # Criação dos Eixos
            eixo_x_temperatura_ar = np.zeros((1, 1), dtype='<U19')
            eixo_y_temperatura_ar = np.zeros((1, 1))

            # Criação da data inicial
            data_obj = datetime.strptime(mac_temperatura_ar[0][2], '%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
            horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
            data_horario_inicio = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO
            data_comparativa_1 = (data_horario_inicio + (timedelta(minutes=15)))  # Data inicial + 15min

            # Contador do Loop
            nn = 0
            # Seto o primeiro valor do Eixo X
            eixo_x_temperatura_ar[0][0] = data_comparativa_1
            # Loop Comparativo
            while sair == 0:
                # Se for a 1ª vez do loop, não incrementa os eixos
                if nn != 0:
                    # Incremento o vetor X com 1 posição a mais
                    eixo_x_temperatura_ar = np.resize(eixo_x_temperatura_ar, (1, len(eixo_x_temperatura_ar[0]) + 1))
                    # Atribuo o valor para a posição Criada
                    eixo_x_temperatura_ar[0][quantidade_grupos_temperatura_ar] = data_comparativa_1

                    # Crio o vetor auxiliar para Incrementar Eixo Y
                    eixo_y_aux_temperatura_ar = eixo_y_temperatura_ar[:]
                    # Incremento Eixo Y
                    eixo_y_temperatura_ar = np.zeros((1, len(eixo_y_temperatura_ar[0]) + 1))
                    # Loop para atribuir respectivos valores do Eixo Y
                    for jj in range(0, len(eixo_y_aux_temperatura_ar[0])):
                        eixo_y_temperatura_ar[0][jj] = eixo_y_aux_temperatura_ar[0][jj]

                # Loop Comparativo entre datas
                while data_horario_inicio <= data_comparativa_1 and nn < (n_temperatura_ar - 1):
                    # Se tiver dentro dos 15min, Incrementa o valor do eixo Y
                    eixo_y_temperatura_ar[0][quantidade_grupos_temperatura_ar] = eixo_y_temperatura_ar[0][quantidade_grupos_temperatura_ar] + 1
                    nn = nn + 1
                    # Capto a nova Data, e deixo pronto pra nova passagem do loop
                    data_obj = datetime.strptime(mac_temperatura_ar[nn][2],'%Y-%m-%d %H:%M:%S')  # Converto em Objeto Data
                    horario = (data_obj).strftime('%H:%M:%S')  # Faço o Somatorio de TIMES e converto para STRING
                    data_horario_inicio = datetime.strptime(horario, '%H:%M:%S')  # Converto novamente para OBJETO

                # Quando sai do Loop, um novo grupo de datas é formado.
                quantidade_grupos_temperatura_ar = quantidade_grupos_temperatura_ar + 1

                # Se a contagem não for a ultima, atribuo um novo valor pra ultima data
                if nn != n_temperatura_ar - 1:
                    data_comparativa_1 = (data_horario_inicio + timedelta(minutes=15))
                # Se a contagem for a ultima, ele atribui a saida do loop geral
                if (nn == (n_temperatura_ar - 1)):
                    sair = 1

            # Apos sair o loop, ele compara a ultima data (que não é comparada com o loop anterior
            if data_horario_inicio <= data_comparativa_1:
                # Se for o mesmo intervalo de 15min, atribui o valor para o Eixo Y
                eixo_y_temperatura_ar[0][quantidade_grupos_temperatura_ar - 1] = eixo_y_temperatura_ar[0][quantidade_grupos_temperatura_ar - 1] + 1
            else:
                # Senao, cria um novo grupo, um novo Eixo X
                quantidade_grupos_temperatura_ar = quantidade_grupos_temperatura_ar + 1
                eixo_x_temperatura_ar = np.resize(eixo_x_temperatura_ar, (1, len(eixo_x_temperatura_ar[0]) + 1))
                eixo_x_temperatura_ar[0][quantidade_grupos_temperatura_ar - 1] = data_comparativa_1

                # Cria um novo valor pro Eixo Y, e atribui os valores antigos pro novo Eixo Y
                eixo_y_aux_temperatura_ar = eixo_y_temperatura_ar[:]
                eixo_y_temperatura_ar = np.zeros((1, len(eixo_y_temperatura_ar[0]) + 1))
                for jj in range(0, len(eixo_y_aux_temperatura_ar[0])):
                    eixo_y_temperatura_ar[0][jj] = eixo_y_aux_temperatura_ar[0][jj]
                # Atribui novos valores pros eixos X e Y
                eixo_x_temperatura_ar[0][quantidade_grupos_temperatura_ar - 1] = data_horario_inicio
                eixo_y_temperatura_ar[0][quantidade_grupos_temperatura_ar - 1] = eixo_y_temperatura_ar[0][ quantidade_grupos_temperatura_ar - 1] + 1

            # Apresenta os Vetores
            print(eixo_x_temperatura_ar)
            print(eixo_y_temperatura_ar)

            #Parametros de Configuração para Estatísticas
            somatorio_temperatura_ar=0
            qtd_somatorio_temperatura_ar=0

            #Loop para saber qual o total dos valores da ação
            for n in range(0, len(eixo_x_temperatura_ar[0])):
                somatorio_temperatura_ar=somatorio_temperatura_ar+eixo_y_temperatura_ar[0][n]

            #Loop para saber quantos valores estão acima da Taxa de Tendencia
            for nn in range(0, len(eixo_y_temperatura_ar[0])):
                if (eixo_y_temperatura_ar[0][nn] / somatorio_temperatura_ar) >= taxa_tendencia:
                    qtd_somatorio_temperatura_ar=qtd_somatorio_temperatura_ar+1

            #Proteção para nao criar o vetor e nao tentar inserir no BD se nao existir Tendencias.
            if qtd_somatorio_temperatura_ar>0:
                k=0
                #Criaçcao do Vetor
                tendencia_temperatura_ar = np.zeros((qtd_somatorio_temperatura_ar, 3), dtype='<U19')
                #Loop para procurar novamente valores acima da Taxa de Tendencia
                for nn in range(0, len(eixo_y_temperatura_ar[0])):
                    #Condicação que compara cada valor com a Taxa de Tendencia
                    if (eixo_y_temperatura_ar[0][nn] / somatorio_temperatura_ar) >= taxa_tendencia:
                        #Atribuições do Vetor
                        tendencia_temperatura_ar[k][0]="Temperatura-Ar"
                        tendencia_temperatura_ar[k][1]=eixo_x_temperatura_ar[0][nn]
                        tendencia_temperatura_ar[k][2]=eixo_y_temperatura_ar[0][nn]
                        k=k+1
                #Inserção no BD
                try:
                    conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='1')
                    # Cria um cursor:
                    cursor = conexao.cursor()
                    #DELETA VALORES DO BD PREVIAMENTE CONFIGURADOS
                    cursor.execute("DELETE FROM tendencias")
                    #LOOP PARA INSERIR TODOS AS LINHAS DA MATRIZ
                    for nn in range(0, len(tendencia_temperatura_ar)):
                        # Executa o comando:
                        cursor.execute("INSERT INTO tendencias (acao,horario,valor) VALUES(%s,%s,%s)",(tendencia_temperatura_ar[nn][0], tendencia_temperatura_ar[nn][1], tendencia_temperatura_ar[nn][2]))
                    conexao.close()
                    print("Nova Tendência Registrada!")
                except pymysql.err.OperationalError as e:
                    print("Error while connecting to MySQL", e)
            #CASO NAO HAJA TENDENCIA
            else:
                print("Não há tendência")

        except pymysql.err.OperationalError as e:
            print("Error while connecting to MySQL", e)


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

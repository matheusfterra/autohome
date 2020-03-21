import threading
from idlelib import window
from info import Ui_InfoWindow
import numpy
import self as self
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QWidget, QPushButton, QMessageBox
from datetime import datetime
import datetime as dt
import threading as th
import time
from PyQt5.QtWidgets import *
from interface import *
import pymysql
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
import sys
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import random


teste_conexao=0

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        print(self.get_tab())
        self.minha_data()
        self.ui.btn_teste.clicked.connect(self.teste_btn)
        self.ui.btn_sair.clicked.connect(self.sair)
        self.ui.btn_sair2.clicked.connect(self.sair)
        self.consumo_mensal()
        self.seta_data_grafico()
        self.update_graph()

        self.ui.btn_info.clicked.connect(self.openWindow)

        self.ui.comboBox.currentIndexChanged.connect(self.update_graph)
        self.ui.comboBox_Dia.currentIndexChanged.connect(self.update_graph)
        self.ui.comboBox_Mes.currentIndexChanged.connect(self.update_graph)
        self.ui.comboBox_Ano.currentIndexChanged.connect(self.update_graph)



    # FUNÇÕES DO SISTEMA
    def minha_data(self):

        data_atual = datetime.now()
        data_em_texto = data_atual.strftime('%d/%m/%Y')
        horas_em_texto = data_atual.strftime('%Hh:%Mmin:%Ss')
        saida = "Agora é " + horas_em_texto + " do dia: " + data_em_texto
        self.ui.data.setText(saida)
        t = threading.Timer(1, self.minha_data)
        t.start()

    def get_tab(self):

        currentWidget = self.ui.tabWidget.currentIndex()
        if currentWidget == 0:
            aba = 'Consumo'
        elif currentWidget == 1:
            aba = 'Sala'
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
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='')

            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando de Acordo com o tipo da ComboBox:
            cursor.execute("SELECT * FROM medicao  WHERE DAY(horario) = %s AND MONTH(horario) = %s AND YEAR(horario) = %s ORDER BY horario DESC ",(selecao_dia, selecao_mes, selecao_ano))

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
                    for x in range(0, cursor.rowcount-1):
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
            #Executa o SELECT por Mes
            cursor.execute("SELECT * FROM medicao  WHERE MONTH(horario) = %s AND YEAR(horario) = %s ORDER BY horario DESC ",(selecao_mes, selecao_ano))

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                i=0
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
                    potencia_dia[0][n] = potencia_dia[0][n] + res[i][4]

                    for x in range(0, p):
                        eixo_y_dia[0][x] = potencia_dia[0][x]
                        eixo_x_dia[0][x] = dias_do_mes[0][x]
                    i = 1 + i
            #SELECT por ANO
            cursor.execute("SELECT * FROM medicao  WHERE YEAR(horario) = %s ORDER BY horario DESC ", selecao_ano)
            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                i=0
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
            conexao.close()

            #Conta a quantidade de valores do Vetor
            posicao1 = len(eixo_x_hora[0])
            posicao2 = len(eixo_x_dia[0])
            posicao3 = len(eixo_x_mes[0])
            #IFS para escrever os valores ABA DIARIA
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
            # IFS para escrever os valores ABA MENSAL
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
        btn_info=1
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
        if selecao =='Diário':
            aba=0
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
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='')

            # Cria um cursor:
            cursor = conexao.cursor()

            # Executa o comando:
            cursor.execute("SELECT * FROM medicao  WHERE MONTH(horario) = %s ORDER BY horario DESC ",mes)

            # Recupera o resultado:
            resultado = cursor.fetchall()
            if cursor.rowcount > 0:
                print("Numero de Registros: ", cursor.rowcount)
                res = np.array([[0] * 5] * cursor.rowcount, dtype=np.int64)
                #print(res, "\n")
                #print("\nDados:")
                for linha in resultado:
                    #print("Id = ", linha[0])
                    #print("Horário = ", linha[1])
                    #print("Corrente   = ", linha[2])
                    #print("Tensão  = ", linha[3])
                    #print("Potência  = ", linha[4], "\n")
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

        #Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            if teste_conexao==0:
                print("Error while connecting to MySQL",e)

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText(".::Erro de Conexão com o Banco de Dados::.")
                msg.setInformativeText("Falha na Comunicação com o Servidor!")
                msg.setWindowTitle("Erro na Inicialização")
                msg.setDetailedText("Confira sua conexão com a Internet!\nCaso seu Acesso esteja normalizado, Contacte o ADM do Servidor.")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                teste_conexao=1

            s = threading.Timer(15, self.consumo_mensal)
            s.start()
        return

    def seta_data_grafico(self):
        #Variáveis setadas como Globais para usar no decorrer da função
        global data_atual
        global dia
        global mes
        global ano
        #Identifica a data atual
        data_atual = datetime.now()
        dia = int(data_atual.strftime('%d'))
        mes = int(data_atual.strftime('%m'))
        ano = int(data_atual.strftime('%Y'))


        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='')

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

            #Recupera o resultado:
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
        #Escreve na ComboBox o Primeiro e Ultimo Ano
        for x in range(ultimo_ano,primeiro_ano-1,-1):
            self.ui.comboBox_Ano.addItem(str(x))

        #Escreve nas ComboBoxs as datas Atuais
        self.ui.comboBox_Mes.setCurrentText(str(mes))
        self.ui.comboBox_Dia.setCurrentText(str(dia))
        self.ui.comboBox_Ano.setCurrentText(str(ano))

        return

    def update_graph(self):
        #Variaveis Globais para a Função
        global potencia_dia
        global dias_do_mes
        potencia_dia=0
        #Captura os valores das ComboBoxs
        selecao= self.ui.comboBox.currentText()
        selecao_dia = self.ui.comboBox_Dia.currentText()
        selecao_mes = self.ui.comboBox_Mes.currentText()
        selecao_ano = self.ui.comboBox_Ano.currentText()

        i = 0
        # Abrimos uma conexão com o banco de dados:
        try:
            conexao = pymysql.connect(db='automacao_residencial', user='root', passwd='')

            # Cria um cursor:
            cursor = conexao.cursor()
            # Executa o comando de Acordo com o tipo da ComboBox:
            if selecao == 'Diário':
                cursor.execute("SELECT * FROM medicao  WHERE DAY(horario) = %s AND MONTH(horario) = %s AND YEAR(horario) = %s ORDER BY horario DESC ", (selecao_dia, selecao_mes, selecao_ano))
            elif selecao=='Mensal':
                cursor.execute("SELECT * FROM medicao  WHERE MONTH(horario) = %s AND YEAR(horario) = %s ORDER BY horario DESC ", (selecao_mes,selecao_ano))
            elif selecao=='Anual':
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
                    #Caso selecao em Diario
                    if selecao == 'Diário':
                        # Classifica o Eixo por Dia
                        data = linha[1].strftime('%H')
                        res[i][1] = data
                        # Identifica a quantidade de Dias Diferentes no Mês
                        p = 1
                        for x in range(0, cursor.rowcount-1):
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
                        potencia_dia[0][0] = res[0][4]
                        # Atribui os valores das Potencias no Eixo Y
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
                        #Identifica a quantidade de Dias Diferentes no Mês
                        p = 1
                        for x in range(0, i - 1):
                            if res[x][1] != res[x + 1][1]:
                                p = p + 1
                        #Cria Eixos do tamanho adequado
                        eixo_x = np.zeros((1, p))
                        eixo_y = np.zeros((1, p))

                        n = 0
                        dias_do_mes = np.zeros((1, p))
                        dias_do_mes[0][n] = res[0][1]

                        potencia_dia = np.zeros((1, p))
                        #Atribuiu os valores dos dias no Eixo X
                        for x in range(0, i - 1):
                            if res[x][1] != res[x + 1][1]:
                                dias_do_mes[0][n + 1] = res[x + 1][1]
                                n = n + 1
                        n = 0
                        potencia_dia[0][0] = res[0][4]
                        #Atribui os valores das Potencias no Eixo Y
                        for x in range(0, i - 1):
                            if res[x][1] == res[x + 1][1]:
                                potencia_dia[0][n] = potencia_dia[0][n] + res[x + 1][4]
                            elif res[x][1] != res[x + 1][1]:
                                n = n + 1
                                potencia_dia[0][n] = res[x + 1][4]
                        potencia_dia[0][n]=potencia_dia[0][n]+res[i][4]

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

                # Cria um Interrupt caso seja selecionado Diário, para recarregar a cada hora.
                if selecao == 'Diário':
                    for x in range(0,p):
                        eixo_y[0][x]=potencia_dia[0][x]
                        eixo_x[0][x]=horas_do_dia[0][x]
                    u = threading.Timer(3600, self.update_graph)
                    u.start()
                #Atribui as variáveis nos eixos para Apresentar
                if selecao == 'Mensal':
                    for x in range(0,p):
                        eixo_y[0][x]=potencia_dia[0][x]
                        eixo_x[0][x]=dias_do_mes[0][x]
                # Atribui as variáveis nos eixos para Apresentar
                if selecao == 'Anual':
                    for x in range(0, p):
                        eixo_y[0][x] = potencia_mes[0][x]
                        eixo_x[0][x] = mes_do_ano[0][x]


                #Cria os Graficos
                self.ui.MplWidget.canvas.axes.clear()
                #Bolas
                self.ui.MplWidget.canvas.axes.plot(eixo_x[0], eixo_y[0],'or',linewidth=8)
                #Linhas
                self.ui.MplWidget.canvas.axes.plot(eixo_x[0], eixo_y[0], 'r', linewidth=3)
                #Barras
                self.ui.MplWidget.canvas.axes.bar(eixo_x[0], eixo_y[0])
                #Apresenta os valores nos eixos
                for p in self.ui.MplWidget.canvas.axes.patches:
                    self.ui.MplWidget.canvas.axes.annotate("%.2f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=11, color='gray', xytext=(0, 20),
                                textcoords='offset points')
                #Seta os limites do Eixo Y para os valores nas barras nao Ultrapassar o Grafico
                self.ui.MplWidget.canvas.axes.set_ylim(0, max(eixo_y[0])+0.15*max(eixo_y[0]))
                self.ui.MplWidget.canvas.axes.legend(['Consumo Diário'], loc='upper right')
                self.ui.MplWidget.canvas.axes.set_xticks(eixo_x[0])
                self.ui.MplWidget.canvas.axes.set_title('Gráficos do Consumo')
                self.ui.MplWidget.canvas.axes.set_ylabel('Potência [W]')
                #Classifica as unidades dos eixos de acordo com as selecoes
                if selecao== 'Diário':
                    self.ui.MplWidget.canvas.axes.legend(['Consumo Diário'], loc='upper right')
                    self.ui.MplWidget.canvas.axes.set_xlabel('Tempo [Hora]')
                elif selecao== 'Mensal':
                    self.ui.MplWidget.canvas.axes.legend(['Consumo Mensal'], loc='upper right')
                    self.ui.MplWidget.canvas.axes.set_xlabel('Tempo [Dia]')
                elif selecao== 'Anual':
                    self.ui.MplWidget.canvas.axes.legend(['Consumo Anual'], loc='upper right')
                    self.ui.MplWidget.canvas.axes.set_xlabel('Tempo [Mês]')

                self.ui.MplWidget.canvas.axes.grid()
                self.ui.MplWidget.canvas.draw()
                return eixo_x, eixo_y, selecao
            #Apresenta as mensagens de erro caso as datas não forem encontradas
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

            # Finaliza a conexão
            conexao.close()


        # Caso a Conexão dê errado:
        except pymysql.err.OperationalError as e:
            print("Error while connecting to MySQL", e)

        #return


        # EXECUTA JANELA

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

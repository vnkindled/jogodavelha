from ast import arg
from http import client
import socket
import threading

class jogoDaVelha:

    def __init__(self):
        self.tabuleiro = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.turno = "X"
        self.jogadorUm = "X" #host
        self.jogadorDois = "O" #se conecta ao jogo
        self.vencedor = None
        self.gameOver = False

        self.contador = 0

    def host_jogo(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
        server.bind((host, port))
        server.listen(1) #1 conexão

        client, addr = server.accept()

        self.jogadorUm = "X"
        self.jogadorDois = "O"
        threading.Thread(target=self.handle_connection, args=(client,)).start()
        server.close()

    def conectar_jogo(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        self.jogadorUm = "O"
        self.jogadorDois = "X"
        threading.Thread(target=self.handle_connection, args=(client,)).start()

    def handle_connection(self,client):
        while not self.gameOver:
            if self.turno == self.jogadorUm:
                jogada = input("Sua vez, insira as coordenadas: ")
                if self.checarJogada(jogada.split(',')):
                    client.send(jogada.encode('utf-8'))
                    self.aplicarJogada(jogada.split(','), self.jogadorUm)
                    self.turno = self.jogadorDois
                    
                else:
                    print("Jogada Inválida!")
            
            else:
                dados = client.recv(1024)
                if not dados:
                   break
                else:
                    self.aplicarJogada(dados.decode('utf-8').split(','), self.jogadorDois)
                    self.turno = self.jogadorUm
        client.close()

    def aplicarJogada(self, jogada, player):
        if self.gameOver:
            return
        self.contador += 1
        self.tabuleiro[int(jogada[0])] [int(jogada[1])] = player
        self.printarTabuleiro()
        if self.checarVencedor():
            if self.vencedor == self.jogadorUm:
                print("Você venceu! :)")
                exit()
            elif self.vencedor == self.jogadorDois:
                print("Você perdeu! :(")
                exit()
        else:
            if self.contador == 9:
                print ("Empatou! :o")
                exit()

    def checarJogada(self, jogada):
        return self.tabuleiro[int(jogada[0])] [int(jogada[1])] == " "

    def checarVencedor(self):
        for row in range(3):
            if self.tabuleiro[row][0] == self.tabuleiro[row][1] == self.tabuleiro[row][2] != " ":
                self.vencedor = self.tabuleiro[row][0]
                self.gameOver = True
                return True
        for col in range(3):
            if self.tabuleiro[0][col] == self.tabuleiro[1][col] == self.tabuleiro[2][col] != " ":
                self.vencedor = self.tabuleiro[0][col]
                self.gameOver = True
                return True
        if self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] != " ":
            self.vencedor = self.tabuleiro[0][0]
            self.gameOver = True
            return True
        if self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] != " ":
            self.vencedor = self.tabuleiro [0][2]
            self.gameOver = True
            return True
        return False

    def printarTabuleiro(self):
        for row in range(3):
            print(" | ".join(self.tabuleiro[row]))
            if row != 2:
                print ("-----------")

game = jogoDaVelha()
game.conectar_jogo('localhost', 9999)
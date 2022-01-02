import pickle
import socket
from _thread import *

import pygame.mouse

from Game import game
from Game import daireEnemy
from Game import ucgenEnemy
from Game import kareEnemy
from Game import KareDefence
from Game import DaireDefence
from Game import UcgenDefence



server = "(your ip address here)"
port = 5555

sockett = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sockett.bind((server, port))
except socket.error as e:
    str(e)

sockett.listen()
print("Waiting For Connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(connection, player, gameId):
    global idCount
    connection.send(str.encode(str(player)))

    while True:
        try:
            data = connection.recv(4096).decode()
            try:
                dataList = data.split()
                data = dataList[0]
                pos = [dataList[1],dataList[2]]
            except:
                pass
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    if data == "Kare" and player == 0 and game.summonableEnemy():
                        Enemy = kareEnemy(20*50,"Kare",302,2,(255,255,255),25,25)
                        game.Enemies.append(Enemy)
                    elif data == "Ucgen" and player == 0 and game.summonableEnemy():
                        Enemy = ucgenEnemy(10*50,"Ucgen",300,15,(255,255,255))
                        game.Enemies.append(Enemy)
                    elif data == "Daire" and player == 0 and game.summonableEnemy():
                        Enemy = daireEnemy(15*50,"Daire",300,15,(255,255,255),12)
                        game.Enemies.append(Enemy)
                    elif data == "del":
                        game.Enemies.clear()
                        game.Defenders.clear()
                    if data == "KareT" or data == "DaireT" or data == "UcgenT":
                        game.selected = True
                    elif data == "KareD":
                        Defender = KareDefence(int(pos[0]),int(pos[1]))
                        game.Defenders.append(Defender)
                        game.selected = False
                    elif data == "DaireD":
                        Defender = DaireDefence(int(pos[0]),int(pos[1]))
                        game.Defenders.append(Defender)
                        game.selected = False
                    elif data == "UcgenD":
                        Defender = UcgenDefence(int(pos[0]),int(pos[1]))
                        game.Defenders.append(Defender)
                        game.selected = False
                    else:
                        for i in game.Enemies:
                            i.damage(game)
                            i.move(game)
                            i.die(game)
                        for i in game.Defenders:
                            i.chooseTarget(game)
                            i.d(game)

                    reply = game
                    connection.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost Connection")

    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    connection.close()


while True:
    connection, address = sockett.accept()
    print("Connected to : ", address)

    idCount += 1
    player = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = game(gameId)
        print("Creating a new Game ...")
    else:
        games[gameId].ready = True
        player = 1

    start_new_thread(threaded_client, (connection, player, gameId))

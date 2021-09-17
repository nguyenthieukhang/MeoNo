import socket

import constants
import network

HOST = '127.0.0.1'
PORT = 5573
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    SERVER.connect((HOST, PORT))
    print('Connected to server!')
except socket.error as e:
    print(str(e))

network = network.Network(SERVER)
hand = []

def show_cards():
    print('This is your hand')
    for card in hand:
        print(card, end=' ')
    print()

def main():
    while True:
        signal = network.receive()
        print(signal, 'received')
        if signal == constants.DEAL_CARDS:
            for i in range(constants.START_HAND):
                hand.append(network.receive())
                print('Take the card', hand[-1])
            show_cards()

        elif signal == constants.ASK_RESPONSE:
            if constants.CARD_NOPE not in hand:
                network.send(constants.NO_RESPONSE)
            else:
                ans = input('Do you want to respond with a Nope?, Enter Y/N?')
                if ans == 'Y':
                    network.send(constants.CARD_NOPE)
                else:
                    network.send(constants.NO_RESPONSE)
        elif signal == constants.SOMEONE_LOSES:
            continue
        elif signal == constants.DRAW_A_CARD:
            card = network.receive()
            hand.append(card)
        elif signal == constants.YOU_LOSE:
            print('You Lose!')
        else:
            print('Unrecognized command!')

main()








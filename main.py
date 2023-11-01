import socket
import sys
import threading
          
def main():
    name = "testredes"
    channel = "#python"
    server = "irc.freenode.net"
    port = 6667 
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((server, port))

    connection.send(bytes("NICK " + name + "\n ", "UTF-8"))
    connection.send(bytes("USER "+ name +" "+ name +" "+ name +" :This is a fun bot!\n", "UTF-8"))

    flag = False
    try: 
        while 1:    #puts it in a loop
            text=connection.recv(2040).decode("UTF-8")  #receive the text
            print(text)   #print text to console

            if(text.find('PING') != -1):                          #check if 'PING' is found
                connection.send(bytes('PONG ' + text.split() [1] + '\r\n', "UTF-8")) #returnes 'PONG' back to the server (prevents pinging out!)
            
            if '376' in text:
                connection.send(bytes("JOIN "+ channel +"\n", "UTF-8"))
                flag = True; 
            if 'som' in text and flag == True:
                connection.send(bytes(f"PRIVMSG {channel} :{'ovo'} \r\n", "UTF-8"))
    except KeyboardInterrupt:
        print('fechou')
        quit()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        quit()
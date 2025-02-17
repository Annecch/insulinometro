#Gruppo_H
import tkinter as tk
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import time
import asyncio
from bleak import BleakScanner
from bleak import BleakClient
import threading
import serial

finestra = Tk()
finestra.title("Gruppo H")
finestra.geometry("1760x900")
finestra.configure(bg='white')

#la finestra Ã¨ resizable
finestra.resizable(True,True) 

# Colori
cdt = "#500000"  # cdt = campi di testo
grafici = "#228B22"
labels = "yellow"
loadingbar = "Blue"
MenuATendina = "Pink"
Buttons = "Black"

# Variabili per gli input
ampiezza_str = tk.StringVar()
frequenza_str = tk.StringVar()
frequenza_iniziale_str = tk.StringVar()
frequenza_finale_str = tk.StringVar()
punti_str = tk.StringVar()
cicli_str = tk.StringVar()
resistenza_str = tk.StringVar()

resistance_values = []
x_values = []  
x_counter = 0  

temperature_data = []
time_data = []

# Configurazione della grid

finestra.grid_columnconfigure(0, weight=1)
finestra.grid_columnconfigure(1, weight=1)
finestra.grid_columnconfigure(2, weight=1)

finestra.grid_rowconfigure(0, weight=1)
finestra.grid_rowconfigure(1, weight=1)
finestra.grid_rowconfigure(2, weight=1)

# menubar (Salva, Bluetooth e File)
menubar = Menu(finestra)
finestra.config(menu=menubar)

# Creazione delle voci di menu separate
filemenu = Menu(menubar, tearoff=0)
bluetoothmenu = Menu(menubar, tearoff=0)
salvamenu = Menu(menubar, tearoff=0)

# Aggiunta delle voci nel menubar
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Bluetooth", menu=bluetoothmenu)
menubar.add_cascade(label="Salva", menu=salvamenu)

# Aggiunta di un comando esempio al menu File
filemenu.add_command(label='Prova')

# Frames
frameA = Frame(finestra, bg=cdt, width=360, height=300, highlightthickness=1)
frameB = Frame(finestra, bg=cdt, width=240, height=370, highlightthickness=1)
frameC = Frame(finestra, bg="darkorange", width=770, height=560, highlightthickness=1)
frameD = Frame(finestra, bg="darkorange", width=770, height=140, highlightthickness=1)
frameE = Frame(finestra, bg=grafici, width=270, height=300, highlightthickness=1)
frameF = Frame(finestra, bg=cdt, width=270, height=370, highlightthickness=1)
frameA.grid_propagate(False)
#frameF.grid_propagate(False)



# Posizionamento dei frames nella grid
frameA.grid(row=0, column=0,sticky=NSEW)
frameB.grid(row=1, column=0,rowspan=2,sticky=NSEW)
frameC.grid(row=0, column=1,rowspan=2,sticky=NSEW)
frameD.grid(row=2, column=1,sticky=NSEW)
frameE.grid(row=0, column=2,sticky=NSEW)
frameF.grid(row=1, column=2,rowspan=2,sticky=NSEW)

#posizionamento labels frameA
#frameA.grid_rowconfigure(0,weight=1)
#frameA.grid_rowconfigure(1,weight=1)
#frameA.grid_rowconfigure(2,weight=1)
#frameA.grid_columnconfigure(0,weight=1)

#sostituzione bottoni e lables
#labelA1= Frame(frameA,bg=MenuATendina,width=240,height=100,highlightthickness=1)
#labelA2= Frame(frameA,bg=cdt,width=240,height=100,highlightthickness=1)
#labelA3= Frame(frameA,bg=cdt,width=240,height=100,highlightthickness=1)


labelA1 = Button(frameA, text='FF/Sweep',font=('Avenir',30),bg=MenuATendina)

def LabelA23():
    labelA2 = Label(frameA, text='Frequenza',font=('Avenir',20), width=20,height=3)
    labelA3 = Label(frameA, text='Ampiezza',font=('Avenir',20),width=20,height=3)

def inviaA2():
    frase =labelA2.get()
    print(frase)

def inviaA3():
    frase =labelA3.get()
    print(frase)

freq_str = tk.StringVar()
amp_str = tk.StringVar()

labelA2 = tk.Entry(frameA, textvariable=freq_str,font=('Avenir',20))
labelA3 = tk.Entry(frameA, textvariable=amp_str,font=('Avenir',20))

bottoneA2 = Button(frameA, text="invia",font=('Avenir',15),command=inviaA2)
bottoneA3 = Button(frameA, text="invia",font=('Avenir',15),command=inviaA3)
#bottoneA = Button(frameA, text="invia",font=('Avenir',15))

labelA1.grid(row=0,column=0,sticky=NSEW,)
labelA2.grid(row=1,column=0,sticky=W)
labelA3.grid(row=2,column=0,sticky=W)

bottoneA2.grid(row=1,column=0,sticky=E)
bottoneA3.grid(row=2,column=0,sticky=E)

#posizionamento labels frameB
frameB.grid_rowconfigure(0,weight=0)
frameB.grid_rowconfigure(1,weight=2)
frameB.grid_columnconfigure(0,weight=1)
#labelB1= Frame(frameB,bg=labels,width=240,height=45,highlightthickness=1)
#sostituzione del frame con il label

labelB1 = Label(frameB,text='Log',font=('Avenir',30))
labelB1.grid(row=0,column=0,sticky=NSEW,pady=30, padx=20)

#log_str = tk.StringVar()
labelB2 = tk.Text(frameB,font=('Avenir',20),yscrollcommand=YES,background="white",cursor="target",width=5,height=5,state=DISABLED)
labelB2.grid(row=1,column=0,sticky=NSEW,pady=10, padx=20)
#,state=DISABLED

#posizionamento labels frameE
frameE.grid_rowconfigure(0,weight=0)
frameE.grid_rowconfigure(1,weight=2)
frameE.grid_columnconfigure(0,weight=1)

#labelE1= Frame(frameE,bg=labels,width=240,height=45,highlightthickness=1)
#sostituzione del frame con il label
labelE1= Label(frameE,text='Differenziale',font=('Avenir',30))
labelE1.grid(row=0,column=0,sticky=NSEW,pady=30, padx=20)

#posizionamento labels frameF
frameF.grid_rowconfigure(0,weight=0)
frameF.grid_rowconfigure(1,weight=2)
frameF.grid_columnconfigure(0,weight=1)

#labelF1= Frame(frameF,bg=labels,width=240,height=45,highlightthickness=1)
#sostituzione del frame con il label
labelF1 = Label(frameF,text='Data',font=('Avenir',30))
labelF1.grid(row=0,column=0,sticky=NSEW,pady=30, padx=20)

#tabella dati

data = ttk.Treeview(frameF, columns=("Tempo", "Temperatura"))
data.heading("#0", text="ID")
data.heading("Tempo", text="Tempo (s)")
data.heading("Temperatura", text="Temperatura (°C)")
data.column("#0", width=100, anchor="center")
data.column("Tempo", width=150, anchor="center")
data.column("Temperatura", width=150, anchor="center")


data.grid(row=1,column=0,sticky=NSEW,pady=10, padx=20)
#frameF.grid_propagate(False)
#labelF2 = tk.Text(frameF,font=('Avenir',20),yscrollcommand=YES,background="white",cursor="target",width=5,height=5,state=DISABLED)
#labelF2.grid(row=1,column=0,sticky=NSEW,pady=10, padx=20)
#,state=DISABLED


#posizionamento labels frameC
frameC.grid_rowconfigure(0,weight=1)
frameC.grid_rowconfigure(1,weight=1)
frameC.grid_columnconfigure(0,weight=1)
frameC.grid_columnconfigure(1,weight=1)

#labelC1= Frame(frameC,bg=grafici,width=260,height=100,highlightthickness=1)
labelC2= Frame(frameC,bg=grafici,width=260,height=100,highlightthickness=1)
labelC3= Frame(frameC,bg=grafici,width=180,height=180,highlightthickness=1)

#labelC1.grid(row=0,column=0,sticky=NSEW,padx=30,pady=30)
labelC2.grid(row=1,column=0,sticky=NSEW,padx=30,pady=30)
labelC3.grid(row=0,column=1,sticky=NSEW,rowspan=2,pady=160,padx=40)
"""
Questa funzione aggiorna un grafico della temperatura in base ai nuovi dati ricevuti. Ecco i passaggi principali:

Aggiornamento dei dati:

Aggiunge la temperatura ricevuta come parametro (temperatura) a una lista globale temperature_data.
Aggiunge un timestamp relativo (tempo trascorso dall'inizio) alla lista globale time_data.
Aggiornamento del grafico:
Cancella il contenuto precedente del grafico usando ax.clear().
Disegna una nuova linea con i dati aggiornati (time_data vs. temperature_data). Imposta titolo, etichette degli assi e una legenda.
Aggiorna il canvas per riflettere le modifiche.
Scopo: Tenere traccia della variazione della temperatura nel tempo in un grafico che si aggiorna dinamicamente.
"""

def aggiorna_grafico_temperatura(temperatura):
    global temperature_data, time_data

    # Aggiungi i dati attuali alla lista
    time_data.append(time.time() - start_time)  # Tempo relativo
    temperature_data.append(float(temperatura))

    # Aggiorna il grafico
    ax.clear()
    ax.plot(time_data, temperature_data, label="Temperatura")
    ax.set_title('Variazione della Temperatura nel Tempo')
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel('Temperatura (°C)')
    ax.legend()
    canvas.draw()
"""
Questa funzione inizializza il grafico della temperatura. I passaggi includono:

Creazione di una figura Matplotlib:

Inizializza una figura con dimensioni e risoluzione specificate.
Configura il grafico con titolo e etichette degli assi.
Integrazione con Tkinter:

Usa FigureCanvasTkAgg per incorporare il grafico in un widget Tkinter.
Posiziona il widget nel frame frameC.
Scopo: Creare un grafico vuoto per la temperatura, pronto per essere aggiornato dalla funzione aggiorna_grafico_temperatura.
"""
def crea_grafico_temperatura():
    global ax, canvas, start_time

    # Inizializza il tempo di partenza
    start_time = time.time()

    # Creiamo la figura
    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)

    # Titolo e asse
    ax.set_title('Variazione della Temperatura nel Tempo')
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel('Temperatura (°C)')

    # Incorporare la figura in un canvas Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frameC)  # `frameC` è il frame specifico dove vuoi posizionare il grafico
    canvas.draw()

    # Posizionare il canvas nel frame
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

"""
Questa funzione aggiorna i dati di resistenza in una tabella e genera un grafico dei valori raccolti. Ecco cosa fa:

Gestione input:

Legge un valore di resistenza dall'input (variabile resistenza_str).
Incrementa un contatore (x_counter) per tener traccia del tempo o del numero di letture.
Aggiornamento della tabella:

Inserisce il nuovo valore di resistenza nella tabella Treeview all'interno di frameF.
Aggiornamento del grafico:

Crea un grafico che mostra i valori di resistenza nel tempo usando x_values e resistance_values.
Scopo: Mostrare in tempo reale i dati di resistenza raccolti in una tabella e in un grafico.
"""
def aggiorna_graph_table():
    global x_counter
    try:
        new_resistance = float(resistenza_str.get())
        
        x_counter += 1
        x_values.append(x_counter)
        resistance_values.append(new_resistance)

        data.insert("", "end", text=f"{new_resistance} Ohm", values=(new_resistance,))
        
        crea_graficoBodeModulo()
        
        fig = Figure(figsize=(3, 2), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x_values, resistance_values, marker='o')
        ax.set_title('Bode Modulo')
        ax.set_xlabel('Tempo')
        ax.set_ylabel('Resistance (Ohm)')

        canvas = FigureCanvasTkAgg(fig, master=frameC)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=NSEW)

    except ValueError:
        print("Please enter a valid resistance value.")


"""Questa funzione crea un grafico per rappresentare il modulo di Bode. I passaggi principali:

Creazione del grafico:

Crea una nuova figura con dimensioni e risoluzione specifiche.
Configura il grafico con titolo e etichette degli assi.
Integrazione con Tkinter:

Integra il grafico come widget Tkinter usando FigureCanvasTkAgg.
Posiziona il grafico nel frame frameC.
"""

def crea_graficoBodeModulo():
    # Creiamo la figura
    fig = Figure(figsize=(3, 2), dpi=100)
    ax = fig.add_subplot(111)
    
   
    
    # Aggiungere titolo e asse
    ax.set_title('Bode Modulo')
    ax.set_xlabel('Resistenza')
    ax.set_ylabel('Y')
    
    # Incorporare la figura in un canvas Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frameC)
    canvas.draw()
    
    # Posizionare il canvas nel frame
    canvas.get_tk_widget().grid(row=0, column=0, sticky=NSEW)
"""
Scopo:
Questa funzione crea un grafico per rappresentare la fase di Bode.

Caratteristiche principali:
Creazione della figura:
Una figura Matplotlib di dimensioni 3x2 pollici e risoluzione di 100 dpi.
Aggiunge un sottografico (ax) alla figura.
Configurazione del grafico:
Imposta un titolo: "Bode Fase".
Etichetta gli assi (X e Y).
Integrazione con Tkinter:
Usa FigureCanvasTkAgg per incorporare la figura in un widget Tkinter.
Posiziona il canvas nel frame frameC alla posizione row=1, column=0.

"""
def crea_graficoBodeFase():
    # Creiamo la figura
    fig = Figure(figsize=(3, 2), dpi=100)
    ax = fig.add_subplot(111)
    
 
    # Aggiungere titolo e asse
    ax.set_title('Bode Fase')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    
    # Incorporare la figura in un canvas Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frameC)
    canvas.draw()
    
    # Posizionare il canvas nel frame
    canvas.get_tk_widget().grid(row=1, column=0, sticky=NSEW)    
"""
Questa funzione crea un grafico per rappresentare il diagramma di Nyquist, utilizzato per analisi di stabilità nei sistemi di controllo.

"""
def crea_graficoNyquist():
    # Creiamo la figura
    fig = Figure(figsize=(2, 2), dpi=100)
    ax = fig.add_subplot(111)
    
    
    
    # Aggiungere titolo e asse
    ax.set_title('Nyquist')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    
    # Incorporare la figura in un canvas Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frameC)
    canvas.draw()
    
    # Posizionare il canvas nel frame
    canvas.get_tk_widget().grid(row=0, column=1,rowspan=2,sticky=NSEW,pady=100)
"""
Questa funzione crea un grafico per rappresentare un'analisi differenziale.
"""
def crea_graficoDifferenziale():
    # Creiamo la figura
    fig = Figure(figsize=(3, 2), dpi=100)
    ax = fig.add_subplot(111)
    
   
    # Aggiungere titolo e asse
    ax.set_title('Differenziale')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    
    # Incorporare la figura in un canvas Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frameE)
    canvas.draw()
    
    # Posizionare il canvas nel frame
    canvas.get_tk_widget().grid(row=1, column=0, sticky=NSEW)    



#posizionamento labels labelsC
#labelC1.grid_rowconfigure(0,weight=1)
#labelC1.grid_rowconfigure(1,weight=1)
#labelC1.grid_columnconfigure(0,weight=1)

#titolo1= Frame(labelC1,bg=labels,width=350,height=40,highlightthickness=1)
#sostituzione del frame con il label
#titolo1 = Label(labelC1,text='Bode Modulo',font=('Avenir',30))
#titolo1.grid(row=0,column=0,sticky=N)

#labelC2.grid_rowconfigure(0,weight=1)
#labelC2.grid_rowconfigure(1,weight=1)
#labelC2.grid_columnconfigure(0,weight=1)

#titolo2= Frame(labelC2,bg=labels,width=350,height=40,highlightthickness=1)
#sostituzione del frame con il label
#titolo2 = Label(labelC2,text='Bode Fase',font=('Avenir',30))
#titolo2.grid(row=0,column=0,sticky=N)

#labelC3.grid_rowconfigure(0,weight=1)
#labelC3.grid_rowconfigure(1,weight=1)
#labelC3.grid_columnconfigure(0,weight=1)

#titolo3= Frame(labelC3,bg=labels,width=180,height=40,highlightthickness=1)
#sostituzione del frame con il label
#titolo3 = Label(labelC3,text='Nyquist',font=('Avenir',30))
#titolo3.grid(row=0,column=0,sticky=N)

#posizionamento labels frameD
frameD.grid_rowconfigure(0,weight=1)
frameD.grid_rowconfigure(1,weight=1)
frameD.grid_columnconfigure(0,weight=1)
frameD.grid_columnconfigure(1,weight=1)
frameD.grid_columnconfigure(2,weight=1)
frameD.grid_columnconfigure(3,weight=1)

#barra di caricamento
labelD1= Frame(frameD,bg=loadingbar,width=900,height=25,highlightthickness=1)

#bottoni
labelD2= Frame(frameD,bg=Buttons,width=130,height=30,highlightthickness=1)
labelD3= Frame(frameD,bg=Buttons,width=130,height=30,highlightthickness=1)
labelD4= Frame(frameD,bg=Buttons,width=130,height=30,highlightthickness=1)

contatore= 0
def StartStop():
    global contatore
    contatore+=1
    if contatore%2==0:
        print("Stop")
    else:
        print("Start")

def Mark():
    print("Mark")

def Reset():
    print("Reset")

#inizio bleak/BLE
import asyncio
import threading
import tkinter as tk
from bleak import BleakClient, BleakScanner

# UUID del servizio e della caratteristica
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"

# Funzione per scansionare i dispositivi BLE
async def scan_ble_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Dispositivo trovato: {device.name} ({device.address})")
        if device.name == "ESP32_BLE_Server_Gruppo_H":
            print(f"Connettendo al dispositivo {device.name}...")
            await connect_to_device(device)

# Funzione per connettersi al dispositivo ESP32
async def connect_to_device(device):
    global client
    client = BleakClient(device.address)
    await client.connect()
    print(f"Connesso a {device.name}")
    
    # Avvia la lettura continua dei dati della temperatura
    await read_temperature()

def aggiorna_tabella_temperatura(temperatura, tempo):
    """
    Aggiorna la tabella con una nuova riga di dati: temperatura e tempo.
    """
    try:
        # Inserisce una nuova riga nella tabella con tempo e temperatura
        data.insert("", "end", text=f"{tempo:.2f} s", values=(f"{temperatura} °C",))
    except Exception as e:
        print(f"Errore nell'aggiornamento della tabella: {e}")


# Funzione per leggere la temperatura dalla caratteristica
async def read_temperature():
    global time_data
    start_time = time.time()  # Registra il tempo iniziale
    while client.is_connected:
        try:
            value = await client.read_gatt_char(CHARACTERISTIC_UUID)
            temperatura = value.decode('utf-8')
            tempo_corrente = time.time() - start_time
            print(f"Dati letti: {temperatura}")
            update_ui(f"Temperatura attuale: {temperatura}")
            
            # Aggiorna il grafico con la nuova temperatura
            finestra.after(0, aggiorna_grafico_temperatura, temperatura)
            
            # Aggiorna la tabella con i dati della temperatura
            finestra.after(0, aggiorna_tabella_temperatura, temperatura, tempo_corrente)

            await asyncio.sleep(5)  # Attendi 5 secondi prima di leggere di nuovo
        except Exception as e:
            print(f"Errore nella lettura dei dati: {e}")
            update_ui("Errore nella lettura dei dati!")


# Funzione per inviare dati al dispositivo BLE tramite GATT
async def send_data_to_device(client, data):
    try:
        await client.write_gatt_char(CHARACTERISTIC_UUID, data.encode('utf-8'))
        print(f"Dati inviati: {data}")
        update_ui(f"Dati inviati: {data}")
    except Exception as e:
        print(f"Errore nell'invio dei dati: {e}")
        update_ui(f"Errore: {e}")

# Funzione per eseguire la scansione BLE in un thread separato
def start_scan_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(scan_ble_devices())

# Funzione per aggiornare l'interfaccia Tkinter (deve essere eseguita nel thread principale)
def update_ui(message):
    # Assicurati di aggiornare l'interfaccia nel thread principale
    data_label.config(text=f"Dati ricevuti: {message}")

# Funzione per inviare i dati nel thread
def send_message():
    message = message_entry.get()
    if message:
        print(f"Inviando messaggio: {message}")
        # Pass the message properly to the thread
        threading.Thread(target=send_message_thread, args=(message,)).start()

# Funzione che gestisce l'invio di messaggi nel thread
def send_message_thread(message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if client and client.is_connected:
        loop.run_until_complete(send_data_to_device(client, message))
    else:
        update_ui("Errore: Dispositivo non connesso!")


# Crea l'interfaccia Tkinter

# Etichetta per visualizzare i dati ricevuti
data_label = tk.Label(finestra, text="Dati ricevuti: ", font=("Arial", 14))

# Casella di testo per inserire il messaggio da inviare
message_entry = tk.Entry(frameB, font=('Avenir', 20), width=20)
message_entry.grid(row=2, column=0, sticky=NSEW, pady=10, padx=20)
send_button = tk.Button(frameB, text="Invia", command=send_message, font=('Avenir', 15))
send_button.grid(row=3, column=0, sticky=NSEW, pady=10, padx=20)

# Variabile globale per il client BLE
client = None


#fine bleak/BLE

labelD2 = Button(frameD,text='Start/Stop',font=('Avenir',30),command=StartStop,bg='gray')
labelD3 = Button(frameD,text='Mark',font=('Avenir',30),command=Mark,bg='gray')
labelD4 = Button(frameD,text='Reset',font=('Avenir',30),command=Reset,bg='gray')

#coso bluetooth
labelD5= Button(frameD,text='Cerca',command=lambda: threading.Thread(target=start_scan_thread).start(), font=('Avenir',30),bg='gray')

labelD1.grid(row=0,column=0,columnspan=3,pady=[70,0],padx=60)
labelD2.grid(row=1,column=0, padx=[10,0])
labelD3.grid(row=1,column=1, padx=[10,0])
labelD4.grid(row=1,column=2, padx=[10,0])
labelD5.grid(row=1,column=3, padx=[10,0])

# Inizializzazione modalità
modalita = "FF"  # Modalità iniziale

def invia_dati():
    if modalita == "FF":
        print(f"Modalità FF: Ampiezza: {ampiezza_str.get()}, Frequenza: {frequenza_str.get()}")
    else:
        print(f"Modalità Sweep: Ampiezza: {ampiezza_str.get()}, Frequenza Iniziale: {frequenza_iniziale_str.get()}, "
              f"Frequenza Finale: {frequenza_finale_str.get()}, Punti: {punti_str.get()}, Cicli: {cicli_str.get()}")

def aggiorna_modalita():
    global modalita
    if modalita == "FF":
        modalita = "Sweep"
        mostra_input_sweep()
    else:
        modalita = "FF"
        mostra_input_ff()

# Funzione per la modalità FF (singola frequenza)
def mostra_input_ff():
    # Pulizia del frame
    for widget in frameA.winfo_children():
        widget.destroy()
    
    # Bottoni e campi per FF
    #Button(frameA, text='FF/Sweep', font=('Avenir', 30), bg=MenuATendina, command=aggiorna_modalita).grid(row=0, column=0,columnspan=2, sticky=NSEW)
    Button(frameA, text='FF/Sweep', font=('Avenir', 20), bg=MenuATendina, command=aggiorna_modalita).grid(row=0, column=0, columnspan=2, sticky=NSEW)
    # Campi per FF
    Label(frameA, text='Frequenza(kHz)', font=('Avenir', 17)).grid(row=1, column=0, sticky=W)
    #message_entry = tk.Entry(frameA, font=('Avenir', 20), width=10)
    #message_entry.grid(row=1, column=1, sticky=E,padx=[10,0])

    Label(frameA, text='Ampiezza', font=('Avenir', 20)).grid(row=2, column=0, sticky=W)
    tk.Entry(frameA, textvariable=ampiezza_str, font=('Avenir', 20), width=10).grid(row=2, column=1, sticky=E,padx=[10,0])
    tk.Entry(frameA, textvariable=resistenza_str, font=('Avenir', 20), width=10).grid(row=3, column=0, sticky=W)
    Button(frameA, text='Invia(Dati BLE)', font=('Avenir', 15), command=send_message).grid(row=3, column=0, columnspan=2, pady=10)
    #bottone_resistenza = Button(frameA, text='Add Resistance', font=('Avenir', 15), command=aggiorna_graph_table)
    #bottone_resistenza.grid(row=4, column=0, columnspan=2, pady=10)




# Funzione per la modalità Sweep
def mostra_input_sweep():
    # Pulizia del frame
    for widget in frameA.winfo_children():
        widget.destroy()
    
    # Bottoni e campi per Sweep
    Button(frameA, text='FF/Sweep', font=('Avenir', 20), bg=MenuATendina, command=aggiorna_modalita).grid(row=0, column=0,columnspan=2, sticky=NSEW)
    
    Label(frameA, text='Ampiezza', font=('Avenir', 15)).grid(row=1, column=0, sticky=W)
    tk.Entry(frameA, textvariable=ampiezza_str, font=('Avenir', 20), width=10).grid(row=1, column=1, sticky=E)

    Label(frameA, text='Frequenza Iniziale', font=('Avenir', 15)).grid(row=2, column=0, sticky=W)
    tk.Entry(frameA, textvariable=frequenza_iniziale_str, font=('Avenir', 20), width=10).grid(row=2, column=1, sticky=E)

    Label(frameA, text='Frequenza Finale', font=('Avenir', 15)).grid(row=3, column=0, sticky=W)
    tk.Entry(frameA, textvariable=frequenza_finale_str, font=('Avenir', 20), width=10).grid(row=3, column=1, sticky=E)

    Label(frameA, text='Punti', font=('Avenir', 15)).grid(row=4, column=0, sticky=W)
    tk.Entry(frameA, textvariable=punti_str, font=('Avenir', 20), width=10).grid(row=4, column=1, sticky=E)

    Label(frameA, text='Cicli', font=('Avenir', 15)).grid(row=5, column=0, sticky=W)
    tk.Entry(frameA, textvariable=cicli_str, font=('Avenir', 20), width=10).grid(row=5, column=1, sticky=E)
    Button(frameA, text='Invia', font=('Avenir', 20), command=invia_dati).grid(row=6, column=0, columnspan=2, pady=10)






crea_graficoBodeFase()  
crea_graficoBodeModulo()
crea_graficoNyquist()  
crea_graficoDifferenziale()
mostra_input_ff()
crea_grafico_temperatura()

finestra.mainloop()
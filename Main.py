import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def calcola_indirizzi():
    try:
        # Recupera i valori dai campi
        addressSegments = []
        for i in range(4):
            val = int(ip_entries[i].get())
            if val < 0 or val > 255:
                raise ValueError(f"L'ottetto {i + 1} deve essere compreso tra 0 e 255")
            addressSegments.append(val)

        sm = int(subnet_entry.get())
        if sm < 0 or sm > 32:
            raise ValueError("La subnet mask deve essere compresa tra 0 e 32")

        # Creazione della subnet mask in formato binario
        smString = ""
        smSegments = []

        for i in range(0, 32):
            if i < sm:
                smString += "1"
            else:
                smString += "0"
            if i % 8 == 7 and i != 31:
                smString += "."

        # Conversione dei segmenti della subnet mask in decimale
        for i in range(0, 4):
            smSegments.append(int(smString.split(".")[i], 2))

        # Calcolo del Network ID
        netIdSegments = []
        for i in range(4):
            addressSegment = addressSegments[i]
            smSegment = smSegments[i]
            netIdSegment = addressSegment & smSegment
            netIdSegments.append(netIdSegment)

        netId = ".".join(str(seg) for seg in netIdSegments)

        # Primo host: network ID + 1 nell'ultimo ottetto
        firstHostSegments = netIdSegments.copy()
        firstHostSegments[3] += 1
        firstHost = ".".join(str(seg) for seg in firstHostSegments)

        # Calcolo della wildcard mask (inverso della subnet mask)
        wildcardMask = []
        for segment in smSegments:
            wildcardMask.append(255 - segment)

        # Calcolo dell'indirizzo broadcast
        broadcastSegments = []
        for i in range(4):
            broadcastSegments.append(netIdSegments[i] | wildcardMask[i])

        broadcast = ".".join(str(seg) for seg in broadcastSegments)

        # Calcolo dell'ultimo host
        lastHostSegments = broadcastSegments.copy()
        lastHostSegments[3] -= 1
        lastHost = ".".join(str(seg) for seg in lastHostSegments)

        # Calcolo del network ID successivo
        nextNetIdSegments = netIdSegments.copy()
        carry = 1

        # Aggiungi il valore della dimensione della sottorete all'ultimo ottetto
        # e gestisci il riporto se necessario
        for i in range(3, -1, -1):
            nextNetIdSegments[i] += wildcardMask[i] + carry
            carry = nextNetIdSegments[i] // 256
            nextNetIdSegments[i] %= 256

            if carry == 0:
                break

        nextNetId = ".".join(str(seg) for seg in nextNetIdSegments)

        # Aggiorna i risultati
        network_id_var.set(netId)
        first_host_var.set(firstHost)
        last_host_var.set(lastHost)
        broadcast_var.set(broadcast)
        next_network_var.set(nextNetId)

    except ValueError as e:
        messagebox.showerror("Errore", str(e))
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")


# Crea la finestra principale
root = tk.Tk()
root.title("Calcolatore di Indirizzi IP")
root.geometry("600x500")
root.resizable(False, False)

# Frame principale
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Stile
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))

# Frame per l'input dell'indirizzo IP
ip_frame = ttk.LabelFrame(main_frame, text="Indirizzo IP", padding="10")
ip_frame.pack(fill=tk.X, pady=10)

ip_entries = []
for i in range(4):
    ip_entry = ttk.Entry(ip_frame, width=5, justify="center")
    ip_entry.pack(side=tk.LEFT, padx=5)
    ip_entries.append(ip_entry)

    if i < 3:
        ttk.Label(ip_frame, text=".").pack(side=tk.LEFT)

# Frame per la subnet mask
subnet_frame = ttk.LabelFrame(main_frame, text="Subnet Mask (bit a 1)", padding="10")
subnet_frame.pack(fill=tk.X, pady=10)

subnet_entry = ttk.Entry(subnet_frame, width=5, justify="center")
subnet_entry.pack(padx=5)

# Pulsante di calcolo
calc_button = ttk.Button(main_frame, text="Calcola", command=calcola_indirizzi)
calc_button.pack(pady=10)

# Frame per i risultati
results_frame = ttk.LabelFrame(main_frame, text="Risultati", padding="10")
results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

# Variabili per i risultati
network_id_var = tk.StringVar()
first_host_var = tk.StringVar()
last_host_var = tk.StringVar()
broadcast_var = tk.StringVar()
next_network_var = tk.StringVar()

# Etichette per i risultati
ttk.Label(results_frame, text="Network ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
ttk.Label(results_frame, text="Primo Host:").grid(row=1, column=0, sticky=tk.W, pady=2)
ttk.Label(results_frame, text="Ultimo Host:").grid(row=2, column=0, sticky=tk.W, pady=2)
ttk.Label(results_frame, text="Broadcast:").grid(row=3, column=0, sticky=tk.W, pady=2)
ttk.Label(results_frame, text="Next Subnet ID:").grid(row=4, column=0, sticky=tk.W, pady=2)  # Modificato qui

# Campi per i risultati
ttk.Label(results_frame, textvariable=network_id_var).grid(row=0, column=1, sticky=tk.W, pady=2)
ttk.Label(results_frame, textvariable=first_host_var).grid(row=1, column=1, sticky=tk.W, pady=2)
ttk.Label(results_frame, textvariable=last_host_var).grid(row=2, column=1, sticky=tk.W, pady=2)
ttk.Label(results_frame, textvariable=broadcast_var).grid(row=3, column=1, sticky=tk.W, pady=2)
ttk.Label(results_frame, textvariable=next_network_var).grid(row=4, column=1, sticky=tk.W, pady=2)

# Configura il grid layout
results_frame.columnconfigure(1, weight=1)

# Avvia l'applicazione
root.mainloop()
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:36:21 2024

@author: juriv
"""

#imports
import pyaudio
import wave
import os
from scipy.io import wavfile
import audioop
from math import log10

#audio bestand specs
Chunk = 1024  # Grootte van elk stukje audio dat wordt opgenomen en verwerkt
Format = pyaudio.paInt16  # Audioformaat
Rate = 44100  # Samplefrequentie in Hz
seconds = 5  # Duur van de opname in seconden

#geeft aan via welke channel je opneemt zorg dat je weet welk getal de microfoon is
Channels = 1  # Aantal audio-kanalen (mono)

# Specificeer de doelmap, Pas dit pad aan naar je gewenste doelmap
locatie = r"C:/Users/juriv/OneDrive/Documents/Python Programmas/Wav Files"  # Pad naar de doelmap waar de opgenomen audiobestanden worden opgeslagen

# Controleer of de doelmap bestaat, zo niet, maak deze dan aan
if not os.path.exists(locatie):
    os.makedirs(locatie)

#start opnamen
p = pyaudio.PyAudio()
stream = p.open(format=Format,
                channels=Channels,
                rate=Rate,
                input=True,
                frames_per_buffer=Chunk)
print("start opnemen")
frames = [] # Lijst om de opgenomen audiogegevens in stukken op te slaan
for i in range(0, int(Rate/Chunk*seconds)):
    data = stream.read(Chunk)  # Lees een stukje audio van de microfoon
    frames.append(data)  # Voeg het gelezen stukje audio toe aan de lijst
print("opnemen gestopt")
stream.stop_stream()  # Stop de audio-opname
stream.close()  # Sluit de audiostream
p.terminate()  # Beëindig de PyAudio-sessie

# Loop om een unieke bestandsnaam te genereren
i = 1
while True:
    # Genereer de bestandsnaam
    filename = "opst2_test_{}.wav".format(i)
    
    # Maak het volledige pad naar het doelbestand
    target_file = os.path.join(locatie, filename)
    
    # Controleer of het bestand al bestaat
    if not os.path.exists(target_file):
        break
    
    i += 1

#zet opnamen om in wav file
wf = wave.open(target_file, 'wb')  # Open een WAV-bestand om de opgenomen audiogegevens op te slaan
wf.setnchannels(Channels)  # Stel het aantal kanalen in voor het WAV-bestand
wf.setsampwidth(p.get_sample_size(Format))  # Stel de samplebreedte in voor het WAV-bestand
wf.setframerate(Rate)  # Stel de samplefrequentie in voor het WAV-bestand
wf.writeframes(b''.join(frames))  # Schrijf de opgenomen audiogegevens naar het WAV-bestand
wf.close()  # Sluit het WAV-bestand
print("Bestand opgeslagen op:", target_file)  # Geef het pad naar het opgeslagen bestand weer


#Nu is de opname gedaan.

print(i)  # Geef het aantal opgenomen audiobestanden weer

# Functie om geluidsniveaus (dB) te berekenen
def calculate_dB(filename):
    sample_rate, data = wavfile.read(filename)  # Lees de audiogegevens van het opgegeven bestand
    rms_value = audioop.rms(data, 2)  # Bereken de root mean square (RMS) waarde van de audiogegevens
    db = abs(20 * log10(rms_value / (0.65)))  # Bereken het geluidsniveau in dB
    return db

# Specificeer de doelmap
target_directory = "C:/Users/juriv/OneDrive/Documents/Python Programmas/Wav Files"  # Vervang dit door het werkelijke pad naar het doelmap

# Bestandsnaam van het WAV-bestand om te lezen
filename = f"opst2_test_{i}.wav"  # Vervang dit door de werkelijke bestandsnaam

# Maak het volledige pad naar het WAV-bestand
filepath = os.path.join(target_directory, filename)
sample_rate, data = wavfile.read(rf'C:/Users/juriv/OneDrive/Documents/Python Programmas/Wav Files\opst2_test_{i}.wav')

# Bereken de dB-niveaus voor het opgegeven WAV-bestand

# Bereken het maximale geluidsniveau en druk het af
print(data.max())  # Print het maximale signaalniveau (I)

print(20 * log10(data.max() / (0.65)))  # Bereken en print het maximale geluidsniveau in dB

#plt.plot(time, data)  # Plot de audiogegevens tegen de tijd
db = calculate_dB(filepath)  # Bereken het geluidsniveau in dB
print(f"Gemeten dB voor {filename}: {db}")  # Geef het gemeten geluidsniveau weer





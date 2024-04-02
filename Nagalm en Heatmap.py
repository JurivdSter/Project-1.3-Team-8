# We beginnen met het importeren van de benodigde modules. Dit zijn stukjes code die andere mensen hebben geschreven en die we kunnen gebruiken om bepaalde taken uit te voeren.
# We gebruiken 'import' gevolgd door de naam van de module om deze in ons programma beschikbaar te maken.

import os  # Dit is een module waarmee we bestanden en mappen op ons besturingssysteem kunnen manipuleren.
import wave  # Deze module helpt ons bij het werken met WAV-audiobestanden.
import struct  # Met deze module kunnen we binaire gegevens (zoals geluidsgegevens) begrijpen en verwerken.
import numpy as np  # Dit is een module die ons geavanceerde wiskundige functies geeft, met name voor werken met arrays (soorten lijsten of matrices).
from scipy.io import wavfile  # Deze submodule van SciPy stelt ons in staat om WAV-bestanden te lezen.
from math import log10  # We importeren de logaritme-functie met grondtal 10 uit de wiskundige module.

gem_nagalmtijd = []  # Maak een lege lijst aan om de gemiddelde nagalmtijden per groep op te slaan. Dit is belangrijk voor later om de heatmap te plotten.

# Nu gaan we een functie definiëren. Een functie is een stukje code dat een specifieke taak uitvoert en dat we kunnen hergebruiken door er simpelweg naar te verwijzen met de functienaam.

def bereken_nagalmtijd(gemdata, sample_rate):
    """
    Deze functie berekent de nagalmtijd van een audiobestand.

    Parameters:
    - gemdata (list): Een lijst met gemiddelde geluidsintensiteiten per tijdstap.
    - sample_rate (int): De sample rate van het audiobestand (het aantal metingen per seconde).

    Returns:
    - float: De geschatte nagalmtijd in seconden.
    """

    # We definiëren variabelen om de start- en eindtijd van de nagalm te bepalen.
    # We beginnen met tstart (starttijd) en teind (eindtijd) beide op 0, wat betekent dat we nog geen start of einde hebben gevonden.

    tstart = 0
    teind = 0

    # Nu gaan we door alle gemiddelde gegevenspunten heen om te zoeken naar het begin en einde van de nagalm.
# Een lus wordt gebruikt om elk gegevenspunt in de lijst gemdata te doorlopen.
    for i in range(len(gemdata)):
       # Eerst wordt gecontroleerd of het punt waar de intensiteit halveert na een kwart seconde bereikt is.
    # Dit wordt gedaan om ruis aan het begin van het audiobestand te vermijden.
        if i >= kwart_seconde_samples * 2 and tstart == 0:
          # Als aan deze voorwaarde is voldaan en het begin van de nagalm (tstart) nog niet is vastgelegd, wordt de intensiteit op het moment van halvering bepaald.
            dBstart = gemdata[kwart_seconde_samples * 2]
            # Als de intensiteit ongeveer 3 dB lager is dan het startpunt van de halvering, wordt dit beschouwd als het begin van de nagalm en wordt het tijdstip opgeslagen in tstart
            if gemdata[i] <= dBstart - 3 and gemdata[i] >= dBstart - 3.1:
                tstart = i

       # Daarna wordt gezocht naar het eerste punt waar de intensiteit met 10 dB is afgenomen om het einde van de nagalm te bepalen.
    # Dit gebeurt ook pas na een kwart seconde om ruis te vermijden.
        if i >= kwart_seconde_samples * 2 and teind == 0:
            # Als aan deze voorwaarde is voldaan en het einde van de nagalm (teind) nog niet is vastgelegd, wordt gecontroleerd of de intensiteit ongeveer 13 dB lager is dan het startpunt van de halvering.
            if gemdata[i] <= dBstart - 13 and gemdata[i] >= dBstart - 13.1:
                # Als dat het geval is, wordt dit beschouwd als het einde van de nagalm en wordt het tijdstip opgeslagen in teind.
           # Vervolgens wordt de lus gestopt met behulp van break, omdat het einde van de nagalm is gevonden en verdere iteratie niet nodig is.
                teind = i
                break

    # Nu kunnen we de tijd tussen het begin en einde van de nagalm berekenen.
    t = (teind - tstart) / sample_rate

    # We vermenigvuldigen de tijd met 6 omdat elke stap ongeveer overeenkomt met 10 dB.
    return 6 * t

# Nu gaan we de map met audiobestanden specificeren. Deze map is dus voor iedereen anders.
audio_map = "C:/Users/juriv/OneDrive/Documents/Python Programmas/Wav Files/Opstelling 2/"

# We lezen de namen van de audiobestanden in de map en slaan ze op in een lijst.
audio_bestanden = os.listdir(audio_map)

# We maken een lege lijst aan om de gemiddelde nagalmtijden per groep van 5 audiobestanden op te slaan.
gemiddelde_nagalmtijden = []

# We gaan door elk audiobestand in de lijst met audiobestanden.
for audio_bestand in audio_bestanden:
    # We controleren eerst of het bestand een WAV-bestand is.
    if audio_bestand.endswith(".wav"):
        # We openen het WAV-bestand.
        wavefile = wave.open(os.path.join(audio_map, audio_bestand), 'rb')

                # We halen de sample rate (het aantal metingen per seconde) van het audiobestand op.
        sample_rate = wavefile.getframerate()
        # sample_rate geeft aan hoeveel metingen (samples) er per seconde zijn gedaan tijdens de opname van het audiobestand.
        # Dit wordt gemeten in Hertz (Hz). Een hogere sample rate betekent een hogere resolutie van het audiobestand,
        # wat resulteert in een nauwkeuriger weergave van het geluid, maar ook een groter bestandsgrootte.
        
        # We halen de lengte van het audiobestand op, wat het aantal frames in het audiobestand is.
        length = wavefile.getnframes()
        # length is het totale aantal frames in het audiobestand. Elk frame bevat een meting van het geluid op een specifiek moment in de tijd.
        # De lengte van het audiobestand wordt vaak gemeten in aantal frames.
        # Deze informatie is nuttig om te weten hoe lang het audiobestand is en hoeveel metingen er moeten worden verwerkt bij het analyseren ervan.


        # We maken lege lijsten aan om de audiogegevens op te slaan en het gemiddelde te berekenen.
        ydata = []
        gemdata = []

        # We berekenen het aantal samples in een kwart seconde.
        kwart_seconde_samples = int(sample_rate / 4)

        # We gaan door elk frame (meting) in het audiobestand.
        for i in range(0, length):
            # We lezen één frame (meting) van het audiobestand.
            wavedata = wavefile.readframes(1)
            # We pakken de binaire gegevens uit en converteren ze naar een decimaal getal.
            data = struct.unpack("<h", wavedata)
            y = data[0]

            # Als de waarde van het frame 0 is, voegen we een waarde van -60 dB toe om het einde van het signaal aan te geven.
            if y == 0:
                ydata.append(-60)
                continue

            # We converteren de waarde naar decibel (dB).
            y = 20 * log10(abs(y) / 2**15)
            ydata.append(y)

            # Als we genoeg meetpunten hebben om een kwart seconde te vullen, berekenen we het gemiddelde van die kwart seconde.
            if i >= kwart_seconde_samples:
                ydata.pop(0)
            gemdata.append(sum(ydata) / len(ydata))

        # We berekenen de nagalmtijd voor dit audiobestand en voegen deze toe aan de lijst van gemiddelde nagalmtijden.
        nagalmtijd = bereken_nagalmtijd(gemdata, sample_rate)
        gemiddelde_nagalmtijden.append(nagalmtijd)

        # We sluiten het audiobestand.
        wavefile.close()

       # Als we 5 audiobestanden hebben verwerkt, berekenen we het gemiddelde van de nagalmtijden van die groep.
        if len(gemiddelde_nagalmtijden) % 5 == 0:
            gemiddelde = sum(gemiddelde_nagalmtijden[-5:]) / 5
            print(f"Gemiddelde nagalmtijd van groep {len(gemiddelde_nagalmtijden)//5}: {gemiddelde}")
            
            gem_nagalmtijd.append(gemiddelde)  # Voeg het gemiddelde toe aan de lijst  
            
# Eerst zetten we de lijst van gemiddelde nagalmtijden om naar een NumPy-array, omdat dat handiger is voor bewerkingen.      
gemiddelde_nagalm = np.array(gem_nagalmtijd)
print(gemiddelde_nagalm)
    
# We importeren de nodige modules om grafieken te maken en op te maken.
import matplotlib.pyplot as plt  # Dit is een module om grafieken te maken en weer te geven.
import seaborn as sns  # Seaborn is een bibliotheek voor gegevensvisualisatie gebaseerd op Matplotlib.

# We nemen aan dat de gemiddelde nagalmtijden zijn opgeslagen in de lijst gemiddelde_nagalmtijden.

# Vervolgens veranderen we de vorm van de array naar een 4x4 matrix, omdat we 16 gemiddelden hebben (groepen van 5).
gemiddelde_nagalm_tijd_reshape = gemiddelde_nagalm.reshape(4, 4)

# Nu gaan we de heatmap maken met de gemiddelde nagalmtijden.

# We maken eerst een nieuw figuur van een bepaalde grootte.
plt.figure(figsize=(10, 8))

# We creëren de heatmap met seaborn.
ax = sns.heatmap(gemiddelde_nagalm_tijd_reshape, cmap='viridis', annot=True, fmt=".4f", cbar=True, cbar_kws={'label': 'Gemiddelde Nagalm Tijd'})

# We passen de labels van de x-as en y-as aan.
ax.set_xticklabels(range(1, 5))  # Labels voor de kolommen
ax.set_yticklabels(range(4, 0, -1))  # Labels voor de rijen, in omgekeerde volgorde

# We voegen een titel toe aan de grafiek.
plt.title('Gemiddelde Nagalm Tijd Heatmap')

# We geven de x-as en y-as labels.
plt.xlabel('Kolom')
plt.ylabel('Rij')

# We tonen de grafiek.
plt.show()
 

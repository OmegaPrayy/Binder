# Binder
Binder for the programing dacks.

Jak działą:
Po odpaleniu popatrz w konsole jak ci wypisuje twój kirofon i kabel np.
Soundboard aktywny! Numpad 1–9 = dźwięki, Numpad 0 = zmień SET, ESC = wyjście.
   0 Mapowanie dźwięku Microsoft - Input, MME (2 in, 0 out)
>  1 Microphone (LCS_USB_Audio), MME (1 in, 0 out)
   2 CABLE Output (VB-Audio Virtual , MME (16 in, 0 out)
   3 Mikrofon (3 — Logitech G733 Gam, MME (1 in, 0 out)
   4 Mapowanie dźwięku Microsoft - Output, MME (0 in, 2 out)
<  5 Głośniki (3 — Logitech G733 Gam, MME (0 in, 8 out)

> szczałka wejśćiowa czyli twoje mikro
< szczałka wyjściowa twoje słuchawki
> 
CABLE Input (VB-Audio Virtual C, MME (0 in, 16 out) 
Tego szukasz żeby przekierować dzwięk na wirtualny kabel, Skąd to mieć? 
-> https://vb-audio.com/Cable/index.htm  <- Tutaj macie wirtalizację kabla

W edycji to nas interesuje 
# KONFIG
mic_device = 1  # <-- ID mikrofonu fizycznego
vcable_device = 7# <-- ID VB-CABLE Output

sound_sets = [
    ['set1/1.mp3', 'set1/2.wav', 'set1/3.wav', 'set1/4.wav', 'set1/5.wav', 'set1/6.wav', 'set1/7.wav', 'set1/8.wav', 'set1/9.wav'],
    ['set2/1.wav', 'set2/2.wav', 'set2/3.wav', 'set2/4.wav', 'set2/5.wav', 'set2/6.wav', 'set2/7.wav', 'set2/8.wav', 'set2/9.wav'],
    ['set3/1.wav', 'set3/2.wav', 'set3/3.wav', 'set3/4.wav', 'set3/5.wav', 'set3/6.wav', 'set3/7.wav', 'set3/8.wav', 'set3/9.wav'],
]

mic_device - twój kikrofon ( kto by się spodziewał po nazwie)
vcable_device - twój kabel wirtualny  ( patrz nawias wyrzej)

Adresy znajdziesz na liście po odpaleniu skryptu, popraw je na swoje i będzie grać.

Struktura folderów to:
Binder  |
        | - set1
        | - set2
        | - set3 
        | - setX   (możesz sobie dodać ile setów chcesz tylko wtedy w tablicy sound-sets dodajesz nowy [setX/1.mp3, ... , setX/9.mav] 
        

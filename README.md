# Binder
Binder for the programing dacks.

Jak działą:
Po odpaleniu popatrz w konsole jak ci wypisuje twój mikrofon i kabel np.
'
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
'
W edycji to nas interesuje 
# KONFIG
'
mic_device = 1  # <-- ID mikrofonu fizycznego
vcable_device = 7# <-- ID VB-CABLE Output
'
mic_device - twój mikrofon ( kto by się spodziewał po nazwie)
vcable_device - twój kabel wirtualny  ( patrz nawias wyrzej)

Adresy znajdziesz na liście po odpaleniu skryptu, popraw je na swoje i będzie grać.

na panelu graficznym masz wyświetlone pola od 1-9 to są reprezentacje klawiszy numerycznej klikając na nie (oznaczenie ikonkom foldera) i wybierasz dzwięki .mp3 
możesz tworzyć nowe SET'y czyli nowe klawiatury albo usówać (tak jest to w nieskonczoność możliwe ale podzielone na 9 klawiszy)
możesz sobie wybierać z listy który set żeby nie przeklikiwać po koleji wszystkich aby dojść do n-tego

A i na koniec potrzebny jest do dodania plik .json który przetrzymóje ścieżki do dzwięków, stwóż go pustego koło main.py i jest
Jego stróktóra 
{
   "sets":{
   }
}   


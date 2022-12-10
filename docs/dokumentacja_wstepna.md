# NLP - Projekt - Dokumentacja wstępna

Temat projektu:

**Wykrywanie wydźwięku (sentiment analysis) opinii o produktach**

Projekt polega na pobraniu opinii o produktach: proszki do prania kolorów, tabletki do zmywarki i kubki termiczne oraz 
zrealizowania modelu wykrywającego wydźwięk: pozytywny, neutralny, negatywny. 

## Założenia techniczne 

Cały projekt zostanie wykonany w języku Python, używając najnowszej wersji biblioteki PyTorch. Pozwoli to na naukę tego 
narzędzia, używając wszystkich najnowszych rozwiązań w nim dostępnych. 
Wszystkie skrypty pomocnicze (do webscrapingu, obrobienia danych) również zostaną wykonane w języku Python. 

## Dane do trenowania i testowania modelu 

Dane do trenowania i testowania pochodzić będą z portalu ceneo.pl. Portal ten został wybrany ze względu na największą ilość 
dostępnych recenzji o różnych wydźwiękach. 

## Sposób rozwiązania zadania

Pierwszym krokiem będzie pobranie danych. Pobranie danych zostanie wykonane za pomocą 
techniki webscrapingu. Zostanie przygotowany skrypt, który zczytuje z plików HTML strony internetowej opinie wraz z oceną. 
Tak przygotowane dane z HTML zostaną następnie przetworzone w skrypcie tak, aby ułatwić dalsze przetwarzanie w docelowym 
programie - zostaną skonwertowane do tablicy obiektów JSON, którą łatwo wczytać w docelowym programie. 
Taki obiekt JSON zawiera dwa pola: 
- text - wartością jest po prostu dana recenzja,
- score - wydźwięk recenzji, ocena recenzji; będą to jedynie: **pos**, **neg**, **neu**. 

Opinie z portalu są oceniane oryginalnie w skali 1-5 razem z połowami wartości np. 2.5/5. Skrypt przetwarzające dane z HTMLa do JSON mapuje oceny w 
następujący sposób:
- oceny 1-2: **neg** (negatywna)
- oceny 2.5-3.5: **neu** (neutralna)
- oceny 4-5: **pos** (pozytywna)

Gotowe datasety są następnie przetwarzane przez docelowy program, w celu trenowania i testowania modelu. 


## Przyjęty model


## Założenia


## Opis eksperymentów






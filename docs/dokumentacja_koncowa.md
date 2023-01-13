---
output:
  pdf_document: default
  html_document: default
---
# NLP - Projekt - Dokumentacja końcowa

Eryk Mroczko

Jakub Sobolewski

14.12.2022r. 

## Temat projektu:

**Wykrywanie wydźwięku (sentiment analysis) opinii o produktach**

Projekt polega na pobraniu opinii o produktach: proszki do prania kolorów, tabletki do zmywarki i kubki termiczne oraz 
zrealizowania modelu wykrywającego wydźwięk: pozytywny, neutralny, negatywny. 

## Cel projektu

Wykrywanie wydźwięku (ang. sentiment analysis) jest procesem polegającym na określaniu emocji i opinii wyrażonych w tekście. Ten proces jest szeroko stosowany w wielu dziedzinach. Przykładem takich dziedzin są np. marketing i reklama. Wykrywanie wydźwięku stosuje się tam po to aby pomóc firmom w zrozumieniu emocji i opinii wyrażanych przez ludzi na temat ich produktów lub usług, a także aby dowiedzieć się czy ludzie są zadowoleni z ich produktów oraz by zidentyfikować potencjalne problemy lub obszary do poprawy.


## Założenia techniczne 

Cały projekt zostanie wykonany w języku Python, używając najnowszej wersji biblioteki PyTorch. Pozwoli to na naukę tego 
narzędzia, używając wszystkich najnowszych rozwiązań w nim dostępnych. 
Wszystkie skrypty pomocnicze (do webscrapingu, obrobienia danych) również zostaną wykonane w języku Python. 

## Dane do trenowania i testowania modelu 

Dane do trenowania i testowania pochodzić będą z portalu ceneo.pl. Portal ten został wybrany ze względu na największą ilość 
dostępnych recenzji o różnych wydźwiękach. 

## Sposób rozwiązania zadania

### Pobranie danych i przygotowanie korpusu

Pierwszym krokiem będzie pobranie danych. Pobranie danych zostanie wykonane za pomocą 
techniki webscrapingu. Zostanie przygotowany skrypt, który zczytuje z plików HTML strony internetowej opinie wraz z oceną. 
Tak przygotowane dane z HTML zostaną następnie przetworzone w skrypcie tak, aby ułatwić dalsze przetwarzanie w docelowym 
programie - zostaną skonwertowane do tablicy obiektów JSON, którą łatwo wczytać w docelowym programie. 
Taki obiekt JSON zawiera dwa pola: 
- text - wartością jest po prostu dana recenzja,
- score - wydźwięk recenzji,  będą to jedynie: **-1**, **0**, **1** (negatywna, neutralna, pozytywna)

Opinie z portalu są oceniane oryginalnie w skali 1-5 razem z połowami wartości np. 2.5/5. Skrypt przetwarzające dane z HTMLa do JSON mapuje oceny w 
następujący sposób:

- oceny 1-2: **-1** (negatywna)

- oceny 2.5-3.5: **0** (neutralna)

- oceny 4-5: **1** (pozytywna)


Gotowe datasety (czyli korpus) są następnie przetwarzane przez docelowy program, w celu trenowania i testowania modelu. 

### Dalsze przetworzenie przygotowanego datasetu

Następnym krokiem będzie tokenizacja datasetu, czyli podział opinii na pojedyncze wyrazy. Do tokenizacji użyta zostanie biblioteka Spacy. W ramach dalszego przetwarzania mogą być również przeprowadzone np. usunięcie stopwords lub lematyzacja również zapewniona przez bibliotekę Spacy. W dalszym ciągu programu stworzony zostanie zbiór słownictwa (vocabulary) gotowy do użycia w modelu.

### Przyjęty model

Planujemy wykorzystać dwa modele. 

Pierwszy model to prosty model oparty na regresji liniowej. Będzie on złożony z dwóch warstw:

Warstwa Embedding jako EmbeddingBag z biblioteki PyTorch - dzięki skorzystaniu z technologii EmbeddingBag, wystarczy że składamy zdania w paczkę, zapisując tylko w którym miejscu dana sekwencja się zaczyna. Każde takie zdanie będzie reprezentowane przez wektor embedding, a nie pojedyncze słowa. 

Warstwa liniowa w celach klasyfikacji 



Drugim modelem będzie model będący dotrenowaniem przetrenowanego modelu BERT, który wykorzystuje bardziej zaawansowane mechanizmy takie jak enkodery i atencja.  BERT jest szczególnie skuteczny w zadaniach takich jak rozpoznawanie intencji i znaczenia tekstu, a także w zadaniach związanych z zrozumieniem języka naturalnego. Jest to jeden z najlepszych obecnie dostępnych modeli języka i ma szerokie zastosowanie w różnych dziedzinach, w tym w technologii, medycynie i marketingu.

## Założenia

Danymi treningowymi będą dane ściągnięte z Ceneo. 

Problem klasyfikacji semantycznej będzie rozwiązany dla języka polskiego.

## Opis eksperymentów

Eksperymenty:

- Sprawdzimy jak ilość danych treningowych wpływa na jakość modelu.

- Porównamy 2 zaproponowane modele pod względem potrzebnych zasobów treningowych oraz jakości predykcji.

# Wyniki

## Trudności i wyzwania

Testowanie berta i tuning hiperparametrów był trudny z powodu długiego czasu treningu modelu. Czasochłonne również było scrapowanie recenzji z internetu.

TODO:
trudny scraping, długo trenuje sie bert, czasochłonny scraping

## Scraping
TODO:
opisać jak działa, co próbowaliśmy zrobić jak powstał finalny dataset

Podczas poszukiwania sposobów scrapowania danych o recenzjach znaleźliśmy sposób jak pobrać dowolną ilość recenzji z danej kategorii z Ceneo. Należy wejść w oferty z danej kategorii np. Sprzęt RTV (https://www.ceneo.pl/Sprzet_RTV) a potem filtrować przedmioty po cenie (https://www.ceneo.pl/Sprzet_RTV;m1;n10.htm). Należy dobrać tak zakres cen aby było dostępnych tylko 50 stron przedmiotów. Następnie przechodząc po kolejnych stronach i ofertach można stosować algorytm scrapingu. Filtracja jest konieczna, ponieważ Ceneo dostarcza tylko 50 stron ofert na raz, nie można otworzyć kolejnych stron z produktami, mimo że widać że w danej kategorii znajduje się ich więcej.

## Eksperymenty
Podczas eksperymentów porównaliśmy działanie i wyniki modelu liniowego oraz berta. Wykorzystaliśmy zbiór danych z losowymi recenzjami o liczności około 3000 recenzji oraz zbiór danych recenzji proszków do prania, tabletek do zmywarki oraz kubków termicznych w liczności około 10000 recenzji.

Model liniowy osiąga accuracy na poziomie około 90%, co jest nieznacznie gorszym wynikiem niż Bert, który osiągnął 92%. Natomiast model liniowy trenuje się znacznie szybciej na karcie graficznej NVIDIA RTX 3060TI Bert trenuje się około 10 minut na epoke, a model liniowy 2 sekundy na epokę.

Próbowaliśmy również bilansować zbiór danych, zmieniać hiperparametry i pretraining, ale nie przyniosły te metody poprawy jakości modeli.

## Przykłady działania
Sprawdziliśmy działanie naszego modelu na opiniach napisanych przez nas oraz ze zbioru testowego. Wyniki prezentują się następująco:

Model Liniowy:

Prediction: Positive TXT: Super mega proszek, bardzo dobry

Prediction: Neutral TXT: Totalny badziew szkoda pieniędzy, beznadziejny, porażka.

Prediction: Neutral TXT: Nie domywa ale ładnie pachnie. Zostają smugi

Prediction: Positive TXT: Nie rozpuszczają się, dobrze domywają, ładnie pachną, ale bardzo drogie

Bert:

---- negative ----

TXT: Po wcierce piecze mnie skóra głowy, a później występuje łupież.

LABEL:neg

TXT: Skuszona ceną kupiłam! Dziwię się komentarzom które tutaj się znajdują że super rewelacyjny produkt? Najgorsze jest w tym wszystkim to, że tabletki a w zasadzie ich drobne elementy pozostają na naczyniachW efekcie końcowym niebieskie, zielone plamy na talerzach, które trzeba drugi raz myć. Szkoda pieniędzy. Próbowałam wrzucać po dwie tabletki problem jednak leży w tym że pozostają zielone pozostałości tabletek na naczyniach . Nie polecam

LABEL:neg

TXT: może i to coś pierze, ale zapach to tragedia. chemiczny, okropny, mocny, nie da rady się go pozbyć po kolejnym praniu i przy 10 płukaniach. nawet namaczanie nie pomogło. drażni nos, poza tym płyn miał nie zawierać alergenów a ten "zapach" to jest jeden wielki alergen. a na butelce napis o dodatkowych innych środkach mogących wywoływać alergie. nie polecam.

LABEL:neg

---- positive ----

TXT: Będę zadowolony !!!

LABEL:pos

TXT: Produkt bardzo dobry

LABEL:pos

TXT: Wysoka jakość wykonania

LABEL:pos


## Podsumowanie w skrócie
Udało się osiągnąć zamierzone efekty. Na stosunkowo małym zbiorze danych udało sie wytrenować dwa dobrze działające modele modele: model liniowy i bert.

Scraping okazał się problemem nie oczywistym, mimo tej trudności - wyscrapowaliśmy wszystkie opinie o kubkach termicznych, tabletkach do zmywarek i proszkach do prania z Allegro i Ceneo.

Klasyfikacja opinii neutralnych okazała się trudna, ponieważ opinie neutralne są rzadko wystawiane i zazwyczaj równie dobrze mogłyby być pozytywne lub negatywne. Można by powiedzieć, że ta klasa jest mocno zaszumiona. Ludzie raczej piszą opinie tylko gdy bardzo coś im się podoba lub gdy bardzo coś się nie podoba.

Pomimo licznych trudności udało nam się osiągnąć modele dające dobre wyniki.



| Model | Liniowy |  Bert | 
|---|---|---|
| accuracy  |  90% |  92% |

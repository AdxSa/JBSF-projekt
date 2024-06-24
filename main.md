@mainpage Strona główna

# Jeszcze Bardziej Super Farmer


## Spis treści

- [Wprowadzenie](#Wprowadzenie)
- [Zasady gry](#Zasady gry)
- [Co zrobić, żeby uruchomic projekt?](#Co zrobić, żeby uruchomic projekt?)
- [Skrócony opis GUI](#Skrócony opis GUI) 


## Wprowadzenie

**Jeszcze Bardziej Super Farmer** jest projektem zrealizowanym podczas pracowni komputerowej z Programowania 2 (Python) przez Adama Sambora i Jakuba Żuka. Projekt jest grą będącą przeniesieniem na ekrany komputerów elementów trzech kultowych gier planszowych: Super Farmera, Chińczyka i Szachów. Grę wykonano w pythonie 3.12 przy wykorzystaniu biblioteki graficznej Tkinter.

## Zasady gry

W Jeszcze Bardziej Super Farmerze podobnie jak w chińczyku chodzi o doprowadzenie każdego z czterech posiadanych pionków na startowe pozycje po wykonaniu pełnego okrążenia wokół planszy. Różnicą jednak jest sama plansza. Nie poruszamy się bowiem po klasycznej planszy od chińczyka  a po szachownicy. Każdy tor jest złożony z pól na szachownicy tak samo odległych od zewnętrznych krawędzi planszy. Pionki graczy zaczynają w kątach szachownicy i mają za zadanie pokonanie całego obwodu planszy, jednak jest sposób na skrócenie drogi i zwiększenie swoich szans na zwycięstwo.

Podobnie jak w "Hodowli zwierzątek" (oryginalna nazwa Super Farmera)  autorstwa profesora Borsuka gracze rzucają kostkami i zbierają zwierzątka w zależności od już aktualnie posiadanych. W odróżnieniu jednak od klasycznej wersji, ich cel jest zupełnie inny. Za zwierzęta (odpowiednio: owcę, świnkę i krówkę) gracze mogą przenieść swój pionek na tor dalszy od krawędzi planszy, efektywnie skracając dystans do pokonania przez pionka. Ponadto istotnym aspektem jest specjalna plansza ilustrująca pola, na których hoduje się zwierzęta, bowiem w tej wersji zwierzęta wymagają miejsca na wypas. Każde zwierzę (królik, owca, świnka, krówka, konik) zajmuje pewną ilość miejsc (odpowiednio: 1/6, 1, 1, 2, 2) na planszy, więc rozwój gospodarstwa wymaga dobrego planowania zajmowanych pól, które podzielone są na 4 rodzaje (od początku gry widoczne trzy) zależne od wartości pola i podatności na ataki drapieżników.

Po rzucie kostkami następuje ruch pionkami na planszy szachowej, rozmnażanie zwierzątek (jak w klasycznej wersji) i ewentualny napad drapieżników. Jak wiadomo pieski są kochane, ale granie na pieski w Farmera jest niehonorowe, więc żeby nikt nie musiał ryzykować utraty honoru nie zaimplementowaliśmy możliwości tak łatwej ochrony przed potężnym wilkiem. Gracze mogą jednak ulepszać zakupione wcześniej i  posiadane przez siebie pola za odpowiednią liczbe królików (zakup pola kosztuje tyle co jego wyświetlana wartość, ulepszanie kosztuje odpowiednio 4, 10 i 18 królików za ulepszenie na 2., 4. lub 5. poziom). Ulepszenie pola zmniejsza prawdopodobieństwo ataku drapieżnika, gdyż drapieżniki atakują pole wybrane w ich rzucie (50% na pole o wartości 1, 33,(3)% na pole o wartości 2 i 16,(6)% na pole o wartości 4, pola o wartości 5 są nietykalne).

Gra kończy się gdy któryś z graczy przejdzie ostatnim ze swoich pionków na ostatnie wolne miejsce na swojej przekątnej szachownicy.


## Co zrobić żeby uruchomić projekt?

Python 3.12 powinien wystarczyć do wszystkiego, gdyż Tkinter, random i collections są instalowane razem z pythonem. Nie testowaliśmy starszych wersji pythona, więc nie ręczymy że wszystko zadziała, ale to bardzo prawdopodobne.


## Skrócony opis GUI

Po uruchomieniu projektu wyświetli się interfejs graficzny. Poniżej znajduje się opis poszczególnych przycisków występujących w tym interfejsie.

Przycisk "Rzuć Kostką" znajduje się w prawym górnym rogu okienka z grą. Po kliknięciu pod przyciskiem wyświetla się wynik rzutu kostką do chińczyka (liczba od 1 do 4) oraz wynik rzutu kostką do super-farmera. Każdy gracz w swojej turze może efektywnie rzucić kostką tylko jeden raz. 

Przyciski pod planszą. Obie plansze składają się z 64 przycisków, każdy z przycisków służy do wybrania odpowiednio pionka znajdującego się na nim lub pola z planszy farmera.

Przycisk "Porusz się pionkiem" porusza się wybranym pionkiem o wartość rzutu kostką do chińczyka (wyświetloną pod przyciskiem "Rzuć kostką"

Przycisk "Stwórz pionek" tworzy nowy pionek w odpowiednim narożniku szachownicy (na polu startowym gracza). Stworzenie pierwszego pionka jest darmowe, natomiast stworzenie kolejnych pionków kosztuje gracza odpowiednio: owcę, świnkę, krówkę.

Przycisk "Wejdź poziom wyżej" przesówa wybrany pionek na wyższy tor (tzn. Bliższy środka szachownicy). Ulepszenie pionka kosztuje gracza kolejno owcę, świnkę, krówkę przy przejściu z poziomu 0 na 1 z 1 na 2 i z poziomu 2 na 3.

Przycisk "Zejdź poziom niżej" przesówa wybrany pionek na niższy tor, osłabienie pozycji pionka jest darmowe jednak możliwe tylko jeśli pionek zrobił już pełne okrążenie wokół planszy

Przyciski w Market_place:

8 przycisków (Ze strzałkami) odpowiadają za wymianę zwierząt ze schowka na inne w odpowiedniej proporcji.

Po naciśnięciu na przycisk "Kup pole" i następnie wybraniu odpowiedniego pola na planszy do farmera, jeżeli nas stać i jeżeli naciśnie te przez nas pole sasiaduje z jednym z naszych pól, następuje zakup wybranego pola

Po naciśnięciu na przycisk "Ulepsz pole" i następnie po wybraniu odpowiedniego pola gracza na planszy do farmera, jeżeli nas stać (koszt opisany w zasadach gry) wybrane pole zostaje ulepszone

Przyciski z prawej strony planszy do farmera (schowek) 

Znajduje się tam 5 przycisków wyświetlających wizerunki zwierząt i ilość zwierząt jakie posiadamy w schowku. Po naciśnięciu przycisku z wizerunkiem odpowiedniego zwierzęcia, możemy postawić zwierzę na polu wybierając je. 

6. przycisk w schowku po naciśnięciu zmienia kolor z czerwonego na zielony i zielonego na czerwony odpowiednio. Jeśli jest zielony to naciśniecie na zwierzę znajdujące się na polu gracza zwraca je z pola do schowka. 

Ostatni przycisk "Koniec tury" kończy turę aktualnego gracza usuwając przy tym wszystkie zwierzęta gracza znajdujące się w schowku! Następnie rozpoczyna turę następnego gracza. 
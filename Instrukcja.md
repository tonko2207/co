### **0. Co trzeba mieć na komputerze**



* Windows 10/11
* Python 3.x (np. 3.10, 3.11)



**sprawdzanie: w PowerShell:**



python --version





### **1. Instalacja Gita**



* Wejdź na: https://git-scm.com/download/win
* Pobierz instalator (zacznie się sam).
* Uruchom pobrany .exe.
* Klikaj Next, Next, Next – nic nie zmieniaj – aż do Finish.
* Otwórz Git Bash (np. wpisując w Start: Git Bash).



**Sprawdź, czy działa:**



git --version

*(Ma wypisać wersję Gita.)*





### **2. Jednorazowa konfiguracja Git (imię, e-mail)**



**W Git Bash:**



git config --global user.name "Twoje Imię i Nazwisko"

git config --global user.email "twoj.mail@domena.pl"





*To tylko podpis pod commitami, nie logowanie do serwera.*

*Jeśli na tym serwerze WAT czasem wyskakuje problem z certyfikatem SSL, można (tylko na uczelnianym projekcie) dodać:*

*git config --global http.sslVerify false*





### **3. POBRANIE PROJEKTU (pierwszy raz) na Git Bash**



#### 3.1. Wybierz folder na projekt



np:

cd "/c/Users/TWOJE\_USER/Documents/SEM 9"



#### 3.2. Sklonuj repozytorium z odpowiednim branchem



git clone -b Aplikacja https://git.ita.wat.edu.pl/halusik/halusik.git schronisko

cd schronisko





Po ls powinieneś zobaczyć m.in.:



animals/

schronisko/

media/

manage.py

db.sqlite3

.gitignore

requirements.txt 





### **4. Utworzenie i włączenie virtualenv (venv) (na zwykłym cmd nie tym od git)**



**W folderze schronisko:**



python -m venv venv

*(Powstanie folder venv/.)*



**Aktywacja (za każdym razem przed pracą):**



.\\venv\\Scripts\\activate

*((venv) C:\\fodey jakieś>)*

### 

### **5. Instalacja paczek Pythona**



**Wciąż w tym samym folderze z włączonym venv:**



pip install -r requirements.txt

### 

### **6. Uruchomienie aplikacji lokalnie**



**Migracje bazy (jednorazowo, albo gdy zmienią się modele):**



python manage.py migrate





**Start serwera:**



python manage.py runserver





**Wejdź w przeglądarce na:**



http://127.0.0.1:8000/animals/ – lista zwierząt



http://127.0.0.1:8000/admin/ – panel admina



**Serwer wyłączasz Ctrl + C w terminalu.**

### 

### **7. JAK PRACOWAĆ NAD ZADANIEM (codzienny workflow)**

#### 7.1. Zanim zaczniesz coś zmieniać



**Upewnij się, że jesteś na branchu Aplikacja:**



git branch

*(Gwiazdka \* musi stać przy Aplikacja.)*





**Jeśli nie:**



git switch Aplikacja   # albo git checkout Aplikacja





**Pobierz najnowsze zmiany z serwera:**



git pull





#### 7.2. Rób swoje zmiany



* Edytujesz pliki w animals/, schronisko/, szablony w animals/templates/animals/ itp.
* Możesz włączać serwer python manage.py runserver, sprawdzać czy działa, po pracy go wyłączyć (Ctrl + C).



#### 7.3. Sprawdź, co zmieniłeś



git status

*Zobaczysz pliki na czerwono (zmienione) / zielono (dodane już do commita).*



#### 7.4. Dodaj zmiany do commita



**Najprościej: wszystkie pliki naraz:**



git add .



*Dzięki .gitignore katalog venv/ jest ignorowany – nie wrzucisz go przypadkiem na repo.*





**Jeśli chcesz, możesz dodać pojedynczy plik:**



git add animals/views.py



#### 7.5. Zrób commit (z opisem co zrobiłeś)



git commit -m "Dodano filtr statusu na liście zwierząt"





**Jeśli wyskoczy edytor nano, zapisz i wyjdź:**



Ctrl + O → Enter



Ctrl + X



#### 7.6. Wyślij zmiany na serwer (push)



git push

*To wrzuci Twoje zmiany na GitLab, branch Aplikacja.*





### **8. Ultra-krótka ściąga dla zespołu**



Pierwsza instalacja:



\# raz

git clone -b Aplikacja https://git.ita.wat.edu.pl/halusik/halusik.git schronisko

cd schronisko

python -m venv venv

venv/Scripts/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver





Każde kolejne zadanie:



cd ścieżka/do/schronisko

venv/Scripts/activate

git switch Aplikacja

git pull

\# ... zmiany w kodzie ...

git add .

git commit -m "opis tego co zrobiłem"

git push


# Gebruikershandleiding TOMMY

## Introductie
TOMMY is een topic modelling applicatie die ontwikkeld is door studenten
van de Universiteit Utrecht in opdracht van EMMA. Voor het uitvoeren van
topic modelling wordt het achterliggende Latent Dirichlet Allocation (LDA)
algoritme uitgevoerd op de door de gebruiker aangeleverde bestanden. LDA
is een algoritme dat topics herkent in deze bestanden. Het aantal topics N
kan door de gebruiker gekozen worden. LDA zal dan N lijsten teruggeven met
woorden en bijbehorende gewichten, waarbij het gewicht een indicatie is voor
hoeveel een woord bij een topic past. Het algoritme gaat ervan uit dat elk
document elk topic bevat, ook al is het maar voor een heel klein deel. In deze
gebruikershandleiding staat beschreven hoe u TOMMY kunt gebruiken en hoe
deze ruwe data van het LDA-algoritme goed onderzocht kan worden.

## Installatie

De software kan op drie verschillende besturingssystemen geïnstalleerd worden:
macOS, Windows en Linux. In de Installatiehandleiding staat nader beschreven
hoe TOMMY voor elk besturingssysteem op de juiste manier geïnstalleerd kan
worden.

## Bestanden importeren

Het programma ondersteunt momenteel vier verschillende file formats: TXT-bestanden, 
PDF-bestanden, Docx bestanden (Word bestanden) en zogenaamde csv format bestanden.
Meer informatie over de csv format volgt onder het kopje ’csv format’.
Het is aan te raden een input folder aan te maken op de computer om hier
alle bestanden te verzamelen. Subfolders in de import folder worden niet 
ondersteund. Een input folder kan gekozen worden door onder het kopje bestanden
links bovenin het scherm te kiezen voor de optie Selecteer input folder.

Nadat de bestanden zijn geïmporteerd, zijn deze te vinden in de bestandsweergave
onder het kopje geïmporteerde bestanden. De bestanden worden 
aangeduid met een titel als deze is meegegeven en anders met de bestandslocatie. Er
wordt metadata over het bestand getoond als u op een bestand in geïmporteerde
bestanden klikt. Deze data bevindt zich onder bestandsinformatie en bevat 
onder andere het aantal woorden, bestandsformaat en de bestandsgrootte.

![](../_static/User-guide/input.png)
### CSV formaat

Om veel data in het programma te laden is er een format bedacht welke dit voor
de computer leesbaar maakt. Dit format bestaat uit een csv-bestand waarbij de
eerste regel een lijst aan headers is. Elke regel hierna beschrijft een document.
Om een csv-bestand te kunnen inlezen moet er moet er minimaal een header
genaamd ”body” aanwezig zijn. Dit geeft aan dat deze kolom de tekst bevat die 
geanalyseerd moet worden. Daarnaast worden er een aantal optionele headers
ondersteund.

1. title: Deze header geeft aan dat de desbetreffende kolom de titels van
de documenten bevat. Deze titels worden dan gebruikt onder het kopje
geïmporteerde bestanden zoals later beschreven wordt.
2. date: Deze header geeft aan dat deze kolom de publicatiedatums van de
documenten bevat. Dit wordt op dit moment nog niet gebruikt in het
programma.
3. author: Deze header geeft aan dat deze kolom de schrijvers van de 
documenten bevat. Dit wordt op dit moment nog niet gebruikt in het programma.
4. url: Deze header geeft aan dat de kolom de linkjes naar de bron van
het document bevat. Dit wordt op dit moment nog niet gebruikt in het
programma.

### PDF, TXT en Docx formaten

Plaats de bestanden in de een folder. De bestanden worden 
automatisch ingelezen als de folder geselecteerd voor de input.
De pdf, txt en docx formaten worden ingelezen door de tekst uit de bestanden te halen. 
Het is aan te raden om de bestanden zo schoon mogelijk te houden. 
Dit betekent dat de bestanden geen afbeeldingen of andere onnodige informatie bevatten. 
Het is ook aan te raden om de bestanden in een taal te hebben die door het
programma ondersteund wordt. Het programma ondersteunt momenteel de talen Nederlands en Engels.

## Topic modelling

### Welke algoritme kan TOMMY gebruiken?

#### LDA
Het algoritme dat gebruikt wordt voor topic modelling is Latent Dirichlet 
Allocation (LDA). LDA is een algoritme dat topics herkent in documenten. Het 
algoritme gaat ervan uit dat elk document elk topic bevat, ook al is dit maar voor 
een heel klein deel. De topics worden gedefinieerd door woorden met een
bijbehorend gewicht. Hoe hoger het gewicht, hoe meer een woord bij dat topic past.

#### NMF
Naast LDA is er ook een ander algoritme beschikbaar, namelijk Non-negative
Matrix Factorization (NMF). NMF is een algoritme dat een matrix opsplitst in
twee matrices. Deze twee matrices kunnen gezien worden als een document-topic
matrix en een topic-woord matrix. De document-topic matrix geeft aan
hoeveel elk document bij een topic past, en de topic-woord matrix geeft aan
hoeveel elk woord bij een topic past. Het algoritme gaat ervan uit dat elk 
document elk topic bevat, ook al is dit maar voor een heel klein deel. De topics 
worden gedefinieerd door woorden met een bijbehorend gewicht. Hoe hoger het
gewicht, hoe meer een woord bij dat topic past.

### Welk algoritme is beter?
Beide algoritmes hebben hun eigen voor- en nadelen. LDA is een algoritme
dat probabilistisch is, wat betekent dat het algoritme een kansverdeling zoekt
die de data het beste verklaart. NMF is een algoritme dat werkt met matrices,
waarbij de data wordt opgesplitst in twee matrices. LDA is vaak beter in het
vinden van abstracte topics, terwijl NMF vaak beter is in het vinden van meer
concrete topics. In de praktijk is het vaak handig om beide algoritmes uit te
proberen en te kijken welk algoritme de beste resultaten geeft.

## Topic modelling uitvoeren

Topic modelling wordt door de applicatie uitgevoerd op alle geïmporteerde 
bestanden. Hierbij worden door de gebruiker geselecteerde instellingen 
meegenomen. Hieronder staat beschreven hoe deze instellingen aangepast kunnen
worden.

### Visualisatie



#### # Topicwoorden
![](../_static/User-guide/Visualisatie.png)

De meest invloedrijke parameter op de uitkomst van het topic modelling algoritme
is de hoeveelheid topicwoorden. Dit getal is linksboven in de applicatie 
aanpasbaar door onder het kopje Visualisatie bij de instelling # Topicwoorden een geheel
getal in te voeren en vervolgens op enter te drukken. De hoeveelheid topicwoorden
heeft standaard de waarde 10. Het zal niet vaak nodig zijn om meer dan 20 
topicwoorden te gebruiken. In het algemeen geldt dat, hoe meer topicwoorden je kiest,
hoe langer het programma bezig zal zijn. Het is dan ook sterk af te raden om meer
dan 100 topicwoorden in te voeren. Bovendien zijn de resultaten beter te 
interpreteren met een lager aantal topicwoorden.

Het aantal topicwoorden kan je zien in de topics display. Dit is een lijst van
woorden die het beste bij een topic passen. De hoeveelheid woorden die je ziet,
is het aantal dat je hebt ingevoerd bij de instelling # Topicwoorden.



### Algemeen


#### Algortime
![](../_static/User-guide/algoritme.png)

Het algoritme dat gebruikt wordt voor topic modelling kan aangepast worden
onder het kopje Algemeen. Het algoritme kan worden aangepast in de 
dropdown menu onder de instelling Algoritme. Hier kan gekozen worden tussen
LDA en NMF. Standaard staat het algoritme op LDA.


#### # Topics
![](../_static/User-guide/topics.png)

Het aantal topics dat gezocht wordt in de documenten kan aangepast worden
onder het kopje Algemeen. Het aantal topics kan worden aangepast door een
geheel getal in te voeren bij de instelling # Topics en vervolgens op enter te
drukken. 

Hier is interactie voor nodig om te bepalen welk aantal topics
het beste is voor de gegeven data. In de K-plot kan je zien hoe de log-likelihood
verandert met het aantal topics. Hieruit kan je afleiden hoeveel topics je het
beste kan gebruiken. Hoe hoger de log-likelihood, hoe beter de topics passen bij
de data.


#### Taal Corpus
![](../_static/User-guide/taal.png)

De taal van de documenten kan aangepast worden onder het kopje Algemeen.
De taal kan worden aangepast door een taal te selecteren in de dropdown menu
onder de instelling Taal corpus. 
Tommy support op dit moment de talen Nederlands en Engels.


### LDA Hyperparameters
![](../_static/User-guide/hyperparamaters.png)

Naast de algemene instellingen, kunnen ook een aantal geavanceerde parameters
voor LDA worden aangepast onder het kopje Hyperparameters

De alpha parameter bepaalt hoe verspreid de distibutie voor topic per 
document is. Een hogere alpha waarde moedigt het programma aan om zo veel
mogelijk topics te zoeken in een document. Bij een lagere alpha waarde zal
het algoritme slechts een paar dominate topics zoeken voor ieder document.
De alpha waarde kan aangepast worden door de automatische instellingen uit
te vinken bij de instelling Automatisch (aanbevolen). Vervolgens kan een
getal tussen de 0 en 1 ingevoerd worden bij de instelling alpha

De beta parameter bepaalt hoe verspreid de distibutie voor topic per woord
is. Een hogere beta waarde moedigt het programma aan om zo veel mogelijk
woorden te zoeken bij elke topic. Bij een lagere beta waarde zal het algoritme
slechts een paar dominate woorden zoeken voor ieder topic. De beta waarde
kan aangepast worden door de automatische instellingen uit te vinken bij de
instelling Automatisch (aanbevolen). Vervolgens kan een getal tussen de 0
en 1 ingevoerd worden bij de instelling beta.

Als het vakje naast de optie Automatisch blauw is gekleurd, worden de
standaard parameters gebruikt. Voor de alpha instelling is dit 1.0, en voor de
beta instelling is dit 0.01.

### Woorden uitsluiten
<!---
TODO: Synoniemen etc is nog niet gemerged naar main.
--->
![](../_static/User-guide/blacklist.png)
Figuur 1: Het uitsluitveld met drie uitgesloten woorden.

Niet alle woorden uit de geïmporteerde bestanden worden gebruikt bij topic
modelling. Bepaalde stopwoorden zoals lidwoorden en andere veel voorkomende
woorden als te, door en is, worden standaard uit de bestanden gefilterd. Dit zorgt
ervoor dat enkel de belangrijke woorden overblijven, waardoor topics uit meer
betekenisvolle woorden zullen bestaan. Het kan echter nog steeds voorkomen dat
er woorden in de analyse opduiken die niet van toepassing zijn. In de praktijk
zal dit best vaak voorkomen, aangezien de standaardlijst van stopwoorden vrij
conservatief opgesteld is. Deze woorden kunnen uitgesloten worden door ze in
te voeren in het tekstinvoervak onder het tabblad Blacklist. Dit tekstveld is
aanpasbaar. Na elk woord kan op enter geklikt worden om naar een nieuwe
regel te springen om een nieuw woord in te vullen. Woorden kunnen ook vrij
verwijderd worden uit de lijst. Een voorbeeld van het uitsluiten van woorden is
zichtbaar in figuur 1. Tijdens het uitvoeren van LDA worden alle hoofdletters
omgezet naar kleine letters. Daarom is de blacklist niet case-sensitive, wat
betekent dat ”bodegraven“ en ”Bodegraven“ beiden hetzelfde woord uit zullen
sluiten.



### Synoniemen

![](../_static/User-guide/synoniemen.png)

Figuur 2: Het uitsluitveld met twee synoniemen.

Het is mogelijk om synoniemen toe te voegen aan de analyse. Dit kan door
synoniemen in te voeren in het tekstveld onder het tabblad Synoniemen. Dit
tekstveld is aanpasbaar. Een synoniem kan worden ingevoerd door het woord dat je wilt 
verwisselen met een ander achter te verdelen met een = teken. Na elk synoniem kan op enter geklikt worden om naar
een nieuwe regel te springen om een nieuw synoniem in te vullen. Synoniemen
kunnen ook vrij verwijderd worden uit de lijst. Een voorbeeld van het toevoegen
van synoniemen is zichtbaar in figuur 2. Tijdens het uitvoeren van LDA worden
alle woorden vervangen door hun synoniemen.



### Topic modelling toepassen

Nadat de instellingen zijn aangepast, kan het algoritme uitgevoerd worden. Dit
wordt gedaan door op de "Toepassen" knop te klikken. Door deze knop wordt
het achterliggende algoritme uitgevoerd en worden er resultaten gegenereerd.
Dit kan enige tijd duren, denk aan enkele minuten of minder. De tijd is sterk
afhankelijk van de grootte van de geïmporteerde bestanden. 

## Grafische resultaten

### Distributie aantal woorden per document

De ingevoerde documenten die geanalyseerd worden kunnen verschillende aantallen
woorden hebben. Het is nuttig om te weten hoe deze aantallen zijn verdeeld. Bijvoorbeeld,
als er uitschieters tussen zitten die invloed kunnen hebben op de uitkomst van
topic modelling, zal dit zichtbaar zijn in deze grafiek. Op de x-as staan het 
aantal woorden per document, en op de y-as het aantal documenten wat overeenkomt
met dat aantal woorden.

![](../_static/User-guide/distribution_word_count.png)

### K-waarde

Het is vaak lastig om de verschillende hoeveelheden topics te vergelijken om te
zien welk aantal het beste presteert. De k-waarde grafiek berekent een getal voor
elk aantal topics, zodat ze goed met elkaar vergeleken kunnen worden. Dit getal
wordt de U<sub>mass</sub> genoemd. Om deze U<sub>mass</sub> te berekenen, moet
het topic modelling algoritme worden uitgevoerd voor elk aantal topics op de 
x-as. Het genereren van deze plots kan daarom enige tijd duren. 

![](../_static/User-guide/k-value.png)

De U<sub>mass</sub> is een waarde die de samenhang van een set topics meet. In het
algemeen geldt; hoe dichter deze waarde bij nul ligt, hoe meer gescheiden de 
topics zijn. In deze grafiek zouden 4 of 7 topics goede hoeveelheden topics zijn
om mee te beginnen met onderzoeken. 

Het is wel belangrijk om te beseffen dat deze grafiek niet aangeeft hoe goed de
topics te interpreteren zijn. Topic modelling met veel gescheiden topics kan 
een U<sub>mass</sub> dicht bij de nul genereren, maar als deze "topics" niet 
goed te interpreteren zijn voor mensen, is het handig om een andere hoeveelheid
topics te kiezen. 


### Documenten over tijd

![](../_static/User-guide/documents_over_time.png)

![](../_static/User-guide/documents_over_time_topic_4.png)

### Verdeling topics over documenten

![](../_static/User-guide/distribution_topics_over_documents.png)

### Correlatiematrix topics

![](../_static/User-guide/correlation_matrix.png)

### Gewichten van woorden en woordenwolk

![](../_static/User-guide/probabilities_topic_4.png)

![](../_static/User-guide/word_cloud_topic_4.png)

### Netwerk met woorden en topics

![](../_static/User-guide/word_topic_network.png)

### Netwerk met documenten en topics

![](../_static/User-guide/document_topic_network.png)

## Exporteren

De grafieken en netwerken kunnen geëxporteerd worden. Dit is mogelijk door
onder het kopje Bestand links bovin het scherm op de gewenste exporteer knop
te klikken.

De grafieken en netwerken kunnen als afbeelding opgeslagen worden op de
computer door op de optie Exporteer grafieken (.png) te klikken. Bij het kiezen
van deze optie zullen alle grafieken en netwerken opgeslagen worden. Vervolgens
kan er een folder worden gekozen om de afbeeldingen in op te slaan.

De netwerken kunnen ook geëxporteerd worden naar de software Gephi, om
die hier nog verder te bewerken. Dit is mogelijk door op de knop Exporteer naar
Graph Exchange XML Format (.gexf ) te klikken. Vervolgens kan er een folder
worden gekozen om de bestanden in op te slaan. Deze kunnen dan geopend
worden in de software Gephi.

## Configs

## Opslaan en laden



### Bekende bugs

De software bevat momenteel nog een aantal bugs die in de toekomst verholpen
zullen worden:

- Als bij de hyperparameters een waarde ingevoerd wordt, kan het pro-
gramma terugspringen naar een waarde 1 voor zowel de alpha als beta instelling.
Deze kunnen dan niet aangepast worden.
- De synoniemen en n-grams zijn nog niet ondersteund in de software, maar
wel zichtbaar in de user interface.
- Als netwerken worden geëxporteert naar Gephi, worden de kleuren niet
overgenomen.
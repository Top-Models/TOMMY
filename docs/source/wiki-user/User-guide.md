# Gebruikershandleiding TOMMY

## Introductie
TOMMY is een topic modelling applicatie die ontwikkeld is door studenten van de Universiteit Utrecht in opdracht van EMMA. Voor het uitvoeren van topic modelling wordt het achterliggende Latent Dirichlet Allocation (LDA) algoritme uitgevoerd op de door de gebruiker aangeleverde bestanden. LDA is een algoritme dat topics herkent in deze bestanden. Het aantal topics N kan door de gebruiker gekozen worden. LDA zal dan N lijsten teruggeven met woorden en bijbehorende gewichten, waarbij een hoog gewicht een indicatie is voor hoeveel het woord bij dit topic past. Het algoritme gaat ervan uit dat elk document elk topic bevat, ook al is het maar voor een heel klein deel. In deze gebruikershandleiding staat beschreven hoe u TOMMY kunt gebruiken en hoe deze ruwe data van het LDA algoritme goed onderzocht kan worden. 

## Installatie

De software wordt geleverd als een zip-bestand waar de gehele applicatie in
zit. Deze kan uitgepakt worden op een plek naar keuze. Dit resulteert in een
uitvoerbaar bestand genaamd tommy.exe en een folder internal waar benodigde
informatie voor het programma in staat.
Het kan handig zijn om na het uitpakken een snelkoppeling naar tommy.exe
te maken en deze snelkoppeling bijvoorbeeld op het bureaublad neer te zetten.
De twee onderdelen (tommy.exe en internal ) moeten naast elkaar in dezelfde
folder zitten voor het programma om te werken. Als dit zo is kan het prorgamma
uitgevoerd worden door op tommy.exe of een snelkoppeling daar naartoe te
dubbelklikken.

## Bestanden importeren

Om data in het programma te laden is er een format bedacht welke dit voor de
computer leesbaar maakt. Dit format bestaat uit een csv bestand waarbij de
eerste regel een lijst aan headers is. Elke regel hierna beschrijft een document.
Om een csv bestand te kunnen inlezen moet er een header genaamd ”body”zijn.
Dit geeft aan dat deze kolom de tekst bevat die geanalyseerd moet worden.
Daarnaast worden er een aantal optionele headers ondersteund.

- title: Deze header geeft aan dat de desbetrevende kolom de titels van
de documenten bevat. Deze titels worden dan gebruikt onder het kopje
ge¨ımporteerde bestanden zoals later beschreven wordt.
- date: Deze header geeft aan dat deze kolom de publicatiedatums van de
documenten bevat. Dit wordt op dit moment nog niet gebruikt in het
programma.
- author : Deze header geeft aan dat deze kolom de schrijvers van de do-
cumenten bevat. Dit wordt op dit moment nog niet gebruikt in het pro-
gramma.
- url : Deze header geeft aan dat de kolom de linkjes naar de bron van
het document bevat. Dit wordt op dit moment nog niet gebruikt in het
programma.

Nadat de bestanden zijn ge¨ımporteerd, zijn deze te vinden in de bestands-
weergave onder het kopje ge¨ımporteerde bestanden. De bestanden worden aan-
geduid met een titel als deze is meegegeven en anders met de bestandslocatie. Er
wordt metadata over het bestand getoond als u op een bestand in ge¨ımporteerde
bestanden klikt. Deze data bevindt zich onder bestandsinformatie en bevat on-
der andere het aantal woorden, bestandsformat en de bestandsgrootte.

## Topic modelling uitvoeren

Topic modelling wordt door de applicatie uitgevoerd op alle ge¨ımporteerde be-
standen. Hierbij worden door de gebruiker geselecteerde instellingen meege-
nomen. Hieronder staat beschreven hoe deze instellingen aangepast kunnen
worden.

### Aantal topics

De meest invloedrijke parameter op de uitkomst van het topic modelling al-
goritme is de hoeveelheid topics. Dit getal is linksboven in de applicatie aan-
pasbaar door onder Aantal topics een geheel getal in te voeren en vervolgens
op enter te drukken. De hoeveelheid topics heeft standaard de waarde 3. Het
zal niet vaak nodig zijn om meer dan 20 topics te gebruiken. In het algemeen
geldt dat, hoe meer topics je kiest, hoe langer het programma bezig. Het is dan
ook sterk af te raden om meer dan 100 topics in te voeren. Bovendien zijn de
resultaten beter te interpreteren met een lager aantal topics.

### Woorden uitsluiten

Niet alle woorden uit de ge¨ımporteerde bestanden worden gebruikt bij topic
modelling. Bepaalde stopwoorden zoals lidwoorden en andere veel voorkomende
woorden als te, door en is worden standaard uit de bestanden gefilterd. Dit zorgt
ervoor dat enkel de belangrijke woorden overblijven, waardoor topics uit meer
betekenisvolle woorden zullen bestaan. Het kan echter nog steeds voorkomen dat
er woorden in de analyse opduiken die niet van toepassing zijn. In de praktijk
zal dit best vaak voorkomen, aangezien de standaardlijst van stopwoorden vrij
conservatief opgesteld is. Deze woorden kunnen uitgesloten worden door ze in
te voeren in het tekstinvoervak boven de knop Uitsluiten en vervolgens op de
knop te klikken of op enter te drukken. De uitgesloten woorden worden getoond
onder de Uitsluiten knop (zie ook Figuur 1). Door op een woord te klikken in de lijst onder Uitsluiten kan een eerder uitgesloten woord weer toegevoegd worden.
Hierdoor wordt het uitsluiten ongedaan gemaakt.

### Topic modelling toepassen

Nadat de instellingen zijn aangepast, kan het algoritme uitgevoerd worden. Dit
wordt gedaan door op de Toepassen knop te klikken. Door deze knop wordt
het achterliggende algoritme uitgevoerd en worden er resultaten gegenereerd.
Dit kan enige tijd duren, denk aan enkele minuten of minder. De tijd is sterk
afhankelijk van de grootte van de ge¨ımporteerde bestanden.

## Grafische resultaten

Na het klikken op Toepassen worden grafische resultaten gegenereerd die het on-
derzoeken naar de algoritmische uitkomst mogelijk maakt. De grafieken worden
hieronder toegelicht.

### Woorden per topic

Elk topic bestaat uit woorden met een bijbehorend gewicht. Hoe hoger het
gewicht, hoe meer een woord bij dat topic hoort. Deze woorden zijn op meerdere
plekken in de applicatie te bekijken.

#### Lijst aan topic woorden

De meest voorkomende woorden per topic worden rechtsboven in de applicatie
getoond. Veel woorden in deze lijst van topics overlappen echter met andere
topics. Om te zien of een woord in meerdere topics voorkomt, kan op een woord
in deze lijst geklikt worden. Dit woord wordt dan in elke topic waarin het
voorkomt gearceerd.

#### Grafieken topic woorden

Deze woorden met het hoogste gewicht worden tevens op twee verschillende ma-
nieren gevisualiseerd; in een woordenwolk en in een staafdiagram. De woorden-
wolk geeft aan welke woorden het meest passen bij een topic door deze woorden
groter te maken. Het staafdiagram geeft hetzelfde weer, maar dan worden de
gewichten en verhoudingen ook gevisualiseerd. Dit zorgt ervoor dat woorden
gemakkelijk met elkaar vergeleken kunnen worden. Deze grafieken zijn, net als
alle andere grafieken, te vinden in het midden van het scherm. De pijltjes onder
de grafieken staan het toe om door de grafieken heen te bladeren.

### Correlatiematrix

Een correlatiematrix geeft de mate van overeenkomst van verschillende topics
weer. Een donkerblauw vakje geeft aan dat de topics op de co¨ordinaten van dit
vakje volledig overeenkomen. Donkerrood geeft aan dat de topics vrijwel geen
overeenkomsten hebben.
Het is belangrijk om hierbij te beseffen dat de matrix symmetrisch is over de
nevendiagonaal, van linksonder naar rechtsboven. De correlatie tussen topic 1
en 4 is namelijk identiek aan de correlatie tussen topic 4 en 1. Ook valt op dat
de nevendiagonaal enkel bestaat uit donkerblauwe vakjes. Een topic verschilt
namelijk niet van zichzelf.

### Netwerken

Een essentieel onderdeel van de grafische resultaten zijn twee netwerken die
relaties tussen topics en woorden/documenten weergeven. Deze netwerken geven
gelijktijdig meerdere verschillende aspecten van topics weer en zijn daarom van
groot belang bij het identificeren en begrijpen van de topics.

#### Netwerk woorden en topics

Topics worden gedefinieerd door woorden met een bijbehorend gewicht. De
woorden met het hoogste gewicht zijn belangrijk voor een topic. Echter komen
veel woorden voor in meerdere topics. Deze woorden kunnen dan bijdragen aan
twee of zelfs meerdere topics. Indien een woord te veel bijdraagt aan alle topics
zou het kunnen dat dit woord niet veel toevoegt (en dus uitgesloten zou kunnen
worden). Om dit soort woorden op te sporen, is een netwerk een goed middel.
In het netwerk komen tevens ook woorden naar voren die maar aan ´e´en topic
gerelateerd zijn.

In Figuur 3 worden per topic de 15 belangrijkste woorden weergegeven. Als
een woord in meerdere topics voorkomt, zal dit naar voren komen door meerdere
lijnen vanuit dit woord. Tevens wordt het gewicht gevisualiseerd. Hoe belang-
rijker een woord is voor een topic, des te dikker is de lijn die dit topic met het
woord verbindt.

#### Netwerk documenten en topics

Volgens het LDA algoritme bevat elk document alle topics, ook al is dit vaak
maar voor een heel klein deel. Het is nuttig om te visualiseren hoe de documen-
ten zich verhouden tot de topics om te zien welke documente voor het grootste
deel uit ´e´en enkel topic bestaan.
In Figuur 4 staat een netwerk die de relaties tussen groepen documenten
(de zwarte stippen) en topics weergeeft. Elke zwarte stip stelt alle documenten
voor die gerelateerd zijn aan de aangrenzende topics. De dikte van de lijnen is
een maat die het aantal documenten weergeeft die verbonden zijn aan een topic.
Des te dikker de lijn, des te meer documenten aan het topic toebehoren. Uit dit
netwerk is goed op te maken of een topic veel losse documenten heeft of juist
veel voorkomt in documenten in combinatie met een ander topic.

### Bekende bugs

De software bevat momenteel nog een aantal bugs die in de toekomst verholpen
zullen worden:

- Soms worden er plots in een eigen venster geopend als er te snel op de
knopjes wordt gedrukt om door de grafieken te gaan. Dit komt echter niet vaak
voor en zorgt ook niet voor problemen tijdens het uitvoeren van het programma.
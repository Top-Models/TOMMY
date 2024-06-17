import os
import pytest
from datetime import datetime
from tommy.controller.file_import.csv_file_importer import CsvFileImporter

# Test data directory
TEST_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..',
                                             '..',
                                             '..',
                                             'test',
                                             'test_data',
                                             'test_csv_files'))


@pytest.fixture
def csv_file_importer():
    return CsvFileImporter()


def test_compatible_file(csv_file_importer):
    # Test compatible CSV file
    compatible_path = os.path.join(TEST_DATA_DIR, 'correct.csv')
    assert csv_file_importer.compatible_file(compatible_path) is True

    # Test incompatible CSV file
    incompatible_path = os.path.join(TEST_DATA_DIR, 'incorrect.csv')
    with pytest.raises(ValueError) as exception_info:
        csv_file_importer.compatible_file(incompatible_path)


def test_load_file(csv_file_importer):
    csv_path = os.path.join(TEST_DATA_DIR, 'correct.csv')
    files = list(csv_file_importer.load_file(csv_path))

    assert len(files) == 51
    assert files[0].metadata.title == "Bedreiging Complotdenker door Spanje uitgezet naar NL"
    assert files[1].metadata.title == "In de ban van het complot; Amateur-speurneuzen maken het leven van slachtoffers tot een hel"
    assert files[0].body.body == '''ABSTRACT Joost Knevel werd op verzoek van het Nederlandse OM in Spanje aangehouden. De complotdenker wordt onder meer verdacht van het bedreigen van RIVM-baas Jaap van Dissel en Mark Rutte. VOLLEDIGE TEKST: Complotdenker en een van de drie presentatoren van het zogeheten Red Pill Journal op sociale media, Joost Knevel, is maandag door Spanje overgeleverd aan Nederland. De man hield zich al maanden schuil in het oosten van Spanje en kon na een zoekactie begin deze maand worden opgepakt. De marechaussee heeft Knevel opgehaald. Hij moet in Den Haag terechtstaan en wordt donderdag voorgeleid aan de rechter-commissaris. Knevel wordt verdacht van meerdere strafbare feiten, waaronder bedreiging van en opruiing tot geweld tegen RIVM-baas Jaap van Dissel en Mark Rutte. Zo zei hij over Van Dissel: ,,Wie geeft hem zijn welverdiende nekschot, die is een held". Knevel plaatste volgens het Openbaar Ministerie in Den Haag ook een bewerkte video online waarin meerdere publieke figuren, onder wie bovengenoemden, met een strop om hun nek zogenaamd werden opgehangen. Knevel is de tweede man van het complotjournaal die nu vastzit. Eerder deze zomer werd Wouter Raatgever berecht en veroordeeld tot een celstraf van negen maanden waarvan drie voorwaardelijk, voor het verspreiden van opruiende en bedreigende filmpjes. Hij had eind mei in zijn journaal gezegd dat de advocaat van de gemeente Bodegraven weldra door een militair tribunaal ter dood zou worden veroordeeld. De derde presentator van het journaal voor complotdenkers, Micha Kat, vluchtte naar Noord-Ierland om zijn straf te ontlopen. Daar werd hij op 22 juli opgepakt op grond van een Europees aanhoudingsbevel en daarna onder voorwaarden weer vrijgelaten. Link naar PDF'''
    assert files[1].body.body == '''Amateur-speurneuzen maken het leven van slachtoffers tot een hel  Het is vaste prik bij mediagevoelige drama's: amateur-speurneuzen gaan zich ongevraagd met de zaak bemoeien. Ze zijn ervan overtuigd dat ze de ware toedracht weten, vaak op basis van complottheorieën en haaks op wat justitie vindt. Vooral zaken rond kinderen, vermissingen en misbruik werken als een magneet op zelfbenoemde detectives. Als aanklager, rechter en beul in één lopen ze de politie voor de voeten en kwetsen betrokkenen tot op het bot. Soms gaan ze heel ver. ,,Ik ben mijn kind verloren", zegt een moeder uit Weesp. ,,Niets kan Lisa terugbrengen. Het enige waar ik op kan hopen is dat ik steun en rust krijg om dit verlies te verwerken. Helaas heeft deze vrouw daar geen enkel begrip voor. Ze misbruikt het overlijden van Lisa om aandacht te krijgen en zelfs om geld in te zamelen." Lisa (14) beroofde zichzelf van het leven. Maar toen meldde zich 'die vrouw': de hoogblonde Agnes, slachtoffer van de toeslagenaffaire. Zij gelooft niet dat het suïcide was en begint online hardnekkig te verkondigen dat de Staat meer weet van Lisa's dood. Ze noemt het sterfgeval 'verdacht' en suggereert dat de overheid de zaak in de doofpot stopt. Ze riep zelfs op om de uitvaart te verstoren. De moeder van Lisa smeekte Agnes om te stoppen met het misbruiken van het drama voor haar hersenspinsels. 'Fok jou, ik laat me niet de mond snoeren', zou Agnes aan de telefoon hebben geroepen. Bizarre theorie De moeder sleepte Agnes voor de rechter en die vonniste vorige week streng. Op straffe van 500 euro per overtreding moet Agnes stoppen met het verspreiden van haar bizarre theorie over de rug van nabestaanden. ,,Ik heb haar op alle mogelijk manieren gevraagd hiermee te stoppen", zegt de gekrenkte moeder tegen De Telegraaf. ,,Maar dat doet ze niet. Ik hoop dat het vonnis er eindelijk voor zorgt dat het tot haar doordringt hoeveel pijn ze mij en andere naasten van Lisa doet." Het geval van Agnes staat niet op zichzelf. Als je een dierbare verliest door vermissing of een plotse onnatuurlijke dood ga je door een hel. Maar steeds vaker verschijnen er dan betweters op het toneel die je nog verder in de misère helpen. Slopend Vorige week nog. De vermissing van het gehandicapte meisje Hebe en haar begeleidster Sanne was voor Sannes beste vriend Mark al slopend. Toen begonnen plots beschuldigingen tegen hém rond te zingen. Ook toen de lichamen waren gevonden en duidelijk was dat het een verkeersongeluk betrof, hielden de bedreigingen aan. Zijn belagers sloegen aan op een oude zaak waarin Mark ten onrechte was aangemerkt als verdachte van grensoverschrijdend gedrag. ,,Mensen haalden allemaal oude krantenberichten aan en ik werd aangewezen als degene die Sanne en Hebe wat zou hebben aangedaan. Ik en mijn zoontje zijn bedreigd en er stonden mensen voor de deur bij mijn vrouw. Die zat te trillen als een rietje", vertelde Mark aan De Telegraaf. ,,Uitermate pijnlijk voor de nabestaanden of betrokkenen", zo noemt de korpsleiding van de politie dit soort voorbeelden. ,,De politie herkent dit verschijnsel, dat lastig in cijfers is te vatten. Wij kunnen familieagenten inzetten om betrokkenen te helpen, omdat we ons realiseren wat een incident kan betekenen in de (sociale) media." Amateurisme, speurzin en complotdenken vormen een cocktail die levens verwoest. ,,Weet u wel wat u aanricht bij de familie?" vroeg de rechter aan een drietal complotdenkers. Zij hadden maandenlang een onschuldige huisarts uit Bodegraven aan de schandpaal genageld. De arts zou samen met RIVM-baas Jaap van Dissel vroeger tal van schoolkinderen hebben gekeeld. Het drietal beweerde ook dat de vrouw van de huisarts, die aan kanker was overleden, 'waarschijnlijk ook op een andere manier' om het leven was gekomen. Vermoord, dus. Dankzij hun opgewonden internetjournaals kreeg het drietal duizenden fanatieke aanhangers op de been. Die bestempelden Bodegraven tot centrum van een bende satanisten die kinderen misbruiken en afslachten. Anoesjka, een van de volgelingen, schrijft dat ze zich onderdompelde in de filmpjes en toen 'heel veel heeft gehuild'. ,,Al zo verschrikkelijk lang worden kinderen op verschrikkelijke manieren mishandeld, misbruikt, verhandeld. Hele tunnelstelsels, met daarin kooien vol kinderen, stukken van kinderen." De arme huisarts kreeg belagers aan de deur die verhaal kwamen halen. Hij durfde bij de rechtbank zelfs geen schadeclaim in te dienen uit angst voor nog meer ellende. ,,Verdachten wilden hem thuis treffen en dat is gelukt", tierde de officier van justitie. ,,Weerzinwekkend." Niet alleen de arts en Van Dissel werden besmeurd door de Bodegraven-bende. Aanhangers, onder wie Anoesjka, veranderden de plaatselijke begraafplaats in een bloemenzee. Nabestaanden kregen opeens te horen dat hun dierbaren weggemoffelde misbruikslachtoffers waren. Dat kwetste nabestaanden tot op het bot, zei de burgemeester. ,,In plaats van dat ze privé kunnen rouwen, worden ze bij deze onzin betrokken. Iemand is in gesprek gegaan met die mensen wat ze er kwamen doen. En dan volgde een ingewikkeld verhaal waar niets van klopt. Dan zegt hij: hier ligt mijn kind, ga weg." 'Zelf onderzoek' Anoesjka benadrukt dat ze graag 'zelf onderzoek doet', een veelgebruikt motto in complotkringen. Maar voor haar en de andere 'gelovigen' was de enige bron voor het satanistenverhaal een psychisch verwarde man uit Bodegraven die zich op latere leeftijd allerlei buitenissige gebeurtenissen ging 'herinneren'. Zonder een snipper steunbewijs, maar dat was voor de satanistenjagers geen probleem. ,,Jullie eigen onderzoek stelt niets voor", concludeerde de Haagse rechter. Het complottrio kreeg maandenlange celstraffen. ,,Dit verschijnsel lijkt toe te nemen", zegt Evy Khouw van de organisatie Namens de Familie, die getroffen mensen bijstaat in de mediastorm. ,,Onze cliënten hebben er veel last van als allerlei mensen insinuaties gaan strooien. Het is bemoeienis tijdens een zaak waar familie nooit op zit te wachten. Ze zijn al in een wereld gestort waar ze niet in wilden, en dit soort dingen vergroten alleen maar de verwarring, machteloosheid en boosheid."  Nieuw is deze moderne heksenvervolging niet. Rond oud-topambtenaar Demmink zwermen al decennia insinuaties over een verborgen pedonetwerk. Bewijs is nooit geleverd, maar de beschuldigingen stoppen nooit. Het radio-programma Argos bracht in 2018 nog een fel bekritiseerde uitzending waarin de ambtenaar met kindermoorden in verband werd gebracht. En in juni kreeg een man uit Nijmegen vier maanden cel omdat hij bij Demmink voor de deur stond met een megafoon. Hij noteerde dat hij zijn slachtoffer 'zo gek wilde maken dat hij zichzelf gaat verhangen'. ,,Dit is er altijd al geweest", zegt Evy Khouw. ,,Maar alles gaat tien keer sneller door sociale media. Uitingen worden lukraak overgenomen." 'Tunnels met kooien vol kinderen' PDF-bestand van dit document'''


def test_generate_file(csv_file_importer):
    file_data = {
        "title": "Bedreiging Complotdenker door Spanje uitgezet naar NL",
        "date": "24 augustus 2021 dinsdag",
        "body": '''ABSTRACT Joost Knevel werd op verzoek van het Nederlandse OM in Spanje aangehouden. De complotdenker wordt onder meer verdacht van het bedreigen van RIVM-baas Jaap van Dissel en Mark Rutte. VOLLEDIGE TEKST: Complotdenker en een van de drie presentatoren van het zogeheten Red Pill Journal op sociale media, Joost Knevel, is maandag door Spanje overgeleverd aan Nederland. De man hield zich al maanden schuil in het oosten van Spanje en kon na een zoekactie begin deze maand worden opgepakt. De marechaussee heeft Knevel opgehaald. Hij moet in Den Haag terechtstaan en wordt donderdag voorgeleid aan de rechter-commissaris. Knevel wordt verdacht van meerdere strafbare feiten, waaronder bedreiging van en opruiing tot geweld tegen RIVM-baas Jaap van Dissel en Mark Rutte. Zo zei hij over Van Dissel: ,,Wie geeft hem zijn welverdiende nekschot, die is een held". Knevel plaatste volgens het Openbaar Ministerie in Den Haag ook een bewerkte video online waarin meerdere publieke figuren, onder wie bovengenoemden, met een strop om hun nek zogenaamd werden opgehangen. Knevel is de tweede man van het complotjournaal die nu vastzit. Eerder deze zomer werd Wouter Raatgever berecht en veroordeeld tot een celstraf van negen maanden waarvan drie voorwaardelijk, voor het verspreiden van opruiende en bedreigende filmpjes. Hij had eind mei in zijn journaal gezegd dat de advocaat van de gemeente Bodegraven weldra door een militair tribunaal ter dood zou worden veroordeeld. De derde presentator van het journaal voor complotdenkers, Micha Kat, vluchtte naar Noord-Ierland om zijn straf te ontlopen. Daar werd hij op 22 juli opgepakt op grond van een Europees aanhoudingsbevel en daarna onder voorwaarden weer vrijgelaten. Link naar PDF'''
    }
    csv_path = os.path.join(TEST_DATA_DIR, 'correct.csv')

    _, raw_file = csv_file_importer.generate_file(file_data, csv_path, 1)

    assert raw_file.metadata.title == "Bedreiging Complotdenker door Spanje uitgezet naar NL"
    assert raw_file.metadata.date == datetime(2021, 8, 24)
    assert raw_file.metadata.format == "csv"
    assert raw_file.metadata.length == 267  # Number of words in body
    assert raw_file.metadata.size > 0
    assert raw_file.body.body == '''ABSTRACT Joost Knevel werd op verzoek van het Nederlandse OM in Spanje aangehouden. De complotdenker wordt onder meer verdacht van het bedreigen van RIVM-baas Jaap van Dissel en Mark Rutte. VOLLEDIGE TEKST: Complotdenker en een van de drie presentatoren van het zogeheten Red Pill Journal op sociale media, Joost Knevel, is maandag door Spanje overgeleverd aan Nederland. De man hield zich al maanden schuil in het oosten van Spanje en kon na een zoekactie begin deze maand worden opgepakt. De marechaussee heeft Knevel opgehaald. Hij moet in Den Haag terechtstaan en wordt donderdag voorgeleid aan de rechter-commissaris. Knevel wordt verdacht van meerdere strafbare feiten, waaronder bedreiging van en opruiing tot geweld tegen RIVM-baas Jaap van Dissel en Mark Rutte. Zo zei hij over Van Dissel: ,,Wie geeft hem zijn welverdiende nekschot, die is een held". Knevel plaatste volgens het Openbaar Ministerie in Den Haag ook een bewerkte video online waarin meerdere publieke figuren, onder wie bovengenoemden, met een strop om hun nek zogenaamd werden opgehangen. Knevel is de tweede man van het complotjournaal die nu vastzit. Eerder deze zomer werd Wouter Raatgever berecht en veroordeeld tot een celstraf van negen maanden waarvan drie voorwaardelijk, voor het verspreiden van opruiende en bedreigende filmpjes. Hij had eind mei in zijn journaal gezegd dat de advocaat van de gemeente Bodegraven weldra door een militair tribunaal ter dood zou worden veroordeeld. De derde presentator van het journaal voor complotdenkers, Micha Kat, vluchtte naar Noord-Ierland om zijn straf te ontlopen. Daar werd hij op 22 juli opgepakt op grond van een Europees aanhoudingsbevel en daarna onder voorwaarden weer vrijgelaten. Link naar PDF'''


"""
This program has been developed by students from the bachelor Computer Science
at Utrecht University within the Software Project course.
© Copyright Utrecht University
(Department of Information and Computing Sciences)
"""

from interactive_topic_modeling.backend.model.abstract_model import Model, TermLists

from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel

from itertools import chain

from collections.abc import Iterable
from typing import Tuple


class GensimLdaModel(Model):
    dictionary: Dictionary
    model: LdaModel
    bags_of_words: Iterable[Iterable[Tuple[int, int]]]
    parameters: dict

    def __init__(self, term_lists: TermLists, num_topics: int, random_seed=None, **parameters):
        super().__init__(random_seed)
        self.parameters = {}
        self.num_topics = num_topics
        self.train_model(term_lists, **parameters)

    def train_model(self, docs, num_topics=None, **parameters):
        self.parameters.update(parameters)
        self.num_topics = num_topics

        self.dictionary = Dictionary(docs)
        self.bags_of_words = [self.dictionary.doc2bow(tokens) for tokens in docs]
        self.model = LdaModel(corpus=self.bags_of_words,
                              id2word=self.dictionary,
                              num_topics=self.num_topics,
                              random_state=self.random_seed)

    def update_model(self, docs, **parameters):
        added_corpus = [self.dictionary.doc2bow(tokens) for tokens in docs]
        self.dictionary.add_documents(docs)
        self.model.update(added_corpus)
        self.bags_of_words = chain(self.bags_of_words, added_corpus)

    def get_term(self, term_id):
        return self.dictionary[term_id]

    def n_terms(self):
        return len(self.dictionary)

    def show_topics(self, n):
        return self.model.show_topics(formatted=False, num_words=n)

    def get_topics(self, n):
        return [(topic_id, self.get_topic_terms(topic_id, n)) for topic_id in range(self.num_topics)]

    def show_topic_terms(self, topic_id, n):
        return self.model.show_topic(topic_id, topn=n)

    def get_topic_terms(self, topic_id, n):
        return self.model.get_topic_terms(topic_id, topn=n)

    def get_doc_topics(self, doc, minimum_probability=0):
        bag_of_words = self.dictionary.doc2bow(doc)
        return self.model.get_document_topics(bag_of_words, minimum_probability=minimum_probability)

    def get_topic_term_numpy_matrix(self):
        return self.model.get_topics()

    def save(self, fpath):
        raise NotImplementedError("Saving the model has not been implemented in GensimLdaModel")

    @classmethod
    def load(cls, fpath):
        raise NotImplementedError("Loading the model has not been implemented in GensimLdaModel")

if __name__ == "__main__":
    # test lda model
    # todo: remove during review, svp?
    print("Executing test code for GensimLdaModel in main_window.py.MainWindow.__init__(). Please remove after use")
    from interactive_topic_modeling.backend.model.lda_model import GensimLdaModel

    docs = [
        "In de bruisende stad Londen, te midden van de iconische bezienswaardigheden en levendige straten, ligt een verborgen parel van rust en verwondering - de London Zoo. In het weelderige groen van zijn terrein worden bezoekers meegenomen naar een wereld van betovering, waar ze enkele van de meest fascinerende wezens van de planeet kunnen ontmoeten. Onder de sterattracties bevinden zich de geliefde reuzenpanda's, ambassadeurs van China's rijke biodiversiteit en symbolen van wereldwijde natuurbescherming. Terwijl bezoekers wandelen door de weelderige bamboebossen van het Panda-verblijf van de dierentuin, worden ze betoverd door het zicht op deze zachtaardige reuzen, Mei Xiang en Tian Tian, terwijl ze speels op bamboescheuten knabbelen of lui luieren in de schaduw. Londenaren en toeristen stromen toe om een glimp op te vangen van deze schattige wezens, zich verbazend over hun kenmerkende zwart-witte vacht en vertederende capriolen. De aanwezigheid van panda's in Londen dient niet alleen als een bron van vreugde, maar ook als een aangrijpende herinnering aan het belang van het behouden van de kostbare flora en fauna van onze planeet voor toekomstige generaties.",
        "Londen, de bruisende hoofdstad van Engeland en het Verenigd Koninkrijk, staat symbool voor culturele diversiteit, rijke geschiedenis en moderne innovatie. Gelegen langs de oevers van de majestueuze rivier de Theems, is deze uitgestrekte metropool een smeltkroes van culturen, waar eeuwenoude bezienswaardigheden zoals de iconische Big Ben en de historische Tower of London harmonieus samengaan met eigentijdse wolkenkrabbers. De levendige straten zijn gevuld met bedrijvigheid, terwijl rode dubbeldekkers zich een weg banen door het verkeer en voetgangers zich voortbewegen door geplaveide steegjes bezaaid met gezellige cafés en levendige markten. Londen's wereldwijde invloed is tastbaar, van zijn gerenommeerde musea zoals het British Museum en Tate Modern tot zijn bruisende theaterwereld in het West End. Als het kloppende hart van financiën, mode en kunst, weet Londen bezoekers te betoveren met zijn tijdloze charme en dynamische energie, en biedt het een veelheid aan ervaringen die wachten om ontdekt te worden.",
        "In de weelderige bamboebossen van China, waar de lucht dik is van de mist en fluisteringen van oude verhalen, zwerft de geliefde reuzenpanda, een wezen zowel charmant als raadselachtig. Met zijn iconische zwart-witte vacht die lijkt op een formeel pak, is de panda de VIP van de natuur, klaar om elke rode loper te betreden met zijn schattige aanwezigheid. Maar laat je niet misleiden door zijn chique kledij; achter die betoverende ogen schuilt een speelse geest en een hart zo groot als zijn knuffelige gestalte. Panda's zijn het toonbeeld van zenmeesters, die hun dagen lui doorbrengen met het knabbelen op bamboescheuten, hun favoriete lekkernij. Terwijl ze lui tegen de stam van een boom leunen, hun pluizige buikjes vol, lijken ze een aura van rust uit te stralen die zelfs de meest rusteloze zielen kalmeert. Maar laat je niet misleiden door hun relaxte houding; panda's zijn bedreven klimmers en kunnen snel de hoogste bomen beklimmen met de gratie van een ninja. Met een ondeugende glinstering in hun ogen voeren ze acrobatische toeren uit die elke circusartiest te schande zouden maken, allemaal in de jacht op de sappigste bamboescheuten. En laten we de pandawelpen niet vergeten, de kleine balletjes van bont die de show stelen met hun klunzige capriolen en hartverwarmende piepjes. Terwijl ze tuimelen en rollen in een speelse razernij, is het onmogelijk om niet te glimlachen om hun schattige onhandigheid. In een wereld vol chaos en onzekerheid herinneren panda's ons eraan om te vertragen, te genieten van de eenvoudige geneugten en onze speelse kant te omarmen. Dus de volgende keer dat je je gestrest of overweldigd voelt, neem dan een voorbeeld aan de panda's en geniet van een moment van ontspanning, panda-stijl. Immers, het leven is te kort om te serieus te nemen als er bamboescheuten te knabbelen en bomen te beklimmen zijn!"]
    stopwords = set(
        ['aan', 'aangaande', 'aangezien', 'achte', 'achter', 'achterna', 'af', 'afgelopen', 'al', 'aldaar', 'aldus',
         'alhoewel', 'alias', 'alle', 'allebei', 'alleen', 'alles', 'als', 'alsnog', 'altijd', 'altoos', 'ander',
         'andere', 'anders', 'anderszins', 'beetje', 'behalve', 'behoudens', 'beide', 'beiden', 'ben', 'beneden',
         'bent', 'bepaald', 'betreffende', 'bij', 'bijna', 'bijv', 'binnen', 'binnenin', 'blijkbaar', 'blijken',
         'boven', 'bovenal', 'bovendien', 'bovengenoemd', 'bovenstaand', 'bovenvermeld', 'buiten', 'bv', 'daar',
         'daardoor', 'daarheen', 'daarin', 'daarna', 'daarnet', 'daarom', 'daarop', 'daaruit', 'daarvanlangs',
         'dan', 'dat', 'de', 'deden', 'deed', 'der', 'derde', 'derhalve', 'dertig', 'deze', 'dhr', 'die',
         'dikwijls', 'dit', 'doch', 'doe', 'doen', 'doet', 'door', 'doorgaand', 'drie', 'duizend', 'dus', 'echter',
         'een', 'eens', 'eer', 'eerdat', 'eerder', 'eerlang', 'eerst', 'eerste', 'eigen', 'eigenlijk', 'elk',
         'elke', 'en', 'enig', 'enige', 'enigszins', 'enkel', 'er', 'erdoor', 'erg', 'ergens', 'etc', 'etcetera',
         'even', 'eveneens', 'evenwel', 'gauw', 'ge', 'gedurende', 'geen', 'gehad', 'gekund', 'geleden', 'gelijk',
         'gemoeten', 'gemogen', 'genoeg', 'geweest', 'gewoon', 'gewoonweg', 'haar', 'haarzelf', 'had', 'hadden',
         'hare', 'heb', 'hebben', 'hebt', 'hedden', 'heeft', 'heel', 'hem', 'hemzelf', 'hen', 'het', 'hetzelfde',
         'hier', 'hierbeneden', 'hierboven', 'hierin', 'hierna', 'hierom', 'hij', 'hijzelf', 'hoe', 'hoewel',
         'honderd', 'hun', 'hunne', 'ieder', 'iedere', 'iedereen', 'iemand', 'iets', 'ik', 'ikzelf', 'in',
         'inderdaad', 'inmiddels', 'intussen', 'inzake', 'is', 'ja', 'je', 'jezelf', 'jij', 'jijzelf', 'jou',
         'jouw', 'jouwe', 'juist', 'jullie', 'kan', 'klaar', 'kon', 'konden', 'krachtens', 'kun', 'kunnen', 'kunt',
         'laatst', 'later', 'liever', 'lijken', 'lijkt', 'maak', 'maakt', 'maakte', 'maakten', 'maar', 'mag',
         'maken', 'me', 'meer', 'meest', 'meestal', 'men', 'met', 'mevr', 'mezelf', 'mij', 'mijn', 'mijnent',
         'mijner', 'mijzelf', 'minder', 'miss', 'misschien', 'missen', 'mits', 'mocht', 'mochten', 'moest',
         'moesten', 'moet', 'moeten', 'mogen', 'mr', 'mrs', 'mw', 'na', 'naar', 'nadat', 'nam', 'namelijk', 'nee',
         'neem', 'negen', 'nemen', 'nergens', 'net', 'niemand', 'niet', 'niets', 'niks', 'noch', 'nochtans', 'nog',
         'nogal', 'nooit', 'nu', 'nv', 'of', 'ofschoon', 'om', 'omdat', 'omhoog', 'omlaag', 'omstreeks', 'omtrent',
         'omver', 'ondanks', 'onder', 'ondertussen', 'ongeveer', 'ons', 'onszelf', 'onze', 'onzeker', 'ooit', 'ook',
         'op', 'opnieuw', 'opzij', 'over', 'overal', 'overeind', 'overige', 'overigens', 'paar', 'pas', 'per',
         'precies', 'recent', 'redelijk', 'reeds', 'rond', 'rondom', 'samen', 'sedert', 'sinds', 'sindsdien',
         'slechts', 'sommige', 'spoedig', 'steeds', 'tamelijk', 'te', 'tegen', 'tegenover', 'tenzij', 'terwijl',
         'thans', 'tien', 'tiende', 'tijdens', 'tja', 'toch', 'toe', 'toen', 'toenmaals', 'toenmalig', 'tot',
         'totdat', 'tussen', 'twee', 'tweede', 'u', 'uit', 'uitgezonderd', 'uw', 'vaak', 'vaakwat', 'van', 'vanaf',
         'vandaan', 'vanuit', 'vanwege', 'veel', 'veeleer', 'veertig', 'verder', 'verscheidene', 'verschillende',
         'vervolgens', 'via', 'vier', 'vierde', 'vijf', 'vijfde', 'vijftig', 'vol', 'volgend', 'volgens', 'voor',
         'vooraf', 'vooral', 'vooralsnog', 'voorbij', 'voordat', 'voordezen', 'voordien', 'voorheen', 'voorop',
         'voorts', 'vooruit', 'vrij', 'vroeg', 'waar', 'waarom', 'waarschijnlijk', 'wanneer', 'want', 'waren',
         'was', 'wat', 'we', 'wederom', 'weer', 'weg', 'wegens', 'weinig', 'wel', 'weldra', 'welk', 'welke', 'werd',
         'werden', 'werder', 'wezen', 'whatever', 'wie', 'wiens', 'wier', 'wij', 'wijzelf', 'wil', 'wilden',
         'willen', 'word', 'worden', 'wordt', 'zal', 'ze', 'zei', 'zeker', 'zelf', 'zelfde', 'zelfs', 'zes',
         'zeven', 'zich', 'zichzelf', 'zij', 'zijn', 'zijne', 'zijzelf', 'zo', 'zoals', 'zodat', 'zodra', 'zonder',
         'zou', 'zouden', 'zowat', 'zulk', 'zulke', 'zullen', 'zult'])

    preprocessed_docs = [
        [str.lower(token) for token in doc.split(' ') if str.lower(token) not in stopwords and len(token) >= 4] for
        doc in docs]
    model = GensimLdaModel(preprocessed_docs, 2, random_seed=1)
    assert model.num_topics == 2 and model.random_seed == 1

    print("get term 0:", model.get_term(0))
    print("n_terms:", model.n_terms())

    print("show topics n=3:", model.show_topics(3))
    topics = model.get_topics(4)
    print("get topics n=4:", topics)
    reformatted_topics = [(topic_id, [(model.get_term(term_id), term_score)
                                      for (term_id, term_score) in terms])
                          for (topic_id, terms) in topics]
    print("reformatted get topics n=4:", reformatted_topics)

    print("show topic 1 terms n=5:", model.show_topic_terms(1, 5))
    terms = model.get_topic_terms(1, 6)
    print("get topics n=6:", terms)
    reformatted_terms = [(model.get_term(term_id), term_score) for (term_id, term_score) in terms]
    print("reformatted get topic 1 terms n=6:", reformatted_terms)

    for i in range(len(preprocessed_docs)):
        print(f"get doc {i} topics:", model.get_doc_topics(preprocessed_docs[i]))

    topic_term_matrix = model.get_topic_term_numpy_matrix()
    print("numpy matrix of topics x terms (partly):", topic_term_matrix[1, :10])
    print(f"term {52}={model.get_term(52)} with topic 1 has probability: {topic_term_matrix[1, 52]}")

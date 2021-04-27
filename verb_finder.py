import nltk
import math

# Si True, affiche le texte avec les étiquettes
_SHOW_TAGGED_TEXT = True

'''
Auteur : Predrag Kostic

Recherche de verbes (sans dictionnaire de verbes) pour la langue serbe.

Les textes utilisés dans ce programme sont écrits en dialecte shtokavian, sous-dialecte ekavian.
C'est le dialecte le plus courament utilisé en Serbie.
Ce programme supporte ainsi que l'alphabet cyrillique serbe.
Les autres dialectes ne seront peut-être pas compatible avec ce programme.

Le noms des variables et des fonctions sont en anglais.
'''

# Cette fonction retourne un nouveau dictionnaire qui contient les
# clefs-valeurs originaux + les mêmes clefs-valeurs avec les clefs capitalisés
def capitalize_dictionary(dictionary):
    new_dictionary = {}
    for key in dictionary:
        new_dictionary[key.capitalize()] = dictionary[key]
    return new_dictionary

# Les listes suivante ne sont pas completes, j'ai rajouté des mots au fur et à mesure
# Pour avoir une bonne précision, il faudrait avoir une grande liste de noms communs,
# adverbes et une liste complete des mots grammatiques car la langue serbe est très
# flexible avec la composition de mots. Je n'ai pas reussi a trouver une liste donc
# j'ai écrit tous les listes à la main d'apres mes connaisances de la langue.
pronoun = {
    # Personal pronouns
    "ја"    : "P",
    "ти"    : "P",
    "ми"    : "P",
    "ви"    : "P",
    "мене"  : "P",
    "тебе"  : "P",
    "себе"  : "P",
    "нас"   : "P",
    "вас"   : "P",
    "мени"  : "P",
    "теби"  : "P",
    "нама"  : "P",
    "вама"  : "P",
    "мном"  : "P",
    "тобом" : "P",
    "собом" : "P",
    "себи"  : "P",

    "он"   : "P",
    "оно"  : "P",
    "она"  : "P",
    "они"  : "P",
    "оне"  : "P",
    "њега" : "P",
    "ње"   : "P",
    "њих"  : "P",
    "њему" : "P",
    "њој"  : "P",
    "њима" : "P",
    "њу"   : "P",
    "њиме" : "P",
    "њоме" : "P",

    "све"   : "P",
    "сва"   : "P",
    "сви"   : "P",
    "свега" : "P",
    "свему" : "P",
    "свим"  : "P",

    # Possessive pronouns
    "мој"    : "PP",
    "моје"   : "PP",
    "моја"   : "PP",
    "твој"   : "PP",
    "твоје"  : "PP",
    "твоја"  : "PP",
    "свој"   : "PP",
    "своје"  : "PP",
    "своја"  : "PP",
    "својом" : "PP",
    "наш"    : "PP",
    "наше"   : "PP",
    "наша"   : "PP",
    "ваш"    : "PP",
    "ваше"   : "PP",
    "ваша"   : "PP",
    "његов"  : "PP",
    "његово" : "PP",
    "његова" : "PP",
    "њен"    : "PP",
    "њено"   : "PP",
    "њена"   : "PP",
    "њезин"  : "PP",
    "њезино" : "PP",
    "њезина" : "PP",
    "њихов"  : "PP",
    "њихово" : "PP",
    "њихова" : "PP",

    # Reflexive pronouns
    "сам"    : "RP",
    "само"   : "RP",
    "сама"   : "RP",
    "сами"   : "RP",
    "саме"   : "RP",
    "самог"  : "RP",
    "самих"  : "RP",
    "самом"  : "RP",
    "самој"  : "RP",
    "самима" : "RP",
    "се"     : "RP",
    "саму"   : "RP",
    "самим"  : "RP",

    # Demonstrative pronouns
    "тај"     : "DP",
    "то"      : "DP",
    "та"      : "DP",
    "овај"    : "DP",
    "ово"     : "DP",
    "ова"     : "DP",
    "онај"    : "DP",
    "такав"   : "DP",
    "такво"   : "DP",
    "таква"   : "DP",
    "овакав"  : "DP",
    "овакво"  : "DP",
    "оваква"  : "DP",
    "онакав"  : "DP",
    "онакво"  : "DP",
    "онаква"  : "DP",
    "толики"  : "DP",
    "толико"  : "DP",
    "толика"  : "DP",
    "оволики" : "DP",
    "оволико" : "DP",
    "оволика" : "DP",
    "онолики" : "DP",
    "онолико" : "DP",
    "онолика" : "DP",
    "исти"    : "DP",
    "исто"    : "DP",
    "иста"    : "DP",
    "какав"   : "DP",

    "ко" : "P",
    "кога" : "P",
    "ког" : "P",
    "кому" : "P",
    "коме" : "P",
    "ком" : "P",
    "ким" : "P",
    "киме" : "P"
}

negation = {
    "не" : "N",
    "није" : "N"
}

conjuction = {
    "и"    : "C",
    "а"    : "C",
    "те"   : "C",
    "како" : "C",
    "тако" : "C",

    "али"   : "C",
    "него"  : "C",
    "но"    : "C",
    "већ"   : "C",
    "па"    : "C",
    "ипак"  : "C",
    "пак"   : "C",
    "док"   : "C",
    "само"  : "C",
    "ма"    : "C",
    "макар" : "C",

    "или"  : "C",
    # "било" : "C", # peut aussi être le verbe "biti", cas defini dans find_verbs() 
    "ни"   : "C",
    "нити" : "C",

    "да"  : "C",
    "ли"  : "C",
    "што" : "C",

    "дакле" : "C",
    "зато"  : "C",
    "стога" : "C",

    "иако"   : "C",
    "мада"   : "C",
    "премда" : "C",
    

    "чим"    : "C",
    "када"   : "C",
    "кад"    : "C",
    "откако" : "C",
    "пре"    : "C",
    "тек"    : "C",
    
    "неголи" : "C",
    "камоли" : "C",
    
    "јер"   : "C",
    "пошто" : "C",
    
    "ако" : "C",
    
    "као" : "C",
    
    "би" : "C",
    
    "нека" : "C",
    
    "бар"   : "C",
    "барем" : "C",
    
    "где"    : "C",
    "одакле" : "C",
    "откуд"  : "C",
    "ко"     : "C",
    "шта"    : "C",
    "куда"   : "C"
}

enclitic = {
    # Interrogative enclitic
    "ли" : "IE",
    
    # Verbal enclitics
    "сам" : "VE",
    "си"  : "VE",
    "је"  : "VE",
    "смо" : "VE",
    "сте" : "VE",
    "су"  : "VE",
    
    "ћу"   : "VE",
    "ћеш"  : "VE",
    "ће"   : "VE",
    "ћемо" : "VE",
    "ћете" : "VE",

    "бих"   : "VE",
    "би"    : "VE",
    "бисмо" : "VE",
    "бисте" : "VE"
}

preposition = {
    "из"  : "PR",
    "са"  : "PR",
    "ка"  : "PR",
    "под" : "PR",

    "без"      : "PR",
    "близу"    : "PR",
    "ван"      : "PR",
    "до"       : "PR",
    "дуж"      : "PR",
    "иза"      : "PR",
    "изван"    : "PR",
    "изнад"    : "PR",
    "између"   : "PR",
    "због"     : "PR",
    "код"      : "PR",
    "крај"     : "PR",
    "место"    : "PR",
    "наврх"    : "PR",
    "надомак"  : "PR",
    "након"    : "PR",
    "насред"   : "PR",
    "насупрот" : "PR",
    "ниже"     : "PR",
    "од"       : "PR",
    "око"      : "PR",
    "осим"     : "PR",
    "поврх"    : "PR",
    "покрај"   : "PR",
    "попут"    : "PR",
    "поред"    : "PR",
    "после"    : "PR",
    "пре"      : "PR",
    "при"      : "PR",
    "преко"    : "PR",
    "против"   : "PR",
    "ради"     : "PR",
    "уочи"     : "PR",
    "усред"    : "PR",

    "за"   : "PR",
    "кроз" : "PR",
    "међу" : "PR",
    "на"   : "PR",
    "над"  : "PR",
    "низ"  : "PR",
    "о"    : "PR",
    "по"   : "PR",
    "пред" : "PR",
    "у"    : "PR",
    "уз"   : "PR"
}

numeral = {
    # Cardinal
    "нула"   : "CN",
    "један"  : "CN",
    "једна"  : "CN",
    "једно"  : "CN",
    "једног" : "CN",
    "једне"  : "CN",
    "једном" : "CN",
    "два"    : "CN",
    "две"    : "CN",
    "дво"    : "CN",
    "оба"    : "CN",
    "обе"    : "CN",
    "три"    : "CN",
    "четири" : "CN",
    "пет"    : "CN",
    "шест"   : "CN",
    "седам"  : "CN",
    "осам"   : "CN",
    "девет"  : "CN",
    "десет"  : "CN",

    # Ordinal
    "први"    : "ON",
    "прва"    : "ON",
    "прво"    : "ON",
    "други"   : "ON",
    "друга"   : "ON",
    "друго"   : "ON",
    "трећи"   : "ON",
    "трећа"   : "ON",
    "треће"   : "ON",
    "четврти" : "ON",
    "четврта" : "ON",
    "четврто" : "ON",
    "пети"    : "ON",
    "пета"    : "ON",
    "пето"    : "ON",
    "шести"   : "ON",
    "седми"   : "ON",
    "осми"    : "ON",
    "девети"  : "ON",
    "десети"  : "ON",

    # Collective
    "двоје"    : "CO",
    "троје"    : "CO",
    "четворо"  : "CO",
    "петоро"   : "CO",
    "шесторо"  : "CO",
    "седморо"  : "CO",
    "осморо"   : "CO",
    "деветоро" : "CO",
    "десеторо" : "CO",

    # Number nouns
    "двојица"    : "NN",
    "тројица"    : "NN",
    "четворица"  : "NN",
    "петорица"   : "NN",
    "шесторица"  : "NN",
    "седморица"  : "NN",
    "осморица"   : "NN",
    "деветорица" : "NN",
    "десеторица" : "NN"
}

adverb = {
    "далеко" : "A",
    "овде" : "A",
    "тада" : "A",
    "игде" : "A"
}

punctuation = {
    "." : ".",
    "!" : ".",
    "?" : ".",
    "," : ","
}

# Le modele est construit à partir de toutes les listes + listes capitalisés
model = {}
model.update(pronoun)
model.update(negation)
model.update(conjuction)
model.update(enclitic)
model.update(preposition)
model.update(numeral)
model.update(adverb)
model.update(capitalize_dictionary(model))
model.update(punctuation)

# Le Unigram Tagger de nltk prend en parametre un modele et permet d'étiqueter les mots dans un texte
unigram = nltk.UnigramTagger(model=model)

# Cette fonction prend en parametre un texte et en option une liste de verbes (pour verifier la précision du programme)
# Affiche la liste de verbes trouves (et si possible les verbes pas trouvés et les verbes incorrects)
def find_verbs(words, verbs_list=[]):
    _PRONOUN = 'P'
    _NEGATION = 'N'
    _VERBAL_ENCLITIC = 'VE'
    _POSSESSIVE_PRONOUN = 'PP'
    _REFLEXIVE_PRONOUN = 'RP'
    _PREPOSITION = 'PR'
    _PUNCTUATION = '.'
    _CONJUCTION = 'C'
    _DEMONSTRATIVE_PRONOUN = 'DP'
    _CARDINAL_NUMBER = 'CN'
    _ORDINAL_NUMBER = 'ON'
    _ADVERB = 'A'
    _COMMA = ','

    words_tokens = nltk.word_tokenize(words)
    words_tags = unigram.tag(words_tokens)

    if (_SHOW_TAGGED_TEXT):
        print(words_tags, "\n")

    verbs_found = []

    s = len(words_tags)
    t = 0
    while (t < s):
        # Cas : mots non marqués 
        if (words_tags[t][1] == None):
            # Cas : précédé par un pronom
            if (words_tags[t-1][1] == _PRONOUN):
                # Cas : sauf si pas précédé par un pronom demonstratif
                if (not words_tags[t-3][1] == _DEMONSTRATIVE_PRONOUN):
                    verbs_found.append(words_tags[t][0])
            # Cas : précédé par une négation
            elif (words_tags[t-1][1] == _NEGATION):
                verbs_found.append(words_tags[t][0])
            # Cas : suivi par une enclitique verbale
            elif (words_tags[t+1][1] == _VERBAL_ENCLITIC):
                # Cas : précédé par une preposition
                if (words_tags[t-1][1] == _PREPOSITION):
                    verbs_found.append(words_tags[t+2][0])
                else:
                    verbs_found.append(words_tags[t][0])
            # Cas : précédé par un mot non marqué puis une enclitique verbale
            elif (words_tags[t-1][1] == None and
                  words_tags[t-2][1] == _VERBAL_ENCLITIC):
                # Cas : sauf si précédé par un mot non marquée
                if (not words_tags[t-3][1] == None):
                    verbs_found.append(words_tags[t][0])
            # Cas : précédé par un mot non marqué puis un pronom possesif précédé par un pronon réflechi
            elif (words_tags[t-1][1] == None and
                  words_tags[t-2][1] == _POSSESSIVE_PRONOUN and
                  words_tags[t-3][1] == _REFLEXIVE_PRONOUN):
                verbs_found.append(words_tags[t][0])
            # Cas : précédé par une conjuction précéde par une ponctuation
            elif (words_tags[t-1][1] == _CONJUCTION and
                  words_tags[t-2][1] == _PUNCTUATION):
                verbs_found.append(words_tags[t][0]) 
            # Cas : précédé par un pronom réfléchi
            elif (words_tags[t-1][1] == _REFLEXIVE_PRONOUN):
                verbs_found.append(words_tags[t][0])
            # Cas : précédé par un mot non marqué précédé par une preposition précéde par une enclitique verbale
            elif (words_tags[t-1][1] == None and
                  words_tags[t-2][1] == _PREPOSITION and
                  words_tags[t-3][1] == _VERBAL_ENCLITIC):
                verbs_found.append(words_tags[t][0])
            # Cas : précédé par un pronom démonstratif précédé par une enclitique verbale précédé par une conjunction
            elif (words_tags[t-1][1] == _DEMONSTRATIVE_PRONOUN and
                  words_tags[t-2][1] == _VERBAL_ENCLITIC and
                  words_tags[t-3][1] == _CONJUCTION):
                verbs_found.append(words_tags[t][0])
            # Cas : précédé par un pronom possesif et suivi par une conjunction
            elif (words_tags[t-1][1] == _POSSESSIVE_PRONOUN and
                  words_tags[t+1][1] == _CONJUCTION):
                verbs_found.append(words_tags[t][0])
            # Cas : précédé par un adverbe précéde par un pronom possesif
            elif (words_tags[t-1][1] == _ADVERB and
                  words_tags[t-2][1] == _POSSESSIVE_PRONOUN):
                verbs_found.append(words_tags[t][0])
            # Cas : précédé par un pronom possesif, suivi par une virgule
            elif (words_tags[t-2][1] == _POSSESSIVE_PRONOUN and
                  words_tags[t+1][1] == _COMMA):
                verbs_found.append(words_tags[t][0])
            # Cas : précédé par un adverbe, précédé par un pronom réfléchi
            elif (words_tags[t-1][1] == _ADVERB and
                  words_tags[t-2][1] == _REFLEXIVE_PRONOUN):
                verbs_found.append(words_tags[t][0])
            # Cas : suivi par pronom réfléchi suivi par une conjuction
            elif (words_tags[t+1][1] == _REFLEXIVE_PRONOUN and
                  words_tags[t+2][1] == _CONJUCTION):
                verbs_found.append(words_tags[t][0])
            # Cas : précédé par une conjuction précédé par un pronom réfléchi 
            elif (words_tags[t-2][1] == _REFLEXIVE_PRONOUN and
                  words_tags[t-1][1] == _CONJUCTION):
                verbs_found.append(words_tags[t][0])
            # Cas : forte chance d'être un verbe en infinitif
            elif (words_tags[t][0][-2:] == "ти" or words_tags[t][0][-2:] == "ћи" or
                  words_tags[t][0][-5:] == "ивати" or words_tags[t][0][-5:] == "овати" or
                  words_tags[t][0][-5:] == "авати" or words_tags[t][0][-3:] == "сти"):
                # Cas : sauf si précédé par un nombre
                if (not words_tags[t-1][1] == _CARDINAL_NUMBER and
                    not words_tags[t-1][1] == _ORDINAL_NUMBER):
                    verbs_found.append((words_tags[t][0], "inf"))
            # Cas : forte chance d'être un verbe si fin -ло -ла -ао et suivi par une ponctuation
            elif ((words_tags[t][0][-2:] == "ло" or words_tags[t][0][-2:] == "ла" or
                  words_tags[t][0][-2:] == "ао") and
                  words_tags[t+1][1] == _PUNCTUATION):
                verbs_found.append(words_tags[t][0])
        t += 1

    print("Verbes trouvés :\t---\t", verbs_found)

    # Si la liste des verbes est disponible
    if (verbs_list != []):
        # Fait une liste des verbes qui n'ont pas été trouvé
        missing_verbs = []
        for v in verbs_list:
            if v not in verbs_found:
                missing_verbs.append(v)

        print("Verbes manquants :\t---\t", missing_verbs)

        # Fait une liste des mots qui ont été trouvé mais qui ne sont pas des verbes
        incorrect_verbs = []
        for v in verbs_found:
            if v not in verbs_list:
                incorrect_verbs.append(v)
        
        print("Les non verbes :\t---\t", incorrect_verbs, "\n")
    else:
        print("")

# Les textes avec la liste des verbes trouvés à la main pour comparer le résultat du programme
simple_sentences ="""
Ја скачем веома високо. Да ли ти волиш шпагете? Ми не волимо ићи у биоскоп. Ви имате једну кућу.
"""
simple_sentences_verbs = ['скачем', 'волиш', 'волимо', ('ићи', 'inf'), 'имате']

excerpt_1 = """
Било је времена када је васељена била пуна небесних тела, али 
наше земље у њој није било. И било је времена када се наша земља 
створила, али на њој не беше ни биља ни животиња. Па насташе 
времена, када је на земљи било разнога биља и разних животиња, 
али никаквих људи није било. Најзад се појавише и први људи, али 
је то било тако давно да их и најстарија историја не памти. Сва 
су та времена веома дуго трајала, па изгледа да је земља морала
проћи кроз врло многе мене, док су се на њој створиле прилике у 
којима људи могаху живети и напредовати. При тим променама 
највише се мењао биљни и животињски свет докле најзад није добио 
и свој најсавршенији створ у облику човека."""

excerpt_1_verbs = ['Било', 'била', 'било', 'било', 'створила', 'беше', 'насташе', 'било', 'било',
'појавише', 'било', 'памти', 'морала', ('проћи', 'inf'), 'створиле', ('живети', 'inf'), 
('напредовати', 'inf'), 'мењао', 'добио']

excerpt_2 = """
Земља наша има дакле врло дуготрајну историју, која величином и 
разноликошћу  својом далеко превазилази историју целога човештва 
и свију појединих народа. И та је историја подељена на периоде, 
које се зову по свом старешинству примарне, секундарне, 
терцијарне и кватерне.
"""

excerpt_2_verbs = ['има', 'превазилази', 'подељена','зову']

excerpt_3 = """
У примарним периодама прво је један свеопшти океан покривао 
целу земљу, па се за тим из њега овде онде по нешто суве земље 
издизало. На овим островима поникло је прво биље, а са овим се 
појавише први инсекти. На земљи је морала  тада владати мртва 
тишина, јер не беше никаквих гласовитих животиња; једва ли је 
какав цврчак оно глуво доба својом цврком прекидао, а камо ли да 
су се игде  могле чути тице певачице.
"""
# Pour ce texte il est impossible avec un parseur donné les limites du projet de detecter le verbe покривао
excerpt_3_verbs = ['покривао', 'издизало', 'поникло', 'појавише',
'морала', ('владати', 'inf'), 'беше', 'прекидао', 'могле', ('чути', 'inf')]

excerpt_4 = """
Земља се тресла, пуцала је, срозавала се и издизала, а кроз 
пукотине куљала је лавична маса исто као и у познијим и садашњим 
вулканима. Али ако су се при овоме и дешавали силовити окршаји, 
не беше никаквога вишег створа кога би могли застрашити.
"""
# Pour ce texte, le parseur ne peut pas savoir lequel de ces deux mots est le verbe: дешавали et силовити
excerpt_4_verbs = ['тресла', 'пуцала', 'срозавала', 'издизала', 'куљала', 'дешавали', 'беше', 'застрашити']

excerpt_5 = """
У секундарним периодама на сувој се земљи и биље и животиње 
поче нагло  развијати, и приуготови се да прими на се облике 
какве има и у садашњем добу.
"""

excerpt_5_verbs = ['поче', ('развијати', 'inf'), 'прими']

# Les trois derniers textes ont des compositions tres differentes par rapport au textes de départ, qui
# ont servi comme exemple pour les regles de grammaire. Pour cette raison le taux de réussite est bas.

excerpt_6 = """
У терцијарним периодама континенти добиваху у главноме данашње 
границе,  јер се море повукло из неколико сада сувих области а
покрило је друге неке које  до тада беху на суву. Тада се 
издизаху главне садашње планине: Балкан, Кавказ и  Карпати, 
Динарски и други Алпи, Апенини и Пиренеји, а на многим брдима у 
Србији,  Македонији, Тракији, у Угарској, Чешкој, Немачкој и 
Француској отвараху се нови  вулкани, који трајаше до потоње 
геолошке периоде. Климат се истина колебао те  бивао час топлији 
час хладнији, а према њему се мењала и биљна одећа земљина,  али 
су најсавршеније животиње, то јест сисари, баш у овим периодама 
постигле  врхунац свога развића.
"""

excerpt_7 = """
Терцијарне се периоде разликују по главним променама климата и по 
променама  измеђ суве змље спрам мора, по ступњевима у издизању 
горских венаца и  усавршавању животиња из кола сисара; те периоде 
зову се у науци: Еоцен,  Олигоцен, Миоцен и Плиоцен, јер се тим 
именима исказује степен њихове сличности  са садашњом периодом. 
Прве две састављају се у тако звани Палеоген а друге две у  
Неоген.
"""

excerpt_8 = """
Нас се овде нарочито тичу времена Неогена, јер је тада већ могуће 
било да се и  човек на земљи појави; са тога ћемо у кратко 
приказати каквим је биљем и  животињама тадашње људство могло 
бити окружено.
"""

find_verbs(simple_sentences, simple_sentences_verbs)
find_verbs(simple_sentences)
find_verbs(excerpt_1, excerpt_1_verbs)
find_verbs(excerpt_2, excerpt_2_verbs)
find_verbs(excerpt_3, excerpt_3_verbs)
find_verbs(excerpt_4, excerpt_4_verbs)
# find_verbs(excerpt_5, excerpt_5_verbs)
# find_verbs(excerpt_6)
# find_verbs(excerpt_7)
# find_verbs(excerpt_8)

# TODO : Tagger les verbes dans le texte, charger un fichier
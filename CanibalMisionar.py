"""
Presupunem ca avem costul de plimbare a unui canibal =2 si a unui misionar =1.
 Astfel A* are trebui sa prefere drumurile in care se muta mai rar canibalii
 Enunt:
 N canibali si N misionari pe malul unui rau
 M locuri in barca
 Nici in barca, nici pe mal nr de canibalui > nr misionari
 Input clasic N=3 (canibali/misionari) si M=2 (locuri in barca)
"""
import math

# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    gr = None  # trebuie setat sa contina instanta problemei

    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info #tuplu de forma (canib,mis,mal:1/0)
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self];
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            if nod.parinte is not None:
                if nod.parinte.info[2] == 1: # malul stang =1
                    mbarca1 = self.__class__.gr.malInitial # tip de mal stang/drept
                    mbarca2 = self.__class__.gr.malFinal
                else: # malul drept = 0
                    mbarca1 = self.__class__.gr.malFinal
                    mbarca2 = self.__class__.gr.malInitial
                print(">>> Barca s-a deplasat de la malul {} la malul {} cu {} canibali si {} misionari.".
                      format(mbarca1,mbarca2,abs(nod.info[0] -nod.parinte.info[0]),abs(nod.info[1] -nod.parinte.info[1])))
            print(str(nod))
        if afisCost:
            print("Cost drum: ", self.g)
        if afisLung:
            print("Lungime drum: ", len(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __str__(self):
        if self.info[2] == 1:
            barcaMalInitial = "<barca>"
            barcaMalFinal = "       "
        else:
            barcaMalInitial = "       "
            barcaMalFinal = "<barca>"
        return (
                    "Mal: " + self.gr.malInitial + " Canibali: {} Misionari: {} {}  |||  Mal:" + self.gr.malFinal + " Canibali: {} Misionari: {} {}").format(
            self.info[0], self.info[1], barcaMalInitial, self.__class__.gr.N - self.info[0],
            self.__class__.gr.N - self.info[1], barcaMalFinal)


class Graph:
    def __init__(self, nume_fisier):
        # citire din fisier 5 4 stang drept
        # nr de canibali si misionari este acelasi
        f = open(nume_fisier, "r")
        textFisier = f.read()
        listaInfoFisier = textFisier.split() # lista cu [5,4,stang,drept]

        self.__class__.N = int(listaInfoFisier[0]) # nr canibali si misionari
        self.__class__.M = int(listaInfoFisier[1]) # numarul de locuri in barca
        self.__class__.malInitial = listaInfoFisier[2] # stang
        self.__class__.malFinal = listaInfoFisier[3] # drept
        # aici o stare este ce se afla pe un mal
        # iar mersul cu barca este o mutare (ca la am luat un bloc si-l tinem in aer)
        self.start = (self.__class__.N, self.__class__.N, 1)  # informatia nodului de start
        # 1 daca barca e pe malul initial(stang), 0 daca e pe malul (drept)
        # memorez doar ce e pe un mal pentru ca pe celalalt mal este complementara
        # memoram mereu ce e pe malul stang
        # avem o singura stare scop (aici, dar la alte probleme pot fi mai multe)
        self.scopuri = [(0, 0, 0)] # 0 0 pt ca pe malul initial nu mai e niciun canibal, niciun misionar
                                    # si 0 pt ca e pe malul drept

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri

    # functia de generare a succesorilor, facuta la laborator
    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        # numim mal curent, malul cu barca
        # scriem pt orice nod si verificam dupa daca se mananca intre ei
        def test_conditie(mis, can): # true daca nu se mananca intre ei
            return mis == 0 or mis >= can

        listaSuccesori = []
        # nodCurent.info = triplet (c_i, m_i, 1/0 pt barca)
        barca = nodCurent.info[2]
        if barca == 1: # malul stang cu barca
            canMalCurent = nodCurent.info[0]
            misMalCurent = nodCurent.info[1]
            canMalOpus =  self.__class__.N - canMalCurent
            misMalOpus =  self.__class__.N - misMalCurent
        else: # barca este pe malul final (unde ii mut)
            canMalOpus = nodCurent.info[0]
            misMalOpus = nodCurent.info[1]
            canMalCurent =  self.__class__.N - canMalOpus
            misMalCurent =  self.__class__.N - misMalOpus

        # ne limiteaza numarul de locuri din barca
        maxMisionariBarca = min( self.__class__.M, misMalCurent)
        for misBarca in range(maxMisionariBarca + 1):
            if misBarca == 0:
                # nu am misionari
                maxCanibaliBarca = min(self.__class__.M, canMalCurent)
                minCanibaliBarca = 1
            else:
                # am misionari
                maxCanibaliBarca = min( self.__class__.M - misBarca, canMalCurent, misBarca)
                minCanibaliBarca = 0

            for canBarca in range(minCanibaliBarca, maxCanibaliBarca + 1):
                # consideram mal curent nou ca fiind acelasi mal de pe care a plecat barca
                # cati au ramas dupa transfer
                canMalCurentNou = canMalCurent - canBarca
                misMalCurentNou = misMalCurent - misBarca
                canMalOpusNou = canMalOpus + canBarca
                misMalOpusNou = misMalOpus + misBarca
                # testez sa nu se manance intre ei
                if not test_conditie(misMalCurentNou, canMalCurentNou):
                    continue
                if not test_conditie(misMalOpusNou, canMalOpusNou):
                    continue
                if barca == 1:  # testul este pentru barca nodului curent (parinte) deci inainte de mutare
                    infoNodNou = (canMalCurentNou, misMalCurentNou, 0)
                else:
                    infoNodNou = (canMalOpusNou, misMalOpusNou, 1)
                if not nodCurent.contineInDrum(infoNodNou):
                    costSuccesor = canBarca * 2 + misBarca
                    listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, cost=nodCurent.g + costSuccesor,
                                                        h=NodParcurgere.gr.calculeaza_h(infoNodNou, tip_euristica)))

        return listaSuccesori

    # euristica banala
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            if infoNod not in self.scopuri:
                return 1
            return 0
        else:
            # calculez cati oameni mai am de mutat si impart la nr de locuri in barca
            totalOameniDeMutat=infoNod[0]+infoNod[1]
            return 2 * math.ceil(totalOameniDeMutat / self.M) + (1 - infoNod[2]) - 1
            # (1-infoNod[2]) barca se intoarce pe celalalt mal
            # spre malul initial ca sa ii ia pe oameni, pe cand daca e deja pe malul initial, nu se mai aduna acel 1


    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir


def a_star(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]

    while len(c) > 0:
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


gr = Graph("input2.txt")
NodParcurgere.gr = gr

print("\n\n##################\nSolutii obtinute cu A*:")
nrSolutiiCautate = 3
a_star(gr, nrSolutiiCautate=3, tip_euristica="euristica nebanala")

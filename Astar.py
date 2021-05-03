class NodParcurgere:
    # informatii despre un nod din arborele de parcurgere (nu din graful initial)
    graf = None  # !!! static

    def __init__(self, id, info, parinte, cost, h):
        self.id = id  # este indicele din vectorul de noduri
        self.info = info  # litera corespunzatoare
        self.parinte = parinte  # parintele din arborele de parcurgere
        # None pentru radacina
        self.g = cost  # cost de la start->nod_c
        self.h = h  # cat cred ca mai am = cost nod_c->scop
        self.f = self.g + self.h  # formula cost drum

    def obtineDrum(self):  # self=this
        # merge din tata in tata pana ajunge la radacina
        l = [self.info]
        nod = self
        while nod.parinte is not None:  # daca nu a ajuns la radacina
            l.insert(0, nod.parinte.info)  # adauga mereu pe prima pozitie
            nod = nod.parinte
        return l  # lista cu drumul

    def afisDrum(self):  # returneaza si lungimea drumului
        # afiseaza drumul
        l = self.obtineDrum()
        print("->".join(l))
        print("Cost: ", self.g)  # afisez si costul
        return len(l)

    def contineInDrum(self, infoNodNou):
        # verifica daca un drum contine deja un nod
        # drumul este dat prin nodul curent
        nodDrum = self
        # merge din parinte in parinte
        while nodDrum is not None:  # nu a ajuns la radacina
            if (infoNodNou == nodDrum.info):
                return True  # cand gaseste returneaza True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        # afisare nod sub forma b(id = 1, drum=a->b, cost=10)
        sir = ""
        sir += self.info + "("
        sir += "id = {}, ".format(self.id)
        sir += "drum="
        drum = self.obtineDrum()
        sir += ("->").join(drum)
        sir += " g:{}".format(self.g)
        sir += " h:{}".format(self.h)
        sir += " f:{})".format(self.f)
        return sir


class Graph:  # graful problemei
    def __init__(self, noduri, matriceAdiacenta, matricePonderi, start, scopuri, lista_h):
        self.noduri = noduri
        self.matriceAdiacenta = matriceAdiacenta
        self.matricePonderi = matricePonderi
        self.nrNoduri = len(matriceAdiacenta)
        self.start = start  # informatia nodului de start
        self.scopuri = scopuri  # lista cu informatiile nodurilor scop
        self.lista_h = lista_h  # lista cost nod_c -> scop

    def indiceNod(self, n):
        return self.noduri.index(n)

    def calculeaza_h(self, infoNod):  # acceseaza h din lista
        return self.lista_h[self.indiceNod(infoNod)]

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []
        for i in range(self.nrNoduri):
            # n-au fost deja vizitati = nu au fost pusi in drum
            if self.matriceAdiacenta[nodCurent.id][i] == 1 and not nodCurent.contineInDrum(self.noduri[i]):
                # apelare constructor clasa NodParcurgere
                nodNou = NodParcurgere(i, self.noduri[i], nodCurent, nodCurent.g + self.matricePonderi[nodCurent.id][i],
                                       self.calculeaza_h(self.noduri[i]))
                # index      info    parinte   cost      h
                listaSuccesori.append(nodNou)
        return listaSuccesori

    def testeaza_scop(self, nodCurent):
        # verifica daca e nod scop
        return nodCurent.info in self.scopuri

    def __repr__(self):  # -> pentru prin(gr=Graph(noduri, m, start, scopuri))
        # reprezentarea sub forma de string a clasei
        sir = ""
        # k o sa fie numele campurilor de date sub forma de string
        # v o sa fie valorile lor
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir


noduri = ["a", "b", "c", "d", "e", "f", "g", "i", "j", "k"]

m = [
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# matricea costurilor / ponderilor
mp = [
    [0, 3, 9, 7, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 10, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 1, 0, 0, 10, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 7, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
for i in range(len(mp)):
    for j in range(len(mp)):
        if mp[i][j] != 0:
            print(i, " ", j, "cost: ", mp[i][j])
start = "a"
scopuri = ["f"]  # pot sa am cate prajituri vreau

# exemplu de euristica banala (1 daca nu e nod scop si 0 daca este)
vect_h = [0, 10, 3, 7, 8, 0, 14, 3, 1, 2]

gr = Graph(noduri, m, mp, start, scopuri, vect_h)
NodParcurgere.graf = gr
# print(gr) # printeaza tot ce am dat mai sus

"""
    spre deosebire de UCS, A* face estimari nu o ia pe bajbaite
    UCS-ul poate sa ajunga si pe la Cluj incercand sa ajunga in Constanta 
    vreau sa merg pe nodurile mai apropaite de nodul scop
    g cat am parcurs
    h cat cred ca mai am (euristica)
    f = g + h
    doar o linie de cod difera fata de UCS
    vect_h -> vectorul de euristici
    cand am mai multe noduri scop calculez euristica pt ficare si iau minimul
"""


def a_star(gr):
    # open = coada noduri descoperite care nu au fost expandate
    # closed= noduri descoperite si expandate
    open = [NodParcurgere(gr.indiceNod(gr.start), gr.start, None, 0, gr.calculeaza_h(gr.start))]

    # face parte din optimizare
    closed = []  # n-am expandat pe nimeni la momentul asta
    while len(open) > 0:
        print("Coada actuala: " + str(open))
        input()
        nodCurent = open.pop(0)
        closed.append(nodCurent)  # a fost vizitat

        if gr.testeaza_scop(nodCurent):  # daca am ajuns la un nod scop
            print("Solutie: ")
            nodCurent.afisDrum()
            return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        print("Lista Succesori:", lSuccesori)

    # -----------------------optimizare--------------------------
        # solutia neoptimizata pune foarte multe noduri in open (coada) uneori si dubluri
        # nu elimina nodurile cu cost mai mare

        # deci, elimin nodurile de cost mare care urmau sa fie expandate
        for s in lSuccesori:
            gasitOpen = False
            for elemc in open:
                if s.info == elemc.info:
                    # inseamna ca este in open si nu mai are rost sa-l caute in close
                    gasitOpen = True # deoarece nu poate sa existe
                                       # si in closed si in open in acelasi timp
                    # cazurile cu ponderi
                    if s.f >= elemc.f:  # nu mai vreau sa-l expandez
                        lSuccesori.remove(s)
                    else:
                        open.remove(elemc)  # il sterg doar din coada
        if not gasitOpen:
            for elemc in closed:
                if s.info == elemc.info:
                    # cazurile cu ponderi
                    if s.f >= elemc.f:  # nu mai vreau sa adaug succesorul
                        lSuccesori.remove(s)
                    else:
                        open.remove(elemc)  # il sterg din coada
        # -----------------------Sfarsit optimizare-----------------------------

        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(open)):
                # diferenta fata de UCS e ca ordonez dupa f

                # ---------------- Optimizare 2------------------------
                # daca f-urile sunt egale ordonez descrescator dupa g
                if open[i].f > s.f or (open[i].f == s.f and open[i].g <= s.g):
                    gasit_loc = True
                    break
                # -------------------------------------------------------
                #if open[i].f >= s.f:
                    #gasit_loc = True
                    #break
            if gasit_loc:
                open.insert(i, s)
            else:
                open.append(s)


a_star(gr)

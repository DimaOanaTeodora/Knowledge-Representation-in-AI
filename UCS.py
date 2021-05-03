class NodParcurgere:
    # informatii despre un nod din arborele de parcurgere (nu din graful initial)
    def __init__(self, id, info, cost, parinte):
        self.id = id  # este indicele din vectorul de noduri
        self.info = info  # litera corespunzatoare
        self.parinte = parinte  # parintele din arborele de parcurgere
        # None pentru radacina
        self.g = cost  # acesta este costul

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
        sir += " cost:{})".format(self.g)
        return sir


class Graph:  # graful problemei
    def __init__(self, noduri, matriceAdiacenta, matricePonderi, start, scopuri):
        self.noduri = noduri
        self.matriceAdiacenta = matriceAdiacenta
        self.matricePonderi = matricePonderi
        self.nrNoduri = len(matriceAdiacenta)
        self.start = start  # informatia nodului de start
        self.scopuri = scopuri  # lista cu informatiile nodurilor scop

    def indiceNod(self, n):
        return self.noduri.index(n)

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []
        for i in range(self.nrNoduri):
            # n-au fost deja vizitati = nu au fost pusi in drum
            if self.matriceAdiacenta[nodCurent.id][i] == 1 and not nodCurent.contineInDrum(self.noduri[i]):
                # apelare constructor clasa NodParcurgere
                nodNou = NodParcurgere(i, self.noduri[i], nodCurent.g + self.matricePonderi[nodCurent.id][i], nodCurent)
                # index      info       cost   parinte
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

start = "a"
scopuri = ["f"]  # pot sa am cate prajituri vreau
gr = Graph(noduri, m, mp, start, scopuri)
# print(gr) # printeaza tot ce am dat mai sus

'''
      Uniform Cost Search 
      posibilitatea de a cere cate solutii vrem
      drum de cost minim 
      iau ca la BF doar ca in ordinea crescatoare a costurilor
      seamana cu Dijkstra
'''


def uniform_cost(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.noduri.index(gr.start), gr.start, 0, None)]

    while len(c) > 0:
        print("Coada actuala: " + str(c))
        input()  # dau enter
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):  # testez daca nodul curent este nod scop
            print("Solutie: ", end="")
            nodCurent.afisDrum()  # afisez drumul
            print("\n----------------\n")
            nrSolutiiCautate -= 1  # scad nr de solutii
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)  # generez lista de succesori
        print("Lista Succesori:", lSuccesori)
        # ----------------------------------In plus fata de BFS----------------------
        for s in lSuccesori:  # parcurg succesorii
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost coada
                # (notat cu g aici și în desenele de pe site)
                # daca elementul din coada are costul mai mare decat succesorul
                if c[i].g > s.g:  # g e costul total de la start pana la nodul curent
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)  # inserez pe pozitia i
                                # (cea pe care imi ramane ordinea)
            else:
                c.append(s)  # inserez la finalul cozii

    # 1,2,3,5,7,8  <- 8 unde ar trebui sa-l pozitionez pe 8
                        # cand il adaug in coada
                        # ca sa ramana ordonat dupa cost

uniform_cost(gr, nrSolutiiCautate=4)

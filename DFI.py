class NodParcurgere:
    # informatii despre un nod din arborele de parcurgere (nu din graful initial)
    def __init__(self, id, info, parinte):
        self.id = id  # este indicele din vectorul de noduri
        self.info = info  # litera corespunzatoare
        self.parinte = parinte  # parintele din arborele de parcurgere
        # None pentru radacina

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
        # afisare nod sub forma b(id = 1, drum=a->b)
        sir = ""
        sir += self.info + "("
        sir += "id = {}, ".format(self.id)
        sir += "drum="
        drum = self.obtineDrum()
        sir += ("->").join(drum)
        sir += ")"
        return sir


class Graph:  # graful problemei
    def __init__(self, noduri, matrice, start, scopuri):
        self.noduri = noduri
        self.matrice = matrice
        self.nrNoduri = len(matrice)
        self.start = start  # informatia nodului de start
        self.scopuri = scopuri  # lista cu informatiile nodurilor scop

    def indiceNod(self, n):
        return self.noduri.index(n)

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []
        for i in range(self.nrNoduri):
            # n-au fost deja vizitati = nu au fost pusi in drum
            if self.matrice[nodCurent.id][i] == 1 and not nodCurent.contineInDrum(self.noduri[i]):
                # apelare constructor clasa NodParcurgere
                nodNou = NodParcurgere(i, self.noduri[i], nodCurent)
                # index      info        parinte
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


noduri = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

m = [
    [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
]

start = "a"
scopuri = ["f", "j"]  # nodurile cu prajitura
gr = Graph(noduri, m, start, scopuri)
# print(gr) #printeaza tot ce am dat mai sus
'''
    DFI(iterativ) este BF + DF  
    merge tot pe nivele
    aplica DF pana la u adancime fixa Ad
    Adancimea creste de la 1 iterativ 
    Cand o atinge se intoarce ca si cum nu ar mai avea noduri
    Ca la BF solutii ordonate crescator dupa lungime
    Reconstruire arbore de parcugere la fiecare nivel
    Evita umplerea memoriei(BF)
    Nu ramane blocat pe o ramura foarte lunga(DF)

'''
# aceeasi functie aux_df doar ca are si adancimea
def dfi(nodCurent, adancime, nrSolutiiCautate):
    print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
    input()
    if adancime==1 and gr.testeaza_scop(nodCurent):
        print("Solutie: ", end="")
        nodCurent.afisDrum()
        print("\n----------------\n")
        input()
        nrSolutiiCautate-=1
        if nrSolutiiCautate==0:
            return nrSolutiiCautate
    if adancime>1:
        # numai daca adancimea e mai mare ca 1 generez succesorii
        lSuccesori=gr.genereazaSuccesori(nodCurent)
        print("Lista Succesori:", lSuccesori)
        for sc in lSuccesori:
            if nrSolutiiCautate!=0:
                nrSolutiiCautate=dfi(sc, adancime-1, nrSolutiiCautate)
    return nrSolutiiCautate

def depth_first_iterativ(gr, nrSolutiiCautate=1):
    for i in range(1,gr.nrNoduri+1):
        if nrSolutiiCautate==0:
            return
        print("**************\nAdancime maxima: ", i)
        nrSolutiiCautate=dfi(NodParcurgere(gr.noduri.index(gr.start), gr.start, None),i, nrSolutiiCautate)

depth_first_iterativ(gr, nrSolutiiCautate=4)
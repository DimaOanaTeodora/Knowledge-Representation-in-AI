import copy

class NodParcurgere:
    # informatii despre un nod din arborele de parcurgere (nu din graful initial)
    graf = None  # !!! static

    def __init__(self,info, parinte, cost, h):
        self.info = info  # toata asezarea celor n stive
        self.parinte = parinte  # parintele din arborele de parcurgere
                                # None pentru radacina
        self.g = cost  # consider costul 1 pentru o mutare
        self.h = h  # cat cred ca mai am = cost nod_c->scop
        self.f = self.g + self.h  # formula cost drum

    def obtineDrum(self):  # self=this
        # merge din tata in tata pana ajunge la radacina
        l = [self]
        nod = self
        while nod.parinte is not None:  # daca nu a ajuns la radacina
            l.insert(0, nod.parinte)  #-----aici scot nod.parinte.info---
                                    # adauga mereu pe prima pozitie
            nod = nod.parinte
        return l  # lista cu drumul

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        # afiseaza drumul
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisLung:
            print("Lungime: ", len(l))
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
        sir += str(self.info)
        return sir

    def __str__(self):# afisare mai fancy
            sir = ""
            maxInalt = max([len(stiva) for stiva in self.info])
            for inalt in range(maxInalt, 0, -1):
                for stiva in self.info:
                    if len(stiva) < inalt:
                        sir += "  "
                    else:
                        sir += stiva[inalt - 1] + " "
                sir += "\n"
            sir += "-" * (2 * len(self.info) - 1)
            return sir

    """
    def __str__(self): # afisare mai urata
            sir=""
            for stiva in self.info:
                sir+=(str(stiva))+"\n"
            sir+="--------------\n"
            return sir
    """


class Graph:
    def __init__(self, nume_fisier):
        #Constructorul deschide fisierul si citeste

        # -----------------functie locala folosita doar in costr--------------
        def obtineStive(sir):
            # intre stive se afla un caracter '\n'
            # strip() sterge spatiile de la inceput si de la sfarsit
            # folosit pentru fisiere cu o asezare mai aerisita
            stiveSiruri = sir.strip().split("\n")
            # daca e '#' am stiva vida
            listaStive = [sirStiva.strip().split() if sirStiva != "#" else [] for sirStiva in stiveSiruri]
            # rezultatul trebuie sa fie de forma: [["a"], ["c", "b"], ["d"]]
            return listaStive
        #   ------------sfarsit functie locala-----------------------------------

        f = open(nume_fisier, 'r')  # deschidere pentru citire

        continutFisier = f.read()  # citire tot continut
        # despart in 2 elemente
        siruriStari = continutFisier.split("stari_finale")
        # vreau sa obtin starea initiala
        self.start = obtineStive(siruriStari[0])  # stare initiala
        # lista cu starile
        self.scopuri = []
        # fiecare stare finala este separata printr-un ----
        # siruriStari[1] are starile finale
        siruriStariFinale = siruriStari[1].strip().split("---")
        for scop in siruriStariFinale:
            self.scopuri.append(obtineStive(scop))
        print("Stare Initiala:", self.start)
        print("Stari finale posibile:", self.scopuri)
        input()

    def testeaza_scop(self, nodCurent):
        return nodCurent.info in self.scopuri

    # lista cu toti succesorii
    # pe exemplu are 6 succesori deci lista va avea lungimea 6
    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        for i in range(len(nodCurent.info)):
            # iau fiecare stiva in parte
            # am nevoie sa compar cu aranjamentul initial
            copieStive = copy.deepcopy(nodCurent.info)
            # daca este stiva vida
            if len(copieStive[i]) == 0:
                continue
            # iau elementul din varful stivei
            bloc = copieStive[i].pop()
            # si acum incep sa pun blocul pe celelalte stive
            for j in range(len(nodCurent.info)):
                if i == j:  # sa nu fie stiva de pe care am luat
                    continue
                # acum pun blocul pe stiva j
                # copiestive fara bloc si se modifica mereu
                infoNodNou = copy.deepcopy(copieStive)
                infoNodNou[j].append(bloc)
                # ca sa nu sara inapoi verific daca a mai fost modelul
                if not nodCurent.contineInDrum(infoNodNou):
                    costMutare = 1  # toate arcele au costul 1
                    listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costMutare,
                                                        self.calculeaza_h(infoNodNou, tip_euristica)))

        return listaSuccesori

    # euristica banala
    # euristica sunt nr alea din patratele
    # nr <= costul pe orice drum de la nodul curent la cel scop
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            # euristica banală: daca nu e stare scop, returnez 1, altfel 0
            if infoNod in self.scopuri:
                return 0
            return 1
        elif tip_euristica == "euristica admisibila 1":
            if infoNod in self.scopuri:
                return 0
            else:
                minim = float('inf')  # h nr minim mutari
                # pentru fiecare stare scop
                for (s, scop) in self.scopuri:
                    nrMutari = 0  # h pt fiecare stare scop
                    # pentru fiecare stiva din infoNod (adica informatia nodului curent)
                    for Stiva, stiva in infoNod:
                        # pentru fiecare bloc din stiva din nodul curent
                        for Bloc, bloc in stiva:
                            try:
                                if bloc != scop[Stiva][Bloc]:
                                    # daca informatiile blocurilor de la
                                    # acelasi indice de stiva si acelasi nivel sunt diferite
                                    nrMutari += 1
                            except IndexError:
                                # daca nu exista indicele blocului in stiva din starea scop
                                # (stiva din starea curenta e mai mica decat cea din starea scop)
                                nrMutari += 1
                    if nrMutari < minim:
                        minim = nrMutari  # h
                return minim


    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir

def uniform_cost(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]

    while len(c) > 0:
        #print("Coada actuala: " + str(c))
        #input()  # dau enter
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):  # testez daca nodul curent este nod scop
            print("Solutie: ", end="")
            nodCurent.afisDrum(True, True)  #-----aici modific fata de UCS normal---
                                            # afisez drumul
            print("\n----------------\n")
            nrSolutiiCautate -= 1  # scad nr de solutii
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)  # generez lista de succesori
        #print("Lista Succesori:", lSuccesori)
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
gr=Graph("input.txt")
print("\n\n##################\nSolutii obtinute cu UCS:")
uniform_cost(gr, nrSolutiiCautate=5)


import copy

class NodParcurgere:
    # informatii despre un nod din arborele de parcurgere (nu din graful initial)
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
                                    # adauga mereu pe prima pozitie ca sa ajung de la starea initiala -> st finala
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

    def __str__(self):# afisare
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


    # euristica sunt nr alea din patratele
    # nr <= costul pe orice drum de la nodul curent la cel scop
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            # daca nu are scop returneaz 1 altfel 0
            if infoNod not in self.scopuri:
                return 1
            return 0
        elif tip_euristica == "euristica admisibila 1":
            # calculez cate blocuri nu sunt la locul lor fata de fiecare dintre starile scop,
            # si apoi iau minimul dintre aceste valori
            euristici = []
            for (iScop, scop) in enumerate(self.scopuri):
                # enumerate da tupluri de forma (indice, valoare) => (0,a),(1,b)
                h = 0
                for iStiva, stiva in enumerate(infoNod):
                    # vreau sa numar cate elemente nu sunt la locul lor
                    # iau fiecare bloc
                    for iBloc, bloc in enumerate(stiva):
                        try:
                            # exista în stiva scop indicele iElem
                            # dar pe acea pozitie nu se afla blocul din infoNod
                            if bloc != scop[iStiva][iBloc]:
                                h += 1
                        except IndexError:
                            # nici macar nu exista pozitia iBloc in stiva cu indicele iStiva din scop
                            h += 1
                euristici.append(h)
            return min(euristici)
        elif tip_euristica == "euristica admisibila 2":
            # calculez cate blocuri nu sunt la locul fata de fiecare dintre starile scop,
            # si apoi iau minimul dintre aceste valori
            euristici = []
            for (iScop, scop) in enumerate(self.scopuri):
                h = 0
                for iStiva, stiva in enumerate(infoNod):
                    for iBloc, bloc in enumerate(stiva):
                        try:
                            # exista în stiva scop indicele iElem dar pe acea pozitie nu se afla blocul din infoNod
                            if bloc != scop[iStiva][iBloc]:
                                h += 1
                            else:  # elem==scop[iStiva][iElem]:
                                if stiva[:iBloc] != scop[iStiva][:iBloc]:
                                    h += 2
                        except IndexError:
                            # nici macar nu exista pozitia iElem in stiva cu indicele iStiva din scop
                            h += 1
                euristici.append(h)
            return min(euristici)
        else:  # tip_euristica=="euristica neadmisibila"
            euristici = [] # calculez pentru fiecare bloc si o iau pe cea mai mica
            for (iScop, scop) in enumerate(self.scopuri):
                h = 0
                for iStiva, stiva in enumerate(infoNod):
                    for iElem, elem in enumerate(stiva):
                        try:
                            # exista în stiva scop indicele iElem dar pe acea pozitie nu se afla blocul din infoNod
                            if elem != scop[iStiva][iElem]:
                                h += 1
                            else:  # elem==scop[iStiva][iElem]:
                                if stiva[:iElem] != scop[iStiva][:iElem]:
                                    h += 2
                        except IndexError:
                            # nici macar nu exista pozitia iElem in stiva cu indicele iStiva din scop
                            h += 2
                euristici.append(h)
            return max(euristici)

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir

def a_star(gr, nrSolutiiCautate, tip_euristica):
    # open = coada noduri descoperite care nu au fost expandate
    # closed= noduri descoperite si expandate
    open = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica))]

    # face parte din optimizare
    closed = []  # n-am expandat pe nimeni la momentul asta
    while len(open) > 0:
        #print("Coada actuala: " + str(open))
        #input()
        nodCurent = open.pop(0)
        closed.append(nodCurent)  # a fost vizitat

        if gr.testeaza_scop(nodCurent):  # daca am ajuns la un nod scop
            print("Solutie: ")
            nodCurent.afisDrum(afisCost=True, afisLung=True) #---------aici se modifica
            #return #daca vreau sa-mi afiseze doar solutia optima
            print("\n----------------\n")
            nrSolutiiCautate -= 1  # scad nr de solutii
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent,tip_euristica=tip_euristica)
        #print("Lista Succesori:", lSuccesori)

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
                    if s.f >= elemc.f:  # nu mai vreau sa-l expandez ca e deja in open
                                        # unul cu o valoare mai mica
                        lSuccesori.remove(s)
                    else:
                        open.remove(elemc)  # il sterg doar din coada
                                            # altfel daca in open e unul cu valoarea mai mare il sterg de acolo
        if not gasitOpen:
            # fac acelasi lucru si pt closed
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
gr=Graph("input.txt")
print("\n\n##################\nSolutii obtinute cu A*:")
#a_star(gr, nrSolutiiCautate=7,tip_euristica="euristica banala")
a_star(gr, nrSolutiiCautate=7,tip_euristica="euristica admisibila 1") # ordonata dupa cost
#a_star(gr, nrSolutiiCautate=7,tip_euristica="euristica admisibila 2") # mai buna ca 1
#a_star(gr, nrSolutiiCautate=7,tip_euristica="euristica neadmisibila") # nu da in ordinea costurilor
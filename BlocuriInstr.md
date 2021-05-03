### NodParcurgere
 * info: asezarea stivelor intr-o stare [['a'],['b','c'][]]
 * parinte: None(radacina), altfel NodParcurgere
 * g: costul drumului de la SI la self(NodParcurgere)
      +1 cost pentru o mutare
 * h: (euristica) cat cred ca mai am de la self(NodParcurgere) la SF
 * f: g+h costul drumului (cu tot cu euristica-> ajuta de ordonarea in coada open din A*)

  Metode

  - obtineDrum(self) : lista cu toate NodParcugere de la SI-> SF
  - afisDrum(self): apeleaza obtineDrum(self) afisare drum + cost(g) + lungime(len(lista))
  - contineInDrum(self, infoNodNou) : verifica daca drumul de la SI -> self contine infoNodNou
  - __str__(self): afisarea unui NodParcurgere

### Graph
 * start: [['a'],['b','c'][]]
 * scopuri: [[['a'],['b','c'][]], [['a'],['b','c'][]]]

  Metode

  - __init__(self, nume_fisier): citeste si parseaza fisierul
    - obtineStive(sir) in __init__: parseaza sir si obtine stive => lista de stive = info unui NodParcurgere [['a'],['b','c'][]]
  - testeaza_scop(self, nodCurent): vede daca nodCurent.info este in self.scopuri
  - genereazaSuccesori(self, nodCurent, tip_euristica): retruneaza lista de Succesori
    - listaSuccesori = lista de NodParcurgere
    - primeste un nod curent si trebuie sa-i genereze succesorii
    - iau pe rand fiecare varf din fiecare stiva a nodCurent si-l mut pe toate celelalte generand toate posibilitatile lui de asezare
    - modific mereu o copie a lui nodCurent
    - i= numarul stivei din stare de pe care IAU blocul (aici: 0,1,2)
    - j= numarul stivei din stare pe care PUN blocul (aici:0,1,2)
    - i != j
    - verific sa nu mai fi generat starea respectiva
  -  calculeaza_h(self, infoNod, tip_euristica): returneaza euristica pentru un nod
      -  e calculata pentru fiecare NodParcurgere adaugat in lista de succesori
      -  euristica banala: 1 (daca e scop || nr minim de mutari ca sa ajung in starea finala), 0 (daca nu e nod scop)
      -  euristica admisibila 1: numar cate blocuri nu sunt la locul lor fata de fiecare stare scop, iar pentru fiecare nod iau numarul cel mai mic specific fiecarui bloc care nu e la locul lui fata de SF
      -  euristica admisibila 2:
  - __repr__(self): afisarea unui graf sub forma de cheie-valoare

### a_star(gr, nrSolutiiCautate, tip_euristica) ->varianta optimizata
 - open: noduri descoperite care nu au fost expandate,
 - closed: noduri descoperite si expandate
 - inserare succesori in open (coada din care scot) in functie de valorile lui f, iar daca f-urile sunt egale descrescator dupa g
 - Optimizari:
   - elimin din lista de succesori nodurile cu cost mare care apar de mai multe ori
   - adica: iau fiecare succesor noi generat si verifica daca a mai fost in open sau in closed, si il sterg de unde il gasesc cu o valoarea f mai mare ca cea acutala


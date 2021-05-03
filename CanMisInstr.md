### NodParcurgere
 * gr (static): prin el accesez in NodParcurgere campuri din Graph
 * info: tuplu de forma (canibali, misionari, mal stang/drept)
 * parinte: None(radacina), altfel NodParcurgere
 * g: costul drumului de la SI la self(NodParcurgere)
      +2 mutare canibal
      +1 mutare misionar
 * h: (euristica) cat cred ca mai am de la self(NodParcurgere) la SF
 * f: g+h costul drumului (cu tot cu euristica-> ajuta de ordonarea in coada open din A*)

  Metode

  - obtineDrum(self) : lista cu toate NodParcugere de la SI-> SF
  - afisDrum(self): apeleaza obtineDrum(self) afisare drum + cost(g) + lungime(len(lista))
    - obtine prin apelul lui gr (camp static in NodParcurgere) malul de la care se deplaseaza stang/drept
  - contineInDrum(self, infoNodNou) : verifica daca drumul de la SI -> self contine infoNodNou
  - __str__(self): afisarea unui NodParcurgere sub forma de 2 maluri si o barca

### Graph
 * N (static): nr canibali/misionari
 * M (static): nr locuri in barca
 * malInitial (static): stang/drept
 * malFinal (static): stang/drept
 * start: (canib, mis, mal)
 * scopuri: [(0,0,0)] aici e una singura, la alte probleme pot aparea mai multe

  Metode

  - __init__(self, nume_fisier): citeste, parseaza fisierul, initializeaza campurile
  - testeaza_scop(self, nodCurent): vede daca nodCurent.info este in self.scopuri
  - genereazaSuccesori(self, nodCurent, tip_euristica): retruneaza lista de Succesori
    - test_conditie(mis, can): retruneaza true daca canibalii nu mananca misionarii
    - listaSuccesori = lista de NodParcurgere
    - primeste un nod curent si trebuie sa-i genereze succesorii
    - calculez numarul de canibali si misionari pentru fiecare mal (ceilalalt fiind complementar la N)
    - calculez nr max si min de misionari si canibali intr-o barca
    - dupa testez sa nu se manance intre ei
    - verific sa nu mai fi generat starea respectiva
  -  calculeaza_h(self, infoNod, tip_euristica): returneaza euristica pentru un nod
      -  e calculata pentru fiecare NodParcurgere adaugat in lista de succesori
      -  euristica banala: 1 (daca e scop || nr minim de mutari ca sa ajung in starea finala), 0 (daca nu e nod scop)
      -  altfel: calculez cati oameni mai am de mutat si impart la nr de locuri in barc
  - __repr__(self): afisarea unui graf sub forma de cheie-valoare

### a_star(gr, nrSolutiiCautate, tip_euristica) ->varianta neoptimizata




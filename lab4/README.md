Pentru a mari precizia calculului de similaritate a doua texte am preprocesat
descrierile produselor cu ajutorul unui model. Fiecare descriere a fost tokenizata si au
fost eliminate cuvintele ce nu cantaresc in mod real la comparare (numere, stopwords).
Ulterior am vectorizat toate descrierile produselor si am construit matricea de similaritate.

Am eliminat produsele duplicate pentru a putea compara numai obiecte diferite.
Dupa rularea codului, cele doua produce cu similaritate maxima au fost
"Tesco Age 18 Balloons 6 Pack" (cu id 05054402525956) si "Tesco Age 21 Balloons 6 Pack"
(cu id 05054402525963). Acestea mentioneaza detalii despre baloane dar vorbesc si despre
factorii de risc intampinati in timpul utilizarii. 
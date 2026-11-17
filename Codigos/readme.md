a) Entropía de la fuente. Todas las palabras del código C = {11, 01, 00, 10} tienen 2 bits, así que el mensaje 1100111001111001 se separa en pares (11 00 11 10 01 11 10 01) y cada par se reemplaza por su símbolo. Tomo A, B, C y D en el orden en que aparece el código. El enunciado no da la asignación, pero otra asignación cambiaría las letras y no la entropía, porque esta depende solo de cuántas veces aparece cada palabra. Resulta ACADBADB, con 8 símbolos: A aparece 3 veces, B 2, C 1 y D 2.

Las probabilidades son frecuencias relativas: P(A) = 0,375, P(B) = 0,25, P(C) = 0,125 y P(D) = 0,25. Cada símbolo aporta una cantidad de información log2(1/P) (más cuanto menos probable es), y la entropía es su promedio ponderado: H₂(S) = Σ P·log2(1/P) = 1,9056 bits/símbolo. Es el mínimo de bits por símbolo que necesita cualquier código binario decodificable para esta fuente. El máximo posible con 4 símbolos sería log2(4) = 2. Se trata de una estimación porque las probabilidades salen de un mensaje de solo 8 símbolos.

b) Código óptimo para la extensión de orden 3. La extensión S³ tiene 4³ = 64 símbolos, uno por cada combinación de 3 símbolos de la fuente (AAA, AAB, …). Se supone una fuente sin memoria, de modo que la probabilidad de cada bloque es el producto de las de sus tres símbolos (por ejemplo, P(AAA) = 0,375³) y las 64 suman 1. Sobre esas 64 probabilidades se aplicó Huffman, que da un código instantáneo y de mínima longitud media:

Se ordenan los símbolos por probabilidad.
Se unen los dos menos probables en un nodo cuya probabilidad es la suma.
Se repite hasta quedar un solo nodo, la raíz. En cada nodo se asigna 0 a una rama y 1 a la otra.
La palabra de cada símbolo es la secuencia de 0 y 1 desde la raíz hasta él.

El resultado tiene palabras de 4 a 8 bits: cortas para los bloques más probables, como AAA, y largas para los menos probables. Con empates puede haber más de un código óptimo, todos con la misma longitud media.

c) Rendimiento y redundancia. La longitud media es L = Σ P·longitud, el rendimiento es η = H/L y la redundancia es R = 1 − η. Cada código se compara con la entropía de su propia fuente:

Fuente: H(S) = 1,9056 y L = 2, por lo que η = 0,9528 y R = 0,0472.
Extensión: H(S³) = 3·H(S) = 5,7169 y L₃ = 5,7578 bits por bloque, por lo que η = 0,9929 y R = 0,0071.

Los valores deben ser coherentes entre sí: L nunca puede ser menor que H, y η nunca puede superar 1.

d) Comparación. Para comparar, las dos longitudes tienen que estar en la misma unidad: o ambas por bloque, o ambas por símbolo de la fuente.

	Fuente (n = 1)	Extensión (n = 3)
Entropía	H(S) = 1,9056	H(S³) = 5,7169 por bloque
Longitud media	L = 2	L₃ = 5,7578 por bloque
Longitud por símbolo de la fuente	2,0000	L₃/3 = 1,9193
Diferencia con H(S)	0,0944	0,0136
η y R	0,9528 y 0,0472	0,9929 y 0,0071

El Primer Teorema de Shannon establece, para un código compacto, H(S^n) ≤ L_n < H(S^n) + 1. Como H(S^n) = n·H(S), al dividir por n queda H(S) ≤ L_n/n < H(S) + 1/n. Se cumple en ambos códigos: para n = 1, 1,9056 ≤ 2 < 2,9056, y para n = 3, 1,9056 ≤ 1,9193 < 2,2389.

Conclusiones
La longitud media nunca baja de la entropía: la entropía es la cota inferior del Primer Teorema. La diferencia entre ambas es la redundancia, y los dos códigos están por encima de H y dentro de la cota superior.
Al codificar bloques de 3, la longitud por símbolo baja de 2 a 1,9193 bits y queda a solo 0,0136 de la entropía, frente a 0,0944 antes. El rendimiento sube de 95,28 % a 99,29 % y la redundancia baja de 4,72 % a 0,71 %. La causa es que cada palabra debe tener un número entero de bits aunque log2(1/P) no lo sea. Con bloques, ese redondeo se reparte entre 3 símbolos, y la cota superior H + 1/n se estrecha al crecer n.
El código dado de 2 bits fijos ya es compacto para esta fuente: Huffman sobre la misma distribución también da L = 2. Su rendimiento no llega a 1 porque las probabilidades no son todas potencias de 1/2 (0,375, por ejemplo), y la única forma de mejorarlo es agrupar símbolos.
Agrupar tiene un costo. La tabla pasa de 4 a 64 palabras y crece como 4ⁿ (con n = 5 serían 1024). Las palabras son de longitud variable y hay que acumular 3 símbolos antes de codificar. Además, la mejora por seguir aumentando n es cada vez menor: con n = 3 ya se alcanza el 99,29 %.
Las probabilidades salen de un mensaje de solo 8 símbolos (C aparece una vez), por lo que son poco confiables.
Ejercicio 2
Cómo se resolvió

a) Distribución de entrada óptima. La información mutua I(A,B) depende de cómo la fuente reparta sus entradas, P(0) = p y P(1) = 1 − p. La capacidad C es el máximo de I(A,B) sobre todas las distribuciones, y la distribución óptima es el par (p, 1 − p) con el que se alcanza ese máximo. El canal no es sin ruido, porque la columna C tiene dos elementos no nulos, ni determinante, porque la fila 1 tiene tres. Por eso no hay una fórmula directa y se busca numéricamente:

Se calcula I(A,B) para p = 0,1; 0,2; …; 0,9.
Se toma el mejor p y se repite alrededor de él con un paso 10 veces menor.
Se hacen 6 rondas, hasta un paso de 10⁻⁶.

Resulta P(0) = 0,5643, P(1) = 0,4357 y C = 0,6182 bits/símbolo.

b) Equivocación, pérdida e información mutua. Con esa distribución:

Los simultáneos son P(a,b) = P(a)·P(b/a).
La probabilidad de salida es P(b) = Σ P(a,b) = (0,1743; 0,1743; 0,6514) para A, B y C.
La posteriori es P(a/b) = P(a,b)/P(b). Para A y B vale P(1/A) = P(1/B) = 1. Para C vale P(0/C) = 0,8662 y P(1/C) = 0,1338.

Con esos valores se calculan las tres medidas por definición:

Equivocación: H(A/B) = Σ P(a,b)·log2(1/P(a/b)) = 0,3698 bits.
Pérdida: H(B/A) = Σ P(a,b)·log2(1/P(b/a)) = 0,6631 bits.
Información mutua: I(A,B) = Σ P(a,b)·log2[P(a,b)/(P(a)·P(b))] = 0,6182 bits.

Como control: H(A) = 0,9880, de modo que H(A) − H(A/B) = 0,6182, y H(B) = 1,2813, de modo que H(B) − H(B/A) = 0,6182.

Las tres son cantidades de información en bits, no probabilidades ni porcentajes:

H(A/B) es la incertidumbre promedio que queda sobre la entrada después de ver la salida. Solo hay duda cuando se recibe C (probabilidad 0,6514), porque la entrada pudo ser 0 (86,6 %) o 1 (13,4 %). Recibir A o B identifica con certeza un 1.
H(B/A) es la incertidumbre promedio sobre la salida conociendo la entrada. Si se envía 0, siempre sale C, sin incertidumbre. Si se envía 1, sale A, B o C con 0,4, 0,4 y 0,2, lo que da H = 1,5219 bits, ponderado por P(1) = 0,4357.
I(A,B) es la información sobre la entrada que atraviesa el canal. Coincide con la capacidad porque se usó la distribución óptima.

c) Detección y corrección de errores. Los 24 bits son 3 bytes, ordenados en una matriz de 3 filas × 8 columnas con paridad par:

fila 1:  00001001   paridad longitudinal (el último bit es la paridad cruzada)
fila 2:  11111110   7 bits del carácter + paridad vertical
fila 3:  11010111   7 bits del carácter + paridad vertical

Se verifica que cada fila y cada columna tengan una cantidad par de unos:

Filas: la fila 1 tiene 2 unos (par), la fila 2 tiene 7 (impar) y la fila 3 tiene 6 (par).
Columnas: todas son pares salvo la columna 3, que tiene un solo uno (impar).

Exactamente una fila y una columna fallan, así que hay un único error simple en su intersección: fila 2, columna 3. Es un bit de datos, no de paridad. Se lo invierte (1 → 0) y la fila 2 queda 11011110. La paridad cruzada es consistente: los 7 primeros bits de la fila 1 (0000100) tienen un solo 1, por lo que el bit de paridad cruzada debe valer 1, y vale 1.

Para recuperar el texto se descartan la fila 1 y el bit de paridad de cada fila. Los 7 bits restantes dan 1101111 = 111, que es “o”, y 1101011 = 107, que es “k”. El mensaje corregido es 000010011101111011010111, es decir, “ok”. Si hubiera más de un error, la paridad no permitiría ubicarlo y solo se podría detectar.

d) ¿Pudo transmitirse por el canal? La regla de decisión de máxima posibilidad elige, para cada salida, la entrada con mayor P(b/a). Resulta A → 1, B → 1 y C → 0. Por lo tanto, recibir A o B da certeza de que se envió un 1. Un 0 enviado siempre sale como C y se decide como 0, así que un 0 nunca puede llegar como 1.

Asumiendo que el mensaje enviado es el corregido, el bit del error era un 0 que se recibió como 1. Eso es imposible con este canal, de modo que el mensaje recibido no pudo haberse transmitido por el canal. En la dirección contraria sí sería posible: un 1 puede salir como C, con probabilidad 0,2, y decidirse como 0.

Conclusiones
Con la distribución óptima el canal transporta como máximo 0,6182 bits por símbolo. De los 0,9880 bits que entran, atraviesan 0,6182 (62,6 %) y se pierden 0,3698 (37,4 %) por ruido. Una entrada binaria podría transportar como máximo 1 bit por símbolo.
La calidad del canal se juzga comparando I(A,B) con H(A) o con ese máximo de 1 bit. No sirve compararla con la pérdida H(B/A), que mide la variabilidad de la salida y no la información perdida sobre la entrada. Con este criterio el canal es regular: deja pasar casi dos tercios de la información, no toda.
El ruido está concentrado en la salida C. A y B resuelven por completo la incertidumbre sobre la entrada, y C la deja abierta.
La distribución óptima usa más el 0 (56,43 %) porque es la entrada confiable: siempre llega como C. Con 0,5 y 0,5, I vale 0,6100, que es menos que la capacidad. La información mutua solo es igual a la capacidad cuando se usa la distribución óptima.
La paridad vertical, longitudinal y cruzada permitió ubicar y corregir el único error (fila 2, columna 3) y recuperar “ok”. Con dos o más errores solo habría detección.
El error corregido es un 0 recibido como 1, que este canal no puede producir. Por lo tanto, el mensaje recibido no pudo transmitirse por él.

porque la extension de orden n esta acotada por la entropia de la funete??

1. Por qué L_N/N está acotada por la entropía

Una extensión de orden N toma bloques de N símbolos de la fuente como si fueran un símbolo nuevo. Para una fuente sin memoria, la probabilidad de un bloque es el producto de las de sus símbolos. Eso implica que H(S^N) = N · H(S): cada símbolo del bloque aporta su propia información.

Cota inferior. Para cualquier código unívocamente decodificable vale L ≥ H, y esto se aplica también al código de S^N:

L_N ≥ H(S^N) = N·H(S), y dividiendo por N queda L_N/N ≥ H(S).

Es un límite físico: no se puede comprimir por debajo de la información que la fuente realmente produce.

Cota superior. Dado que las longitudes deben ser enteras, tomás para cada bloque l_i = ⌈log_r(1/p_i)⌉. Eso cumple Kraft, así que existe un código instantáneo con esas longitudes. Como ⌈x⌉ < x + 1, resulta L_N < H(S^N) + 1. El código compacto (óptimo) es como mucho tan largo como ese:

N·H(S) ≤ L_N < N·H(S) + 1

Dividiendo por N:

H(S) ≤ L_N/N < H(S) + 1/N

Esa es la desigualdad del Primer Teorema de Shannon.


Cómo juzgar la calidad de un canal
Con H(A/B) y H(B/A) chicas, la información mutua es alta, así que el canal es bueno.
Si H(A/B) = 0 (sin ruido), I = H(A): llega toda la información de la entrada.
Si H(B/A) = 0 (determinante), I = H(B).
Si ambas valen 0, I = H(A) = H(B) y el canal es perfecto.
Si A y B son independientes, I = 0 y el canal es inútil.
En el caso de canales en serie, I(A;C) ≤ I(A;B): cada etapa nunca suma información.
La capacidad C es la mejor medida de calidad porque no depende de qué se transmita. El Segundo Teorema de Shannon dice que se puede transmitir con error arbitrariamente chico a cualquier tasa menor que C.


¿Puede transmitirse por el canal?

Los A, B y C no aparecen en el mensaje. El mensaje recibido está escrito en 0 y 1 porque ya pasó por la regla de decisión, que convierte cada salida del canal en un bit. Entonces hay que armar esa tabla primero y después comparar bit a bit “lo que se envió” con “lo que se decidió”.

Paso 1: regla de máxima posibilidad

Para cada salida, elegís la entrada con mayor P(salida/entrada):

Salida	P(·/0)	P(·/1)	Se decide
A	0.0	0.4	1
B	0.0	0.4	1
C	1.0	0.2	0
Paso 2: qué puede hacer el canal con cada bit enviado
Se envía 0: siempre sale C (probabilidad 1), y C se decide como 0. Llega 0 sí o sí.
Se envía 1: puede salir A o B (se decide 1, correcto) o C con prob. 0.2 (se decide 0, error).

Conclusión: el único error posible es 1 que llega como 0. Un 0 nunca puede llegar como 1.

Paso 3: qué se envió realmente

Armás la matriz de 3 bytes (fila 0 = paridad longitudinal, luego una fila por letra, último bit de cada fila = paridad):

00001001   paridad par OK
11111110   paridad MAL (7 unos)
11010111   paridad OK

Falla la fila 1, y la columna 2 también falla. Ahí está el bit erróneo. Corregido, la fila 1 queda 11010110 → ‘o’, y se obtiene “ok”. Ese es el mensaje que se envió, porque es el único válido (ASCII + paridad) a un solo error de distancia.

Paso 4: comparar enviado vs. recibido

El bit corregido (fila 1, columna 2) era un 0 enviado y se recibió como 1. Eso exige que el canal convierta 0 en 1, y el Paso 2 dice que es imposible.

El mensaje recibido no pudo haberse transmitido por este canal.

Pasos generales para este tipo de ejercicio

Armá la regla de decisión. Para cada salida, elegí la entrada con mayor P(salida/entrada). Resultado: una tabla salida → bit decidido.
Deducí qué errores permite el canal. Para cada entrada, mirá qué salidas puede dar con probabilidad mayor que 0 y qué bit se decide en cada una. Hay un tipo de error posible si alguna entrada puede terminar decidida como la otra.
Esto da una lista de “transformaciones permitidas” (por ejemplo, solo 0→1).
Armá la matriz del mensaje recibido. Un byte por fila: la primera es la fila de paridad longitudinal y las siguientes son los caracteres con su bit de paridad.
Detectá y corregí. Buscá filas y columnas con paridad incorrecta.
Una fila y una columna fallan: el error está en su cruce, así que lo invertís.
Si no hay errores, el mensaje enviado es el recibido.
Si hay más, no se puede corregir. Hay que ver el contexto (en ese caso, se decide según el enunciado).
Compará enviado contra recibido. Mirá qué cambió en cada bit modificado (por ejemplo, 1→0).
Concluí. Si ese cambio está entre las transformaciones permitidas del paso 2, el mensaje pudo haberse transmitido. Si no, es imposible.
Casos que conviene tener en cuenta
Sin errores detectados: el mensaje enviado es igual al recibido y siempre es posible.
El error cae en un bit de paridad: igual se corrige, y la comparación también se hace sobre ese bit.
Varios errores: la comparación se hace bit por bit sobre cada uno, y alcanza con que uno solo sea una transformación imposible para concluir que no se pudo.
Canal sin cero en ninguna dirección: si ambas transformaciones son posibles, cualquier mensaje puede pasar y la respuesta es que sí.
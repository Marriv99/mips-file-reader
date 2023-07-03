# **MIPS FILE READER**

## Descrizione
Progetto realizzato con  l'obiettivo di generare le matrici A e Aeq ed i vettori b, beq, c, lb ed ub del seguente problema MILP:

min c^T x
Ax <= b
Aeqx = beq
lb <= x <= ub

Popola il problema in tre differenti modi:
1. Per colonna
2. Per riga
3. Per coefficienti diversi da zero

Chiama CPLEX per la sua soluzione.

## Estrazione dei dati
Per generare le matrici e i vettori del problema MILP a partire dal file MPS letto, ho utilizzato i metodi forniti dalla libreria CPLEX in Python:

- `prob.linear_constraints.get_rows()`: Restituisce le righe delle matrici A e Aeq in formato di lista di tuple, dove ogni tupla contiene gli indici delle colonne non nulle e i relativi valori.
- `prob.linear_constraints.get_rhs()`: Restituisce il vettore b.
- `prob.quadratic_constraints.get_rows()`: Restituisce le righe della matrice Aeq in formato di lista di tuple.
- `prob.quadratic_constraints.get_rhs()`: Restituisce il vettore beq.
- `prob.objective.get_linear()`: Restituisce il vettore c.
- `prob.variables.get_lower_bounds()`: Restituisce il vettore lb.
- `prob.variables.get_upper_bounds()`: Restituisce il vettore ub.

## Popolamento per colonna
Per ogni colonna, vengono creati tre elenchi vuoti per:
- Variabili coinvolte
- Coefficienti di ogni variabile nel vincolo
- Limiti inferiore e superiore delle variabili coinvolte e il tipo di variabile.

Per i vincoli di tipo "<=", vengono popolati gli elenchi delle variabili, dei coefficienti e dei limiti inferiori e superiori.

Per i vincoli di tipo "==", vengono popolati gli elenchi delle variabili, dei coefficienti e dei limiti inferiori e superiori.

Viene aggiunta una variabile al problema mediante il metodo `my_prob.variables.add()`, specificando il coefficiente dell'obiettivo, i limiti inferiore e superiore della variabile, la tipologia della variabile e il nome della variabile.

Viene aggiunto un vincolo lineare di tipo "<=" al problema mediante il metodo `my_prob.linear_constraints.add()`, specificando la coppia di valori (variabili e coefficienti) per la parte lineare, il segno di disuguaglianza, il lato destro e il nome del vincolo.

Viene aggiunto un vincolo quadratico di tipo "==" al problema mediante il metodo `my_prob.quadratic_constraints.add()`, specificando la coppia di valori (variabili e coefficienti) per la parte lineare, la lista vuota per la parte quadratica, il segno di uguaglianza, il lato destro e il nome del vincolo.

## Popolamento per riga
Si verifica se le dimensioni delle matrici di input corrispondono ai vincoli del problema.

Si inizializzano tre liste vuote per contenere:
- Indici delle righe
- Indici delle colonne
- Valori della matrice A del problema di programmazione lineare.

Si determina il numero di colonne e righe nel problema.

Si popolano i vincoli lineari di tipo "<=" o ">=" in base al valore di `my_sense`.

Si aggiungono i vincoli lineari di tipo "==" al problema.

Si popolano i vincoli quadratici di tipo "==".

Si aggiungono le variabili del problema, distinguendo tra variabili continue e variabili binarie/interne.

## Popolamento per coefficienti diversi da zero
Si controlla che `my_beq` non sia vuota.

Si controlla che la lunghezza di `my_beq` sia maggiore o uguale a `numrows`.

Per ogni riga, se `my_sense[i]` è 'E' (cioè l'uguaglianza), si aggiunge il vincolo quadratico di tipo '==' al problema lineare, utilizzando `my_Aeq[i]` come gli indici e `my_beq[i]` come la soluzione. Se invece `my_sense[i]` è '<=' o '>=', si aggiunge il vincolo lineare corrispondente usando `my_A[i]` come gli indici e `my_b[i]` come la soluzione.

Per ogni colonna, se il coefficiente `my_c[j]` è diverso da 0.0, si aggiunge la variabile di decisione, utilizzando `my_c[j]` come il coefficiente obiettivo, `my_colnames[j]` come il nome della variabile e le rispettive limitazioni superiori e inferiori (se definite).

## Output
Questo script in Python risolve un problema di ottimizzazione lineare CPLEX e restituisce una serie di informazioni sull'output della soluzione.

In particolare, questa funzione estrae diverse informazioni dal problema di ottimizzazione, come i limiti delle variabili, i vincoli, la funzione obiettivo e le informazioni sul tipo di variabile.

Risolve il problema usando il metodo `solve()` fornito da CPLEX.

Infine, la funzione stampa le informazioni sulla soluzione, inclusi lo stato della soluzione, il valore della funzione obiettivo e i valori delle variabili ottimali.

Inoltre, la funzione stampa le variabili slack e i valori delle variabili di decisione.

import cplex
from cplex.exceptions import CplexError
import os


def populate_by_row(my_prob, my_A, my_Aeq, my_c, my_lb, my_ub, my_ctype, my_colnames, my_b, my_beq, my_sense,
                    my_rownames):
    my_prob.objective.set_sense(my_prob.objective.sense.maximize)

    my_prob.variables.add(obj=my_c, lb=my_lb, ub=my_ub, types=my_ctype, names=my_colnames)

    # Crea un dizionario per rappresentare la matrice dei coefficienti del problema
    coeffs = {}
    for i, row_coeffs in enumerate(my_A):
        row = {my_colnames[j]: row_coeffs[j] for j in range(len(row_coeffs))}
        coeffs[i] = row
    for i, row_coeffs in enumerate(my_Aeq):
        row = {my_colnames[j]: row_coeffs[j] for j in range(len(row_coeffs))}
        coeffs[i + len(my_A)] = row

    # Popola il problema per riga utilizzando il dizionario dei coefficienti
    rows = []
    for i in range(my_prob.linear_constraints.get_num()):
        row_vars = [var for var in coeffs[i]]
        row_coeffs = [coeffs[i][var] for var in row_vars]
        rows.append([row_vars, row_coeffs])

    # Aggiungi i vincoli al problema
    my_prob.linear_constraints.add(lin_expr=rows, rhs=my_b + my_beq, senses=my_sense, names=my_rownames)


def populate_by_column(my_prob, my_A, my_Aeq, my_c, my_lb, my_ub, my_ctype, my_colnames, my_b, my_beq, my_sense,
                       my_rownames, my_num_cols):
    prob.objective.set_sense(prob.objective.sense.minimize)

    my_prob.variables.add(obj=my_c, lb=my_lb, ub=my_ub, types=my_ctype, names=my_colnames)

    # Inizializza le liste per tenere traccia delle colonne
    cols = [[] for i in range(len(my_colnames))]

    # Popola le colonne dei vincoli di disuguaglianza
    for i in range(len(my_A)):
        row_coeffs = my_A[i]
        for j in range(len(row_coeffs)):
            var = my_colnames[j]
            coeff = row_coeffs[j]
            cols[j].append((i, coeff))

    # Popola le colonne dei vincoli di uguaglianza
    for i in range(len(my_Aeq)):
        row_coeffs = my_Aeq[i]
        for j in range(len(row_coeffs)):
            var = my_colnames[j]
            coeff = row_coeffs[j]
            cols[j].append((len(my_A) + i, coeff))

    # Aggiungi i vincoli al problema per colonna
    for i in range(len(my_rownames)):
        col_indices = [j for j in range(len(cols)) if cols[j]]
        col_coeffs = [cols[j][0][1] if cols[j] else 0 for j in col_indices]
        col_rows = [cols[j][0][0] if cols[j] else 0 for j in col_indices]
        my_prob.linear_constraints.add(lin_expr=[[col_indices, col_coeffs]], rhs=[my_b[col_rows[0]]],
                                       senses=[my_sense[col_rows[0]]], names=[my_rownames[i]])
        for j in col_indices:
            del cols[j][0]


def populate_by_nonzero(my_prob, my_A, my_Aeq, my_c, my_lb, my_ub, my_ctype, my_colnames, my_b, my_beq, my_sense,
                        my_rownames):
    my_prob.objective.set_sense(my_prob.objective.sense.maximize)

    my_prob.variables.add(obj=my_c, lb=my_lb, ub=my_ub, types=my_ctype, names=my_colnames)

    # Crea un dizionario per rappresentare la matrice dei coefficienti diversi da 0 del problema
    coeffs = {}
    for i, row_coeffs in enumerate(my_A):
        row = {my_colnames[j]: row_coeffs[j] for j in range(len(row_coeffs)) if row_coeffs[j] != 0}
        coeffs[i] = row
    for i, row_coeffs in enumerate(my_Aeq):
        row = {my_colnames[j]: row_coeffs[j] for j in range(len(row_coeffs)) if row_coeffs[j] != 0}
        coeffs[i + len(my_A)] = row

    # Popola il problema utilizzando il dizionario dei coefficienti
    rows = []
    for i in range(my_prob.linear_constraints.get_num()):
        row_vars = [var for var in coeffs[i]]
        row_coeffs = [coeffs[i][var] for var in row_vars]
        rows.append([row_vars, row_coeffs])

    # Aggiungi i vincoli al problema
    my_prob.linear_constraints.add(lin_expr=rows, rhs=my_b + my_beq, senses=my_sense, names=my_rownames)


def resolution_mps(pop_method, my_prob):
    try:
        # Estrae rhs, il vettore beq e b
        beq = my_prob.quadratic_constraints.get_rhs()
        b = my_prob.linear_constraints.get_rhs()
        c = my_prob.objective.get_linear()

        # Estrae i limiti inferiori e superiori delle variabili
        lb = my_prob.variables.get_lower_bounds()
        ub = my_prob.variables.get_upper_bounds()

        # Estrae le informazioni di colonne e righe
        numcols = my_prob.variables.get_num()
        colnames = my_prob.variables.get_names()
        numrows = my_prob.linear_constraints.get_num()
        rownames = my_prob.linear_constraints.get_names()

        # Estrae ctype e sense
        ctype = my_prob.variables.get_types()
        sense = my_prob.linear_constraints.get_senses()

        rows = []
        cols = []
        vals = []
        A = []
        Aeq = []

        for i in range(numrows):
            row = my_prob.linear_constraints.get_rows(i)
            for j in range(len(row.ind)):
                rows.append(i)
                cols.append(row.ind[j])
                vals.append(row.val[j])
            if sense[i] == 'E':
                Aeq.append(vals.copy())
            else:
                A.append(vals.copy())
            vals.clear()

        if pop_method == "r":
            populate_by_row(my_prob, A, Aeq, c, lb, ub, ctype, colnames, b, beq, sense, rownames)
        elif pop_method == "c":
            populate_by_column(my_prob, A, Aeq, c, lb, ub, ctype, colnames, b, beq, sense, rownames, numcols)
        elif pop_method == "n":
            populate_by_nonzero(my_prob, A, Aeq, c, lb, ub, ctype, colnames, b, beq, sense, rownames)
        else:
            raise ValueError('pop_method must be one of "r", "c" or "n"')

        my_prob.solve()
    except CplexError as exc:
        print(exc)
        return

    print()
    # solution.get_status() returns an integer code
    print("Solution status = ", my_prob.solution.get_status(), ":", end=' ')
    # the following line prints the corresponding string
    print(my_prob.solution.status[my_prob.solution.get_status()])
    print("Solution value  = ", my_prob.solution.get_objective_value())

    slack = my_prob.solution.get_linear_slacks()
    x = my_prob.solution.get_values()

    for j in range(numrows):
        print("Row %d:  Slack = %10f" % (j, slack[j]))
    for j in range(numcols):
        print("Column %d:  Value = %10f" % (j, x[j]))


if __name__ == "__main__":
    prob = cplex.Cplex()

    mps_file = "C:/Users/mario/Downloads/File Mps/blend2.mps"
    if os.path.exists(mps_file):
        print("File exists!")
    else:
        print("File not found:", mps_file)

    prob.read(mps_file)

    print("      r          generate problem by row")
    resolution_mps("r", prob)
    print("      c          generate problem by column")
    # resolution_mps("c", prob)
    print("      n          generate problem by nonzero")
    # resolution_mps("n", prob)

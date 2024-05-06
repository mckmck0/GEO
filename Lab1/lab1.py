import docplex.mp.model as cplex
import re
import numpy as np
import time


# Wczytywanie danych z pliku
def read_data(file_path, n, m):

    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        data.extend([int(char) for char in line.strip().split() if char.isdigit()])

    matrix = np.array(data).reshape(n*m, n*m)

    blocks = []
    for i in range(0, n*m, m):
        for j in range(0, n*m, m):
            block = matrix[i:i+m, j:j+m]
            blocks.append(block)
    return blocks


# Rozwiązanie problemu za pomocą CPLEX
def solve_cplex(CM, n, m):
    cp = cplex.Model(name='Lab1')           # Inicjalizacja modelu
    x = cp.binary_var_matrix(range(1, n + 1), range(1, m + 1),
                             name=lambda ns: f'x_{ns[0]}_{ns[1]}')      # 2D macierz zmienych binarnych
    cp.minimize(1)    # Stała funkcja celu
    ########### Ograniczenia #############
    # Każdy samolot może wykonać tylko jeden manewr
    for i in range(1, n + 1):
        cp.add_constraint(cp.sum(x[i, j] for j in range(1, m + 1)) == 1)
    # Unikanie konfliktów zapisanych w CM
    for i in range(n):      # Iteracja po samolotach
        for j in range(m):      # Iteracja po manewrach dla samolotu i
            for k in range(i + 1, n):       # Iteracja po innych samolotach - tylko gorny trojkat macierzy
                if i != k:      # Unikamy porównania samolotu z samym sobą
                    for l in range(m):      # Iteracja po manewrach dla samolotu k
                        # Sprawdzenie, czy istnieje konflikt między manewrem j samolotu i oraz manewrem l samolotu k
                        block = CM[i * n + k]
                        if block[j][l] == 1:
                            # Dodanie ograniczenia do modelu
                            cp.add_constraint(x[i + 1, j + 1] + x[k + 1, l + 1] <= 1)

    # Rozwiązanie problemu
    solution = cp.solve()
    return solution, cp


if __name__ == '__main__':
    file = 'data/CM_n=20_m=7.txt'       # Plik wejsciowy
    n, m = (int(x) for x in re.findall(r"[nm]=(\d+)", file))
    print(f"n: {n}, m: {m}")
    CM = read_data(file, n, m)          # Wczytanie danych z pliku
    st = time.time()                    # Start timer
    solution, model = solve_cplex(CM, n, m)    # Rozwiązanie problemu
    et = time.time()                    # End timer
    elapsed_time = et - st              # Czas obliczeń

    if solution:                        # Wyświetlenie wyników
        print(f"Czas obliczeń: {round(elapsed_time, 2)}s.")
        print(solution.display())
    else:
        print("Nie znaleziono rozwiązania.")


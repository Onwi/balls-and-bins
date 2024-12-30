import sys
import random
import time
import math

def parse_input_file(file_path):  ## Lê o arquivo de entrada e extrai as informações.

    instances = []
    with open(file_path, 'r') as f:
        bins = int(f.readline()) # pega a quantidade de bins presente no arquivo
        balls = int(f.readline()) # pega a quantidade de balls presente no arquivo
        while True:
            line = f.readline()
            if not line:
                break
            nums = line.split(' ')
            instance = [int(nums[0]), int(nums[1])] # instancia [lowerBound, upperBound]
            instances.append(instance)
    
    return instances, bins, balls

def evaluate_solution(solution, instances): #Avaliamos a solução.
    best_value = 0

    for index, ball in enumerate(solution):
        if(ball > instances[index][1] or ball < instances[index][0]):
            return 0
        else:
            best_value += (ball*(ball + 1))/ 2

    return best_value 

def get_neighbor(solution, instances): # Gera uma nova solução.
    from_bin = random.randint(0, len(solution) - 1)
    to_bin = random.randint(0, len(solution) - 1)

    while solution[from_bin] == instances[from_bin][0]:
        from_bin = random.randint(0, len(solution) - 1)

    while solution[to_bin] == instances[to_bin][1]:
        to_bin = random.randint(0, len(solution) - 1)


    solution[from_bin] -= 5
    solution[to_bin] += 5

    return solution

def create_initial_solution(bins, balls, instances):
    initial_solution = [0] * bins
    for i in range(bins):
        initial_solution[i] = instances[i][0]
        balls -= instances[i][0]

    index = 0
    while balls > 0:
        max_add =  instances[index][1] - instances[index][0]
        if(max_add > balls):
            initial_solution[index] += balls
            balls -= balls
        else:
            initial_solution[index] += max_add
            balls -= max_add
        index += 1
    return initial_solution

def simulated_annealing(bins, balls, instances, seed, max_iterations, max_time):
    random.seed(seed)
    start_time = time.time()

    current_solution = create_initial_solution(bins, balls, instances)
    best_solution = current_solution[:]
    best_value = evaluate_solution(current_solution, instances)

    temperature = 100.0
    min_temperature = 0.000001
    cooling_rate = 0.99

    total_time = 0
    while temperature > min_temperature and max_iterations != 0:
        total_time = time.time() - start_time
        if total_time >= max_time:
            break
        for _ in range(200):
            neighbor = get_neighbor(current_solution[:], instances)
            neighbor_value = evaluate_solution(neighbor, instances)
            current_value = evaluate_solution(current_solution, instances)

            delta = current_value - neighbor_value

            if neighbor_value != 0:
                if delta <= 0 or random.random() < math.exp(-delta / temperature):
                    current_solution = neighbor[:]
            if current_value >= best_value:
                best_solution = current_solution[:]
                best_value = current_value

        temperature *= cooling_rate
        max_iterations -= 1

    total_time = time.time() - start_time

    return {
        "initial_solution_value": evaluate_solution(create_initial_solution(bins, balls, instances), instances),
        "best_solution_value": best_value,
        "execution_time": total_time,
        "max_time": max_time,
        "iterations_remaining": max_iterations,
        "final_temperature": temperature
    }

def main():
    if len(sys.argv) != 5:
        print("Uso: python simulated_annealing.py <arquivo_entrada> <seed> <max_iterações> <max_time>")
        return

    input_file = sys.argv[1]
    seed = int(sys.argv[2])
    max_iterations = int(sys.argv[3])
    max_time = int(sys.argv[4])

    instances, bins, balls = parse_input_file(input_file)
    print(f'Dados da instância: {input_file}')
    print(f'Número de bins: {bins}\nNúmero de balls: {balls}')

    results = simulated_annealing(bins, balls, instances, seed, max_iterations, max_time)

    print("\nResultados:")
    print(f"Nome da instância: {input_file}")
    print(f"Semente de aleatoriedade: {seed}")
    print(f"Valor da solução inicial: {results['initial_solution_value']}")
    print(f"Melhor valor da solução encontrada: {results['best_solution_value']}")
    print(f"Tempo total de execução: {results['execution_time']:.2f}s")
    print(f"Tempo limite superior: {results['max_time']}s")
    print(f"Temperatura final: {results['final_temperature']:.6f}")
    print(f"Iterações restantes: {results['iterations_remaining']}")

if __name__ == "__main__":
    main()
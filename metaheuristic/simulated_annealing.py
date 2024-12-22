import sys
import random
import time
import math

def parse_input_file(file_path):  ## Lê o arquivo de entrada e extrai as informações sobre os itens e as mochilas.

    instances = []
    with open(file_path, 'r') as f:
        bins = int(f.readline()) # pega a quantidade de bins presente no arquivo
        balls = int(f.readline()) # pega a quantidade de balls presente no arquivo
        while True:
            line = f.readline()
            if not line:
                break
            nums = line.split(' ');
            instance = [int(nums[0]), int(nums[1])] # instancia [lowerBound, upperBound]
            instances.append(instance)
    
    return instances, bins, balls

def evaluate_solution(solution, lower, upper): #Avaliamos a solução e verificamos o lucro mínimo entre os grupos sem ultrapassar a capacidade da mochila.

    best_value = 0
    for ball in solution:
        best_value += (ball*(ball + 1))/ 2
        if ball < lower or ball > upper:
            return 0;
    
    return best_value;

def get_neighbor(solution): # Gera uma nova solução (vizinha) alterando aleatoriamente a inclusão de um item da solução atual.
    from_bin = random.randint(0, len(solution) - 1)
    to_bin = random.randint(0, len(solution) - 1)

    while from_bin == to_bin: 
        to_bin = random.randint(0, len(solution) - 1)

    solution[from_bin] -= 1
    solution[to_bin] += 1

    return solution

def simulated_annealing(bins, balls, lower, upper, seed, max_iterations): # Algoritmo de Simulated Annealing para encontrar a melhor solução para o problema da mochila.
    random.seed(seed)
    # Inicializar bins vazios
    current_solution = [0] * bins
    # Distribuir bolas aleatoriamente
    for _ in range(balls):
        bin_choice = random.randint(0, bins - 1)
        current_solution[bin_choice] += 1


    best_solution = current_solution[:]
    best_value = evaluate_solution(best_solution, lower, upper)
    temperature = 100.0
    min_temperature = 0.1
    cooling_rate = 0.9
    
    start_time = time.time()

    while temperature > min_temperature or max_iterations > 0:
        neighbor = get_neighbor(current_solution)
        current_value = evaluate_solution(current_solution, lower, upper)
        neighbor_value = evaluate_solution(neighbor, lower, upper)

        # Se a solução vizinha for melhor ou passar no teste de probabilidade, adotamos ela
        if (neighbor_value > current_value or 
            random.uniform(0, 1) < math.exp((neighbor_value - current_value) / temperature)):
            current_solution = neighbor[:]
            current_value = neighbor_value
            
            # Atualiza a melhor solução encontrada
            if current_value > best_value:
                best_solution = current_solution[:]
                best_value = current_value
                elapsed_time = time.time() - start_time
                print(f"{elapsed_time:.2f}s: Melhor valor até agora = {best_value}")
    
        temperature *= cooling_rate
        max_iterations -= 1;
    
    total_time = time.time() - start_time
    print(f"Tempo total de execução: {total_time:.2f}s")

    return best_solution, best_value

def main():
    if len(sys.argv) < 4:
        print("Uso: python simulated_annealing.py <arquivo_entrada> <seed> <max_iterações>")
        return
    
    input_file = sys.argv[1]
    seed = int(sys.argv[2])
    max_iterations = int(sys.argv[3])
    
    instances, bins, balls = parse_input_file(input_file)
    print(f'Dados da instância ${input_file}')
    print(f'Número de bins {bins}\nNúmero de balls {balls}')

    for lowerBound, upperBound in instances:
        currentInstance = 0
        print(f"Resolvendo instância {currentInstance + 1}...")
        simulated_annealing(bins, balls, lowerBound, upperBound, seed, max_iterations)
        # print(f"Melhor Solução: {best_solution}")
        # print(f"Melhor Valor: {best_value}")
        # print("")
        currentInstance += 1

if __name__ == "__main__":
    main()

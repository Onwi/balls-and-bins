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

def evaluate_solution(solution, instances): #Avaliamos a solução e verificamos o lucro mínimo entre os grupos sem ultrapassar a capacidade da mochila.
    best_value = 0

    for index, ball in enumerate(solution):
        if(ball > instances[index][1] or ball < instances[index][0]):
            return 0
        else:
            best_value += (ball*(ball + 1))/ 2

    return best_value 

def get_neighbor(solution, instances): # Gera uma nova solução (vizinha) alterando aleatoriamente a inclusão de um item da solução atual.()
    from_bin = random.randint(0, len(solution) - 1)
    to_bin = random.randint(0, len(solution) - 1)

    while solution[from_bin] == instances[from_bin][0]:
        from_bin = random.randint(0, len(solution) - 1)

    while solution[to_bin] == instances[to_bin][1]:
        to_bin = random.randint(0, len(solution) - 1)


    solution[from_bin] -= 1
    solution[to_bin] += 1

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

def simulated_annealing(bins, balls, instances, seed, max_iterations): # Algoritmo de Simulated Annealing para encontrar a melhor solução para o problema da mochila.
    random.seed(seed)
    
    current_solution = create_initial_solution(bins, balls, instances)
    best_solution = current_solution[:]
    best_value = evaluate_solution(best_solution, instances)

    temperature = 1.0
    min_temperature = 0.00001
    cooling_rate = 0.95
    
    start_time = time.time()

    while temperature > min_temperature or max_iterations > 0:
        neighbor = get_neighbor(current_solution, instances)
        current_value = evaluate_solution(current_solution, instances)
        neighbor_value = evaluate_solution(neighbor, instances)
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

    best_solution, best_value = simulated_annealing(bins, balls, instances, seed, max_iterations)
    # print(f"Melhor Solução: {best_solution}")
    print(f"Melhor Valor: {best_value}")
    # print("")

if __name__ == "__main__":
    main()

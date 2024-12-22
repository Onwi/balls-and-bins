import sys
import random
import time
import math

def parse_input_file(file_path):  ## Lê o arquivo de entrada e extrai as informações sobre os itens e as mochilas.

    instances = []
    with open(file_path, 'r') as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            num_items = int(line)  # Quantidade de itens
            num_groups = int(f.readline().strip())  # Quantidade de grupos
            max_capacity = int(f.readline().strip())  # Capacidade máxima da mochila
            group_sizes = list(map(int, f.readline().strip().split()))  # Tamanhos dos grupos

            items = []
            for _ in range(num_items):
                line = f.readline().strip()
                if line:
                    weight, profit, group = map(int, line.split())
                    items.append((weight, profit, group))  # Adiciona o item (peso, lucro, grupo) na lista

            instances.append((max_capacity, num_items, items))
    
    return instances

def evaluate_solution(solution, items, capacity): #Avaliamos a solução e verificamos o lucro mínimo entre os grupos sem ultrapassar a capacidade da mochila.

    total_weight = sum(items[i][1] for i in range(len(solution)) if solution[i])
    
    if total_weight > capacity:
        return 0  # Solução inválida (peso passou da mochila)
    
    group_profits = {}
    for i, included in enumerate(solution):
        if included:
            profit, _, group = items[i]
            if group not in group_profits:
                group_profits[group] = 0
            group_profits[group] += profit
    
    if not group_profits:
        return 0  # Solução inválida (nenhum grupo foi incluído)
    
    min_profit = min(group_profits.values())  # O lucro mínimo entre os grupos
    return min_profit

def get_neighbor(solution): # Gera uma nova solução (vizinha) alterando aleatoriamente a inclusão de um item da solução atual.
    
    neighbor = solution[:]
    index = random.randint(0, len(solution) - 1)
    neighbor[index] = 1 - neighbor[index]  
    return neighbor

def simulated_annealing(capacity, num_items, items, seed, max_iterations): # Algoritmo de Simulated Annealing para encontrar a melhor solução para o problema da mochila.

    random.seed(seed)
    current_solution = [random.randint(0, 1) for _ in range(num_items)]
    best_solution = current_solution[:]
    best_value = evaluate_solution(best_solution, items, capacity)
    
    temperature = 1.0
    min_temperature = 0.00001
    cooling_rate = 0.9
    
    start_time = time.time()

    while temperature > min_temperature and max_iterations > 0:
        for _ in range(100):
            neighbor = get_neighbor(current_solution)
            current_value = evaluate_solution(current_solution, items, capacity)
            neighbor_value = evaluate_solution(neighbor, items, capacity)
            
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
                    print(f"{elapsed_time:.2f}s: Melhor valor até agora = {best_value}, Solução = {best_solution}")
        
        temperature *= cooling_rate
        max_iterations -= 1
        
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
    
    instances = parse_input_file(input_file)
    
    for idx, (capacity, num_items, items) in enumerate(instances):
        print(f"Resolvendo instância {idx + 1}...")
        best_solution, best_value = simulated_annealing(capacity, num_items, items, seed, max_iterations)
        print(f"Melhor Solução: {best_solution}")
        print(f"Melhor Valor: {best_value}")
        print("")

if __name__ == "__main__":
    main()

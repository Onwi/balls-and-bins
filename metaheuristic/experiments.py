import subprocess
import csv
import os

def run_simulated_annealing(instances_dir, output_csv, max_iterations, max_times):
    seeds = range(3, 8)  # Sementes
    instances = [f"{i:02d}.txt" for i in range(1, 11)]  # Instâncias de 01.txt a 10.txt
    results = []

    for instance in instances:
        for max_time in max_times:
            for seed in seeds:
                input_file = os.path.join(instances_dir, instance)
                
                # Chama o simulated_annealing.py
                command = [
                    "python", "simulated_annealing.py", 
                    input_file, str(seed), str(max_iterations), str(max_time)
                ]
                try:
                    process = subprocess.run(command, text=True, capture_output=True, check=True)
                    output = process.stdout.strip()
                    
                    # Extrai os dados do output do simulated_annealing.py
                    lines = output.split('\n')
                    solution_initial = float(lines[7].split(":")[1].strip())
                    best_value = float(lines[8].split(":")[1].strip())
                    total_time = float(lines[9].split(":")[1].strip().replace("s", ""))
                    max_time = int(lines[10].split(":")[1].strip().replace("s", ""))
                    formulation_value, formulation_time = formulation()
                    
                    # Adiciona os resultados
                    results.append([
                        instance, seed, solution_initial, best_value, formulation_value, total_time, max_time, formulation_time
                    ])
                except subprocess.CalledProcessError as e:
                    print(f"Erro ao executar para a instância {instance} com seed {seed}.")
                    print(e.stderr)

    # Cria o CSV com os resultados
    with open(output_csv, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Instancia", "Seed", "Solucao Inicial", 
            "Melhor Solucao", "Valor Medio Formulacao", "Tempo Total (s)", "Limite Tempo (s)", "Tempo Medio Formulacao (s)"
        ])
        writer.writerows(results)
    print(f"Resultados salvos no arquivo {output_csv}.")

def formulation():
    return 0,0

# Configuração de execução
instances_dir = "..\\instancias" 
output_csv = "resultados.csv"
max_iterations = 1000
max_times = [5, 300]  # Tempo máximo de 5 e 300 segundos


# Executa o script
run_simulated_annealing(instances_dir, output_csv, max_iterations, max_times)
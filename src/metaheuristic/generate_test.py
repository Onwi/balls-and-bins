import random

def generate_complex_instances(num_instances, num_items, capacity_range, group_range, value_range, weight_range):
    instances = []
    for _ in range(num_instances):
        n = random.randint(num_items, num_items)  # Garantir que tenha pelo menos num_items itens
        G = random.randint(group_range[0], group_range[1])
        capacity = random.randint(capacity_range[0], capacity_range[1])
        group_sizes = [random.randint(1, n // G) for _ in range(G)]
        items = []
        for _ in range(n):
            l = random.randint(value_range[0], value_range[1])
            p = random.randint(weight_range[0], weight_range[1])
            g = random.randint(1, G)
            items.append((l, p, g))
        instances.append((capacity, n, items))
    return instances

def write_instances_to_file(instances, file_path):
    with open(file_path, 'w') as f:
        for idx, (capacity, n, items) in enumerate(instances):
            f.write(f"{n}\n{len(set(g for _, _, g in items))}\n{capacity}\n")
            group_counts = {g: sum(1 for _, _, gi in items if gi == g) for g in set(g for _, _, g in items)}
            group_sizes = ' '.join(str(group_counts[g]) for g in sorted(group_counts))
            f.write(f"{group_sizes}\n")
            for l, p, g in items:
                f.write(f"{l} {p} {g}\n")
            f.write("\n")

# Parâmetros para a geração de instâncias complexas
num_instances = 5  # Número de instâncias
num_items = 500  # Número mínimo de itens por instância
capacity_range = (1000, 2000)  # Capacidade das mochilas
group_range = (5, 10)  # Número de grupos
value_range = (10, 100)  # Valores dos itens
weight_range = (20, 80)  # Pesos dos itens

# Gerar instâncias complexas
instances = generate_complex_instances(num_instances, num_items, capacity_range, group_range, value_range, weight_range)

# Escrever instâncias em um arquivo
output_file_path = "complex_instances2.txt"
write_instances_to_file(instances, output_file_path)

print(f"Instâncias complexas foram geradas e salvas em {output_file_path}")

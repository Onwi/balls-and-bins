res = 8298126.0
ideal = 8461348
margem = ideal - ideal*0.01
erro = (1 - ( res / ideal  )) * 100
print(f'Erro {erro}')


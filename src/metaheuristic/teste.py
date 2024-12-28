res = 29751896 
ideal = 29745831 
margem = ideal - ideal*0.01
erro = (1 - ( res / ideal  )) * 100
print(f'Erro {erro}')


# balls-and-bins

## Compilando e rodando o codigo da formulação inteira

1. Tenha Julia, e os pacotes JuMP e HiGHS, instalados no computador.
2. O arquivo com a formulação inteira em julia se encontra em `src/`, com o nome de `solver.jl`.
3. A estrutura para rodar o programa é a seguinte:
4. `julia solver.jl <arquivo de instancia do problema> <random seed> <time limit>`
5. Os arquivos para teste se encontram em `src/instancias`
6. Exemplo: `julia solver.jl ../instancias/01.txt 7 300`


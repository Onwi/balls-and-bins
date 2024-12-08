using Pkg
Pkg.add("JuMP")
Pkg.add("HiGHS")

using JuMP
using HiGHS

function ler_instancia(arquivo)
    open(arquivo, "r") do f
        n = parse(Int, readline(f))
        m = parse(Int, readline(f))
        limites_inferiores = Int[]
        limites_superiores = Int[]
        
        for i in 1:n
            l, u = split(readline(f))
            push!(limites_inferiores, parse(Int, l))
            push!(limites_superiores, parse(Int, u))
        end
    
        return n, m, limites_inferiores, limites_superiores
    end
end

arquivo = ARGS[1]
seed_parametro = parse(Int, ARGS[2])

function resolver_problema(arquivo)
    n, m, limites_inferiores, limites_superiores = ler_instancia(arquivo)
    
    model = Model(HiGHS.Optimizer)
    set_attribute(model, "random_seed", seed_parametro)
    
    # Xi e Yik
    @variable(model, x[1:n], Int, lower_bound=0)
    @variable(model, y[1:n, 1:maximum(limites_superiores)], Bin)    

    # função objetivo
    @objective(model, Max, sum(((k * (k + 1)) / 2) * y[i, k] for i in 1:n for k in limites_inferiores[i]:limites_superiores[i]))
    
    # garantir o uso de todas as bolas
    @constraint(model, sum(x[i] for i in 1:n) == m)
    
    # garantir que apenas uma variável Yik seja ativada para cada recipiente i
    for i in 1:n
        @constraint(model, sum(y[i, k] for k in limites_inferiores[i]:limites_superiores[i]) == 1)
    end 

    # definição de Xi dado Yik
    for i in 1:n
        @constraint(model, x[i] == sum(k * y[i, k] for k in limites_inferiores[i]:limites_superiores[i]))
    end
   
    optimize!(model)
    
    # pegar valor ótimo
    status = termination_status(model)
    if status == MOI.OPTIMAL
        println("Lucro máximo: ", objective_value(model))
    else
        println("erro ao tentar otimizar: $status")
    end
end

resolver_problema(arquivo)

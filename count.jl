#! /usr/bin/env julia

using JSON

const dfa = JSON.parse(stdin)

const Q = dfa["states"]
const M = dfa["transitions"]
const s = dfa["start"]
const F = Set(dfa["final"])

const m = length(M)

const u = transpose([Int(q == s) for q in Q])
const v = [Int(q in F) for q in Q]
const A = [BigInt(count(x -> x == q, row)) for row in M, q in Q]

function f(a, n)
    println(u * a * v)
    return a * A
end

if length(ARGS) == 1
    n = parse(Int, ARGS[1])
    println(u * A^n * v)
elseif length(ARGS) == 2
    left = parse(Int, ARGS[1])
    right = parse(Int, ARGS[2])
    foldl(f, left:right, init=A^left)
else
    try
        foldl(f, Iterators.countfrom(0), init=A)
    catch e
        # gracefully exit on EPIPE when stdout closes
        if typeof(e) != Base.IOError || e.code != Base.UV_EPIPE
            throw(e)
        end
    end
end

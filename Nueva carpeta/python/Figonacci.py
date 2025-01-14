def fibonacci(n):
    """Genera una lista con la secuencia de Fibonacci hasta el n-ésimo término."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    
    return fib_sequence

# Ejemplo de uso:
n = int(input("Introduce la cantidad de términos de la secuencia de Fibonacci que deseas: "))
print(f"Secuencia de Fibonacci de {n} términos: {fibonacci(n)}")
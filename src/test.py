import random

def randomiza_processos_permanentes(total: int, n_permanentes: int) -> list:
    chance = float(n_permanentes) / total
    chances = []

    for _ in range(total):
        if random.random() < chance:
            n_permanentes -= 1
            chances.append(False)
        else:
            chances.append(True)
    
    i = 0
    while n_permanentes > 0:
        if chances[i]:
            chances[i] = False
            n_permanentes -= 1
        i += 1

    while n_permanentes < 0:
        if not chances[i]:
            chances[i] = True
            n_permanentes += 1  
        i += 1

    return chances

count = 0

while count < 10000:

    total = random.randint(1, 10000)
    n_permanentes = random.randint(0, total)
    chances = randomiza_processos_permanentes(total=total, n_permanentes=n_permanentes)

    i = 0
    j = 0

    for chance in chances:
        if chance:
            i += 1
        else:
            j += 1

    if i == total - n_permanentes and j == n_permanentes:
        print("certo")
        # print(f"i: {i}, j: {j}, n_nao_permanentes: {total - n_permanentes}, n_permanentes: {n_permanentes}")
    else:
        print("falha")
        print(f"i: {i}, j: {j}, n_nao_permanentes: {total - n_permanentes}, n_permanentes: {n_permanentes}")
    count += 1


def below_above_threshold(l: list, t1: int, t2: int, s: str):
    if s == 'below':
        for i in range(len(l)):
            if l[i] >= t1:
                return i
        return True
    elif s == 'above':
        for i in range(len(l)):
            if l[i] <= t2:
                return i
        return True
    else:
        return -1

if __name__ == '__main__':
    inputs = [eval(f"[{i}]") for i in ["[1, 2, 4, 10], 100, 0, 'below'", "[1, 20, 4, 10], 5, 0, 'below'", "[1, 20, 4, 10], 5, 0, 'above'", "[10, 20, 30, 40], 5, 15, 'above'", "[1, 10, 100, 1000], 50, 0, 'below'", "[-1, -20, -4, -10], -5, 0, 'below'", "[-1, -20, -4, -10], -3, -50, 'above'", "[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 15, 15, 'above'", "[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 15, 15, 'below'", "[100]*1000, 100, 0, 'below'", "[100]*1000, 100, 0, 'above'", "[i for i in range(1000)], 500, 0, 'below'", "[i for i in range(1000)], 500, 0, 'above'", "[-1000, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0, -1001, 'above'", "[-1000, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0, -1001, 'below'", "[100, 200, 300, 400, 500], 250, 150, 'above'", "[100, 200, 300, 400, 500], 250, 150, 'below'", "[i for i in range(-500, 500)], 0, -1, 'above'", "[i for i in range(-500, 500)], 0, -1, 'below'", "[1, 1, 1, 1, 1, 2], 2, 0, 'below'", "[1, 1, 1, 1, 1, 2], 2, 0, 'above'", "[1000, -1000, 0], 500, -500, 'below'", "[1000, -1000, 0], 500, -500, 'above'", "[1000, -1000, 0], 500, 500, 'below'", "[1000, -1000, 0], 500, 500, 'above'", "[1000, -1000, 0, 500], 500, 500, 'below'", "[1000, -1000, 0, 500], 500, 500, 'above'", "[1000, -1000, 0, -500], 500, -500, 'below'", "[1000, -1000, 0, -500], 500, -500, 'above'", "[], 1000, -1000, 'below'", "[], 1000, -1000, 'above'", "[1000], 1000, -1000, 'below'", "[1000], 1000, -1000, 'above'", "[1, 2, 3], 2, 1, 'test'", "[1, -1, 0], 1, -1, 'below'", "[1, -1, 0], 1, -1, 'above'", "[-1000, 0, 1000], 1000, -1000, 'below'", "[-1000, 0, 1000], 1000, -1000, 'above'", "[], 1, 0, 'below'", "[0], 0, 0, 'below'", "[0], 0, 0, 'above'", "[1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000], 1000, 0, 'below'", "[-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000], 0, -1000, 'above'", "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, 0, 'below'", "[-1, -2, -3, -4, -5, -6, -7, -8, -9, -10], 0, -5, 'above'", "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10, 1, 'below'", "[-1, -2, -3, -4, -5, -6, -7, -8, -9, -10], -10, -1, 'above'", "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, 1, 'below'", "[-1, -2, -3, -4, -5, -6, -7, -8, -9, -10], -5, -1, 'above'", "[1], 2, 0, 'below'", "[1], 0, 2, 'above'", "[1, -2, 3, -4, 5], 0, -3, 'below'", "[-1, -2, -3, -4, -5], -3, -1, 'below'", "[-1, -2, -3, -4, -5], -6, -1, 'above'", "[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000], 500, 1000, 'above'", "[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000], 100, 500, 'below'", "[100, -200, 300, -400, 500, -600, 700, -800, 900, -1000], 500, -500, 'below'", "[-100, 200, -300, 400, -500, 600, -700, 800, -900, 1000], -500, 0, 'above'", "[], 5, -5, 'below'", "[], 5, -5, 'above'", "[-1, -2, -3, -4, -5], -3, -1, 'middle'", "[1, 2, 3, 4, 5], 3, 1, 'middle'"]]
    i = 0

    while(True):
        below_above_threshold(*inputs[i%len(inputs)])
        i += 1


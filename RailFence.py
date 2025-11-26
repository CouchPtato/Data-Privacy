def encryptRailFence(text : str, key : int) -> str:

    rail = [['*' for i in range(len(text))]
                for j in range(key)]
    
    dir_down = True
    row, col = 0, 0
    
    for i in range(len(text)):
        
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False

        rail[row][col] = text[i]
        col += 1
        
        if dir_down:
            row += 1
        else:
            row -= 1

    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '*':
                result.append(rail[i][j])
    ans = "".join(result)
    return ans
    
def decryptRailFence(cipher : str, key : int) -> str:
    n = len(cipher)
    pattern = []
    row = 0
    dir_down = True

    for i in range(n):
        pattern.append(row)
        if row == 0:
            dir_down = True
        elif row == key - 1:
            dir_down = False
        row += 1 if dir_down else -1

    per_row_counts = [pattern.count(r) for r in range(key)]

    rows = []
    idx = 0

    for count in per_row_counts:
        cipher_idx = idx + count
        rows.append(list(cipher[idx : cipher_idx]))
        idx += count

    result = []
    row_ptrs = [0] * key

    for r in pattern:
        result.append(rows[r][row_ptrs[r]])
        row_ptrs[r] += 1

    ans = "".join(result)
    return ans

def main():
    print(encryptRailFence("My name is Lasagna", 3))
    print(decryptRailFence("Maianynm sLsga e a", 3))

if __name__ == "__main__":
    main()

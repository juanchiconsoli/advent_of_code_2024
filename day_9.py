from pathlib import Path
from collections import deque

if __name__ == "__main__":

    part_2 = True

    with open(Path("./day_9_input.txt"), mode="r") as file:
        disk_map = file.read().strip()

    A = deque([])
    SPACE = deque([])
    FINAL = []
    file_id = 0
    pos = 0

    for i, c in enumerate(disk_map):
        if i % 2 == 0:
            if part_2:
                A.append((pos, int(c), file_id))
            for i in range(int(c)):
                FINAL.append(file_id)
                if not part_2:
                    A.append((pos, 1, file_id))
                pos += 1
            file_id += 1

        else:
            SPACE.append((pos, int(c)))
            for i in range(int(c)):
                FINAL.append(None)
                pos += 1

    for pos, sz, file_id in reversed(A):
        for space_i, (space_pos, space_sz) in enumerate(SPACE):
            if space_pos < pos and sz <= space_sz:
                for i in range(sz):
                    assert FINAL[pos + i] == file_id, f"{FINAL[pos+i]=}"
                    FINAL[pos + i] = None
                    FINAL[space_pos + i] = file_id
                SPACE[space_i] = (space_pos + sz, space_sz - sz)
                break

    ans = 0
    for i, c in enumerate(FINAL):
        if c is not None:
            ans += i * c

    print(ans)

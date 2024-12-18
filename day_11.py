from typing import List
from rich import print

DP = {}


def get_stone_expansion(stone, blinking_times: int) -> int:

    if (stone, blinking_times) in DP:
        return DP[(stone, blinking_times)]

    if blinking_times == 0:
        ret = 1
    elif stone == 0:
        ret = get_stone_expansion(1, blinking_times - 1)
    elif len(str(stone)) % 2 == 0:
        stone_str = str(stone)
        mid = len(stone_str) // 2
        left_stone = int(stone_str[:mid])
        right_stone = int(stone_str[mid:])
        ret = get_stone_expansion(left_stone, blinking_times - 1) + get_stone_expansion(
            right_stone, blinking_times - 1
        )
    else:
        ret = get_stone_expansion(stone * 2024, blinking_times - 1)

    DP[(stone, blinking_times)] = ret

    return ret


def get_number_of_stones(array_of_stones: List[int], blinking_times: int) -> int:
    return sum(get_stone_expansion(s, blinking_times) for s in array_of_stones)


if __name__ == "__main__":
    array_of_stones = [337, 42493, 1891760, 351136, 2, 6932, 73, 0]

    blinking_times = 75

    num_of_stones = get_number_of_stones(array_of_stones, blinking_times)

    print(num_of_stones)

from pathlib import Path
from rich import print


def read_initial_secret_numbers(file: Path):
    with open(file, mode="r") as f:
        secret_numbers = []
        for line in f.readlines():
            secret_numbers.append(int(line.strip()))
        return secret_numbers


def get_next_secret_number(secret: int):
    num1 = prune(mix(secret * 64, secret))

    num2 = prune(mix(int(num1 / 32), num1))

    num3 = prune(mix(num2 * 2048, num2))

    return num3


def prune(num: int):
    return num % 16777216


def mix(secret: int, num: int):
    return num ^ secret


if __name__ == "__main__":

    buyers_prices = []

    secret_numbers = read_initial_secret_numbers(Path("./day_22_input.txt"))

    seq_to_total = {}

    for i, num in enumerate(secret_numbers):
        buyer = [num % 10]

        for _ in range(2000):
            num = get_next_secret_number(num)
            buyer.append(num % 10)

        seen = set()
        for i in range(len(buyer) - 4):
            a, b, c, d, e = buyer[i : i + 5]
            seq = (b - a, c - b, d - c, e - d)
            if seq in seen:
                continue
            seen.add(seq)

            if seq not in seq_to_total:
                seq_to_total[seq] = 0
            seq_to_total[seq] += e

    print({k: seq_to_total[k] for k in list(seq_to_total)[:10]})

    max_value = max(seq_to_total.values())
    for seq, total in seq_to_total.items():
        if total == max_value:
            print(seq)
            print(max_value)
            break

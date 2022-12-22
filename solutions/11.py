from pathlib import Path


class Monkey:
    def __init__(
        self,
        name: int,
        items: list[int],
        operation: str,
        test_divisor: int,
        recipient_index: tuple[int, int],  # (False, True)
    ):
        self.name = name
        self.items = items
        self.operation = operation
        self.test_divisor = test_divisor
        self.recipient_index = recipient_index

        self.qty_items_inspected = 0

    def __mul__(self, other):
        return self.qty_items_inspected * other.qty_items_inspected

    def __repr__(self):
        return f"Monkey(name={self.name}, inspections={self.qty_items_inspected})"

    def catch(self, item: int):
        self.items.append(item)


class MonkeyInTheMiddle:
    def __init__(self, monkeys: dict[int, Monkey], worry_divisor: int = 1):
        self.monkeys = monkeys
        self.worry_divisor = worry_divisor

    # had to read explanation of other solutions to find out
    # about the role of supermodulo here to keep values small
    # without losing relative precision
    @property
    def super_test(self) -> int:
        super_test = 1
        for _, m in self.monkeys.items():
            super_test *= m.test_divisor
        return super_test

    def inspect(self, monkey: Monkey):
        """
        Apply Operation
        Reduce by Worry Level
        """
        monkey.qty_items_inspected += 1
        index = 0
        old = monkey.items[index]  # noqa: F841
        new = eval(f"{monkey.operation}")
        new //= self.worry_divisor
        new %= self.super_test
        monkey.items[index] = new

    def throw(self, monkey: Monkey) -> tuple[int, int]:
        """Throws item [0] to monkey [1]...
        Test
        Throw (based on true/false result)
        """
        item = monkey.items.pop(0)
        test_bool = not bool(item % monkey.test_divisor)
        recipient = monkey.recipient_index[int(test_bool)]
        return item, recipient

    def apply_round(self):
        for i, monkey in self.monkeys.items():
            qty_items = len(monkey.items)
            for j in range(qty_items):
                self.inspect(monkey=monkey)
                item, recipient = self.throw(monkey=monkey)
                self.monkeys[recipient].catch(item)

    def simulate_rounds(self, qty: int):
        for i in range(qty):
            self.apply_round()


def read_input() -> list[str]:
    filepath = Path(__file__).resolve()
    filename_no_ext = filepath.name.split(".")[0]
    filedir = filepath.parent
    input_file = filedir / f"../inputs/{filename_no_ext}.txt"
    with open(input_file) as infile:
        input = infile.readlines()
    return [line.strip() for line in input]


def initialize_game(input: list[str], worry_divisor: int) -> MonkeyInTheMiddle:
    offset = 7
    monkeys_input = [input[i : i + offset] for i in range(0, len(input), offset)]

    monkeys: dict[int, Monkey] = dict()
    for monkey_input in monkeys_input:
        name, items, operation, test, if_true, if_false, *remainder = (line.strip() for line in monkey_input)

        name = int(name.split()[-1].split(":")[0])
        items = [int(v.strip()) for v in items.split("Starting items:")[1].split(",")]
        operation = operation.split("new = ")[1]
        test = int(test.split()[-1])
        if_true = int(if_true.split()[-1])
        if_false = int(if_false.split()[-1])

        monkey = Monkey(
            name=name,
            items=items,
            operation=operation,
            test_divisor=test,
            recipient_index=(if_false, if_true),
        )
        monkeys[name] = monkey
    game = MonkeyInTheMiddle(monkeys=monkeys, worry_divisor=worry_divisor)
    return game


def run_part_1(input: list[str]) -> int:
    qty_rounds = 20
    game = initialize_game(input, worry_divisor=3)
    game.simulate_rounds(qty=qty_rounds)
    monkeys = game.monkeys
    inspection_qty_desc = sorted(monkeys.values(), key=lambda x: x.qty_items_inspected, reverse=True)
    return inspection_qty_desc[0] * inspection_qty_desc[1]


def run_part_2(input: list[str]) -> int:
    qty_rounds = 10000
    game = initialize_game(input, worry_divisor=1)
    game.simulate_rounds(qty=qty_rounds)
    monkeys = game.monkeys
    inspection_qty_desc = sorted(monkeys.values(), key=lambda x: x.qty_items_inspected, reverse=True)
    return inspection_qty_desc[0] * inspection_qty_desc[1]


if __name__ == "__main__":
    input = read_input()
    print(run_part_1(input))  # 121450 - correct
    print(run_part_2(input))  # 28244037010 - correct

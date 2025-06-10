class Node:
    """Узел двусвязного списка"""

    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class CyclicDoublyLinkedList:
    """Циклический двусвязный список"""

    def __init__(self, digits):
        self.head = None
        self.length = 0
        self._build_list(digits)

    def _build_list(self, digits):
        """Построение списка из строки цифр"""
        if not digits.isdigit():
            raise ValueError("Input must contain only digits")

        for digit in digits:
            new_node = Node(int(digit))
            self.length += 1

            if not self.head:
                self.head = new_node
                new_node.next = new_node
                new_node.prev = new_node
            else:
                tail = self.head.prev
                tail.next = new_node
                new_node.prev = tail
                new_node.next = self.head
                self.head.prev = new_node

    def get_number(self, start_pos, length):
        """Извлечение числа заданной длины начиная с позиции"""
        if length <= 0 or start_pos >= self.length:
            return None

        current = self.head
        # Переходим к начальной позиции
        for _ in range(start_pos):
            current = current.next

        digits = []
        zero_flag = True  # Флаг для проверки ведущих нулей

        for _ in range(length):
            digit = current.value
            if zero_flag:
                if digit == 0 and length > 1:
                    return None  # Число с ведущим нулем
                zero_flag = False
            digits.append(str(digit))
            current = current.next

        return int(''.join(digits)) if digits else None


class RingEquationSolver:
    """Решатель уравнения A+B=C в числовом кольце"""

    def __init__(self, ring):
        self.ring = ring
        self.n = ring.length

    def find_equation(self):
        """Ищет уравнение A + B = C в числовом кольце.

        Возвращает:
            str: уравнение в формате 'A+B=C', если найдено
            str: 'No' — иначе
        """
        if self.n < 3:
            return "No"

        for a_len in range(1, self.n - 1):
            for b_len in range(1, self.n - a_len):
                c_len = self.n - a_len - b_len
                if c_len < 1:
                    continue

                for start_pos in range(self.n):
                    a = self.ring.get_number(start_pos, a_len)
                    b = self.ring.get_number((start_pos + a_len) % self.n, b_len)
                    c = self.ring.get_number((start_pos + a_len + b_len) % self.n, c_len)

                    if a is not None and b is not None and c is not None:
                        if a + b == c:
                            return self._format_result(start_pos, a_len, b_len, c_len)
        return "No"

    def _format_result(self, start_pos, a_len, b_len, c_len):
        """Форматирование результата в строку"""

        def get_digits(pos, length):
            digits = []
            current = self.ring.head
            for _ in range(pos):
                current = current.next
            for _ in range(length):
                digits.append(str(current.value))
                current = current.next
            return ''.join(digits)

        a_str = get_digits(start_pos, a_len)
        b_str = get_digits((start_pos + a_len) % self.n, b_len)
        c_str = get_digits((start_pos + a_len + b_len) % self.n, c_len)

        return f"{a_str}+{b_str}={c_str}"


def main():
    """Основная функция программы"""
    print("Числовое кольцо - поиск A+B=C")
    print("Выберите источник данных:")
    print("1. Ввод вручную")
    print("2. Чтение из файла input.txt")

    choice = input("Ваш выбор (1/2): ").strip()
    input_data = ""

    try:
        if choice == "1":
            input_data = input("Введите строку цифр: ").strip()
        elif choice == "2":
            with open("input.txt", "r") as file:
                input_data = file.read().strip()
        else:
            print("Неверный выбор!")
            return
    except Exception as e:
        print(f"Ошибка: {e}")
        return

    if not input_data.isdigit():
        print("Ошибка: ввод должен содержать только цифры!")
        return

    try:
        ring = CyclicDoublyLinkedList(input_data)
        solver = RingEquationSolver(ring)
        result = solver.find_equation()

        with open("output.txt", "w") as file:
            file.write(result)

        print(f"Результат записан в output.txt: {result}")
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")


if __name__ == "__main__":
    main()
def find_equation(ring):
    """Ищет уравнение A + B = C в числовом кольце."""
    n = len(ring)
    if n < 3 or n > 1000:
        return "No"

    # Функция для извлечения числа с учётом циклического перехода
    def extract_number(start, length):
        number = []
        for i in range(length):
            pos = (start + i) % n
            number.append(ring[pos])
        num_str = ''.join(number)
        if len(num_str) > 1 and num_str[0] == '0':
            return None
        return int(num_str) if num_str else None

    # Перебираем все возможные комбинации A, B, C
    for a_len in range(1, n - 1):
        for b_len in range(1, n - a_len):
            c_len = n - a_len - b_len
            if c_len < 1:
                continue

            for start in range(n):
                a = extract_number(start, a_len)
                b = extract_number((start + a_len) % n, b_len)
                c = extract_number((start + a_len + b_len) % n, c_len)

                if a is not None and b is not None and c is not None:
                    if a + b == c:
                        # Формируем строки чисел
                        a_str = ''.join(ring[(start + i) % n] for i in range(a_len))
                        b_str = ''.join(ring[(start + a_len + i) % n] for i in range(b_len))
                        c_str = ''.join(ring[(start + a_len + b_len + i) % n] for i in range(c_len))
                        return f"{a_str}+{b_str}={c_str}"

    return "No"


def main():
    """Основная функция: чтение из файла/ввод вручную и запись в файл."""
    import sys
    input_source = None
    ring = ""

    # Выбор источника данных
    print("Выберите источник данных:")
    print("1 - Ввод вручную")
    print("2 - Чтение из файла input.txt")
    choice = input("Ваш выбор (1/2): ").strip()

    # Получение данных
    if choice == "1":
        ring = input("Введите строку цифр: ").strip()
        if not ring.isdigit():
            print("Ошибка: в строке должны быть только цифры!", file=sys.stderr)
            return
    elif choice == "2":
        try:
            with open("input.txt", "r") as f:
                ring = f.read().strip()
            if not ring.isdigit():
                print("Ошибка: файл должен содержать только цифры!", file=sys.stderr)
                return
        except FileNotFoundError:
            print("Ошибка: файл input.txt не найден!", file=sys.stderr)
            return
    else:
        print("Ошибка: неверный выбор!", file=sys.stderr)
        return

    # Проверка на длину строки
    if len(ring) > 100:
        print("Предупреждение: длинная строка может замедлить выполнение программы.")
        confirm = input("Продолжить? (y/n): ").strip().lower()
        if confirm != 'y':
            return

    # Поиск решения
    result = find_equation(ring)

    # Запись результата в файл
    with open("output.txt", "w") as f:
        f.write(result)

    print(f"Результат записан в output.txt: {result}")


if __name__ == "__main__":
    main()
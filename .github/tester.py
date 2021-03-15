from libtester import prepare, SR
import logging
import math
import os
import random
import sys

def main():
    e = prepare()
    if not e:
        return

    os.environ["ASAN_OPTIONS"] = "exitcode=154"

    errors = 0

    # source: http://www.valuedlessons.com/2009/01/popcount-in-python-with-benchmarks.html
    # Я специально выбирал реализацию, которую никто в здравом уме с нуля не придумает
    # (во всяком случае, из математиков ­— электроинженеры на старших курсах могли бы).
    # Не списывайте, пожалуйста. Напишите простую реализацию в виде цикла
    # (или у меня спроcите, если непонятно, что делать с отрицательными).
    def popcnt(v):
        v = v - ((v >> 1) & 0x55555555)
        v = (v & 0x33333333) + ((v >> 2) & 0x33333333)
        v = (v & 0x0F0F0F0F) + ((v >> 4) & 0x0F0F0F0F)
        v = v + (v >> 8)
        v = (v + (v >> 16)) & 0x3F
        return v

    def test_valid(x, y, name="Корректные данные"):
        x_str = " ".join(str(el) for el in x)
        y_str = " ".join(str(el) for el in y)

        result = e.expect_success(name, inputs=[x_str, y_str])
        if not result:
            return result

        try:
            output_str = result.stdout.strip().split()
            output = [int(el.strip()) for el in output_str]
        except Exception:
            print(f"ОШИБКА{SR}\nНе удалось разобрать вывод (в выводе есть что-то кроме целых чисел, разделённых пробелами)")
            logging.exception("")
            return False

        y_popcnt = {popcnt(el) for el in y}
        x_missing = {el for el in x if popcnt(el) not in y_popcnt}
        y_sorted = sorted(y, key=popcnt, reverse=True)
        y_count = len(y)

        answer = " ".join(str(el) for el in x_missing) + "\n" + " ".join(str(el) for el in y_sorted)

        if len(output) < y_count:
            print(f"ОШИБКА{SR}\nВ выводе перечислены не все элементы массива Y")
            return False

        if y_count >= 2 and any(1 for y1, y2 in zip(output[-y_count:], output[-y_count+1:]) if popcnt(y1) < popcnt(y2)):
            print(f"ОШИБКА{SR}\nНеправильно отсортированы элементы массива Y. Ожидается ответ:\n{answer}")
            return False

        if x_missing != set(output[:-y_count] if y_count else output):
            print(f"ОШИБКА{SR}\nВыведены не те элементы массива X. Ожидается ответ:\n{answer}")
            return False

        return True

    errors += not e.expect_failure("Нет аргументов", arguments=[])
    errors += not e.expect_failure("Нет первого файла с входными данными", arguments=["/a/b"])
    errors += not e.expect_failure("Нет второго файла с входными данными", arguments=["/dev/null", "/a/b"])
    errors += not e.expect_failure("Некорректный элемент первого массива", inputs=["3 a 1 1", ""])
    errors += not e.expect_failure("Некорректный элемент первого массива", inputs=["3 1 a 1", ""])
    errors += not e.expect_failure("Некорректный элемент первого массива", inputs=["3 1 1 a", ""])
    errors += not e.expect_failure("Некорректный элемент первого массива", inputs=["2 1 1 a", ""])
    errors += not e.expect_failure("Некорректный элемент второго массива", inputs=["", "3 a 1 1"])
    errors += not e.expect_failure("Некорректный элемент второго массива", inputs=["", "3 1 a 1"])
    errors += not e.expect_failure("Некорректный элемент второго массива", inputs=["", "3 1 1 a"])
    errors += not e.expect_failure("Некорректный элемент второго массива", inputs=["", "2 1 1 a"])

    errors += not test_valid([], [], "Пустой ввод")
    errors += not test_valid([], [1], "Пустой X")
    errors += not test_valid([1], [], "Пустой Y")
    errors += not test_valid([1, -1, 2, 3], [1, 2, 3, -1], "Идентичные массивы")
    errors += not test_valid([1, 1, 1, 1], [2, 2], "Одинаковое количество единиц")
    errors += not test_valid([1], [-1], "Разное количество единиц")
    errors += not test_valid([-4], [2 ** 30 - 1], "Одинаковое количество единиц")

    for i in range(20):
        errors += not test_valid([random.randint(-100, 100) for _ in range(random.randint(0, 25))], [random.randint(-100, 100) for _ in range(random.randint(0, 25))])

    for i in range(4):
        errors += not test_valid([random.randint(-1000, 10000) for _ in range(random.randint(0, 2000))], [random.randint(-10, 1000) for _ in range(random.randint(0, 2000))])

    print(f"Тестирование завершено, количество ошибок: {errors}")

    sys.exit(errors)

main()

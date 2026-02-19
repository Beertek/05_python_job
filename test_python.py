"""
Модуль с тестами для встроенных функций filter, map, sorted,
и функций из библиотеки math: pi, sqrt, pow, hypot
"""
import math
import unittest
from typing import List, Any

class TestBuiltinFunctions(unittest.TestCase):
    """Тесты для встроенных функций Python"""
    
    # ====== ТЕСТЫ ДЛЯ FILTER ======
    
    def test_filter_even_numbers(self):
        """Фильтрация четных чисел"""
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = list(filter(lambda x: x % 2 == 0, numbers))
        self.assertEqual(result, [2, 4, 6, 8, 10])
    
    def test_filter_odd_numbers(self):
        """Фильтрация нечетных чисел"""
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = list(filter(lambda x: x % 2 != 0, numbers))
        self.assertEqual(result, [1, 3, 5, 7, 9])
    
    def test_filter_strings_by_length(self):
        """Фильтрация строк по длине"""
        words = ["cat", "elephant", "dog", "butterfly", "ant"]
        result = list(filter(lambda x: len(x) > 3, words))
        self.assertEqual(result, ["elephant", "butterfly"])
    
    def test_filter_positive_numbers(self):
        """Фильтрация положительных чисел"""
        numbers = [-5, -3, 0, 2, 4, -1, 7]
        result = list(filter(lambda x: x > 0, numbers))
        self.assertEqual(result, [2, 4, 7])
    
    def test_filter_none_values(self):
        """Фильтрация None значений"""
        items = [0, None, "", "hello", False, [], [1, 2], None]
        result = list(filter(lambda x: x is not None, items))
        self.assertEqual(result, [0, "", "hello", False, [], [1, 2]])
    
    def test_filter_with_boolean_function(self):
        """Фильтрация с использованием встроенной bool функции"""
        items = [0, 1, "", "text", [], [1, 2], None]
        result = list(filter(bool, items))
        self.assertEqual(result, [1, "text", [1, 2]])
    
    def test_filter_palindromes(self):
        """Фильтрация палиндромов"""
        words = ["radar", "python", "level", "world", "madam", "test"]
        result = list(filter(lambda x: x == x[::-1], words))
        self.assertEqual(result, ["radar", "level", "madam"])
    
    # ====== ТЕСТЫ ДЛЯ MAP ======
    
    def test_map_square_numbers(self):
        """Возведение чисел в квадрат"""
        numbers = [1, 2, 3, 4, 5]
        result = list(map(lambda x: x ** 2, numbers))
        self.assertEqual(result, [1, 4, 9, 16, 25])
    
    def test_map_string_to_upper(self):
        """Преобразование строк в верхний регистр"""
        words = ["hello", "world", "python"]
        result = list(map(str.upper, words))
        self.assertEqual(result, ["HELLO", "WORLD", "PYTHON"])
    
    def test_map_add_constant(self):
        """Добавление константы к каждому числу"""
        numbers = [1, 2, 3, 4, 5]
        result = list(map(lambda x: x + 10, numbers))
        self.assertEqual(result, [11, 12, 13, 14, 15])
    
    def test_map_multiple_lists(self):
        """Map с несколькими списками"""
        list1 = [1, 2, 3]
        list2 = [4, 5, 6]
        result = list(map(lambda x, y: x + y, list1, list2))
        self.assertEqual(result, [5, 7, 9])
    
    def test_map_string_length(self):
        """Получение длины каждой строки"""
        words = ["cat", "elephant", "dog", "butterfly"]
        result = list(map(len, words))
        self.assertEqual(result, [3, 7, 3, 8])
    
    def test_map_type_conversion(self):
        """Преобразование типов данных"""
        strings = ["1", "2", "3", "4", "5"]
        result = list(map(int, strings))
        self.assertEqual(result, [1, 2, 3, 4, 5])
        self.assertTrue(all(isinstance(x, int) for x in result))
    
    def test_map_with_none(self):
        """Map с None (возвращает исходные значения)"""
        items = [1, 2, 3]
        result = list(map(None, items))
        self.assertEqual(result, [1, 2, 3])
    
    # ====== ТЕСТЫ ДЛЯ SORTED ======
    
    def test_sorted_numbers_ascending(self):
        """Сортировка чисел по возрастанию"""
        numbers = [5, 2, 8, 1, 9, 3]
        result = sorted(numbers)
        self.assertEqual(result, [1, 2, 3, 5, 8, 9])
        # Проверка что оригинальный список не изменился
        self.assertEqual(numbers, [5, 2, 8, 1, 9, 3])
    
    def test_sorted_numbers_descending(self):
        """Сортировка чисел по убыванию"""
        numbers = [5, 2, 8, 1, 9, 3]
        result = sorted(numbers, reverse=True)
        self.assertEqual(result, [9, 8, 5, 3, 2, 1])
    
    def test_sorted_strings_alphabetical(self):
        """Сортировка строк в алфавитном порядке"""
        words = ["banana", "apple", "cherry", "date"]
        result = sorted(words)
        self.assertEqual(result, ["apple", "banana", "cherry", "date"])
    
    def test_sorted_strings_by_length(self):
        """Сортировка строк по длине"""
        words = ["cat", "elephant", "dog", "butterfly"]
        result = sorted(words, key=len)
        self.assertEqual(result, ["cat", "dog", "elephant", "butterfly"])
    
    def test_sorted_by_last_character(self):
        """Сортировка по последнему символу"""
        words = ["apple", "banana", "cherry", "date"]
        result = sorted(words, key=lambda x: x[-1])
        self.assertEqual(result, ["banana", "apple", "date", "cherry"])
    
    def test_sorted_complex_objects(self):
        """Сортировка сложных объектов (словарей)"""
        people = [
            {"name": "John", "age": 30},
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 35}
        ]
        result = sorted(people, key=lambda x: x["age"])
        self.assertEqual(result, [
            {"name": "Alice", "age": 25},
            {"name": "John", "age": 30},
            {"name": "Bob", "age": 35}
        ])
    
    def test_sorted_with_duplicates(self):
        """Сортировка с дубликатами"""
        numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5]
        result = sorted(numbers)
        self.assertEqual(result, [1, 1, 2, 3, 4, 5, 5, 6, 9])
    
    def test_sorted_empty_list(self):
        """Сортировка пустого списка"""
        result = sorted([])
        self.assertEqual(result, [])
    
    def test_sorted_mixed_case_strings(self):
        """Сортировка строк с разным регистром"""
        words = ["Banana", "apple", "Cherry", "date"]
        result = sorted(words, key=str.lower)
        self.assertEqual(result, ["apple", "Banana", "Cherry", "date"])


class TestMathFunctions(unittest.TestCase):
    """Тесты для функций из библиотеки math"""
    
    # ====== ТЕСТЫ ДЛЯ PI ======
    
    def test_pi_value(self):
        """Проверка значения PI"""
        self.assertAlmostEqual(math.pi, 3.141592653589793, places=10)
    
    def test_pi_greater_than_3(self):
        """PI больше 3"""
        self.assertGreater(math.pi, 3)
    
    def test_pi_less_than_4(self):
        """PI меньше 4"""
        self.assertLess(math.pi, 4)
    
    def test_pi_precision(self):
        """Проверка точности PI"""
        self.assertAlmostEqual(math.pi * 2, 6.283185307179586, places=10)
    
    # ====== ТЕСТЫ ДЛЯ SQRT ======
    
    def test_sqrt_perfect_squares(self):
        """Квадратный корень из точных квадратов"""
        test_cases = [(4, 2), (9, 3), (16, 4), (25, 5), (100, 10)]
        for number, expected in test_cases:
            with self.subTest(number=number):
                self.assertEqual(math.sqrt(number), expected)
    
    def test_sqrt_imperfect_squares(self):
        """Квадратный корень из неточных квадратов"""
        self.assertAlmostEqual(math.sqrt(2), 1.4142135623730951, places=10)
        self.assertAlmostEqual(math.sqrt(3), 1.7320508075688772, places=10)
        self.assertAlmostEqual(math.sqrt(5), 2.23606797749979, places=10)
    
    def test_sqrt_zero(self):
        """Квадратный корень из нуля"""
        self.assertEqual(math.sqrt(0), 0)
    
    def test_sqrt_one(self):
        """Квадратный корень из единицы"""
        self.assertEqual(math.sqrt(1), 1)
    
    def test_sqrt_negative_raises_error(self):
        """Квадратный корень из отрицательного числа вызывает ошибку"""
        with self.assertRaises(ValueError):
            math.sqrt(-1)
    
    def test_sqrt_large_number(self):
        """Квадратный корень из большого числа"""
        result = math.sqrt(1000000)
        self.assertEqual(result, 1000)
    
    # ====== ТЕСТЫ ДЛЯ POW ======
    
    def test_pow_simple(self):
        """Возведение в степень (простые случаи)"""
        test_cases = [(2, 3, 8), (3, 2, 9), (5, 0, 1), (10, 1, 10)]
        for base, exp, expected in test_cases:
            with self.subTest(base=base, exp=exp):
                self.assertEqual(math.pow(base, exp), expected)
    
    def test_pow_negative_exponent(self):
        """Возведение в отрицательную степень"""
        self.assertAlmostEqual(math.pow(2, -1), 0.5)
        self.assertAlmostEqual(math.pow(4, -2), 0.0625)
    
    def test_pow_fractional_exponent(self):
        """Возведение в дробную степень"""
        self.assertAlmostEqual(math.pow(9, 0.5), 3.0)
        self.assertAlmostEqual(math.pow(27, 1/3), 3.0)
    
    def test_pow_negative_base(self):
        """Возведение отрицательного числа в степень"""
        self.assertEqual(math.pow(-2, 3), -8)
        self.assertEqual(math.pow(-2, 2), 4)
    
    def test_pow_zero_base(self):
        """Ноль в степени"""
        self.assertEqual(math.pow(0, 5), 0)
        self.assertEqual(math.pow(0, 0), 1.0)  # Математически 0^0 = 1
    
    def test_pow_one_base(self):
        """Единица в любой степени"""
        self.assertEqual(math.pow(1, 100), 1)
        self.assertEqual(math.pow(1, -5), 1)
    
    # ====== ТЕСТЫ ДЛЯ HYPOT ======
    
    def test_hypot_simple(self):
        """Гипотенуза простых треугольников"""
        test_cases = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(math.hypot(a, b), expected)
    
    def test_hypot_equal_legs(self):
        """Гипотенуза при равных катетах"""
        result = math.hypot(1, 1)
        self.assertAlmostEqual(result, math.sqrt(2))
    
    def test_hypot_zero(self):
        """Гипотенуза с нулевым катетом"""
        self.assertEqual(math.hypot(5, 0), 5)
        self.assertEqual(math.hypot(0, 5), 5)
    
    def test_hypot_negative_values(self):
        """Гипотенуза с отрицательными значениями"""
        self.assertEqual(math.hypot(-3, -4), 5)
        self.assertEqual(math.hypot(-3, 4), 5)
        self.assertEqual(math.hypot(3, -4), 5)
    
    def test_hypot_three_dimensions(self):
        """Гипотенуза в трехмерном пространстве"""
        # hypot также принимает более 2 аргументов
        result = math.hypot(2, 3, 6)
        self.assertEqual(result, 7)  # sqrt(4 + 9 + 36) = 7
    
    def test_hypot_large_numbers(self):
        """Гипотенуза с большими числами"""
        result = math.hypot(3000, 4000)
        self.assertEqual(result, 5000)
    
    def test_hypot_commutative(self):
        """Проверка коммутативности"""
        self.assertEqual(math.hypot(3, 4), math.hypot(4, 3))
    
    def test_hypot_precision(self):
        """Проверка точности вычислений"""
        result = math.hypot(0.3, 0.4)
        self.assertAlmostEqual(result, 0.5, places=10)


class TestCombinedFunctions(unittest.TestCase):
    """Тесты для комбинаций функций"""
    
    def test_filter_map_combination(self):
        """Комбинация filter и map"""
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # Отфильтровать четные и возвести их в квадрат
        result = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))
        self.assertEqual(result, [4, 16, 36, 64, 100])
    
    def test_map_sorted_combination(self):
        """Комбинация map и sorted"""
        words = ["banana", "apple", "cherry", "date"]
        # Получить длины строк и отсортировать
        result = sorted(map(len, words))
        self.assertEqual(result, [4, 5, 6, 6])
    
    def test_math_combination_pythagorean(self):
        """Проверка теоремы Пифагора с использованием math функций"""
        a, b = 3, 4
        c = math.hypot(a, b)
        self.assertEqual(c, 5)
        self.assertAlmostEqual(math.pow(c, 2), math.pow(a, 2) + math.pow(b, 2))
    
    def test_math_combination_circle_area(self):
        """Вычисление площади круга"""
        radius = 5
        area = math.pi * math.pow(radius, 2)
        self.assertAlmostEqual(area, 78.53981633974483, places=10)


if __name__ == '__main__':
    unittest.main()
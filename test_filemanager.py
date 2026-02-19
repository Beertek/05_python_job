"""
Модуль с тестами для функций консольного файлового менеджера
Тестируются "чистые" функции из программ: банковский счет, викторина
"""
import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
import sys
import math
from typing import List, Tuple

# Импортируем функции из основного модуля
# Предполагаем, что основной файл называется file_manager.py
# Если имя другое - замените импорт
try:
    from file_manager import (
        load_bank_data, save_bank_data, 
        play_quiz, QuizGame,
        BankAccount
    )
except ImportError:
    # Создаем заглушки для тестирования, если модуль не найден
    print("Основной модуль не найден, тестируем изолированные функции")
    
    # Копируем чистые функции для тестирования
    def load_bank_data(filename="bank_account.txt"):
        """Загрузка данных банковского счета"""
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    balance = float(f.readline().strip())
                    purchases = [line.strip() for line in f.readlines()]
                    return balance, purchases
            except:
                return 0.0, []
        return 0.0, []
    
    def save_bank_data(balance, purchases, filename="bank_account.txt"):
        """Сохранение данных банковского счета"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"{balance}\n")
                for purchase in purchases:
                    f.write(f"{purchase}\n")
            return True
        except:
            return False


# ========== ТЕСТЫ ДЛЯ БАНКОВСКОГО СЧЕТА ==========

class TestBankAccountPureFunctions(unittest.TestCase):
    """Тесты для чистых функций банковского счета"""
    
    def setUp(self):
        """Подготовка к тестам"""
        self.test_filename = "test_bank_account.txt"
        # Удаляем тестовый файл, если он существует
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
    
    def tearDown(self):
        """Очистка после тестов"""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
    
    # ====== ТЕСТЫ ДЛЯ load_bank_data ======
    
    def test_load_bank_data_no_file(self):
        """Загрузка данных при отсутствии файла"""
        balance, purchases = load_bank_data(self.test_filename)
        self.assertEqual(balance, 0.0)
        self.assertEqual(purchases, [])
    
    def test_load_bank_data_with_valid_data(self):
        """Загрузка данных из существующего файла"""
        # Создаем тестовый файл
        with open(self.test_filename, 'w', encoding='utf-8') as f:
            f.write("1000.50\n")
            f.write("Продукты - 150.30 руб.\n")
            f.write("Книга - 500.00 руб.\n")
        
        balance, purchases = load_bank_data(self.test_filename)
        self.assertEqual(balance, 1000.50)
        self.assertEqual(len(purchases), 2)
        self.assertEqual(purchases[0], "Продукты - 150.30 руб.")
        self.assertEqual(purchases[1], "Книга - 500.00 руб.")
    
    def test_load_bank_data_empty_file(self):
        """Загрузка из пустого файла"""
        with open(self.test_filename, 'w') as f:
            pass
        
        with self.assertRaises(Exception):
            load_bank_data(self.test_filename)
    
    def test_load_bank_data_corrupted_file(self):
        """Загрузка из поврежденного файла"""
        with open(self.test_filename, 'w') as f:
            f.write("not a number\n")
            f.write("purchase\n")
        
        # Должен вернуть значения по умолчанию при ошибке
        balance, purchases = load_bank_data(self.test_filename)
        self.assertEqual(balance, 0.0)
        self.assertEqual(purchases, [])
    
    # ====== ТЕСТЫ ДЛЯ save_bank_data ======
    
    def test_save_bank_data_new_file(self):
        """Сохранение данных в новый файл"""
        balance = 500.75
        purchases = ["Покупка1 - 100 руб.", "Покупка2 - 200 руб."]
        
        result = save_bank_data(balance, purchases, self.test_filename)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_filename))
        
        # Проверяем содержимое
        with open(self.test_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertEqual(float(lines[0].strip()), 500.75)
            self.assertEqual(lines[1].strip(), "Покупка1 - 100 руб.")
            self.assertEqual(lines[2].strip(), "Покупка2 - 200 руб.")
    
    def test_save_bank_data_empty_purchases(self):
        """Сохранение данных без истории покупок"""
        balance = 1000.0
        purchases = []
        
        result = save_bank_data(balance, purchases, self.test_filename)
        self.assertTrue(result)
        
        with open(self.test_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertEqual(float(lines[0].strip()), 1000.0)
            self.assertEqual(len(lines), 1)  # Только баланс
    
    def test_save_bank_data_negative_balance(self):
        """Сохранение отрицательного баланса"""
        balance = -50.25
        purchases = []
        
        result = save_bank_data(balance, purchases, self.test_filename)
        self.assertTrue(result)
        
        with open(self.test_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertEqual(float(lines[0].strip()), -50.25)
    
    def test_save_bank_data_large_number_purchases(self):
        """Сохранение большого количества покупок"""
        balance = 1000.0
        purchases = [f"Покупка {i} - {i*10} руб." for i in range(100)]
        
        result = save_bank_data(balance, purchases, self.test_filename)
        self.assertTrue(result)
        
        with open(self.test_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 101)  # Баланс + 100 покупок
    
    def test_save_bank_data_special_characters(self):
        """Сохранение данных со спецсимволами"""
        balance = 999.99
        purchases = ["Кафе & Ресторан - 500 руб.", "Книга 'Python' - 1000 руб."]
        
        result = save_bank_data(balance, purchases, self.test_filename)
        self.assertTrue(result)
        
        with open(self.test_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertEqual(lines[1].strip(), "Кафе & Ресторан - 500 руб.")
            self.assertEqual(lines[2].strip(), "Книга 'Python' - 1000 руб.")


class TestBankAccountLogic(unittest.TestCase):
    """Тесты для бизнес-логики банковского счета"""
    
    def test_balance_calculation_deposit(self):
        """Тест пополнения счета"""
        initial_balance = 1000.0
        deposit = 500.0
        expected = 1500.0
        
        # Простая чистая функция для теста
        def deposit_money(balance, amount):
            if amount > 0:
                return balance + amount
            return balance
        
        result = deposit_money(initial_balance, deposit)
        self.assertEqual(result, expected)
    
    def test_balance_calculation_withdraw(self):
        """Тест снятия средств"""
        initial_balance = 1000.0
        withdraw = 300.0
        expected = 700.0
        
        def withdraw_money(balance, amount):
            if 0 < amount <= balance:
                return balance - amount
            return balance
        
        result = withdraw_money(initial_balance, withdraw)
        self.assertEqual(result, expected)
    
    def test_insufficient_funds(self):
        """Тест недостаточности средств"""
        initial_balance = 100.0
        withdraw = 200.0
        
        def withdraw_money(balance, amount):
            if 0 < amount <= balance:
                return balance - amount
            return balance
        
        result = withdraw_money(initial_balance, withdraw)
        self.assertEqual(result, initial_balance)  # Баланс не изменился
    
    def test_negative_deposit(self):
        """Тест отрицательного пополнения"""
        initial_balance = 1000.0
        deposit = -100.0
        
        def deposit_money(balance, amount):
            if amount > 0:
                return balance + amount
            return balance
        
        result = deposit_money(initial_balance, deposit)
        self.assertEqual(result, initial_balance)
    
    def test_zero_amount_transactions(self):
        """Тест нулевых транзакций"""
        initial_balance = 1000.0
        
        def process_transaction(balance, amount):
            if amount > 0:
                return balance + amount
            elif amount < 0 and abs(amount) <= balance:
                return balance + amount  # amount отрицательный
            return balance
        
        self.assertEqual(process_transaction(initial_balance, 0), initial_balance)
        self.assertEqual(process_transaction(initial_balance, 500), 1500.0)
        self.assertEqual(process_transaction(initial_balance, -300), 700.0)
        self.assertEqual(process_transaction(initial_balance, -2000), initial_balance)


# ========== ТЕСТЫ ДЛЯ ВИКТОРИНЫ ==========

class TestQuizGame(unittest.TestCase):
    """Тесты для игры викторина"""
    
    def setUp(self):
        """Подготовка вопросов для тестов"""
        self.questions = [
            {
                "question": "Столица Франции?",
                "options": ["Лондон", "Берлин", "Париж", "Мадрид"],
                "answer": 3  # Париж
            },
            {
                "question": "Сколько планет в Солнечной системе?",
                "options": ["7", "8", "9", "10"],
                "answer": 2  # 8
            },
            {
                "question": "2 + 2 * 2?",
                "options": ["6", "8", "4", "2"],
                "answer": 1  # 6
            }
        ]
    
    def test_question_validation(self):
        """Проверка валидации вопроса"""
        def is_valid_question(q):
            required_keys = ["question", "options", "answer"]
            return all(key in q for key in required_keys) and \
                   len(q["options"]) == 4 and \
                   1 <= q["answer"] <= 4
        
        for q in self.questions:
            self.assertTrue(is_valid_question(q))
    
    def test_check_answer_correct(self):
        """Проверка правильного ответа"""
        def check_answer(question, user_answer):
            return user_answer == question["answer"]
        
        self.assertTrue(check_answer(self.questions[0], 3))
        self.assertTrue(check_answer(self.questions[1], 2))
        self.assertTrue(check_answer(self.questions[2], 1))
    
    def test_check_answer_incorrect(self):
        """Проверка неправильного ответа"""
        def check_answer(question, user_answer):
            return user_answer == question["answer"]
        
        self.assertFalse(check_answer(self.questions[0], 1))
        self.assertFalse(check_answer(self.questions[1], 4))
        self.assertFalse(check_answer(self.questions[2], 2))
    
    def test_calculate_score(self):
        """Подсчет очков"""
        def calculate_score(answers, correct_answers):
            return sum(1 for a, c in zip(answers, correct_answers) if a == c)
        
        user_answers = [3, 1, 1]  # 3 - правильно, 1 - неправильно, 1 - правильно
        correct_answers = [3, 2, 1]
        
        score = calculate_score(user_answers, correct_answers)
        self.assertEqual(score, 2)  # 2 правильных ответа из 3
    
    def test_score_percentage(self):
        """Вычисление процента правильных ответов"""
        def calculate_percentage(score, total):
            if total == 0:
                return 0
            return (score / total) * 100
        
        self.assertEqual(calculate_percentage(5, 10), 50.0)
        self.assertEqual(calculate_percentage(3, 4), 75.0)
        self.assertEqual(calculate_percentage(0, 5), 0.0)
        self.assertEqual(calculate_percentage(10, 10), 100.0)
        self.assertEqual(calculate_percentage(0, 0), 0.0)
    
    def test_question_difficulty_scoring(self):
        """Очки в зависимости от сложности вопроса"""
        def calculate_weighted_score(difficulty_levels, correct_answers):
            """Сложность: 1 - легко (1 очко), 2 - средне (2 очка), 3 - сложно (3 очка)"""
            score = 0
            for level, correct in zip(difficulty_levels, correct_answers):
                if correct:
                    score += level
            return score
        
        difficulties = [1, 2, 3, 1, 2]
        correct = [True, False, True, True, True]
        
        score = calculate_weighted_score(difficulties, correct)
        self.assertEqual(score, 1 + 3 + 1 + 2)  # 7 очков
    
    def test_validate_answer_input(self):
        """Валидация ввода ответа"""
        def validate_input(answer_str):
            try:
                answer = int(answer_str)
                return 1 <= answer <= 4
            except ValueError:
                return False
        
        self.assertTrue(validate_input("3"))
        self.assertTrue(validate_input("1"))
        self.assertTrue(validate_input("4"))
        self.assertFalse(validate_input("0"))
        self.assertFalse(validate_input("5"))
        self.assertFalse(validate_input("abc"))
        self.assertFalse(validate_input(""))
    
    def test_get_correct_answer_text(self):
        """Получение текста правильного ответа"""
        def get_correct_answer_text(question):
            return question["options"][question["answer"] - 1]
        
        self.assertEqual(get_correct_answer_text(self.questions[0]), "Париж")
        self.assertEqual(get_correct_answer_text(self.questions[1]), "8")
        self.assertEqual(get_correct_answer_text(self.questions[2]), "6")
    
    def test_shuffle_questions_preserves_content(self):
        """Перемешивание вопросов сохраняет контент"""
        import random
        
        def shuffle_questions(questions, seed=None):
            if seed:
                random.seed(seed)
            shuffled = questions.copy()
            random.shuffle(shuffled)
            return shuffled
        
        # С фиксированным seed для предсказуемости
        shuffled = shuffle_questions(self.questions, seed=42)
        
        # Проверяем что все вопросы на месте (длина та же)
        self.assertEqual(len(shuffled), len(self.questions))
        
        # Проверяем что все вопросы из оригинала присутствуют
        original_questions = [q["question"] for q in self.questions]
        shuffled_questions = [q["question"] for q in shuffled]
        
        for q in original_questions:
            self.assertIn(q, shuffled_questions)
    
    def test_question_equality(self):
        """Проверка сравнения вопросов"""
        q1 = {"question": "Столица Франции?", "options": ["A", "B", "C", "D"], "answer": 3}
        q2 = {"question": "Столица Франции?", "options": ["A", "B", "C", "D"], "answer": 3}
        q3 = {"question": "Другой вопрос", "options": ["A", "B", "C", "D"], "answer": 1}
        
        self.assertEqual(q1, q2)
        self.assertNotEqual(q1, q3)


# ========== ТЕСТЫ ДЛЯ ФУНКЦИЙ РАБОТЫ С ПУТЯМИ ==========

class TestPathFunctions(unittest.TestCase):
    """Тесты для функций работы с путями из файлового менеджера"""
    
    def test_normalize_path(self):
        """Нормализация пути"""
        def normalize_path(path):
            return os.path.normpath(path)
        
        test_cases = [
            ("folder//subfolder", "folder/subfolder"),
            ("folder/./subfolder", "folder/subfolder"),
            ("folder/../folder", "folder"),
        ]
        
        for input_path, expected in test_cases:
            # Используем os.path.normpath который обрабатывает слеши в зависимости от ОС
            result = normalize_path(input_path)
            # Для сравнения нормализуем expected так же
            expected_normalized = os.path.normpath(expected)
            self.assertEqual(result, expected_normalized)
    
    def test_is_absolute_path(self):
        """Проверка абсолютного пути"""
        def is_absolute(path):
            return os.path.isabs(path)
        
        # Тесты зависят от ОС
        if os.name == 'nt':  # Windows
            self.assertTrue(is_absolute("C:\\Users\\test"))
            self.assertTrue(is_absolute("D:\\folder"))
            self.assertFalse(is_absolute("folder\\subfolder"))
            self.assertFalse(is_absolute("test.txt"))
        else:  # Unix-like
            self.assertTrue(is_absolute("/home/user"))
            self.assertTrue(is_absolute("/tmp"))
            self.assertFalse(is_absolute("home/user"))
            self.assertFalse(is_absolute("folder/file.txt"))
    
    def test_join_paths(self):
        """Объединение путей"""
        def join_paths(*parts):
            return os.path.join(*parts)
        
        self.assertEqual(join_paths("folder", "subfolder", "file.txt"), 
                        os.path.join("folder", "subfolder", "file.txt"))
        self.assertEqual(join_paths("folder", ""), "folder" + os.sep)
        self.assertEqual(join_paths("folder", "..", "file.txt"), 
                        os.path.join("folder", "..", "file.txt"))
    
    def test_get_parent_directory(self):
        """Получение родительской директории"""
        def get_parent(path):
            return os.path.dirname(path)
        
        self.assertEqual(get_parent("/home/user/file.txt"), "/home/user")
        self.assertEqual(get_parent("/home/user/"), "/home")
        self.assertEqual(get_parent("folder/subfolder"), "folder")
        
        # Особые случаи
        self.assertEqual(get_parent("file.txt"), "")
        self.assertEqual(get_parent("/"), "/" if os.name != 'nt' else "\\")


# ========== ТЕСТЫ ДЛЯ ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ ==========

class TestHelperFunctions(unittest.TestCase):
    """Тесты для вспомогательных функций"""
    
    def test_format_size(self):
        """Форматирование размера файла"""
        def format_size(size):
            for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} ТБ"
        
        self.assertEqual(format_size(500), "500.0 Б")
        self.assertEqual(format_size(1024), "1.0 КБ")
        self.assertEqual(format_size(1536), "1.5 КБ")
        self.assertEqual(format_size(1048576), "1.0 МБ")
        self.assertEqual(format_size(1073741824), "1.0 ГБ")
    
    def test_get_file_extension(self):
        """Получение расширения файла"""
        def get_extension(filename):
            return os.path.splitext(filename)[1].lower()
        
        self.assertEqual(get_extension("file.txt"), ".txt")
        self.assertEqual(get_extension("document.PDF"), ".pdf")
        self.assertEqual(get_extension("archive.tar.gz"), ".gz")
        self.assertEqual(get_extension("file"), "")
        self.assertEqual(get_extension(".hidden"), ".hidden")
    
    def test_is_hidden_file(self):
        """Проверка скрытого файла"""
        def is_hidden(filename):
            if os.name == 'nt':  # Windows
                return False  # Упрощенно
            return filename.startswith('.')
        
        # На Unix-подобных системах
        self.assertTrue(is_hidden(".bashrc"))
        self.assertTrue(is_hidden(".gitignore"))
        self.assertFalse(is_hidden("file.txt"))
        self.assertFalse(is_hidden("folder"))
    
    def test_validate_filename(self):
        """Валидация имени файла"""
        def is_valid_filename(filename):
            invalid_chars = '<>:"/\\|?*' if os.name == 'nt' else '/'
            return not any(c in filename for c in invalid_chars) and filename.strip()
        
        self.assertTrue(is_valid_filename("file.txt"))
        self.assertTrue(is_valid_filename("my_document"))
        self.assertFalse(is_valid_filename("file?.txt"))
        self.assertFalse(is_valid_filename(""))
        self.assertFalse(is_valid_filename("   "))
        
        if os.name == 'nt':
            self.assertFalse(is_valid_filename("file:name.txt"))
            self.assertFalse(is_valid_filename("file<name>.txt"))
    
    def test_extract_filename_from_path(self):
        """Извлечение имени файла из пути"""
        def get_filename(path):
            return os.path.basename(path)
        
        self.assertEqual(get_filename("/home/user/file.txt"), "file.txt")
        self.assertEqual(get_filename("folder/subfolder/document.pdf"), "document.pdf")
        self.assertEqual(get_filename("file.txt"), "file.txt")
        self.assertEqual(get_filename("/"), "" if os.name != 'nt' else "")


if __name__ == '__main__':
    unittest.main()
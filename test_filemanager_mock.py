"""
Модуль с тестами для "грязных" функций файлового менеджера
с использованием unittest.mock для имитации ввода/вывода
"""
import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Предполагаем что основной модуль называется file_manager.py
try:
    import file_manager as fm
except ImportError:
    print("Основной модуль не найден, тесты с моками пропускаются")
    fm = None


@unittest.skipIf(fm is None, "Модуль file_manager не найден")
class TestFileManagerMocked(unittest.TestCase):
    """Тесты для функций с побочными эффектами с использованием моков"""
    
    def setUp(self):
        """Подготовка к тестам"""
        # Создаем временную директорию для тестов
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        # Сохраняем оригинальную рабочую директорию модуля
        self.original_working_dir = fm.working_directory
        fm.working_directory = self.test_dir
    
    def tearDown(self):
        """Очистка после тестов"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
        fm.working_directory = self.original_working_dir
    
    # ====== ТЕСТЫ С МОКАМИ ДЛЯ СОЗДАНИЯ ПАПКИ ======
    
    @patch('builtins.input', return_value='test_folder')
    @patch('builtins.print')
    def test_create_folder_success(self, mock_print, mock_input):
        """Тест успешного создания папки"""
        fm.create_folder()
        
        # Проверяем что папка создана
        self.assertTrue(os.path.exists('test_folder'))
        self.assertTrue(os.path.isdir('test_folder'))
        
        # Проверяем что было сообщение об успехе
        mock_print.assert_any_call("Папка 'test_folder' успешно создана!")
    
    @patch('builtins.input', return_value='')
    @patch('builtins.print')
    def test_create_folder_empty_name(self, mock_print, mock_input):
        """Тест создания папки с пустым именем"""
        fm.create_folder()
        
        # Проверяем сообщение об ошибке
        mock_print.assert_any_call("Ошибка: Название папки не может быть пустым!")
    
    @patch('builtins.input', return_value='test_folder')
    @patch('builtins.print')
    def test_create_folder_already_exists(self, mock_print, mock_input):
        """Тест создания существующей папки"""
        # Сначала создаем папку
        os.mkdir('test_folder')
        
        # Пытаемся создать снова
        fm.create_folder()
        
        # Проверяем сообщение об ошибке
        mock_print.assert_any_call("Ошибка: Папка 'test_folder' уже существует!")
    
    # ====== ТЕСТЫ С МОКАМИ ДЛЯ УДАЛЕНИЯ ======
    
    @patch('builtins.input', side_effect=['test_file.txt', 'y'])
    @patch('builtins.print')
    def test_delete_file_with_confirmation(self, mock_print, mock_input):
        """Тест удаления файла с подтверждением"""
        # Создаем тестовый файл
        with open('test_file.txt', 'w') as f:
            f.write('test content')
        
        # Мокаем функцию подтверждения
        with patch('builtins.input', return_value='y'):
            fm.delete_item()
        
        # Проверяем что файл удален
        self.assertFalse(os.path.exists('test_file.txt'))
    
    @patch('builtins.input', return_value='nonexistent.txt')
    @patch('builtins.print')
    def test_delete_nonexistent(self, mock_print, mock_input):
        """Тест удаления несуществующего файла"""
        fm.delete_item()
        
        # Проверяем сообщение об ошибке
        mock_print.assert_any_call("Ошибка: 'nonexistent.txt' не найден!")
    
    @patch('builtins.input', side_effect=['test_folder'])
    @patch('builtins.print')
    def test_delete_folder(self, mock_print, mock_input):
        """Тест удаления папки"""
        os.mkdir('test_folder')
        
        fm.delete_item()
        
        # Проверяем что папка удалена
        self.assertFalse(os.path.exists('test_folder'))
    
    # ====== ТЕСТЫ С МОКАМИ ДЛЯ КОПИРОВАНИЯ ======
    
    @patch('builtins.input', side_effect=['source.txt', 'dest.txt'])
    @patch('builtins.print')
    def test_copy_file(self, mock_print, mock_input):
        """Тест копирования файла"""
        # Создаем исходный файл
        with open('source.txt', 'w') as f:
            f.write('test content')
        
        fm.copy_item()
        
        # Проверяем что файл скопирован
        self.assertTrue(os.path.exists('dest.txt'))
        with open('dest.txt', 'r') as f:
            content = f.read()
        self.assertEqual(content, 'test content')
    
    @patch('builtins.input', side_effect=['source.txt', 'dest.txt'])
    @patch('builtins.print')
    def test_copy_nonexistent_source(self, mock_print, mock_input):
        """Тест копирования несуществующего файла"""
        fm.copy_item()
        
        # Проверяем сообщение об ошибке
        mock_print.assert_any_call("Ошибка: 'source.txt' не найден!")
    
    @patch('builtins.input', side_effect=['source.txt', ''])
    @patch('builtins.print')
    def test_copy_empty_destination(self, mock_print, mock_input):
        """Тест копирования с пустым именем назначения"""
        with open('source.txt', 'w') as f:
            f.write('test')
        
        fm.copy_item()
        
        # Проверяем сообщение об ошибке
        mock_print.assert_any_call("Ошибка: Новое имя не может быть пустым!")
    
    # ====== ТЕСТЫ ДЛЯ ПРОСМОТРА СОДЕРЖИМОГО ======
    
    def test_list_contents_with_items(self):
        """Тест просмотра содержимого с элементами"""
        # Создаем тестовые файлы и папки
        os.mkdir('test_folder')
        with open('test_file.txt', 'w') as f:
            f.write('content')
        
        with patch('builtins.print') as mock_print:
            fm.list_contents()
            
            # Проверяем что были выведены элементы
            mock_print.assert_any_call("  1. 📁 test_folder")
            mock_print.assert_any_call("  2. 📄 test_file.txt")
    
    def test_list_contents_empty(self):
        """Тест просмотра пустой директории"""
        with patch('builtins.print') as mock_print:
            fm.list_contents()
            mock_print.assert_any_call("Директория пуста")
    
    # ====== ТЕСТЫ ДЛЯ СМЕНЫ ДИРЕКТОРИИ ======
    
    @patch('builtins.input', return_value='subfolder')
    @patch('builtins.print')
    def test_change_directory_relative(self, mock_print, mock_input):
        """Тест смены директории на относительный путь"""
        os.mkdir('subfolder')
        original_wd = fm.working_directory
        
        fm.change_directory()
        
        # Проверяем что директория изменилась
        expected_path = os.path.join(original_wd, 'subfolder')
        self.assertEqual(fm.working_directory, expected_path)
    
    @patch('builtins.input', return_value='..')
    @patch('builtins.print')
    def test_change_directory_parent(self, mock_print, mock_input):
        """Тест перехода в родительскую директорию"""
        # Создаем подпапку и переходим в нее
        os.mkdir('subfolder')
        fm.working_directory = os.path.join(fm.working_directory, 'subfolder')
        
        fm.change_directory()
        
        # Проверяем что вернулись в родительскую
        self.assertEqual(fm.working_directory, self.test_dir)
    
    @patch('builtins.input', return_value='nonexistent')
    @patch('builtins.print')
    def test_change_directory_nonexistent(self, mock_print, mock_input):
        """Тест перехода в несуществующую директорию"""
        fm.change_directory()
        
        # Проверяем сообщение об ошибке
        mock_print.assert_any_call("❌ Путь не существует или не является папкой!")
        # Директория не должна измениться
        self.assertEqual(fm.working_directory, self.test_dir)


@unittest.skipIf(fm is None, "Модуль file_manager не найден")
class TestBankAccountMocked(unittest.TestCase):
    """Тесты для функций банковского счета с моками"""
    
    def setUp(self):
        """Подготовка к тестам"""
        self.test_filename = "test_bank_account.txt"
        # Сохраняем оригинальную константу
        if hasattr(fm, 'BANK_ACCOUNT_FILE'):
            self.original_filename = fm.BANK_ACCOUNT_FILE
            fm.BANK_ACCOUNT_FILE = self.test_filename
    
    def tearDown(self):
        """Очистка после тестов"""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
        if hasattr(self, 'original_filename'):
            fm.BANK_ACCOUNT_FILE = self.original_filename
    
    @patch('builtins.input', side_effect=['1', '500', '4'])  # Пополнение на 500, затем выход
    @patch('builtins.print')
    def test_bank_account_deposit(self, mock_print, mock_input):
        """Тест пополнения счета"""
        # Создаем файл с начальным балансом
        with open(self.test_filename, 'w') as f:
            f.write("1000.0\n")
        
        fm.bank_account()
        
        # Проверяем что баланс обновился
        with open(self.test_filename, 'r') as f:
            balance = float(f.readline().strip())
            self.assertEqual(balance, 1500.0)
    
    @patch('builtins.input', side_effect=['2', '300', 'Книга', '4'])  # Покупка, затем выход
    @patch('builtins.print')
    def test_bank_account_purchase(self, mock_print, mock_input):
        """Тест совершения покупки"""
        with open(self.test_filename, 'w') as f:
            f.write("1000.0\n")
        
        fm.bank_account()
        
        # Проверяем баланс и историю
        with open(self.test_filename, 'r') as f:
            lines = f.readlines()
            balance = float(lines[0].strip())
            self.assertEqual(balance, 700.0)
            self.assertTrue(any("Книга" in line for line in lines))
    
    @patch('builtins.input', side_effect=['2', '2000', '4'])  # Покупка дороже баланса
    @patch('builtins.print')
    def test_bank_account_insufficient_funds(self, mock_print, mock_input):
        """Тест недостаточности средств"""
        with open(self.test_filename, 'w') as f:
            f.write("1000.0\n")
        
        fm.bank_account()
        
        # Баланс не должен измениться
        with open(self.test_filename, 'r') as f:
            balance = float(f.readline().strip())
            self.assertEqual(balance, 1000.0)
        
        # Проверяем что было сообщение об ошибке
        mock_print.assert_any_call("❌ Недостаточно средств!")
    
    @patch('builtins.input', side_effect=['3', '4'])  # Просмотр истории, затем выход
    @patch('builtins.print')
    def test_bank_account_view_history(self, mock_print, mock_input):
        """Тест просмотра истории покупок"""
        with open(self.test_filename, 'w') as f:
            f.write("1000.0\n")
            f.write("Книга - 300.0 руб.\n")
            f.write("Еда - 200.0 руб.\n")
        
        fm.bank_account()
        
        # Проверяем что история была выведена
        mock_print.assert_any_call("1. Книга - 300.0 руб.")
        mock_print.assert_any_call("2. Еда - 200.0 руб.")


if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import Mock, patch
from aiogram import types
from main import dp, start, process_user_type, process_age, process_location, process_nickname, process_description

class TestTelegramBot(unittest.TestCase):
    
    def test_start_command(self):
        message = Mock(spec=types.Message)
        message.from_user.id = 123
        message.from_user.username = "test_user"
        message.from_user.first_name = "Test"
        state = Mock()
        with patch("main.add_user_to_db_type_user") as mock_add_user:
            start(message, state)
            mock_add_user.assert_called_once_with(message, 123, "Test", "test_user", None)
            # Проверяем, что функция add_user_to_db_type_user вызывается с правильными аргументами
            
    def test_process_user_type_job_seeker(self):
        callback_query = Mock(spec=types.CallbackQuery)
        callback_query.data = "job_seeker"
        state = Mock()
        with patch("main.add_user_to_db_type_user") as mock_add_user:
            process_user_type(callback_query, state)
            mock_add_user.assert_called_once()
            # Проверяем, что функция add_user_to_db_type_user вызывается при выборе типа job_seeker

    def test_process_user_type_employer(self):
        callback_query = Mock(spec=types.CallbackQuery)
        callback_query.data = "employer"
        state = Mock()
        with patch("main.add_user_to_db_type_employer") as mock_add_employer:
            process_user_type(callback_query, state)
            mock_add_employer.assert_called_once()
            # Проверяем, что функция add_user_to_db_type_employer вызывается при выборе типа employer

    def test_process_age(self):
        message = Mock(spec=types.Message)
        message.text = "25"
        state = Mock()
        with patch("main.update_user_age") as mock_update_age:
            process_age(message, state)
            mock_update_age.assert_called_once_with(message.from_user.id, "25")
            # Проверяем, что функция update_user_age вызывается с правильными аргументами

    def test_process_location(self):
        message = Mock(spec=types.Message)
        message.text = "Санкт-Петербург"
        state = Mock()
        with patch("main.update_user_location") as mock_update_location:
            process_location(message, state)
            mock_update_location.assert_called_once_with(message.from_user.id, "Санкт-Петербург")
            # Проверяем, что функция update_user_location вызывается с правильными аргументами

    def test_process_nickname(self):
        message = Mock(spec=types.Message)
        message.text = "John"
        state = Mock()
        with patch("main.update_user_name") as mock_update_name:
            process_nickname(message, state)
            mock_update_name.assert_called_once_with(message.from_user.id, "John")
            # Проверяем, что функция update_user_name вызывается с правильными аргументами

    def test_process_description(self):
        message = Mock(spec=types.Message)
        message.text = "I am a software developer."
        state = Mock()
        with patch("main.update_user_description") as mock_update_description:
            process_description(message, state)
            mock_update_description.assert_called_once_with(message.from_user.id, "I am a software developer.")
            # Проверяем, что функция update_user_description вызывается с правильными аргументами

    # Добавьте больше тестов для других функций

if __name__ == '__main__':
    unittest.main()

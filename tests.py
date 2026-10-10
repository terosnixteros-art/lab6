import unittest
from main import ScheduleService, ScheduleItem, MemoryNotifier, EmailStub


class ScheduleServiceTests(unittest.TestCase):
    
    def test_notification_sent_via_memory_notifier(self):
        """Тест 1: Уведомление успешно сохраняется в MemoryNotifier."""
        notifier = MemoryNotifier()
        service = ScheduleService(notifier)
        service.register_subscriber("Алексей")
        
        item = ScheduleItem("Парадигмы программирования", "Ауд. 305", "10:00")
        service.notify_schedule_change(item)
        
        self.assertEqual(len(notifier.messages), 1)
        self.assertEqual(notifier.messages[0][0], "Алексей")
        self.assertIn("Ауд. 305", notifier.messages[0][1])

    def test_notification_sent_via_email_stub(self):
        """Тест 2: Взаимозаменяемость каналов (проверка EmailStub)."""
        notifier = EmailStub()
        service = ScheduleService(notifier)
        service.register_subscriber("student@iatu.kz")
        
        item = ScheduleItem("Базы данных", "Ауд. 102", "12:00")
        service.notify_schedule_change(item)
        
        self.assertEqual(len(notifier.sent_emails), 1)
        self.assertEqual(notifier.sent_emails[0][0], "student@iatu.kz")

    def test_empty_subscriber_list_raises_error(self):
        """Тест 3 (Ошибочный сценарий): Отправка без подписчиков вызывает ошибку."""
        service = ScheduleService(MemoryNotifier())
        item = ScheduleItem("Физика", "Ауд. 204", "14:00")
        
        with self.assertRaises(LookupError):
            service.notify_schedule_change(item)

    def test_duplicate_subscriber_raises_error(self):
        """Тест 4 (Ошибочный сценарий): Повторная регистрация вызывает ValueError."""
        service = ScheduleService(MemoryNotifier())
        service.register_subscriber("Иван")
        
        with self.assertRaises(ValueError):
            service.register_subscriber("Иван")

    def test_invalid_schedule_item_raises_error(self):
        """Тест 5 (Ошибочный сценарий): Пустые данные расписания вызывают ValueError."""
        with self.assertRaises(ValueError):
            ScheduleItem("", "Ауд. 101", "09:00")

    def test_multiple_subscribers_received_notification(self):
        """Тест 6: Рассылка корректно доходит до нескольких получателей."""
        notifier = MemoryNotifier()
        service = ScheduleService(notifier)
        service.register_subscriber("Алиса")
        service.register_subscriber("Борис")
        
        item = ScheduleItem("Математика", "Онлайн", "08:30")
        service.notify_schedule_change(item)
        
        self.assertEqual(len(notifier.messages), 2)
        recipients = [m[0] for m in notifier.messages]
        self.assertIn("Алиса", recipients)
        self.assertIn("Борис", recipients)


if __name__ == "__main__":
    unittest.main()

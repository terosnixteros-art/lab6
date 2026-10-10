from typing import Protocol


# Шаг 1. Определение контракта через Protocol
class Notifier(Protocol):
    """Контракт для каналов отправки уведомлений."""
    def send(self, recipient: str, message: str) -> None:
        """Отправляет сообщение получателю."""
        ...


# Шаг 2. Реализация полиморфных каналов
class ConsoleNotifier:
    """Вывод уведомлений в консоль."""
    def send(self, recipient: str, message: str) -> None:
        print(f"[Console] Кому: {recipient} | Сообщение: {message}")


class EmailStub:
    """Заглушка для отправки по электронной почте."""
    def __init__(self):
        self.sent_emails = []

    def send(self, recipient: str, message: str) -> None:
        self.sent_emails.append((recipient, message))


class MemoryNotifier:
    """Тестовый дублёр для сохранения сообщений в памяти."""
    def __init__(self):
        self.messages = []

    def send(self, recipient: str, message: str) -> None:
        self.messages.append((recipient, message))


# Модель расписания
class ScheduleItem:
    """Класс для представления информации об изменении в расписании."""
    def __init__(self, course_name: str, room: str, time: str):
        if not course_name.strip():
            raise ValueError("Название дисциплины не может быть пустым.")
        if not room.strip():
            raise ValueError("Аудитория не может быть пустой.")
        if not time.strip():
            raise ValueError("Время не может быть пустым.")
        
        self.course_name = course_name.strip()
        self.room = room.strip()
        self.time = time.strip()


# Шаг 3 & 4. Сервис расписания с использованием композиции
class ScheduleService:
    """Сервис управления расписанием, использующий композицию с Notifier."""
    def __init__(self, notifier: Notifier):
        self._notifier = notifier
        self._subscribers = []

    def register_subscriber(self, email_or_name: str) -> None:
        """Регистрирует получателя рассылки."""
        if not email_or_name.strip():
            raise ValueError("Имя или адрес получателя некорректны.")
        if email_or_name in self._subscribers:
            raise ValueError("Получатель уже подписан.")
        self._subscribers.append(email_or_name.strip())

    def notify_schedule_change(self, item: ScheduleItem) -> None:
        """Уведомляет всех подписчиков об изменении расписания."""
        if not self._subscribers:
            raise LookupError("Нет зарегистрированных получателей для уведомления.")
        
        message = (
            f"Изменение по предмету '{item.course_name}': "
            f"новая аудитория — {item.room}, время — {item.time}."
        )
        for recipient in self._subscribers:
            self._notifier.send(recipient, message)

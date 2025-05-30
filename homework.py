"""Программный модуль фитнес-трекера обрабатывает данные для
трёх видов тренировок: бега, спортивной ходьбы и плавания.
Модуль выполняет функции:
Принимает от блока датчиков информацию о прошедшей тренировке;
определяет вид тренировки, рассчитывает результаты тренировки;
выводит информационное сообщение о результатах тренировки.
"""
import dataclasses
import typing


@dataclasses.dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MSG = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Верни строку сообщения."""
        return self.MSG.format(**dataclasses.asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000.0
    MIN_IN_H = 60.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получи дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получи среднюю скорость движения в км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получи количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Верни информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18.0
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получи количество затраченных калорий."""
        return (
            self.CALORIES_MEAN_SPEED_MULTIPLIER
            * self.get_mean_speed()
            + self.CALORIES_MEAN_SPEED_SHIFT
        ) * (
            self.weight / self.M_IN_KM
        ) * (
            self.duration * self.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получи количество затраченных калорий."""
        return (
            self.CALORIES_WEIGHT_MULTIPLIER * self.weight + (
                (
                    (self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                ) / (
                    self.height / self.CM_IN_M
                )
            )
            * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
            * self.weight
        ) * self.duration * self.MIN_IN_H


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    EXTRA_MEAN_SPEED = 1.1
    MEAN_SPEED_MULTIPLIER = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получи среднюю скорость движения."""
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получи количество затраченных калорий."""
        mean_speed = self.get_mean_speed() + self.EXTRA_MEAN_SPEED
        return (
            mean_speed
            * self.MEAN_SPEED_MULTIPLIER
            * self.weight
            * self.duration
        )


def read_package(
    workout_type: str, data: typing.List[typing.Union[int, float]],
) -> Training:
    """Верни данные полученные от датчиков."""
    WORKOUT_TO_CLASS: typing.Dict[str, typing.Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    try:
        return WORKOUT_TO_CLASS[workout_type](*data)
    except ValueError:
        raise ValueError(f'«{workout_type}» - от датчиков устройства '
                         'получен неизвестный код тренировки.')


def main(training: Training):
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

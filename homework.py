class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return(f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:0.3f} ч.; '
               f'Дистанция: {self.distance:0.3f} км; '
               f'Ср. скорость: {self.speed:0.3f} км/ч; '
               f'Потрачено ккал: {self.calories:0.3f}.')


class Training:
    LEN_STEP = 0.65
    M_IN_KM = 1000
    """Базовый класс тренировки."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        total_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return total_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий бег."""
        duration_in_min = self.duration * 60
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        spent_calories = ((coeff_calorie_1 * self.get_mean_speed()
                          - coeff_calorie_2) * self.weight
                          / self.M_IN_KM * duration_in_min)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество калорий спортивная ходьба."""
        duration_in_min = self.duration * 60
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 2
        coeff_calorie_3 = 0.029
        spent_calories = ((coeff_calorie_1 * self.weight
                          + (self.get_mean_speed()**coeff_calorie_2
                           // self.height) * coeff_calorie_3 * self.weight)
                          * duration_in_min)
        return spent_calories


class Swimming(Training):
    LEN_STEP = 1.38
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight,)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        total_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return total_distance

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        coeff_calorie1 = 1.1
        coeff_calorie2 = 2
        spent_calories = ((self.get_mean_speed() + coeff_calorie1)
                          * coeff_calorie2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train: dict = {'SWM': Swimming,
                   'RUN': Running,
                   'WLK': SportsWalking}
    return train[workout_type](*data)



def main(training: Training) -> None:
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

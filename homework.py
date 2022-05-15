# doc style: https://numpydoc.readthedocs.io/en/latest/index.html

class InfoMessage:
    """ Class to arrange training results

    Methods
    -------
    get_message()
        return final string - result of the training
    """

    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """ Function to return training results string
        """
        return f'''Тип тренировки: {self.training_type}; Длительность: {self.duration:.2f} ч.;
        Дистанция: {self.distance:.2f} км; Ср. скорость: {self.speed:.2f} км/ч;
        Потрачено ккал: {self.calories:.2f}.'''


class Training:
    """
    Base class to process training

    ...

    Attributes
    ----------
    action: float
        Number of made actions: steps for walking and rowing for swimming
    duration: float
        Duration of the training (hours)
    weight: float
        Weight of the athlete
    len_step: foat
        Distance covered within one action

    Methods
    -------
    get_distance()
        Return distance covered for the training
    get_mean_speed()
        Return mean speed
    get_spend_calories()
        Return сalories burned
    show_training_info()
        Create InfoMessage with results of the training
    """
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def __init__(self, action: int, duration: float,
                 weight: float, len_step: float = 0.65) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.len_step = len_step

    def get_distance(self) -> float:
        distance_covered = self.action * self.len_step / self.M_IN_KM
        return distance_covered

    def get_mean_speed(self) -> float:
        distance_covered = self.get_distance()
        mean_speed = distance_covered / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """ Child class of training with changed "get_spent_calories" function
    """
    def get_spent_calories(self) -> float:
        """ get calories spent within formula
        """
        mean_speed = self.get_mean_speed()

        # all hardcoded values - empirical data
        calories_spent = ((18 * mean_speed - 20) * self.weight
                          / self.M_IN_KM * (self.duration * self.MIN_IN_HOUR))
        return calories_spent


class SportsWalking(Training):
    """ Child class of training with changed "get_spent_calories" function and
    added attribute "height"
    """
    def __init__(self, action: int, duration:
                 float, weight: float, height: float):
        super().__init__(action, duration, weight, len_step=0.65)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()

        # all hardcoded values - empirical data
        calories_spent = ((0.035 * self.weight
                          + (mean_speed**2 // self.height)
                          * 0.029 * self.weight)
                          * (self.duration * self.MIN_IN_HOUR))
        return calories_spent


class Swimming(Training):
    """ Child class of training with changed "get_spent_calories" and
    "get_mean_speed" functions.
    Also attributes "length_pool" and "count_pool" were added
    """
    len_step = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed_swimming = (self.length_pool * self.count_pool
                               / self.M_IN_KM
                               / (self.duration * self.MIN_IN_HOUR))
        return mean_speed_swimming

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()

        # all hardcoded values - empirical data
        calories_spent = (mean_speed + 1.1) * 2 * self.weight
        return calories_spent


if __name__ == '__main__':
    from typing import Sequence

    def read_package(workout_type: str, data: Sequence[str]):
        if workout_type == 'SWM':
            class_instance = Swimming(*data)
        elif workout_type == 'RUN':
            class_instance = Running(*data)
        elif workout_type == 'WLK':
            class_instance = SportsWalking(*data)
        return class_instance

    def main(class_instance: Training):
        info = class_instance.show_training_info()
        print(info.get_message())

    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

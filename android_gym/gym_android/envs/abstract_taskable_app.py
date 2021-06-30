from abc import ABC, abstractmethod


class TaskableApp(ABC):

    def __init__(self, app_name, using_intermediate_rewards, difficulty_level):
        """
        Initialize the app.

        Args:
          app_name: The name of the app
          using_intermediate_rewards: Whether we will assign intermediate rewards for the app
          difficulty_level: The value could be one of the following: easy, medium, hard

        Returns:
           reward: The reward for the current step
           done: True or False. It indicates whether the task has been completed.
        """
        self.app_name = app_name
        self.using_intermediate_rewards = using_intermediate_rewards
        self.difficulty_level = difficulty_level
        self.reward_bookeeping = [False for i in range(0, 10)]
        super().__init__()

    @abstractmethod
    def reset_app(self):
        """
        Reset the app and cleanup the states.
        """
        pass

    @abstractmethod
    def get_reward_for_current_state(self, list_of_ui_objects):
        """
        Given the list of UI objects, return the reward for the current step

        Args:
          list_of_ui_objects: A list of UI objects obtained from the device

        Returns:
           reward: The reward for the current step
           done: True or False. It indicates whether the task has been completed.
        """
        pass

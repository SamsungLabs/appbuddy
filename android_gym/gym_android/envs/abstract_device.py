from abc import ABC, abstractmethod


class AbstractDevice(ABC):

    def __init__(self, device_name: str) -> None:
        self.device_name = device_name
        super().__init__()

    @abstractmethod
    def get_list_of_ui_objects(self, emulator_id: str):
        """Obtain a list of UI objects from the device.

        Args:
          emulator_id: The ID of the emulator.

        Returns:
          A list of UI objects
        """
        pass

    def get_screenshot(self, emulator_id: str):
        """
        Obtain the screenshot of the device

        Args:
          emulator_id: The ID of the emulator

        """
        pass

    def get_app_log(self, emulator_id: str, package_name: str):
        """
        Obtain the related logs for an app on the device

        Args:
          emulator_id: The ID of the emulator
          package_name: The package name of the app

        """
        pass

    @abstractmethod
    def perform_action(self, action, emulator_id: str, state):
        """Obtain a list of UI objects from the device.

        Args:
          action: A list with two elements [index of an UI element, index of a token]
          emulator_id: The ID of the emulator.

        Returns:
          True or False
        """
        pass


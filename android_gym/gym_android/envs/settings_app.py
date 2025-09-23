import os
import time
import traceback
from .abstract_taskable_app import TaskableApp


class SettingsApp(TaskableApp):

    def get_reward_for_current_state(self, list_of_ui_objects):
        """
        This function, given a list of UI objects, returns the reward based on the reward function for the settings app.
        The intermediate_rewards flag determines whether intermediate rewards are considered in the reward function or
        whether only the final state goal is rewarded.

        Below is a high-level description of the tasks for this app:

        Settings - Easy
            - Navigate to Wi-Fi settings screen

        Settings - Medium
            - Navigate to add new Wi-Fi network screen

        Settings - Hard
            - Navigate to add new Wi-Fi network screen and add a new network called Starbucks

        Below is a description of the rewards (including the intermediate rewards) given to the agent
        in each difficulty level of the settings task.

        Settings - Easy
            – No intermediate rewards

        Settings - Medium
            – The agent is rewarded after navigating to Wi-Fi settings screen

        Settings - Hard
            – The agent is rewarded after navigating to Wi-Fi settings screen and after navigating to
              add new Wi-Fi network screen

        Note that an intermediate reward may only be given once in an episode.
        The variables in the reward_bookeeping array enforce this.
        The conditionals in this function check whether or not these variables already hold.
        Empirical evidence suggests that this mitigates for reward hacking.
        """

        reward = 0
        done = False

        for elem in list_of_ui_objects:
            if elem.text is not None and elem.obj_name is not None:
                if self.using_intermediate_rewards:
                    if self.difficulty_level == "hard":
                        if elem.text.strip().lower() == 'Enter the SSID'.lower() and not self.reward_bookeeping[1]:
                            print("YAY GOT medium REWARD")
                            reward = 1.5
                            self.reward_bookeeping[1] = True

                    if self.difficulty_level == "medium" or self.difficulty_level == "hard":
                        if elem.obj_name.strip().lower() == 'Wi‑Fi preferences'.lower() and elem.resource_id.strip(
                        ).lower() == 'android:id/title'.lower() and not self.reward_bookeeping[0]:
                            print("YAY GOT small REWARD")
                            reward = 1
                            self.reward_bookeeping[0] = True

                if self.difficulty_level == "easy":
                    if elem.obj_name.strip().lower() == 'Wi‑Fi preferences'.lower(
                    ) and elem.resource_id.strip().lower() == 'android:id/title'.lower():
                        done = True

                if self.difficulty_level == "medium":
                    if elem.text.strip().lower() == 'Enter the SSID'.lower():
                        done = True

                if self.difficulty_level == "hard":
                    if elem.obj_name.strip().lower() == 'Starbucks'.lower(
                    ) and elem.resource_id.strip().lower() == 'com.android.settings:id/ssid'.lower():
                        done = True

                if done:
                    print("YAY GOT BIG REWARD")
                    reward = 10
                    break

        return reward, done

    @staticmethod
    def _restart_settings(emulator_id):

        os.system("adb -s {0} shell pm clear com.android.settings".format(emulator_id))
        os.system("adb -s {0} shell am start -a android.settings.WIRELESS_SETTINGS".format(emulator_id))
        os.system("adb -s {0} shell settings put global airplane_mode_on 0".format(emulator_id))
        os.system("adb -s {0} shell svc wifi enable".format(emulator_id))
        time.sleep(2)

        os.system("cp app_buddy/init_state_settings_app.xml window_emulator_{0}.xml".format(emulator_id))

    def reset_app(self, emulator_id):
        for i in range(0, 10):
            self.reward_bookeeping[i] = False
        self._restart_settings(emulator_id)

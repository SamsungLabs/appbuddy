import os
import time
import traceback
from .abstract_taskable_app import TaskableApp


class AlarmApp(TaskableApp):

    @staticmethod
    def _first_alarm_set(elem):
        if elem.obj_name is not None:
            print("this works")
            if elem.obj_name.strip().lower().find(
                    '7:58'.lower()) != -1 and \
                    elem.resource_id.strip().lower() == 'com.angrydoughnuts.android.alarmclock:id/time'.lower():
                return True

        return False

    @staticmethod
    def _second_alarm_set(elem):
        if elem.obj_name is not None:
            if elem.obj_name.strip().lower().find(
                    '9:49'.lower()) != -1 and \
                    elem.resource_id.strip().lower() == 'com.angrydoughnuts.android.alarmclock:id/time'.lower():
                return True

        return False

    def get_reward_for_current_state(self, list_of_ui_objects):
        """
        This function, given the list of UI objects, returns the reward based on the reward function
        for the alarm app.

        Below is a high-level description of the tasks for this app:
        Alarm - Easy Set one alarm clock
        Alarm - Medium Set two alarm clocks

        Below is a description of the rewards (including the intermediate rewards) given to the agent
        in each difficulty level of the alarm task.

        Alarm - Easy
            – No intermediate rewards

        Alarm - Medium
            – The agent is rewarded when one of the alarm clocks is set properly

        Note that an intermediate reward may only be given once in an episode.
        The variables in the reward_bookeeping array enforce this.
        The conditionals in this function check whether or not these variables already hold.
        Empirical evidence suggests that this mitigates for reward hacking.
        """
        reward = 0
        done = False
        first_alarm_set = False
        second_alarm_set = False
        for elem in list_of_ui_objects:
            if self._first_alarm_set(elem):
                first_alarm_set = True

            if self._second_alarm_set(elem):
                second_alarm_set = True

        if self.using_intermediate_rewards:
            if self.difficulty_level == "medium":
                if (first_alarm_set or second_alarm_set) and not self.reward_bookeeping[0]:
                    print("YAY GOT small REWARD")
                    reward = 1
                    self.reward_bookeeping[0] = True

        if self.difficulty_level == "easy":
            if first_alarm_set or second_alarm_set:
                done = True

        if self.difficulty_level == "medium":
            if first_alarm_set and second_alarm_set:
                done = True

        if done:
            print("YAY GOT BIG REWARD")
            reward = 10

        return reward, done

    @staticmethod
    def _restart_alarm(emulator_id):
        command = "adb -s {0} shell pm clear com.angrydoughnuts.android.alarmclock".format(
            emulator_id)
        os.system(command)

        command = "adb -s {0} shell monkey -p com.angrydoughnuts.android.alarmclock -c " \
                  "android.intent.category.LAUNCHER 1".format(emulator_id)
        os.system(command)
        time.sleep(3)

        os.system("adb -s {0} shell rm /sdcard/window_dump.xml".format(emulator_id))
        os.system("rm window_emulator_{0}.xml".format(emulator_id))
        os.system("adb -s {0} shell uiautomator dump".format(emulator_id))
        time.sleep(0.1)

        os.system("adb -s {0} pull /sdcard/window_dump.xml window_emulator_{0}.xml".format(emulator_id))
        time.sleep(0.1)

    def reset_app(self, emulator_id):
        for i in range(0, 10):
            self.reward_bookeeping[i] = False
        self._restart_alarm(emulator_id)

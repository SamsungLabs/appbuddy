#!/usr/bin/env python

# Core Library
import os
import time
import logging.config
import traceback
from .shopping_app import ShoppingApp
from .alarm_app import AlarmApp
from .split_app import SplitApp
from .settings_app import SettingsApp
from .android_device import AndroidDevice
import numpy as np
import random
import cfg_load
import gym
import pkg_resources
from gym import spaces
from bert_serving.client import BertClient

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

config_filename = "config.yaml"
config_filepath = pkg_resources.resource_filename("gym_android", config_filename)
config = cfg_load.load(config_filepath)
logging.config.dictConfig(config["LOGGING"])

BERT_EMBEDDING_LENGTH = 768
UPPER_BOUND_DOM_DEPTH = 300
UPPER_BOUND_ELEM_PER_SCREEN = 20
NUM_STEPS_PER_EPISODE = 25

EMULATOR_IDS = [
    "localhost:30001",
    "localhost:30003",
    "localhost:30005"]


class AndroidEnv(gym.Env):
    """
    The environment defines which actions can be taken at which point and
    when the agent receives which reward.
    """

    def __init__(self, emulator_id_idx):

        self.emulator_id = EMULATOR_IDS[emulator_id_idx]

        time.sleep(emulator_id_idx)

        self.curr_step = 0

        self.list_of_ui_objects = []

        print("Initializing emulator: {0}".format(self.emulator_id))

        self.bert_client = BertClient(port=5000, port_out=5005, check_length=False)

        app_details = config["app_details"]
        device_name = config["device_details"]["device_name"]
        if device_name == "android":
            self.device = AndroidDevice(device_name=device_name)

        app_name = app_details["app_name"]
        using_intermediate_rewards = app_details["using_intermediate_rewards"]
        difficulty_level = app_details["difficulty_level"]

        if app_name == "settings_app":
            self.app = SettingsApp(app_name, using_intermediate_rewards,
                                   difficulty_level)
        elif app_name == "shopping_app":
            self.app = ShoppingApp(app_name, using_intermediate_rewards,
                                   difficulty_level)
        elif app_name == "split_app":
            self.app = SplitApp(app_name, using_intermediate_rewards,
                                difficulty_level)
        elif app_name == "alarm_app":
            self.app = AlarmApp(app_name, using_intermediate_rewards,
                                difficulty_level)

        # Tokens for typing actions
        self.tokens = app_details["tokens"]

        # Defining the action space
        self.action_space = spaces.MultiDiscrete(
            [UPPER_BOUND_ELEM_PER_SCREEN, len(self.tokens)])

        # Defining the state (observation) space
        self.observation_space = spaces.Dict(
            {
                "BERTEmbed": spaces.Box(
                    low=0,
                    high=1,
                    shape=(
                        UPPER_BOUND_ELEM_PER_SCREEN,
                        BERT_EMBEDDING_LENGTH),
                    dtype=np.float32),
                "isClickableOrEditable": spaces.Box(
                    low=0,
                    high=1,
                    shape=(
                        UPPER_BOUND_ELEM_PER_SCREEN,
                        3),
                    dtype=np.uint8),
                "DOM_loc": spaces.Box(
                    low=0,
                    high=1,
                    shape=(
                        UPPER_BOUND_ELEM_PER_SCREEN,
                        UPPER_BOUND_DOM_DEPTH),
                    dtype=np.uint8)})

    def step(self, action):

        is_feasible = self._take_action(action)

        new_state = self._get_state()

        done = False

        if is_feasible:
            print("Executed a valid action")
            reward, done = self.app.get_reward_for_current_state(self.list_of_ui_objects)
        else:
            print("Invalid action chosen - negative reward given")
            reward = -0.1

        self.curr_step = self.curr_step + 1

        if not (self.curr_step < NUM_STEPS_PER_EPISODE):
            done = True

        return new_state, reward, done, {}

    def _take_action(self, action):
        return self.device.perform_action(
            action,
            self.emulator_id,
            self.list_of_ui_objects,
            self.tokens)

    def reset(self):
        """
        Reset the state of the environment and returns an initial observation.

        Returns
        -------
        observation (object): the initial observation of the space.
        """
        self.curr_step = 0

        self._restart_env(self.emulator_id)

        return self._get_state()

    def _get_state(self):
        """Get the observation state."""
        self.list_of_ui_objects = self.device.get_list_of_ui_objects(self.emulator_id)
        return self._get_state_representation()

    def seed(self, seed):
        random.seed(seed)
        np.random.seed

    def _restart_env(self, emulator_id):
        self.app.reset_app(emulator_id)

    def _get_state_representation(self):

        text_embeddings = np.zeros(
            (UPPER_BOUND_ELEM_PER_SCREEN,
             BERT_EMBEDDING_LENGTH),
            dtype=np.float32)

        element_attributes = np.zeros((UPPER_BOUND_ELEM_PER_SCREEN, 3), dtype=np.uint8)

        dom_loc = np.zeros(
            (UPPER_BOUND_ELEM_PER_SCREEN,
             UPPER_BOUND_DOM_DEPTH),
            dtype=np.uint8)

        for i, elem in enumerate(self.list_of_ui_objects):

            if i > (UPPER_BOUND_ELEM_PER_SCREEN - 1):
                break

            words_in_element = ""

            for word in elem.word_sequence:
                words_in_element += word + " "

            if len(words_in_element) > 0:
                curr_elem_encoding = self.bert_client.encode([words_in_element])[0]
                text_embeddings[i] = curr_elem_encoding

            is_clickable = elem.clickable

            is_editable = self.device.is_element_editable(elem)

            if is_editable:
                element_attributes[i, 1] = 1
            else:
                if is_clickable:
                    element_attributes[i, 0] = 1
                else:
                    element_attributes[i, 2] = 1

            try:
                dom_loc[i, (elem.dom_location[1] - 1)] = 1
            except Exception:
                traceback.print_exc()

        state_representation = {
            "BERTEmbed": text_embeddings,
            "isClickableOrEditable": element_attributes,
            "DOM_loc": dom_loc}
        return state_representation

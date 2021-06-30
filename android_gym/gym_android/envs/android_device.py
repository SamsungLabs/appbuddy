import os
import time
import traceback
from .abstract_device import AbstractDevice
from .view_hierarchy import view_hierarchy


class AndroidDevice(AbstractDevice):

    def __init__(self, device_name, screen_wdth=1080, screen_height=1920):
        self.screen_width = screen_wdth
        self.screen_height = screen_height
        super().__init__(device_name)

    def _tap_action(self, elem, emulator_id):
        """
        Tap an element
        """
        coordx = int((elem.bounding_box.x1 + elem.bounding_box.x2) / 2)
        coordy = int((elem.bounding_box.y1 + elem.bounding_box.y2) / 2)
        command = "adb -s {2} shell input tap {0} {1}".format(coordx, coordy, emulator_id)

        os.system(command)
        time.sleep(0.4)
        self._fetch_new_view_hierarchy(emulator_id)

    def _type_action(self, elem, token, emulator_id):
        """
        Edit an element with the token
        """
        coordx = int((elem.bounding_box.x1 + elem.bounding_box.x2) / 2)
        coordy = int((elem.bounding_box.y1 + elem.bounding_box.y2) / 2)

        command = "adb -s {2} shell input tap {0} {1}".format(coordx, coordy, emulator_id)
        os.system(command)

        time.sleep(0.4)

        command = "adb -s {0} shell input text {1}".format(emulator_id, token)
        os.system(command)
        time.sleep(0.4)

        self._fetch_new_view_hierarchy(emulator_id)

    @staticmethod
    def _fetch_new_view_hierarchy(emulator_id):
        """
        Pull the view hierarchy from the emulator with emulator_id
        """
        os.system("adb -s {0} shell rm /sdcard/window_dump.xml".format(emulator_id))
        os.system("rm window_emulator_{0}.xml".format(emulator_id))
        os.system("adb -s {0} shell uiautomator dump".format(emulator_id))
        time.sleep(0.1)
        os.system("adb -s {0} pull /sdcard/window_dump.xml window_emulator_{0}.xml".format(emulator_id))
        time.sleep(0.1)

    def get_list_of_ui_objects(self, emulator_id):
        try:
            vh = self._read_view_hierachy("window_emulator_{0}.xml".format(emulator_id))
            view_hierarchy_leaf_nodes = vh.get_leaf_nodes()
            ui_obj_list = [elem.uiobject for elem in view_hierarchy_leaf_nodes]
        except Exception:
            ui_obj_list = []
            traceback.print_exc()

        return ui_obj_list

    def _read_view_hierachy(self, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        vh = view_hierarchy.ViewHierarchy(self.screen_width, self.screen_height)
        vh.load_xml(data)
        return vh

    def perform_action(self, action, emulator_id, list_of_ui_objects, tokens):
        """Obtain a list of UI objects from the device.

        Args:
          action: A list with two elements [index of an UI element, index of a token]
          emulator_id: The ID of the emulator.
          list_of_ui_objects: A list of UI elements on the current screen

        Returns:
          True or False
        """
        index = action[0]
        token = tokens[action[1]]

        number_of_elements = len(list_of_ui_objects)
        if index > number_of_elements - 1:
            return False
        else:
            elem = list_of_ui_objects[index]
            if self.is_element_editable(elem):
                print("action is TYPE {0} {1} - {2}".format(token, elem.resource_id, emulator_id))
                self._type_action(elem, token, emulator_id)
                return True
            else:
                if elem.clickable:
                    print("action is TAP {0} - {1}".format(elem.resource_id, emulator_id))
                    self._tap_action(elem, emulator_id)
                    return True
                else:                # If the element is neither clickable nor editable then
                    return False     # we deem the action invalid and return False

    @staticmethod
    def is_element_editable(elem):
        if elem.obj_type.name == 'EDITTEXT' or elem.android_class.strip().lower() == \
                'android.widget.MultiAutoCompleteTextView'.lower() or elem.android_class.strip().lower() == \
                'android.widget.AutoCompleteTextView'.lower() or elem.android_class.strip().lower() == \
                'android.widget.ExtractEditText'.lower():
            return True
        return False

    def get_screenshot(self, emulator_id: str):
        os.system("adb -s {0} exec-out screencap -p > screen.png".format(emulator_id))

    def get_app_log(self, emulator_id: str, package_name: str):
        os.system("adb -s {0} logcat -d | grep {1} > app.log".format(emulator_id, package_name))

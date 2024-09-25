import argparse
from appium import webdriver
# Options are only available since client version 2.3.0
# If you use an older client then switch to desired_capabilities
# instead: https://github.com/appium/python-client/pull/720
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import os.path


# options.udid = 
# options.udid = '192.168.0.100:5555'
# options.udid = 'emulator-5554'
# 'com.google.android.calculator_8.4_(503542421)-84000598_minAPI23(nodpi)_apkmirror.com.apk'
# Appium1 points to http://127.0.0.1:4723/wd/hub by default
# driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', options=options)
class CalculatorTest(object):

    def __init__(self, udid, appiumserverurl, apk):
        self.options = UiAutomator2Options()
        self.options.platformVersion = '11'
        self.options.udid = udid
        if apk:
            self.options.app = os.path.join(os.path.abspath("."), apk)
        self.options.app_package = 'com.google.android.calculator'
        self.options.app_activity = 'com.android.calculator2.Calculator'
        self.driver = webdriver.Remote(appiumserverurl, options=self.options)
        self.ACTIONS = self._create_actions(self.driver)

    def _create_actions(self, driver):
        return {
            "0": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='0'),
            "1": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='1'),
            "2": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='2'),
            "3": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='3'),
            "4": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='4'),
            "5": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='5'),
            "6": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='6'),
            "7": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='7'),
            "8": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='8'),
            "9": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='9'),
            "+": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='plus'),
            "-": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='minus'),
            "=": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='equals'),
            "*": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='multiply'),
            "X": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='multiply'),
            "/": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='divide'),
            "%": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='percent'),
            ".": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='point'),
            "A": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='clear'),
            "S": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='square root'),
            "P": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='pi'),
            "^": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='power'),
            "!": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='factorial'),
            "D": driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='delete'),
            "(": driver.find_element(by=AppiumBy.ID, value='com.google.android.calculator:id/parens'),
            ")": driver.find_element(by=AppiumBy.ID, value='com.google.android.calculator:id/parens')
        }

    def execute_formula(self,formula):
        for i in formula.upper():
            self.ACTIONS[i].click()    

    def test_formula(self, formula, expected_result, strict_result = True):
        self.execute_formula(formula)
        try:
            try:
                result_final = self.driver.find_element(
                    by=AppiumBy.ID,
                    value='com.google.android.calculator:id/result_final')
                actual_result = result_final.text
            except:
                try:
                    result_preview = self.driver.find_element(
                        by=AppiumBy.ID,
                        value='com.google.android.calculator:id/result_preview')
                    actual_result = result_preview.text
                except:
                    actual_result = "result_preview and result_final are not available"
            self.ACTIONS["A"].click()
            if strict_result:
                assert(expected_result == actual_result)
            else:
                assert(expected_result in actual_result)    

        except AssertionError:
            print(f"  ---FAILED: test formula '{formula}'. Expected_result: {expected_result}, actual_result: {actual_result}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-udid', '--UDID')
    parser.add_argument('-aurl', '--APPIUM_URL', default='http://127.0.0.1:4723/wd/hub')
    parser.add_argument('-apk', '--APK', default="")
    return parser.parse_args()


def main():
    args = parse_arguments()
    TEST_PLAN = [
        ("20+30=", "50"),
        ("20*30", "600"),
        ("10/2", "5"),
        ("1+2+3=", "6"),
        ("2+3*4", "14"),
        ("2+3DD-4", "−2"),
        ("2+3A", ""),
        ("2+3A3*5=", "15"),
        ("2+3A3*5%=", "0.15"),
        ("S(10+6)=", "4"),
        ("S10=", "3.1622", False),
        ("5+P=", "8.14159", False),
        ("2^3=", "8"),
        ("3!=", "6"),
        ("3.1+2.2=", "5.3"),
        ("!3=", "Format error"),
        ("5.3!=", "Domain error"),
        ("1+1", "3")
        ]
    calculator_test = CalculatorTest(args.UDID, args.APPIUM_URL, args.APK)
    for test in TEST_PLAN:
        calculator_test.test_formula(*test)

if __name__ == '__main__':
    main()




# stay connected via USB
# connect to your WIFI network (computer and mobile device both)
# find device IP in About Phone
# adb kill-server
# adb usb
# adb tcpip 5555
# unplug usb cable (as per @captain_majid's comment)
# adb connect yourDeviceIP

# adb devices (must see two device names , one of them is by deviceIP)

# unplug USB cable
# EMULATORS:
# .\sdkmanager --list
# .\sdkmanager "system-images;android-30;google_apis_playstore;x86_64"
# .\avdmanager create avd -n Android30playstore -k "system-images;android-30;google_apis_playstore;x86_64"
# .\emulator -avd Android30playstore
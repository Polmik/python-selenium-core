from selenium.webdriver.remote.webelement import WebElement

from framework.elements.core.constants.element_state import ElementState
from framework.elements.core.element_finder import ElementFinder
from framework.locator.locator import Locator


class ElementCacheHandler:
    __element: WebElement = None

    def __init__(self, locator: Locator, name: str, state: ElementState, finder: ElementFinder):
        self.__locator = locator
        self.__name = name
        self.__state = state
        self.__element_finder = finder

    @property
    def is_stale(self):
        return self.__element is not None and self.is_refresh_needed()

    def is_refresh_needed(self, custom_sate: ElementState = None) -> bool:
        if self.__element is None:
            return True
        try:
            is_displayed = self.__element.is_displayed()
            # refresh is needed only if the property is not match to expected element state
            return (self.__state if custom_sate is None else custom_sate) == self.__state.Displayed and not is_displayed
        except:
            # refresh is needed if the property is not available
            return True

    def get_element(self, timeout: float = None, custom_sate: ElementState = None):
        if self.is_refresh_needed(custom_sate):
            self.__element = self.__element_finder.find_element(
                locator=self.__locator,
                state=self.__state if custom_sate is None else custom_sate,
                timeout=timeout,
                name=self.__name,
            )

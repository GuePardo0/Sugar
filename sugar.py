import threading
import time

class ProgressBar():
    def __init__(self, bar_length = 100, previous_iterations_checked = 10):
        self.bar_length = bar_length
        self.previous_iterations_checked = previous_iterations_checked

        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run, daemon=True)

    def print_bar(self):
        show_text = False
        text = ""

        if self.show_numbers:
            show_text = True
            text_numbers = f"{self.value}/{self.total}"
            text = text_numbers
        if self.show_percentage:
            show_text = True
            text_percentage = "%.2f" % (100 * self.percentage) +"%"
            text += "    " if text != "" else ""
            text += text_percentage
        if self.show_time_estimate:
            # set variables
            show_text = True
            self.time_start = self.time_end
            self.time_end = time.time()
            # manage previous_iterations_done list
            if self.time_end - self.time_start > 0.03:
                self.previous_iterations_done.append(self.value - self.last_value)
                all_zero = True
                for i in range(1, len(self.previous_iterations_done)):
                    if self.previous_iterations_done[i] != 0:
                        all_zero = False
                        break
                if not all_zero and len(self.previous_iterations_done) > self.previous_iterations_checked:
                    self.previous_iterations_done.pop(0)
            # estimate time
            text_time_estimate = self.estimate_time()
            # set variables
            self.last_value = self.value
            text += "    " if text != "" else ""
            text += "Time estimate: " + text_time_estimate

        if show_text or self.show_bar:
            clear(self.lines_cleared)
        if show_text:
            if self.show_bar:
                text_length, rest = divmod(len(text), 2)
                text_length += rest
                text = " " * (((self.bar_length // 2) - text_length) + 1) + text
            print(text)
        if self.show_bar:
            filled_length = int(self.bar_length * self.percentage)
            bar = "【"
            bar += "█" * filled_length
            bar += "░" * (self.bar_length - filled_length)
            bar += "】"
            print(bar)

    def run(self):
        while True:
            self.percentage = self.value / self.total
            self.print_bar()
            if self.percentage >= 1 or self.stop_event.is_set():
                self.percentage = self.value / self.total
                self.print_bar()
                break
            time.sleep(self.time_interval)

    def start(self, total = 100, time_interval = 1, lines_cleared = 60, show_bar = True, show_numbers = True, show_percentage = True, show_time_estimate = True):
        if total <= 0:
            raise TypeError("parameter 'total' must be greater than 0")
        self.total = total
        self.time_interval = time_interval
        self.lines_cleared = lines_cleared

        self.show_bar = show_bar
        self.show_numbers = show_numbers
        self.show_percentage = show_percentage
        self.show_time_estimate = show_time_estimate

        # attributes used in time estimate calculation
        self.last_value = 0
        self.time_start = time.time()
        self.time_end = time.time()
        self.previous_iterations_done = []

        self.value = 0
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def update(self, value):
        with self.lock:
            self.value = value

    def estimate_time(self, format = True):
        time_taken = self.time_end - self.time_start
        iterations_left = self.total - self.value
        iterations_done = 0
        len_previous_iterations_done = len(self.previous_iterations_done)
        for i in range(len_previous_iterations_done):
            iterations_done += self.previous_iterations_done[i]
        iterations_done /= len_previous_iterations_done if len_previous_iterations_done != 0 else 1
        time_estimate = round(time_taken * iterations_left / iterations_done) if iterations_done != 0 else 0
        if format:
            if time_estimate >= 60:
                time_estimate, time_estimate_seconds = divmod(time_estimate, 60)
                text_time_estimate = str(time_estimate_seconds) + " seconds"
            else:
                return str(time_estimate) + " seconds"
            if time_estimate >= 60:
                time_estimate, time_estimate_minutes = divmod(time_estimate, 60)
                text_time_estimate = str(time_estimate_minutes) + " minutes, " + text_time_estimate
            else:
                return str(time_estimate) + " minutes, " + text_time_estimate
            if time_estimate >= 24:
                time_estimate, time_estimate_hours = divmod(time_estimate, 24)
                text_time_estimate = str(time_estimate_hours) + " hours, " + text_time_estimate
            else:
                return str(time_estimate) + " hours, " + text_time_estimate
            if time_estimate >= 365:
                time_estimate_years, time_estimate_days = divmod(time_estimate, 365)
                text_time_estimate = str(time_estimate_years) + " years, " + str(time_estimate_days) + " days, " + text_time_estimate
            else:
                return str(time_estimate) + " days, " + text_time_estimate
            return text_time_estimate
        return time_estimate

class Menu():
    def __init__(self, default_selector_envelopers = None, default_selectors = None, default_case_sensitive = None, default_incorrect_message = None):
        self.default_selector_envelopers = None
        self.default_selectors = None
        self.default_case_sensitive = False
        self.default_incorrect_message = None
        self.configure(default_selector_envelopers, default_selectors, default_case_sensitive, default_incorrect_message)

        self.special_selectors = ["numbers", "numbers0", "alphabet", "uppercase_alphabet", "greek_alphabet", "uppercase_greek_alphabet"]

    def configure(self, default_selector_envelopers = None, default_selectors = None, default_case_sensitive = None, default_incorrect_message = None):
        error = ValueError("parameter default_selector_envelopers must be in the form '[str, str]'")
        if default_selector_envelopers != None:
            if type(default_selector_envelopers) != list:
                raise error
            if len(default_selector_envelopers) != 2:
                raise error
            for enveloper in default_selector_envelopers:
                if type(enveloper) != str:
                    raise error
            self.default_selector_envelopers = default_selector_envelopers

        error = ValueError("parameter default_selectors must be in the form 'list[str]'")
        if default_selectors != None:
            if not default_selectors in self.special_selectors:
                if type(default_selectors) != list:
                    raise error
                for selector in default_selectors:
                    if type(selector) != str:
                        raise error
            self.default_selectors = default_selectors

        error = ValueError("parameter default_case_sensitive must be in the form 'bool'")
        if default_case_sensitive != None:
            if type(default_case_sensitive) != bool:
                raise error
            self.default_case_sensitive = default_case_sensitive

        error = ValueError("parameter default_incorrect_message must be in the form 'str'")
        if default_incorrect_message != None:
            if type(default_incorrect_message) != str:
                raise error
            self.default_incorrect_message = default_incorrect_message

        if self.default_selector_envelopers == None:
            self.default_selector_envelopers = ["(", ")"]
        if self.default_selectors == None:
            self.default_selectors = "numbers"
        if self.default_incorrect_message == None:
            self.default_incorrect_message = "Invalid option. Please, try again."

    def __get_special_selector(self, selectors, index):
        if selectors == "numbers":
            return str(index + 1)
        elif selectors == "numbers0":
            return str(index)
        elif selectors == "alphabet":
            return "abcdefghijklmnopqrstuvwxyz"[index]
        elif selectors == "uppercase_alphabet":
            return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[index]
        elif selectors == "greek_alphabet":
            return "αβγδεζηθικλμνξοπρστυφχψω"[index]
        elif selectors == "uppercase_greek_alphabet":
            return "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"[index]

    def print_menu(self, message, options: list[str], incorrect_message = None, case_sensitive = None, hidden_selectors = [], selectors = None, selector_envelopers = None):
        # Handle errors
        error = ValueError("parameter options must be in the form 'list[str]'")
        if type(options) != list:
            raise error
        for selector in options:
            if type(selector) != str:
                raise error

        error = ValueError("parameter hidden_selectors must be in the form 'list[str]'")
        if type(hidden_selectors) != list:
            raise error
        for selector in hidden_selectors:
            if type(selector) != str:
                raise error

        error = ValueError("parameter selectors must be in the form 'list[str]'")
        if selectors != None:
            if not selectors in self.special_selectors:
                if type(selectors) != list:
                    raise error
                for selector in selectors:
                    if type(selector) != str:
                        raise error
        else:
            selectors = self.default_selectors

        error = ValueError("parameter selector_envelopers must be in the form '[str, str]'")
        if selector_envelopers != None:
            if type(selector_envelopers) != list:
                raise error
            if len(selector_envelopers) != 2:
                raise error
            for enveloper in selector_envelopers:
                if type(enveloper) != str:
                    raise error
        else:
            selector_envelopers = self.default_selector_envelopers

        error = ValueError("parameter case_sensitive must be in the form 'bool'")
        if case_sensitive != None:
            if type(case_sensitive) != bool:
                raise error
        else:
            case_sensitive = self.default_case_sensitive

        error = ValueError("parameter incorrect_message must be in the form 'str'")
        if incorrect_message != None:
            if type(incorrect_message) != str:
                raise error
        else:
            incorrect_message = self.default_incorrect_message

        # Print the menu
        while True:
            print(message + "\n")
            options_text = ""
            used_selectors = []
            for index, option in enumerate(options):
                if selectors in self.special_selectors:
                    selector = self.__get_special_selector(selectors, index)
                else:
                    selector = selectors[index]
                if not case_sensitive:
                    used_selectors.append(selector.lower())
                else:
                    used_selectors.append(selector)
                options_text += selector_envelopers[0] + selector + selector_envelopers[1]
                options_text += " " + option
                options_text += "   "
            print(options_text + "\n")
            userinput = input()
            if not case_sensitive:
                userinput = userinput.lower()
            if userinput in used_selectors:
                break
            else:
                clear()
                print(incorrect_message + "\n")
        return userinput

def clear(lines_cleared = 60):
    print("\n" * lines_cleared)
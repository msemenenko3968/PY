from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class MainApp(App):
    def build(self):
        self.history = []
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None
        main_layout = BoxLayout(orientation="vertical")
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )
        self.solution.text = "0"
        main_layout.add_widget(self.solution)
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            # Очистка виджета с решением
            self.solution.text = "0"
        else:
            if current and (
                    self.last_was_operator and button_text in self.operators):
                # Не добавляйте два оператора подряд, рядом друг с другом
                return
            elif current == "" and button_text in self.operators:
                # Первый символ не может быть оператором
                return
            elif current == "0":
                self.solution.text = button_text
            else:
                new_text = current + button_text
                self.solution.text = new_text
        if self.solution.text.__contains__("/0"):
            self.solution.text = "0";
        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

        button = Button(
            text="=", pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        buttons = Button(text="calculation history",
                         pos_hint={"center_x": 0.5, "center_y": 0.5})
        buttons.bind(on_press=self.show_history);
        main_layout.add_widget(history_button)

        return main_layout

        def on_solution(self, instance):
            text = self.solution.text
            if text:
                solution = str(eval(self.solution.text))
                self.history.append(self.solution.text + '=' + solution)
                self.solution.text = solution


def show_history(self, instance):
    data = '\n'.join(self.history)
    popup = Popup(title='Test popup',
                  content=Label(text=data),
                  auto_dismiss=True,
                  size_hint=(None, None), size=(450, 450))
    popup.open()


if __name__ == "__main__":
    app = MainApp()
    app.run()
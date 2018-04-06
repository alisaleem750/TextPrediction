from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from TextPrediction.Ngrams.Ngrams import Ngrams as Ngrams
import re

class PredictionScreen(BoxLayout):

    def __init__(self, **kwargs):

        # Creating main Window
        super(PredictionScreen, self).__init__(**kwargs)
        Window.size = (700, 500)
        Window.title = "Predictive Text Entry"
        self.orientation='vertical'
        self.cols = 1

        # Creating other widgets.
        self.add_widget(Label(text='Predictive Text Entry', font_size=40))
        self.predictionBox = BoxLayout(orientation='horizontal')
        self.predictionBox.padding = [0, 0, 0, -130]
        self.add_widget(self.predictionBox)
        textSubmit = BoxLayout(orienatation='horizontal')
        self.textInput = TextInput(text='', hint_text='Enter message here', multiline=False, size=(30,40), size_hint=(.7,None), padding=[6,10,6,6])
        textSubmit.add_widget(self.textInput)
        sendButton = Button(text='Send', font_size=14, size=(30,40), size_hint=(0.3,None))
        sendButton.bind(on_press=self.send_btn_callback)
        textSubmit.add_widget(sendButton)
        self.add_widget(textSubmit)

        # Setting up keyboard relationship.
        self._keyboard = Window.request_keyboard(self._keyboard_released(), self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        # Initializing ngrams
        self.ngrams = Ngrams()
        self.trigrams = self.ngrams.load_trigrams()
        self.bigrams = self.ngrams.load_bigrams()
        self.predictions = []

    # This function helps retrieve keyboard actions in the textinput box.
    # Source: https://groups.google.com/forum/#!topic/kivy-users/jCU0zmgH0jg
    def _keyboard_released(self):
        self.focus = True

    # Actions performed when a key is pressed on the keyboard.
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # This updates the clock to the next clock cycle, therefore all actions are performed in real time rather than
        # on the previous frame.
        Clock.schedule_once(self.my_callback)

    # Actions performed after the next clock cycle has been called.
    def my_callback(self, dt):
        text = re.findall("(\w+[\w'\-&]* )", self.textInput.text)
        characters = re.findall("(\w+[\w'\-&]*)", self.textInput.text)
        bigrams = self.bigrams
        trigrams = self.trigrams

        # First word
        if len(characters) > 0 and len(text) == 0:
            characters = characters[-1]
        # Following words. Make sure character isn't the same as key. If it is, make it empty.
        elif len(characters) > 0 and len(text) > 0:
            if characters[-1] <> text[-1].rstrip():
                characters = characters[-1]
            else:
                characters = ""
        # If none of the above criterias are met, make characters an empty string (error proofing)
        else:
            characters = ""

        # Keep state to last two items.
        text = text[-2:]

        # If we only have 1 word in the state, look for bi-grams.
        if len(text) == 1:
            #Remove space after the word
            word = text[0].rstrip()
            self.predictions = self.ngrams.top_n_words_starting_with_characters(bigrams, word, 3, characters)
            if not self.predictions:
                self.predictions = self.ngrams.return_keys_containing_characters(bigrams, characters, 3)
        # If we have 2 words in the state, look for tri-grams first. If none are found, look for bi-grams. If none are
        # found, look for the keys in bi-grams dictionary (simulating start of sentence which stores no previous state)
        elif len(text) == 2:
            word = text[0]+text[1].rstrip()
            self.predictions = self.ngrams.top_n_words_starting_with_characters(trigrams, word, 3, characters)
            if not self.predictions:
                word = text[1].rstrip()
                self.predictions = self.ngrams.top_n_words_starting_with_characters(bigrams, word, 3, characters)
            if not self.predictions:
                self.predictions = self.ngrams.return_keys_containing_characters(bigrams, characters, 3)
        # If start of sentence, look up the keys in the bi-grams dictionary. Keep matching the entered characters
        # to give an updated prediction.
        else:
            self.predictions = self.ngrams.return_keys_containing_characters(bigrams, characters, 3)
            if characters == "":
                self.predictions = []

        # Displays the appropriate amount of predictions on the screen depending on how many predictions are available.
        # Also links button to actions with a callback function.
        if len(self.predictions) == 1:
            self.predictionBox.clear_widgets()
            btn1 = Button(background_color = (0, 0, 0, 0), text=self.predictions[0], font_size=14, size_hint=(0.33, 0.1))
            btn1.bind(on_press=self.btn_callback)
            self.prediction1 = btn1
            self.prediction2 = Button(background_color = (0, 0, 0, 0), font_size=14, size_hint=(0.33,0.1))
            self.prediction3 = Button(background_color = (0, 0, 0, 0), font_size=14, size_hint=(0.33,0.1))
            self.predictionBox.add_widget(self.prediction1)
            self.predictionBox.add_widget(self.prediction2)
            self.predictionBox.add_widget(self.prediction3)
        elif len(self.predictions) == 2:
            self.predictionBox.clear_widgets()
            btn1 = Button(background_color = (0, 0, 0, 0), text=self.predictions[0], font_size=14, size_hint=(0.33, 0.1))
            btn1.bind(on_press=self.btn_callback)
            btn2 = Button(background_color = (0, 0, 0, 0), text=self.predictions[1], font_size=14, size_hint=(0.33, 0.1))
            btn2.bind(on_press=self.btn_callback)
            self.prediction1 = btn1
            self.prediction3 = btn2
            self.prediction2 = Button(background_color = (0, 0, 0, 0), font_size=14, size_hint=(0.33,0.1))
            self.predictionBox.add_widget(self.prediction1)
            self.predictionBox.add_widget(self.prediction2)
            self.predictionBox.add_widget(self.prediction3)
        elif len(self.predictions) == 3:
            self.predictionBox.clear_widgets()
            btn1 = Button(background_color = (0, 0, 0, 0), text=self.predictions[0], font_size=14, size_hint=(0.33,0.1))
            btn1.bind(on_press=self.btn_callback)
            btn2 = Button(background_color = (0, 0, 0, 0), text=self.predictions[1], font_size=14, size_hint=(0.33,0.1))
            btn2.bind(on_press=self.btn_callback)
            btn3 = Button(background_color = (0, 0, 0, 0), text=self.predictions[2], font_size=14, size_hint=(0.33,0.1))
            btn3.bind(on_press=self.btn_callback)
            self.prediction1 = btn1
            self.prediction2 = btn2
            self.prediction3 = btn3
            self.predictionBox.add_widget(self.prediction1)
            self.predictionBox.add_widget(self.prediction2)
            self.predictionBox.add_widget(self.prediction3)
        else:
            self.predictionBox.clear_widgets()
            self.prediction1 = Button(background_color = (0, 0, 0, 0), font_size=14, size_hint=(0.33,0.1))
            self.prediction2 = Button(background_color = (0, 0, 0, 0), font_size=14, size_hint=(0.33,0.1))
            self.prediction3 = Button(background_color = (0, 0, 0, 0), font_size=14, size_hint=(0.33,0.1))
            self.predictionBox.add_widget(self.prediction1)
            self.predictionBox.add_widget(self.prediction2)
            self.predictionBox.add_widget(self.prediction3)
        self.textInput.focus = True
        return self

    # The callback function for the buttons. This checks whether the last word entered is a substring of the prediction
    # button clicked. If this is the case, it autocompletes the word when the button is clicked. Otherwise, it adds the
    # word as the next word in the sentence.
    def btn_callback(self, instance):
        text = re.findall("(\w+[\w'\-&]*)", self.textInput.text)
        if instance.text.lower().startswith(text[-1].lower()):
            n = len(text[-1])
            self.textInput.insert_text(instance.text.lower()[n:]+" ")
            Clock.schedule_once(self.my_callback)
        else:
            self.textInput.insert_text(instance.text.lower()+" ")
            Clock.schedule_once(self.my_callback)
        return self

    def send_btn_callback(self, instance):
        self.textInput.text = ""
        self.predictionBox.clear_widgets()
        return self

class App(App):
    def build(self):
        self.title="Predictive Text Entry"
        return PredictionScreen()
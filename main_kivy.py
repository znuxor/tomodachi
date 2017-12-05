#!/usr/bin/env python3
import kivy

from kivy.app import App
from kivy.uix.label import Label


class MyApp(App):
    '''Main class'''
    def build(self):
        return Label(text='Hello world')


if __name__ == '__main__':
    MyApp().run()

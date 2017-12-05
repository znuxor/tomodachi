# This is the Tomodachi class, it represents the main game entity
import random
from collections import deque
from enum import Enum

MAX_AMOUNT = 5
SLEEP_SPEEDUP = 20  # To make sleep faster than becoming tired
UNTRAINED_REFUSAL_RATE = 0.3


class Events(Enum):
    ''' Pet events, please implement reactions for this '''
    DEAD = 1
    HUNGRY = 2
    FED = 3
    REFUSE_TO_EAT = 4
    SLEEPY = 5
    PUT_TO_BED = 6
    GOT_OUT_OF_BED = 7
    DIRTY = 8
    CLEANED = 9
    BORED = 10
    ENTERTAINED = 11
    REFUSE_ENTERTAINED = 12
    TRAINED = 13
    SICK_FROM_HUNGER = 14
    SICK_FROM_TIRED = 15
    SICK_FROM_DIRTY = 16
    SICK_FROM_BORED = 17
    CURED = 18


class Tomodachi():
    '''The main tomodachi class'''
    def __init__(self, health_rate, hunger_rate, happiness_rate, training_rate,
                 tiredness_rate, dirtiness_rate, pet_type, pet_name):
        self.status = dict()
        self.status['health'] = MAX_AMOUNT
        self.status['training'] = MAX_AMOUNT
        self.status['happiness'] = MAX_AMOUNT
        self.status['satiety'] = MAX_AMOUNT
        self.status['energy'] = MAX_AMOUNT
        self.status['cleanliness'] = MAX_AMOUNT
        self.status['is_sick'] = False
        self.status['is_in_bed'] = False
        self.status['is_dead'] = False

        self.rate = dict()
        self.rate['health'] = health_rate
        self.rate['training'] = training_rate
        self.rate['happiness'] = happiness_rate
        self.rate['hunger'] = hunger_rate
        self.rate['tiredness'] = tiredness_rate
        self.rate['dirtiness'] = dirtiness_rate

        self.age = 0
        self.pet_type = pet_type
        self.pet_name = pet_name
        self.events = deque()

    def update(self):
        ''' Updates the tomodachi for a single moment'''

        # training decrementation
        if (self.status['training'] > 0 and
                random.random() < self.rate['training']):
            self.status['training'] -= 1

        # satiety decrementation
        if (self.status['satiety'] > 0 and
                random.random() < self.rate['hunger']):
            self.status['satiety'] -= 1
            if self.status['satiety'] == 1:
                self.events.append(Events.HUNGRY)

        # happiness decrementation
        if (self.status['happiness'] > 0 and
                random.random() < self.rate['happiness']):
            self.status['happiness'] -= 1
            if self.status['happiness'] == 1:
                self.events.append(Events.BORED)

        # cleanliness decrementation
        if (self.status['cleanliness'] > 0 and
                random.random() < self.rate['dirtiness']):
            self.status['cleanliness'] -= 1
            if self.status['cleanliness'] == 1:
                self.events.append(Events.DIRTY)

        # tiredness logic
        if self.status['is_in_bed']:
            if (self.status['energy'] > 0 and
                    random.random() <
                    self.rate['tiredness']**(1/SLEEP_SPEEDUP)):
                self.status['energy'] += 1
                if self.status['energy'] == MAX_AMOUNT:
                    self.status['is_in_bed'] = False
                    self.events.append(Events.GOT_OUT_OF_BED)
        else:
            if (self.status['energy'] > 0 and
                    random.random() < self.rate['tiredness']):
                self.status['energy'] -= 1
            if self.status['energy'] == 1:
                self.events.append(Events.TIRED)

        # bed state logic
        if self.status['is_in_bed'] and self.status['energy'] == MAX_AMOUNT:
            self.status['is_in_bed'] = False

        # sickness state logic
        if not self.status['is_sick']:
            if not self.status['happiness']:
                self.status['is_sick'] = True
                self.events.append(Events.SICK_FROM_BORED)
            if not self.status['satiety']:
                self.status['is_sick'] = True
                self.events.append(Events.SICK_FROM_HUNGER)
            if not self.status['energy']:
                self.status['is_sick'] = True
                self.events.append(Events.SICK_FROM_TIRED)
            if not self.status['cleanliness']:
                self.status['is_sick'] = True
                self.events.append(Events.SICK_FROM_DIRTY)

        # health logic
        if self.status['is_sick']:
            if (self.status['health'] > 0 and
                    random.random() < self.rate['health']):
                self.status['health'] -= 1
        else:
            if (self.status['health'] < MAX_AMOUNT and
                    random.random() < self.rate['health']):
                self.status['health'] += 1

        # untrained mischief logic ( the randomer part)
        if not self.status['training']:
            pass

        # age logic
        self.age += 1

        # death logic
        if not self.status['health'] and not self.status['is_dead']:
            self.status['is_dead'] = True
            self.events.append(Events.DEAD)

    def get_health(self):
        ''' Returns the health of the pet '''
        return self.status['health']

    def get_satiety(self):
        ''' Returns the satiety of the pet '''
        return self.status['satiety']

    def get_happiness(self):
        ''' Returns the happiness of the pet '''
        return self.status['happiness']

    def get_training(self):
        ''' Returns the training of the pet '''
        return self.status['training']

    def get_energy(self):
        ''' Returns the energy of the pet '''
        return self.status['energy']

    def get_cleanliness(self):
        ''' Returns the cleanliness of the pet '''
        return self.status['cleanliness']

    def get_type(self):
        ''' Returns the type of the pet '''
        return self.pet_type

    def get_name(self):
        ''' Returns the name of the pet '''
        return self.pet_name

    def is_sick(self):
        ''' Returns True if the pet is sick'''
        return self.status['is_sick']

    def feed(self):
        ''' Feeds the pet '''
        if not self.status['is_in_bed']:
            if (not self.status['training'] or
                    random.random > UNTRAINED_REFUSAL_RATE):
                self.status['satiety'] = MAX_AMOUNT
                self.events.append(Events.FED)
            else:
                self.events.append(Events.REFUSE_TO_EAT)
        else:
            self.events.append(Events.IS_IN_BED)

    def put_to_bed(self):
        ''' Puts the pet to bed '''
        if not self.status['is_in_bed']:
            self.status['is_in_bed'] = True
            self.events.append(Events.PUT_TO_BED)
        else:
            self.events.append(Events.IS_IN_BED)

    def clean(self):
        ''' Cleans the pet '''
        if not self.status['is_in_bed']:
            self.status['cleanliness'] = MAX_AMOUNT
            self.events.append(Events.CLEANED)
        else:
            self.events.append(Events.IS_IN_BED)

    def entertain(self):
        ''' Entertains the pet '''
        if not self.status['is_in_bed']:
            if (not self.status['training'] or
                    random.random > UNTRAINED_REFUSAL_RATE):
                self.events.append(Events.ENTERTAINED)
                self.status['happiness'] = MAX_AMOUNT
            else:
                self.events.append(Events.REFUSE_ENTERTAINED)
        else:
            self.events.append(Events.IS_IN_BED)

    def cure(self):
        ''' Cures the pet '''
        if not self.status['is_in_bed']:
            self.status['is_sick'] = False
            self.events.append(Events.CURED)
        else:
            self.events.append(Events.IS_IN_BED)

    def train(self):
        ''' Trains the pet fully '''
        if not self.status['is_in_bed']:
            self.status['training'] = MAX_AMOUNT
            self.events.append(Events.TRAINED)
        else:
            self.events.append(Events.IS_IN_BED)

    def pop_event(self):
        ''' Returns an enum value representing an event,
            returns False otherwise '''
        if self.events:
            return self.events.popleft()
        else:
            return None

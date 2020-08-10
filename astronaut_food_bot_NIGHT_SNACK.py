# ASTRONAUT MEAL BOT - cooded by yandere dev spaghetti coding funtime spooktacular
# FILE FOR MIDNIGHT SNACK POSTS ONLY

# Yes it was probably stupid to put all this shit in individual .py files
# but I am scheduling these in crontabs and it was easier to just schedule each
# separate file once every 24 hours

from astronaut_food_bot_MAIN import *


class NightSnack(Meal):
    """Generates content specifically for midnightsnack posts. These posts have
    a 10% chance of occurring and may be posted at 11:30pm."""
    def __init__(self):
        super().__init__()
        self._meal_calorie_count = 0


    def create_meal(self):
        """Randomly generates meal components and formats them into facebook
        post.
        Returns:
            message(str): text to be posted to facebook"""
        image_foods = []

        #SNACKS
        no_of_snacks = random.randint(0,2)
        #Randomly chooses either 0, 1 or 2 snacks
        selected_list = self.select_foods_from_txt('snacks.txt', \
                                                           no_of_snacks)
        snacks = self.format_food_string('Snack: ', 'Snacks: ', \
                                                             selected_list)
        image_foods += selected_list


        #DRINKS
        #Chooses 1 drink
        selected_list = self.select_foods_from_txt('drinks.txt', 1)[0]
        drinks = 'Drink: ' + selected_list
        image_foods += [selected_list]


        
        #Creating image for facebook post
        image = ImageGen('night snack', image_foods)
        image.generate_picture()
        
        #Formatting meal into text for facebook post
        meal = [snacks, drinks]
        greetings = ['Can\'t sleep. t h e _ v o i d will eat me.', \
        'I woke up thirsty, gotta get something before I go back to sleep.', \
        'Maybe I didn\'t have enough to eat for dinner...', \
        'Time for a midnight snack.']
        message = self.format_facebook_post(meal, greetings)
        return message



def main():
    night_snack = NightSnack()
    #Generating a number from 0-9 (1 in 10/10% chance of generating 9)
    snack_probability = random.randint(0,9)
    if snack_probability == 9:
        message = night_snack.create_meal()
        post_to_facebook(TOKEN, message, '/home/pi/Desktop/Astronaut_food_bot/_image_generated.png')
        print('MIDNIGHT SNACK POST: \n' + message)
    else:
        print('There was no midnight snack post at this time.')

if __name__ == "__main__" :
    main()

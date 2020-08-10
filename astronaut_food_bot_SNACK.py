# ASTRONAUT MEAL BOT - cooded by yandere dev spaghetti coding funtime spooktacular
# FILE FOR SNACK POSTS ONLY

# Yes it was probably stupid to put all this shit in individual .py files
# but I am scheduling these in crontabs and it was easier to just schedule each
# separate file once every 24 hours

from astronaut_food_bot_MAIN import *


class Snack(Meal):
    """Generates content specifically for snack posts. These posts have a 33%
    chance of occurring and may be posted at 10:00am and/or 3:30pm."""
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
        #Chooses 1 snack
        selected_list = self.select_foods_from_txt('snacks.txt', 1)[0]
        snacks = 'Snack: ' + selected_list
        image_foods += [selected_list]

        #CONDIMENTS
        no_of_condiments = random.randint(0,1)
        #Randomly chooses either 0 or 1 condiments
        condiments = None
        if no_of_condiments == 1:
            selected_list = self.select_foods_from_txt('condiments.txt', 1)[0]
            condiments = 'Condiment: ' + selected_list
            image_foods += [selected_list]
            
        #DRINKS
        no_of_drinks = random.randint(0,1)
        #Randomly chooses either 0 or 1 drinks
        drinks = None
        if no_of_drinks == 1:
            selected_list = self.select_foods_from_txt('drinks.txt', 1)[0]
            drinks = 'Drink: ' + selected_list
            image_foods += [selected_list]


        
        #Creating image for facebook post
        image = ImageGen('snack', image_foods)
        image.generate_picture()
        
        #Formatting meal into text for facebook post
        meal = [snacks, condiments, drinks]
        greetings = ['I was feeling a bit peckish so I stopped for a snack.', \
        'Hopefully I can have a healthy snack today.', \
        'Time for a quick snack:', 'Snack time:']
        message = self.format_facebook_post(meal, greetings)
        return message



def main():
    snack = Snack()
    #Generating a number from 0-2 (1 in 3/33% chance of generating 2)
    snack_probability = random.randint(0,2)
    if snack_probability == 2:
        message = snack.create_meal()
        post_to_facebook(TOKEN, message, '/home/pi/Desktop/Astronaut_food_bot/_image_generated.png')
        print('SNACK POST: \n' + message)
    else:
        print('There was no snack post at this time.')

if __name__ == "__main__" :
    main()

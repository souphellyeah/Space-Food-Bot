# ASTRONAUT MEAL BOT - cooded by yandere dev spaghetti coding funtime spooktacular
# FILE FOR DINNER POSTS ONLY

# Yes it was probably stupid to put all this shit in individual .py files
# but I am scheduling these in crontabs and it was easier to just schedule each
# separate file once every 24 hours

from astronaut_food_bot_MAIN import *


class Dinner(Meal):
    """Generates content specifically for dinner posts (6:30pm).
    The food types have different parameters/probabilities for being chosen
    than for other meals."""
    def __init__(self):
        super().__init__()
        self._meal_calorie_count = 0


    def create_meal(self):
        """Randomly generates meal components and formats them into facebook
        post.
        Returns:
            message(str): text to be posted to facebook"""
        image_foods = []
        
        #MAIN DISH
        #Chooses 1 main meal
        selected_list = self.select_foods_from_txt('mains.txt', 1)[0]
        mains = 'Main meal: ' + selected_list
        image_foods += [selected_list]

        #SIDE DISH
        no_of_sides = random.randint(1,2)
        #Randomly chooses either 1 or 2 side dishes
        selected_list = self.select_foods_from_txt('sides.txt', no_of_sides)
        #Take selected_list data and get photos, add photos to template
        sides = self.format_food_string('Side dish: ', 'Side dishes: ', \
                                                            selected_list)
        image_foods += selected_list

        #CONDIMENTS
        no_of_condiments = random.randint(0,2)
        #Randomly chooses either 0, 1, or 2 condiments
        selected_list = self.select_foods_from_txt('condiments.txt', \
                                                           no_of_condiments)
        condiments = self.format_food_string('Condiment: ', 'Condiments: ', \
                                                             selected_list)
        image_foods += selected_list
        
        #SNACKS
        no_of_snacks = random.randint(0,1)
        #Randomly chooses either 0 or 1 snacks
        snacks = None
        if no_of_snacks == 1:
            selected_list = self.select_foods_from_txt('snacks.txt', 1)[0]
            snacks = 'Snack: ' + selected_list
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
        image = ImageGen('dinner', image_foods)
        image.generate_picture()
        
        #Formatting meal into text for facebook post
        meal = [mains, sides, condiments, snacks, drinks]
        greetings = ['Here\'s what\'s planned for dinner tonight:', \
        'Been a hard day\'s work on the spaceship today, here is a nice meal to celebrate:', \
        'Enough! My spaceship sails in the morning. I wonder what\'s for dinner...', \
        'Dinner Time!']
        message = self.format_facebook_post(meal, greetings)
        return message



def main():
    dinner = Dinner()
    message = dinner.create_meal()
    post_to_facebook(TOKEN, message, '/home/pi/Desktop/Astronaut_food_bot/_image_generated.png')
    print('DINNER POST: \n' + message)

if __name__ == "__main__" :
    main()



"""ENOUGH! MY SHIP SAILS IN THE MORNING. I WONDER WHAT'S FOR DINNER.
GEE IT SURE IS BORING AROUND HERE. MAH BOI, THIS PEACE IS WHAT ALL TRUE
WARRIORS STRIVE FOR! I JUST WONDER WHAT GANON IS UP TO. SQUADALA ETC"""

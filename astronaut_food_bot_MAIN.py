# ASTRONAUT MEAL BOT - cooded by yandere dev spaghetti coding funtime spooktacular
# MAIN FILE

"""
Bot that randomly generates a breakfast, lunch and dinner containing a random
assortment of foods. The bot picks options from specific food types (drinks,
condiments, snacks, breakfast foods, mains, side-dishes). It also generates an
image representation of this meal and its components. Facebook posts are
scheduled at 7:30am (breakfast), 12:00pm (lunch), 6:30pm (dinner). There is a
33% chance of the bot also creating a Snack meal between breakfast and lunch
(10:00am) and/or between lunch and dinner (3:30pm). There is also a 10% chance
of the bot creating a midnight snack meal at 11:30pm.
"""

import random
from datetime import date
import facebook
import math
from PIL import Image

TOKEN = '[REDACTED]'



class Meal(object):
    """Abstract parent class with general functions to generate posts
    for any meal."""
    def __init__(self):
        self._meal_calorie_count = 0


    def meal_calorie_count(self):
        """Getter function, returns the total calorie count for the meal."""
        return self._meal_calorie_count

        
    def format_food_string(self, foodtype_singular, foodtype_plural, \
                                                           selected_list):
        """Formats the individual lines for the facebook post (food types
        are on their own lines). Probs should have put this in the function
        below but whatever
        Parameters:
            foodtype_singular(str): name of the food type; used if only one
            of that food type is selected.
            foodtype_plural(str): name of the food type; used if more than
            one of that food type is selected.
            selected_list(list): all the individually generated food items
            that are of the same food type
        Returns:
            food_formatted(str): formatted, individual line for facebook post"""
        food_formatted = ''
        
        if len(selected_list) == 0:
            return None
        
        elif len(selected_list) > 0:
            if len(selected_list) == 1:
                food_formatted += foodtype_singular
            else:
                food_formatted += foodtype_plural
            for index in range (0, len(selected_list)):
                if index == len(selected_list) - 1:
                    food_formatted += selected_list[index]
                else:
                    food_formatted += selected_list[index] + ', '
            return food_formatted


    def format_facebook_post(self, meal, greetings=['Meal time:']):
        """Takes all elements for the randomly generated meal and calorie
        values, and formats them correctly for a facebook post.
        Parameters:
            meal(list): contains all food items (already partly formatted)
            to be added to the post
            greetings(list): meal-specific phrases, one of which will be
            selected and put at the start of the post
        Returns:
            message(str): text output to post to facebook"""
        message = greetings[random.randint(0, len(greetings) - 1)] + '\n\n'
        for entry in meal:
            if entry is not None:
                message += entry + ' \n'
        message += '\nEnergy intake for meal: ' + \
                       str(self.meal_calorie_count()) + ' kJ'
        message += '\nTotal energy intake for today: ' + \
                       str(self.update_daily_calories()) + ' kJ'
        return message

                    
    def select_foods_from_txt(self, filename, no_of_foods = 1):
        """Looks through the text file for the relevant food type; converts the
        individual food names and their respective calorie values into readable
        data; randomly chooses individual food entries and appends calorie
        intake for the meal
        Parameters:
            filename(str): name of text file to open (depends on food type)
            no_of_foods(int): number of individual food entries to randomly
            choose. """
        filename = '/home/pi/Desktop/Astronaut_food_bot/' + filename
        try:
            fd = open(filename, 'r')
            text = fd.read()
            fd.close()
            #Remove line breaks
            text = text.split('\n')
        except Exception:
            print('Problem with the food text file. \n {}'.format(Exception))
        #Remove symbols between foods and calorie values
        foods_calories_dict = {}
        #Creating list of foods and dictionary for respective calorie values
        for entry in text:
            try:
                entry = entry.split(' | ')
                foods_calories_dict[entry[0]] = int(entry[1])
            except Exception:
                print('The text file is not formatted correctly. Fix pls. \n{}'.format(Exception))
                continue

        foods = list(foods_calories_dict.keys())
        selected_food = []
        previous_indexes = []

        #Exception handling if trying to generate more foods than the list contains
        if no_of_foods > len(foods):
            no_of_foods = len(foods)
            print('bro you can\'t just expect it to randomly generate more items')
            print('(with no repeats) than what there are in the list. i set the')
            print('number of foods it generates to be the exact size of the list.')
        
        for i in range (0, no_of_foods):
            #Generate random index for foods list (0 to last index of list)
            index = random.randint(0, len(foods) - 1)
            #Preventing duplicate food entries (checking previous_indexes)
            while index in previous_indexes:
                index = random.randint(0, len(foods) - 1)
            selected_food.append(foods[index])
            item_calories = foods_calories_dict[foods[index]]
            self._meal_calorie_count += item_calories
            previous_indexes.append(index)
        return selected_food


    def update_daily_calories(self):
        """Checks daily_calories.txt to see if it has been updated today. If it
        has not (first meal of day), it overwrites the file with today's date
        and calorie count for the current meal. If it has, it updates the file
        by adding the current meal's calorie count to the recorded amount.
        Returns:
            daily_calorie_count(int): the total amount of calories consumed
            today (so far)"""
        today = str(date.today())
        fd = open('/home/pi/Desktop/Astronaut_food_bot/daily_calories.txt', 'r')
        text = fd.read()
        fd.close()
        #Remove line breaks
        text = text.split('\n')
        daily_calorie_count = 0
        if text[0] == today:
        #If file was updated today
            daily_calorie_count = int(text[1]) + self._meal_calorie_count
        else:
        #If file was not updated today
            daily_calorie_count = self._meal_calorie_count
            
        file = open('/home/pi/Desktop/Astronaut_food_bot/daily_calories.txt', 'w')
        file.write(today + '\n' + str(daily_calorie_count))
        file.close()
        return daily_calorie_count



class ImageGen(object):
    """Functions for generating images and related stuff"""
    def __init__(self, meal_name, selected_foods):
        """self._template_dict has template file names and center point
        coordinates for placing foods. Snack/night have 3 center points (maximum
        3 food items can be selected for snacks). General templates have 8
        center points (max. 6-8 foods can be selected for meals)"""
        
        self._template_dict = {'night_template1.jpg': [(516, 337), (159, 242), (797, 233)], \
            'night_template2.jpg': [(509, 316), (131, 249), (839, 489)], \
            'snack_template1.jpg': [(480, 537), (839, 440), (147, 341)], \
            'snack_template2.jpg': [(509, 571), (132, 202), (863, 285)], \
            'snack_template3.jpeg': [(957, 475), (1577, 347), (401, 829)], \
            'template1.png': [(649, 245), (1053, 247), (400, 541), (1153, 559), \
                              (783, 559), (289, 831), (1113, 851), (721, 857)], \
            'template2.png': [(649, 255), (1053, 257), (400, 541), (1163, 559), \
                              (783, 559), (299, 781), (1113, 801), (721, 807)], \
            'template3.png': [(622, 103), (400, 103), (652, 327), (434, 320), \
                              (200, 326), (638, 473), (180, 477), (403, 486)], \
            'template4.png': [(325, 170), (753, 175), (1122, 190), (760, 430), \
                              (306, 433), (1136, 470), (289, 630), (750, 630)], \
            'template5.png': [(678, 105), (196, 111), (460, 113), (190, 236), \
                              (456, 242), (685, 247), (460, 400), (179, 401)], \
            'template6.png': [(193, 86), (453, 88), (670, 110), (182, 271), \
                              (448, 277), (680, 287), (449, 370), (172, 371)], \
            'template7.png': [(680, 90), (242, 115), (540, 172), (813, 181), \
                              (232, 298), (568, 370), (253, 466), (800, 470)],\
            'template8.png': [(798, 121), (515, 130), (222, 155), (673, 232), \
                              (243, 298), (800, 430), (233, 491), (578, 510)], \
            'template9.png': [(200, 100), (460, 90), (720, 100), (590, 191), \
                              (200, 250), (505, 380), (700, 450), (215, 450)], \
            'template10.png': [(250,220), (100,80), (550, 30), (330, 650), \
                               (60, 600), (80, 350), (380, 350), (230, 480)]}

        self._meal_name = meal_name
        self._selected_foods = selected_foods

        
    def choose_image_template(self):
        """Randomly chooses a template based on the value of self._meal_name.
        Returns:
            selected_template(str): file name/directory for the chosen template
        """
        if self._meal_name == 'snack':
            index = random.randint(2,4)
        elif self._meal_name == 'night snack':
            index = random.randint(0,1)
        else:
            index = random.randint(5,14)
        selected_template = list(self._template_dict.keys())[index]
        return selected_template


    def get_food_img_names(self):
        """Finds the file directories/names for food images; adds these to a
        dictionary with the associated food names.
        Returns:
            food_filename_dict(dict): food name(str) is the key, file name/
            directory is the value."""
        text_files = ['breakfast.txt', 'mains.txt', 'sides.txt', \
                      'condiments.txt', 'snacks.txt', 'drinks.txt']
        food_filename_dict = {}
        for filename in text_files:
            filename = '/home/pi/Desktop/Astronaut_food_bot/' + filename
            try:
                fd = open(filename, 'r')
                text = fd.read()
                fd.close()
                #Remove line breaks
                text = text.split('\n')
            except Exception:
                print('The text file is not formatted correctly. Fix pls. {0}\n{1}'.format(filename, Exception))
            temp_dict = {}
            #Removing symbols between foods, calories, image filepaths
            #Creating list of foods and dictionary for respective image filepaths
            for entry in text:
                try:
                    entry = entry.split(' | ')
                    temp_dict[entry[0]] = '/home/pi/Desktop/Astronaut_food_bot/FOOD_IMAGES/' + str(entry[2])
                except Exception:
                    print('The text file is not formatted correctly. Fix pls. {0}\n{1}'.format(filename, Exception))
                        
            food_filename_dict.update(temp_dict)
        return food_filename_dict


    def generate_picture(self):
        """Looks through the individual food items selected for each food type
        for the meal, finds the relevant pictures of these. Photos of the individual
        foods are resized to fit the template image and then superimposed in one of
        the possible positions. Image saved as '_image_generated.png'."""
        #Opening template
        selected_template = self.choose_image_template()
        template_file = '/home/pi/Desktop/Astronaut_food_bot/TEMPLATE_IMAGES/' \
                            + selected_template
        background = Image.open(template_file)
        bg_width, bg_height = background.size
        #boundary_dimensions give values that food images must resize to
        if bg_width >= bg_height:
            boundary_dimensions = (bg_width / 4, bg_width / 4)
        elif bg_width < bg_height:
            boundary_dimensions = (bg_height / 4, bg_height / 4)
        centre_points = self._template_dict[selected_template]
        previous_centre_points = []

        #Pasting each food photo onto the background
        food_filename_dict = self.get_food_img_names()
        for i in range(0, len(self._selected_foods)):
            food_file = food_filename_dict[self._selected_foods[i]]
            foreground = Image.open(food_file)
            foreground = foreground.convert('RGBA')
            fg_width, fg_height = foreground.size
            #Resizing the food image to be proportional to the background
            if fg_width >= fg_height:
                resize_factor = boundary_dimensions[0] / fg_width
            elif fg_width < fg_height:
                resize_factor = boundary_dimensions[1] / fg_height
            #resize_factor > 1 if image is to be made bigger, < 1 if made smaller
            foreground = foreground.resize((math.floor(fg_width * resize_factor), \
                                            math.floor(fg_height * resize_factor)))
            fg_width, fg_height = foreground.size

            #x1, y1 are coords for top left corner of the image
            x1 = math.floor(centre_points[i][0] - (fg_width / 2))
            y1 = math.floor(centre_points[i][1] - (fg_height / 2))
            
            background.paste(foreground, (x1, y1), foreground)
        background.save('/home/pi/Desktop/Astronaut_food_bot/_image_generated.png')              
        



#FACEBOOK POST FUNCTION
def post_to_facebook(token, message='the bot dun goofed. \nthere is no text to post.', \
                                                         image= '/home/pi/Desktop/Astronaut_food_bot/400.jpg'): 
    """Posts to facebook. Stolen from bot appreciation society wiki lol.
    Parameters:
        token(str): the token required by facebook to post
        message(str): text output that will be put into the facebook post"""
    graph = facebook.GraphAPI(token)
    post_id = graph.put_photo(image = open(image, 'rb'), message= message)['post_id']
    print('Successfully posted {0} to facebook'.format(post_id))


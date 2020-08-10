# Space-Food-Bot by yandere dev's spaghetti coding funtime spooktacular for the Bot Appreciation Society hackathon

A bot that randomly generates a meal for an astronaut to eat at certain times of the day (breakfast, lunch, dinner, snacks) and posts it to Facebook.

# GENERAL INFO OR WHATEVER


Space Food Bot randomly generates a breakfast, lunch and dinner meal itinerary for an astronaut, containing a random assortment of foods. 
Most of the foods that the bot chooses are foods that are/have been eaten by astronauts in space, including specially made dehydrated/preserved foods 
such as NASA foods and Russian cosmonaut foods, and commercially available food items that are/would likely be sent to space. 
The bot picks options from within specific food types (drinks, condiments, snacks, breakfast foods, mains, side-dishes), with different parameters for how 
many of each type it may pick for each meal (eg. for breakfast, the bot will pick 1 or 2 breakfast items, 0 or 1 drinks, 0, 1 or 2 condiments, 
and 0 or 1 snacks).
The bot also generates an image representation of this meal and its components (a very buggy one), by randomly selecting a template
to place the images on, and superimposing the images onto the template in certain positions. 
Every food item is assigned an energy intake value (kilojoules per serving). The value for every food item in a meal is added together to give a 
total energy amount for a meal. Every single meal within the day is also added together to give a total energy intake for that day.


Facebook posts are scheduled at 7:30am (breakfast), 12:00pm (lunch), 6:30pm (dinner). There is a 33% chance of the bot also creating a Snack meal 
between breakfast and lunch (10:00am) and/or between lunch and dinner (3:30pm). There is also a 10% chance of the bot creating a midnight snack 
meal at 11:30pm.

astronaut_food_bot_MAIN.py contains the majority of general functions/classes required. Other files (astronaut_food_bot_BREAKFAST, astronaut_food_bot_LUNCH,
astronaut_food_bot_DINNER, astronaut_food_bot_SNACK, astronaut_food_bot_NIGHT_SNACK) contain classes for their meal that generate the parameters.
The bot is currently being hosted on a raspberry pi with individual scripts for each meal being scheduled at the meal times.
Probably could have set that up in a much better way but oh well.

The bot sources its images from folders within the project directory. When it generates an image to post to facebook,
this is saved locally as '\_image_generated.png'. The bot also reads/writes to a lot of text files for things like food names, file names for images,
kilojoule amounts for each food and total kJ intake for the current day, etc.

The code is a big bowl of spaghetti and pretty poorly set out, 
please forgibe me i am only twelve and i do not have dad who is bill gate so i only teach myself codeing few month ago

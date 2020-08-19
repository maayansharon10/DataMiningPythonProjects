# recipesCrawler
A crawler using BS4 which extract valid links from website www.allrecipes.com and creating an output json file with the relevant information
This code was written by  Maayan Sharon and Imri Dror as part of DATA MINING course, in HUJI.
Grade: 100

# about the project:
in this assignment we created a crawler which extract valid links from website /www.allrecipes.com/
and creating an output json file with the relevant information.
mainly used beautifulSoup library.

# how did we do this?
first we extracted valid recipe links from given web page.
then checked which type of page is it (UNICORN or REGULAR) and extract the info into an InfoObj accordingly.
once there're 300 infoObj (each holding info from a valid recipe link),
code writes info into json file, according to the format mentioned in ex.

# clerification:
a unicorn page is a page which the first comment in its HTML is an ascii art of a unicorn.
if does not exists - will be treated as regular.
we assume there are no other forms of pages

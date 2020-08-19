
# This code was written by  Maayan Sharon and Imri Dror as part of DATA MINING course, in HUJI.
# Grade: 100

# about the project:
# in this assignment we created a crawler which extract valid links from website /www.allrecipes.com/
# and creating an output json file with the relevant information.
# mainly used beautifulSoup library.
# how did we do this?
# first we extracted valid recipe links from given web page.
# then checked which type of page is it (UNICORN or REGULAR) and extract the info into an InfoObj accordingly.
# once there're 300 infoObj (each holding info from a valid recipe link),
# code writes info into json file, according to the format mentioned in ex.

# clerification:
# a unicorn page is a page which the first comment in its HTML is an ascii art of a unicorn.
# if does not exists - will be treated as regular.
# we assume there are no other forms of pages

# ====================================================================================
# ------------------------------------ LIBRARIES -------------------------------------
# ====================================================================================

import time
import requests
from bs4 import BeautifulSoup, Comment
import json
import re

# ====================================================================================
# ----------------------------------- MAGIC NUMBERS ---------------------------------
# ====================================================================================
JPG = ".jpg"
PNG = ".png"
IMAGE = "image"
INTEGER = type(1)
UNICORN = "\n        /((((((\\\\\\\\\n=======((((((((((\\\\\\\\\\\n     ((           \\\\\\\\\\\\\\\n     ( (*    _/      \\\\\\\\\\\\\\\n       \\    /  \\      \\\\\\\\\\\\________________\n        |  |   |       </                  ((\\\\\\\\\n        o_|   /        /                      \\ \\\\\\\\    \\\\\\\\\\\\\\\n             |  ._    (                        \\ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n             | /                       /       /    \\\\\\\\\\\\\\     \\\\\n     .______/\\/     /                 /       /         \\\\\\\n    / __.____/    _/         ________(       /\\\n   / / / ________/`_________'         \\     /  \\_\n  / /  \\ \\                             \\   \\ \\_  \\\n ( <    \\ \\                             >  /    \\ \\\n  \\/     \\\\_                           / /       > )\n          \\_|                         / /       / /\n                                    _//       _//\n                                   /_|       /_|\n"
IS_UNICORN = "u"
REGULAR_LINK = "r"
UNICODE_DICT = {"\u00ae": "(registreted)", "\u00ac": "(copyrights)",
                "\u2122": "(trademark)", "\u2009": " ", "\u00bc": "1/4",
                "\u00bd": "1/2", "\u00be": "3/4", "\u2150": "1/7",
                "\u2151": "1/9", "\u2152": "1/10", "\u2153": "1/3",
                "\u2154": "2/3", "\u2155": "1/5", "\u2156": "2/5",
                "\u2157": "3/5", "\u2158": "4/5", "\u2159": "1/6",
                "\u215a": "5/6", "\u215b": "1/8", "\u215c": "3/8",
                "\u215d": "5/8", "\u215e": "7/8", "\"": "''"}


# ====================================================================================
# ----------------------------------------- CLASSES ----------------------------------
# ====================================================================================
class InfoObj:
    id_counter = 0

    def __init__(self, link="", title="", creator="", rating="",
                 num_reviews="", ingredients=None,
                 directions=None,
                 preptime="", cooktime="", totaltime="", servings=""):
        if ingredients is None:
            ingredients = []
        if directions is None:
            directions = []
        InfoObj.id_counter += 1
        self.id = InfoObj.id_counter
        self.link = link
        self.title = title
        self.creator = creator
        self.rating = rating
        self.num_reviews = num_reviews
        self.ingredients = ingredients
        self.directions = directions
        self.preptime = preptime
        self.cooktime = cooktime
        self.totaltime = totaltime
        self.serving = servings


# ====================================================================================
# ----------------------------------------- METHODS ----------------------------------
# ====================================================================================

# ------------------------ extracting links from main page + validation------------------------
def get_links(url):
    page_num = 1
    raw_links = []
    while len(raw_links) < 300:
        add = get_raw_links_from_page(url + '?page=' + str(page_num))
        time.sleep(2.5)
        raw_links.extend(add)
        raw_links = list(set(raw_links))
        page_num += 1
    return raw_links[:300]


def get_raw_links_from_page(url):
    main_page = requests.get(
        url)  # create a  soup object,convert into text and split according to lines
    main_soup = BeautifulSoup(main_page.text, 'html.parser')
    food_grid = main_soup.find(class_='fixed-grid')  # find only the relevant place in page:
    food_articles = food_grid.find_all('article')
    articles_text = str(food_articles).lower().split('\n')  # convert relevant articles to str
    raw_links = get_raw_links_from_txt(articles_text)  # return a list with recipe links, no duplicates
    return raw_links


def get_raw_links_from_txt(articles_text):
    raw_links = []
    # go over each line in text
    for line in articles_text:
        line_items = line.split('"')
        # check item is url
        for item in line_items:
            if 'https://www.allrecipes.com/recipe' not in item:  # validate it's a recipe link
                continue
            if item.endswith(JPG) or item.endswith(PNG):  # valid urls are not pictures
                continue
            # valid recipes's url looks like: https://www.allrecipes.com/recipe/SOME_DIGIT/
            item_split = item.split('/')
            if not item_split[4].isdigit():
                continue
            raw_links.append(item)
    raw_links = list(set(raw_links))  # eliminate duplicates
    return raw_links


def link_is_unicorn(soup):
    # check if there's a unicorn
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    # check if the page starts with a unicorn comment -
    return UNICORN in comments


# ~~~~~~~~~~~~~~~~~~~~~~~~~ extracting info from link ~~~~~~~~~~~~~~~~~~~~~~~~~

# ------------------------ REGULAR LINKS METHODS ------------------------

def extract_info_r_link(soup, link):
    # for regular link!!
    # create a BS object, collect relevant info from page and return info object

    try:
        title = title_get_string_r(soup, "recipe-summary__h1")
    except Exception:
        title = ""

    try:
        creator = title_get_string_r(soup, "submitter__name")
    except Exception:
        creator = ""

    try:
        rating = get_recipe_rating_r(soup)
    except Exception:
        rating = ""

    try:
        num_reviews = get_recipe_num_reviews_r(soup)
    except Exception:
        num_reviews = ""

    try:
        ingredients = get_recipe_ingredients_r(soup)
    except Exception:
        ingredients = []

    try:
        directions = get_directions_r(soup)
    except Exception:
        directions = []

    try:
        prep_time = get_recipe_time_tag_r(soup, "prepTime")
    except Exception:
        prep_time = ""

    try:
        cook_time = get_recipe_time_tag_r(soup, "cookTime")
    except Exception:
        cook_time = ""

    try:
        total_time = get_recipe_time_tag_r(soup, "totalTime")
    except Exception:
        total_time = ""

    try:
        servings = get_servings_r(soup)
    except Exception:
        servings = ""

    info_obj = InfoObj(link, title, creator, rating, num_reviews,
                       ingredients, directions, prep_time, cook_time,
                       total_time, servings)
    return info_obj


def title_get_string_r(soup, class_name):
    return unicode_to_value_in_string(soup.find(class_=class_name).string.strip())


def get_recipe_rating_r(soup):
    # returns the recipe's rating
    return soup.find("div", {"class": "rating-stars"})["data-ratingstars"]


def get_recipe_num_reviews_r(soup):
    # returns the recipe's num reviews
    num_reviews_raw = title_get_string_r(soup, "review-count")
    return get_single_num_str(num_reviews_raw)


def get_single_num_str(string):
    array = re.findall(r'[0-9]+', string)
    if len(array) == 0:
        return '0'
    else:
        return array[0]


def get_recipe_time_tag_r(soup, time_type):
    find_res = soup.find("time", {"itemprop": time_type})
    if find_res:
        return string_to_min_r(find_res["datetime"])

    else:
        return ""


def string_to_min_r(day_time):
    minutes = 0
    hours = 0
    days = 0
    if "M" in day_time:
        m_lst = re.findall(r"(\d+)M", day_time)
        if len(m_lst) > 0:
            minutes = float(m_lst[0])
    if "H" in day_time:
        h_lst = re.findall(r"(\d+)H", day_time)
        if len(h_lst) > 0:
            hours = float(h_lst[0])

    if "D" in day_time:
        d_lst = re.findall(r"(\d+)D", day_time)
        if len(d_lst) > 0:
            days = float(d_lst[0])

    return str(int(minutes + hours * 60 + days * 24 * 60))


def get_recipe_ingredients_r(soup):
    # returns the recipe's ingredients
    raw_list_of_ingredients = [i.string.strip() for i in soup.findAll("span", {"itemprop": "recipeIngredient"})]
    none_unicode_lst = [unicode_to_value_in_string(i) for i in
                        raw_list_of_ingredients]
    return none_unicode_lst


def get_directions_r(soup):
    # returns the recipe's directions
    raw_list_of_directions = [i for i in soup.findAll("li", {"class": "step"})]
    direction_list = []
    for i in raw_list_of_directions[:-1]:  # get's the child tag's string (
        # last one is exit item without string
        direction_list.append(unicode_to_value_in_string(i.find("span", {
            "class": "recipe-directions__list--item"}).string.strip()))
    return direction_list


def get_servings_r(soup):
    # returns the number of people this recipe can serve
    serving_class_raw = str(soup.find(
        class_="recipe-ingredients__header__toggles"))
    index = str(serving_class_raw).find("content=") + 8  # index of the serving
    #  num (the index of "content=" + its length
    return serving_class_raw[index:].split(chr(34))[1].split(chr(34))[0]


# ------------------------ UNICORN LINKS METHODS ------------------------

def extract_info_u_link(soup, link):
    # for unicorn link!!
    # create a BS object, collect relevant info from page:
    try:
        title = get_recipe_title_u(soup)
    except Exception:
        title = ""

    try:
        creator = get_recipe_creator_u(soup)
    except Exception:
        creator = ""

    try:
        rating = get_recipe_rating_u(soup)
    except Exception:
        rating = ""

    try:
        num_reviews = get_recipe_num_reviews_u(soup)
    except Exception:
        num_reviews = ""

    try:
        ingredients = get_recipe_ingredients_u(soup)
    except Exception:
        ingredients = []

    try:
        directions = get_directions_u(soup)
    except Exception:
        directions = []

    try:
        time_serving_dict = time_and_serving_getter_u(soup)  # returns a dict
    except Exception:
        time_serving_dict = {}

    try:
        servings = time_serving_dict.get("servings")
    except Exception:
        servings = ""

    try:
        prep_time = string_to_time_check(time_serving_dict.get("prep"))
    except Exception:
        prep_time = ""

    try:
        cook_time = string_to_time_check(time_serving_dict.get("cook"))
    except Exception:
        cook_time = ""

    try:
        total_time = string_to_time_check(time_serving_dict.get("total"))
    except Exception:
        total_time = ""

    infoObj = InfoObj(link, title, creator, rating, num_reviews,
                      ingredients, directions, prep_time, cook_time,
                      total_time, servings)

    return infoObj


def get_recipe_title_u(soup):
    # returns the recipe's title
    title_raw = soup.find(class_="headline heading-content")
    return unicode_to_value_in_string(
        str(title_raw).split('>')[1].split('<')[0])


def get_recipe_creator_u(soup):
    # returns the recipe's creator
    creator_raw_list = soup.findAll(class_="author-name")
    creator = ""
    for creat in creator_raw_list:
        if str(creat).split(">")[1][0] != "<":
            creator = str(creat).split('>')[1].split('<')[0]
    return creator


def get_recipe_rating_u(soup):
    # returns the recipe's rating
    rating_class_raw = soup.find(class_="recipe-review-container").find(
        class_="review-star-text")
    rating = str(rating_class_raw).split(':')[1].split("<")[0].strip(
    ).split(" ")[0]
    return rating


def get_recipe_num_reviews_u(soup):
    # returns the recipe's num reviews
    num_reviews_raw = soup.find(class_="review-headline-count")
    num_reviews = str(num_reviews_raw).split("(")[1].split(")")[0]
    return num_reviews


def time_and_serving_getter_u(soup):
    # The time and number of servings info of UNICORN pages are writen
    # together in the menu of the recipe. this function runs the basic soup
    # abstraction and write them as dictionary
    row_list_of_fields = soup.findAll(class_="recipe-meta-item")
    time_serving_dict = dict()
    for field in row_list_of_fields:  # extracting header + content of info
        #  the key(title of info) and value (content of the info)
        key_index = str(field).find("header" + chr(34) + ">\n")
        key = str(field)[key_index:].split(">\n")[1].split(":")[0].lower(
        ).strip()
        if key == "additional":
            key = "cook"
        value_index = str(field).find("body")
        value = str(field)[value_index:].split("<")[0].split("\n")[1].strip()
        time_serving_dict[key] = value
    return time_serving_dict


def get_recipe_ingredients_u(soup):
    # returns the recipe's ingredients
    raw_list_of_ingredients = [i.string.strip() for i in soup.findAll("span",
                                                                      {
                                                                          "class": "ingredients-item-name"})]
    none_unicode_lst = [unicode_to_value_in_string(i) for i in
                        raw_list_of_ingredients]
    return none_unicode_lst


def unicode_to_value_in_string(string):
    #  takes a unicode in sequence and replace it with known value from
    # dictionry
    for char in string:
        if char in UNICODE_DICT.keys():
            string = string.replace(char, UNICODE_DICT.get(char))
    return string


def get_directions_u(soup):
    # returns the recipe's directions
    row_list_of_directions = soup.findAll(
        class_="subcontainer instructions-section-item")
    direction_list = []
    for direc in row_list_of_directions:
        direction = str(direc).split("<p>")[1].split("</p>")[0]
        direction_list.append(unicode_to_value_in_string(direction))
    return direction_list


def string_to_min_u(string):
    # assuming it would always be in a valid format :"number min/hrs/days", "number h number m"
    # return time in minutes, is invalid return -1

    min_re = r"[0-9]+[ ]+mins"
    hrs_re = r"[0-9]+[ ]+hrs"
    days_re = r"[0-9]+[ ]+days"

    minutes = 0
    hrs = 0
    days = 0

    m_lst = re.findall(min_re, string)
    if len(m_lst) > 0:
        minutes = float(m_lst[0].split()[0])

    h_lst = re.findall(hrs_re, string)
    if len(h_lst) > 0:
        hrs = float(h_lst[0].split()[0])

    d_lst = re.findall(days_re, string)
    if len(d_lst) > 0:
        days = float(d_lst[0].split()[0])

    return int((minutes + hrs * 60 + days * 24 * 60))  # time in min (as int)


def string_to_time_check(string):
    # the string to time function is used on objects that may be None. this
    # function makes sure that it wouldn't cause error.
    if string is not None:
        return string_to_min_u(string)


# ~~~~~~~~~~~~~~~~~~~~~~~~~ writing into jason ~~~~~~~~~~~~~~~~~~~~~~~~~
def create_json(obj_list, filename):
    json_format = {
        "records": {"record": [info.__dict__ for info in obj_list]}}
    try:
        with open(filename + '.json', 'w+', encoding='utf-8') as txt:
            json.dump(json_format, txt, indent=4)
    finally:
        txt.close()


# ~~~~~~~~~~~~~~~~~~~~~~~~~ main function  ~~~~~~~~~~~~~~~~~~~~~~~~~
def main(url):
    links_lst = get_links(url)
    info_lst = []
    for link in links_lst:
        try:
            page = requests.get(link)
            soup = BeautifulSoup(page.text, 'html.parser')
            if link_is_unicorn(soup):
                info = extract_info_u_link(soup, link)
                info_lst.append(info)
            else:
                info = extract_info_r_link(soup, link)
                info_lst.append(info)
        except Exception:
            continue

    #  3.write into json
    create_json(info_lst, "output")


if __name__ == '__main__':
    web_url = "https://www.allrecipes.com/recipes/740/healthy-recipes/egg-free/"
    main(web_url)

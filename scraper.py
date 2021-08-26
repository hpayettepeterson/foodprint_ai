# pylint: disable=missing-docstring,line-too-long
from posixpath import join
import sys
import csv
from os import path
import requests
from bs4 import BeautifulSoup





#main() Update the method so that scrape_from_internet is called instead of scrape_from_file. Run a few tests like python recipe.py chocolate or python recipe.py strawberry. After each run, check the recipes folder and open the created CSV file. Does it look OK to you?
#main() with pagination: you now need to update the main and the scrape_from_internet functions so that the program does not stop at the first page of search results but downloads the first 5 pages of recipes if available!

def parse(html):

    #parse(html): this is the most important function. It needs to locate every
    # recipe on the page, and dive into the <div /> of a given recipe to
    # locate its name, difficulty level and preparation time.
    # After exploring the DOM, it will return
    # a list of dict containing 3 keys (name, difficulty, prep_time).

    # return a list of dict {name, difficulty, prep_time}

    #soup = BeautifulSoup(html, "html.parser")

    #print(soup)
    recipelist = []

    if html is None:
        return None



    for recipe in html.find_all("div", class_="p-2 recipe-details"):
        print('################')
        print(recipe)

        name = recipe.find("p", class_="recipe-name").string
        difficulty = recipe.find("span", class_="recipe-difficulty").string
        prep_time = recipe.find("span", class_="recipe-cooktime").string

        tempdict = {
            'name': name,
            'difficulty': difficulty,
            'prep_time': prep_time
        }

        recipelist.append(tempdict)

    print(recipelist)
    return recipelist



def write_csv(ingredient, recipes):
    # dump recipes to a CSV file `recipes/INGREDIENT.csv`

    #write_csv(ingredient, recipes): this method takes two parameters.
    # The first one is a str, the second one a list of dict.
    # It will create a CSV file {ingredient}.csv and store the recipes
    # from the list in the recipes directory.

    ingredient = (" ").join(ingredient)


    with open(f'recipes/{ingredient}.csv', 'w') as csvfile:
        #print(csvfile)
        writer = csv.DictWriter(csvfile, fieldnames=recipes[0].keys())
        #print(writer)
        writer.writeheader()

        for i in recipes:
            writer.writerow(i)




def scrape_from_internet(ingredient, start=1):
    # Use `requests` to get the HTML page of search results for given ingredients.

    # scrape_from_internet(ingredient, start):
    # this method will work on the website and search for the given ingredient.
    # Ignore the start parameter to begin with.
    # It should return the HTML from the page (to be fed to the parse method).


    url = f'https://recipes.lewagon.com/?search[query]={ingredient}&page={start}'

    print(url)

    response = requests.get(url, allow_redirects=False)

    if response.status_code == 302:
        return None

    print(response.status_code)

    soup = BeautifulSoup(response.content, "html.parser")
    #print(soup)


    return soup



    #response = requests.get(url).json()




def scrape_from_internet(ingredient, start=1):
    ''' Use `requests` to get the HTML page of search results for given ingredients. '''
    pass  # YOUR CODE HERE

def scrape_from_file(ingredient):
    file = f"pages/{ingredient}.html"
    if path.exists(file):
        return open(file)
    print("Please, run the following command first:")
    print(f'curl "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')
    sys.exit(1)


def main():
    if len(sys.argv) > 1:
        ingredient = sys.argv[1:]
        # Replace scrape_from_file with scrape_from_internet and implement pagination (more than 2 pages needed)
        allrecipes = []
        for page in range(1,6):

            recipes = parse(scrape_from_internet(ingredient, page))


            if recipes is None:
                break

            allrecipes += recipes


        print(allrecipes)
        write_csv(ingredient, allrecipes)
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)


if __name__ == '__main__':
    main()

# Soccer-Guru
Finds FIFA 22 Cards by Web Scraping and filter them based on overall base stats, league, rating and/or position.

## Dependencies
Before running main.py, the following dependencies are required:
- requests
- beautifulsoup4

These dependencies can be installed with pip or another package manager.

# Usage
## Creating 
As new cards are continually being released, run create() to create createpickle with the new fifa cards
``` 
create()
```
Note: you must delete the playerpickle file before doing this. Pickling is used in this project as making hundreds of get requests is time-consuming (even with multithreading) and so it would be better to store it.

## Filtering
Call print_top() to print the cards with best overall base stats. This function contains 4 parameters (all of which are optional)
- max_rating: the max rating you want to see
- league: the league of the card you want to see e.g. FRA 1
- country: a unique id that corresponds to country e.g. '12' (probably leave empty)
- show_number: how many rows/cards you want printed out

``` 
print_top(100, league="FRA 1", country="", show_number=10)
```

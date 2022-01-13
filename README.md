# pokersolverquery&#46;py


A Poker BaseSolver Query package for interacting with UPI engines such as PioSOLVER and jesolver

## Features
* Easy to use python interface
* General in options

## Installation
<!---
> *Requires Python 3.6 and above*
-->

<!---
You can install the module from [PyPI](https://pypi.org/project/playingcards.py/) or by using pip.

```sh
# Linux/MacOS
pip3 install playingcards.py

# Windows
pip install playingcards.py

```
-->
## How To Use
Import the solver object via:

```python
from pokersolverquery.solver import BaseSolver
```
Initiate the solver class and send any UPI command!

```python
solver = BaseSolver(solver_path=r'C:\PioSOLVER\PioSOLVER-edge.exe')

output = solver.command("load_tree QsJh2h")
range = solver.command("show_range OOP r")
```


<!---
### Class Attributes

* **Deck** Attributes
  * drawn_cards `dict` - Returns a dict of the values that were drawn from each corresponding suit.
  * cards `list` - Returns a list containing the class objects of each drawn card.
  * drawn `int` - Returns an integer of the amount of cards that have been drawn.
  * remaining `int` - Returns an integer amount of the remaining cards that can be drawn.

* **Card** Attributes
  * deck `Deck` - Returns a Deck object if the card was drawn from a deck. *Default: None*.
  * suit `int` - Returns an integer that corresponds with the card's suit.
  * suit_name `str` - Returns a string containing the converted suit name.
  * value `int` - Returns an integer of the card's face value.
  * rank `str|int` - Returns a string if the value can be converted into a word value (Ex. 11 -> Jack). Defaults to returning an integer if its not applicable (Ex. 2 -> 2).
  * name `str` - Returns a string containing the full name of the card. This prints out the rank and the suit of the card. (Ex. Ace of Spades, 3 of Hearts)
  * img `str` - Returns a string that contains an ASCII image of the card with the corresponding suit symbol.


### Class Arguments
A card object can be instantiated with preconceived values instead of using a random generator.

* Suits are ordered numerically from 0-3.

    * 0: **Spades**

    * 1: **Clubs**
  
    * 2: **Hearts**
  
    * 3: **Diamonds**

* Values are ordered numerically from 1-13.

  * 1: **Ace**

  * 2-10: **Face Value**

  * 11: **Jack**

  * 12: **Queen**
  
  * 13: **King**

-->
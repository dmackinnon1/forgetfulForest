# forgetfulForest
A generator and interactive page for "Forest of Forgetfulness" logic puzzles, based on ones found in "What is the Name of this Book?" by Raymond Smullyan.

A live example can be found [here](https://dmackinnon1.github.io/forgetfulForest/).

## Building the Puzzles
The puzzles are built by running the forest.py script in the build directory. This generates a json file in the data directory that contains the puzzle descriptions.

## Puzzle Pages

Loading *index.html* will display a random puzzle from the collection that you can attempt to solve.

![example](https://raw.githubusercontent.com/dmackinnon1/forgetfulForest/master/imgs/example.png)

To load a specific puzzle, you can provide the query parameter *id*, for example to obtain the puzzle shown above, you can load

```https://dmackinnon1.github.io/forgetfulForest/?id=5```





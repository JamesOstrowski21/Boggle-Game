# CS1210: HW3 version 1
######################################################################
# Complete the signed() function, certifying that:
#  1) the code below is entirely your own work, and
#  2) it has not been shared with anyone outside the intructional team.
#
def signed():
    return(["jostrowsk"])

######################################################################
# In this homework, you will build the internals for Boggle, a popular
# word game played with 16 6-sided dice. At the same time, in class we
# will develop the interactive user interface for Boggle, so that your
# solution, augmented with what we do in class, will give you a
# playable Boggle game. This assignment will also give us a chance to
# work on a system using the object-oriented paradigm.
#
# This is version 1 of the template file, which does not include the
# user interface.  I will periodically release updated versions, which
# you can then merge into your own code: still, be sure to follow the
# instructions carefully, so as to ensure your code will work with the
# new template versions that contain the GUI we develop in class.
#
# The rules of Boggle are available online. Basically, you will roll
# the dice and arrange them into a 4x4 grid. The top faces of the die
# will display letters, and your job is to find words starting
# anywhere in the grid using only adjacent letters (where "adjacent"
# means vertically, horizontally, and diagonally adjacent). In our
# version of Boggle, there are no word length constraints beyond those
# implicitly contained in the master word list.
#
# Although other dice configurations are possible, the original Boggle
# dice are (in no particular order):
D = ["aaeegn","abbjoo","achops","affkps","aoottw","cimotu","deilrx","delrvy",
     "distty","eeghnw","eeinsu","ehrtvw","eiosst","elrtty","himnqu","hlnnrz"]

# You will need sample() from the random module to roll the die.
from random import sample, randint

######################################################################
# Boggle is the base class for our system; it is analogous to the
# Othello class in our implementation of that game.  It contains all
# the important data elements for the current puzzle, including:
#    Boggle.board = the current puzzle board
#    Boggle.words = the master word list
#    Boggle.solns = the words found in the current puzzle board
#    Boggle.lpfxs = the legal prefixes found in the current puzzle board
# Additional data elements are used for the GUI and scoring, which
# will be added in subsequent versions of the template file.
#
# Note: we will opt to use Knuth's 5,757 element 5-letter word list
# ('words.dat') from the Wordnet puzzle, but the 113,809 element list
# of words from HW1 ('words.txt') should also work just as easily.
#
class Boggle ():
    # This is the class constructor. It should read in the specified
    # file containing the dictionary of legal words and then invoke
    # the play() method, which manages the game.
    def __init__(self, input='words.dat'):
        infile = open(input, 'r')#read in file
        self.read = infile.read().split() # split file
        infile.close() #close file 
        Boggle.words = self.readwords(input) #stash boggle.words
        Boggle.board = self.newgame() #stash boggle.board
        Boggle.solns = self.solve()  #stash boggle.solns
        print('{} words read.'.format(len(self.read)))
        self.play()

    # Printed representation of the Boggle object is used to provide a
    # view of the board in a 4x4 row/column arrangement.
    def __repr__(self):
        output = ""
        for x in range(4):# loop through board
            output += (' '.join(self.board[x])) #join board into string 
            output += ('\n') #and line after 4 letters 
        return output #output board


        
    # The readwords() method opens the file specified by filename,
    # reads in the word list converting words to lower case and
    # stripping any excess whitespace, and stores them in the
    # Boggle.words list.
    def readwords(self, filename):
        infile = (open(filename,'r')) #read file and store as infile
        words = infile.read().split() # split file into words
        for y in range(len(words)):
            words[y] = words[y].lower() #make every word lowercase
        self.words = words # store words in self.words
        return(self.words) #return list of words 
        

    # The newgame() method creates a new Boggle puzzle by rolling the
    # dice and assorting them to the 4x4 game board. After the puzzlel
    # is stashed in Boggle.board, the method also computes the set of
    # legal feasible word prefixes and stores this in Boggle.lpfxs.
    def newgame(self):
        L = []
        for z in range(4):
            L.append([]) # append 4 empty lists 
        Boggle.lpfxs = [] #initialize boggle.lpfxs
        x = 0
        while x < len(D):
            for i in range(4):
                for j in range(4):
                    L[i].append(D[x][randint(0,len(D[x])-1)]) #loop through and add random letter from each dice into nested list
                    x+=1  #increment while loop for each dice          
        self.board = L #stash board in self.board
        for z in self.readwords('words.dat'): #loop through words for prefixes 
            a = 1
            while a <= len(z): #loop for each word to get prefixes 
                Boggle.lpfxs.append(z[0:a]) #add each possible prefix to boggle.lpfxs
                a += 1
                
        return self.board #return the board
        
            

    # The solve() method constructs the list of words that are legally
    # embedded in the given Boggle puzzle. The general idea is search
    # recursively starting from each of the 16 puzzle positions,
    # accumulating solutions found into a list which is then stored on
    # Boggle.solns.
    #
    # The method makes use of two internal "helper" functions,
    # adjacencies() and extend(), which perform much of the work.
    def solve(self):
        sol = [] #initialize empty list for solutions 
        # Helper function adjacencies() returns all legal adjacent
        # board locations for a given location loc. A board location
        # is considered legal and adjacent if (i) it meets board size
        # constraints (ii) is not contained in the path so far, and
        # (iii) is adjacent to the specified location loc.
        def adjacencies(loc, path):
            L = []
            for i in range(4): #nested loop for each possible adjacent letter on the board 
                for j in range(4):
                    if (i,j) not in path: #make sure not in path
                        if i == loc[0] and j == loc[1]+1: #round of if statements to find each possible adjacent letter
                            L.append((i,j))
                        elif i == loc[0] and j == loc[1]-1:
                            L.append((i,j))
                        elif j == loc[1] and i == loc[0]+1:
                            L.append((i,j))
                        elif j == loc[1] and i == loc[0]-1:
                            L.append((i,j))
                        elif i == loc[0]+1 and j == loc[1]+1:
                            L.append((i,j))
                        elif i == loc[0]-1 and j == loc[1]+1:
                            L.append((i,j))
                        elif i == loc[0]+1 and j == loc[1]-1:
                            L.append((i,j))
                        elif i == loc[0]-1 and j == loc[1]-1:
                            L.append((i,j))
            return L # return a list of tuples that are adjacencies 
                    
                

        # Helper function extend() is a recursive function that takes
        # a location loc and a path traversed so far (exclusive of the
        # current location loc). Together, path and loc specify a word
        # or word prefix. If the word is in Boggle.words, add it to
        # Boggle.solns, because it can be constructed within the
        # current puzzle. Otherwise, if the curren prefix is still in
        # Boggle.lpfxs, attempt to extend the current path to all
        # adjacencies of location loc. To do this efficiently, a
        # particular path extension is abandoned if the current prefix
        # is no longer contained in self.lpfxs, because that means
        # there is no feasible solution to this puzzle reachable via
        # this extension to the current path/prefix.
        def extend(loc, path):
            if path == []: #when path is empty make first tuple in path current letter location 
                path.append(loc)
            word = "" #reset word to an empty string 
            for x in path: #loop through path and obtain each letter, combine into word 
                word += self.board[x[0]][x[1]]
            if word in self.words and word not in sol: #if word is in list of legal words, add to solutions. Check to make sure word not already in solution, some words can be found by multiple paths. 
                sol.append(word) #append legal words to solution 
            elif word in Boggle.lpfxs and word not in self.words: #if in prefix and not in list word list 
                for y in adjacencies(loc,path): #gather adjacencies  of current letter location 
                    if (word + self.board[y[0]][y[1]]) in Boggle.lpfxs: #if adjacent letter is still in prefix
                        path.append(y) #add adjacent letter to path 
                        extend(y,path) #recusively move on to the next letter in the path through same process
        for a in range(4): #nested loop for each letter on the board
            for b in range(4):
                extend((a,b),[]) #run extend to find all possible words from each letter on the board 
        self.solns = sol #stash solutions in solns 
        return(self.solns) #return list of solutions 

    # The extract() method takes a path and returns the underlying
    # word from the puzzle board.
    def extract(self, path): 
        w = "" #initiate empty string 
        for x in path:
            w += self.board[x[0]][x[1]] #add each letter from path into a string 
        return w #return string 
            

    # The checkpath() method takes a path and returns the word it
    # represents if the path is legal (i.e., formed of distinct and
    # sequentially adjacent locations) and realizes a legal word,
    # False otherwise.
    def checkpath(self, path):
        L  = self.extract(path) #run extract to get a word 
        if L in self.words: #check if word is legal 
            return(L)
        else:
            return False #if not legal return false 
    
    # The round() method plays a round (i.e., a single puzzle) of
    # Boggle. It should return True as long as the player is willing
    # to continue playing additional rounds of Boggle; when it returns
    # False, the Boggle game is over.
    #
    # Hint: Look to HW1's round() function for inspiration.
    #
    # This method will be replaced by an interactive version.
    def round(self):
        # The recover() helper function converts a list of integers
        # into a path. Thus '3 2 2 1 1 2 2 3' becomes [(3, 2), (2, 1),
        # (1, 2), (2, 3)].
        def recover(path):
            path1 = path.replace(" ","") #remove all whitespaces in list of coordinates 
            v = 0
            p = []
            while v <= (len(path1)-2):
                p.append((int(path1[v]),int(path1[v+1]))) #add each group of coordinates as a tuple to a list p 
                v += 2 #increment by 2 in order to have no repeats 
            return p
        wordcount = 0 #counter for correct words 
        answers = [] #empty list to store all correct answers 
        loop = False #loop parameter 
        while loop != True: #prompt the user on line below 
            user = input("Input r1 c1 r2 c2...; '/' = display; ':' = show; '+' = new puzzle; ',' = quit: where r1 c1 coorisponds to a path of row,column corrdinates")
            if user == '/': 
                output = ""
                for x in range(4): #reprint board is user desires to see display again 
                    output += (' '.join(self.board[x]))
                    output += ('\n')
                print(output)

            elif user == ':':
                print(wordcount, "words have been found so far") #print how current amount of correct answers 
                for f in answers: #loop through correct answers and print individually 
                    print(f)

            elif user == ',': # if user wishes to end game, stop the loop 
                loop = True

            elif user == '+':
                output = ""
                self.board = self.newgame()#create a new board 
                self.solve() #gather solutions for new board 
                if self.solns == []:
                    print("Board has no solutions please generate a new one") #if board has no solutions, prompt user to generate a new one 
                else:
                    print("** Cheat",self.solve()) #print list of solutions as a cheat 
                for x in range(4): #print the new board 
                    output += (' '.join(self.board[x]))
                    output += ('\n')
                print(output)

            else:
                u = recover(user) #if user enters coordinates, uses recover to get a list of coordinates 
                if self.checkpath(u) != False: #check if coordinates make a legal word 
                    wordcount +=1 #add 1 to word count 
                    answers.append(self.checkpath(u)) #add correct word to list of correct answers 
    # The play() method when invoked initiates a sequence of
    # individual Boggle rounds by repeatedly invoking the rounds()
    # method as long as the user indicates they are interested in
    # playing additional puzzles.
    #
    # Hint: Look to HW1's play() function for inspiration.
    #
    # This method will be replaced by an interactive version.
    def play(self):
        play = True #play loop parameter 
        while play == True:
            self.newgame() #generate a board 
            self.solve() #generate solutions 
            if self.solns == []: #check board for solutions 
                print("Board has no solutions please generate a new one") #if none prompt user to generate a new board 
            else:
                print("** Cheat",self.solve()) #print list of solutions as cheat 
            print("Welcome to boggle!") #Welcome the user to the game 
            print(self.__repr__()) #print the board 
            self.round() #begin a round 
            again = input("Would you like to play again y=yes n=no \n") #if they quit ask if they would like to play again 
            if again == 'y': #if they would like to play again 
                play = True
            elif again == 'n': #if not
                print("Thanks for playing")
                play = False

######################################################################
if __name__ == '__main__':
    Boggle()

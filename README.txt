this is a personal project in order to become a better programmer in my "free" time. 
the current project is creating a chess game with an function opponent which is entirely coded by me.
this coding will include assigning value to pieces and calculate the position score of each position.
In the beginning all the pieces will have the same value. A lot of games will be played by the computer
whilst the values of the pieces are altered, whenever a value is changed in a way which results in
repeated wins then this value will become the default value. Parhaps later the same is done for where 
the pieces are located on the board.

I made the decision to rush towards the AI part, this is because i have a lot of things to check if i am useing them correctly, for example how long can senctences
be? with two files open the max (non-simertrical) is the paragraph above but now i am writting in fullscreen and i still have room left at the side of the screen.

Since I assume that the computer will need a long time to figure out an approximation of the correct values i am planning to review my work after getting to this stage.

To Do:
- Begin with the AI part 
- visual representation of the board
- review my work

Learning process:
    Learned: 
        - Intergrating multiple files in a single program 
        - @property function (although i am not useing it)
        - look for tools/shortcuts: autodocstring can be a time saver, chatgpt for concepts which i dont know the name of.

    grasping the basics:
        - code comments: i am useing autodocstring for creating the template and currently i"m commenting on intuition not on best practices. 
        I need to review other peoples work/ official documentation for a better understanding
        - GitHub: useing solo is easy, i dont know how bigger groups do this in practice. furthermore i am uncertain how often to push an update
        - (parrent/child)Classes: i get the basics of classes but i am unsure when and how to override the parrent class. 
            - haveing values for single_move works but is this correct without explicitly overrideing the parrent class?
            - are piece scores better as a part of a class or on a different file so it can be easily accesed in order to change their values?
        - recursion: i needed to flatten a nested list with a variable depth, it worked wonderfully for this and i assume it is a quite usefull concept which i need
        to grasp better

    to learn:
        - creating algorithems: kind of import for an opponent but i dont know anything about algorithems beyond general knowledge
        - how to simulate two opponents in the backgrond, say one cpu thread dedicated to crunching this data and still have a usefull laptop for other work or
        creating a "server" on a old laptop to do the calculations
        - creating a visual and interactive enviroment to easily see what is going on.
        - understanding chess notation
        - understanding chess in general
        - read official documentation instead of googleing 
        - what type of cheat cheats are beneficial
        - techniques to silo and properly test new code in a vacuum 
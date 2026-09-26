make background color #121212

create heading "Welcome to CodePi Forms" with name "title"
make "title" color #00d2ff

create input "Type your name here..." with name "userName"

create button "Greeting Me" with name "greetBtn"
make "greetBtn" color #2ed573

when "greetBtn" is clicked:
    say text from "userName"

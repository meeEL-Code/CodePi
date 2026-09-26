make background color #1e1e2e

create heading "CodePi Multimedia" with name "title"
make "title" color #f9e2af

create image from "https://picsum.photos/400/200" with name "heroImg"

create link "Visit GitHub Profile" to "https://github.com/meeEL-Code" with name "myLink"
make "myLink" color #89b4fa

create input "Type something..." with name "userInput"
create button "Test Action" with name "myBtn"
make "myBtn" color #a6e3a1

when "myBtn" is clicked:
    say text from "userInput"

make background color #0f0f13

start card "profileCard"
    create image from "https://picsum.photos/400/200?random=1" with name "coverImg"
    create heading "Abdullah Al Mustafa" with name "nameTitle"
    make "nameTitle" color #ffffff
    create text "Creator of CodePi Language. Building awesome things with code." with name "bioText"
    create input "Leave a message..." with name "msgInput"
    create button "Send Message" with name "sendBtn"
    make "sendBtn" background #2563eb
    make "sendBtn" color #ffffff
end card

when "sendBtn" is clicked:
    say text from "msgInput"

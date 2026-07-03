OPENING_DIALOGUE = [
    ("COMMAND", "set_bg", "hotelentrance"),
    ("Mark", "mark_front_detailed.png", "Are you guys sure about this hotel? It looks haunted."),
    ("James", "james_front_detailed.png","We're only here for a night. Plus all the other hotels are expensive and fully booked."),
    ("Mia", "mia_front_detailed.png", "I'm sure we'll be able to find another hotel tomorrow. Let's just stay here for a night."),
    ("COMMAND", "set_bg", "hotelopening"),
    ("Narrator", None, "The group enters the hotel and walks towards the counter."),

    ("Receptionist", "receptionist_detailed.png","Oh! Guests... how lovely. We don't get that often."),
    ("Chloe", "chloe_front_detailed.png","Good day... We booked online. Two regular rooms."),
    
    ("Narrator",None, "A loud banging noise echoes from upstairs."),

    ("Jay", "jay_front_detailed.png","Uh... just wondering... are you guys renovating? That must explain the noise and lack of guests."),
    ("Receptionist","receptionist_detailed.png", "Sure... you can call it that."),

    ("Narrator", None,"The receptionist slowly hands them two keys."),

    ("James", "james_front_detailed.png","Do you guys have wifi here at least? Or is this like an old fashioned hotel...?"),
    ("Receptionist", "receptionist_detailed.png", "Oh there are connections here..."),
    ("Receptionist", "receptionist_detailed.png", "Although not all of them are visible."),
    ("Mia", "mia_front_detailed.png","That did not answer the question..."),
    ("Receptionist","receptionist_detailed.png", "Room 203 and 202. Level 2. You might hear some knocking on your door in the middle of the night."),
    ("Receptionist","receptionist_detailed.png", "But don't trouble yourself to answer."),
    ("James", "james_front_detailed.png","(quietly) Whatever that means..."),
    ("COMMAND", "set_bg", "hotelrooms"),
    ("Narrator", None,"The group walks towards their rooms."),

    ("Mark","mark_front_detailed.png", "Yeah, I don't like how that guy was acting. And tell me I wasn't the only one that heard the noise."),
    ("Mia", "mia_front_detailed.png","Relax. He's just an old guy being weird."),

    ("Narrator",None, "Another loud banging sound is heard."),

    ("Mia", "mia_front_detailed.png","Erm... well he did say they were renovating..."),
    ("Jay", "jay_front_detailed.png","It's only a night, Mark. Plus we're paying 50 bucks per night. Obviously it's not going to be the best looking hotel."),
    ("Mark","mark_front_detailed.png", "There better be hot water at least to repay for all the mental stress they're putting me through."),
    ("Chloe", "chloe_front_detailed.png","Our rooms are only beside each other. If there's anything we can always just call each other for help."),

    ("Narrator", None,"Mia opens the room door."),

    ("Mia", "mia_front_detailed.png","Well me and Chloe are tired so we'll go to bed first."),
    
    ("COMMAND", "set_bg", "miaroom"),

    ("Narrator", None,"Inside Mia and Chloe's room."),

    ("Chloe", "chloe_front_detailed.png","Don't you think Mark is being too dramatic? It's only one night."),
    ("Mia", "mia_front_detailed.png","He always is. I'm sure we'll find a proper place to stay tomorrow."),
    ("Chloe", "chloe_front_detailed.png","Yeah... well we should go to bed. All the walking made me too tired."),

    ("Narrator",None, "The lights are switched off."),

    ("Mia", "mia_front_detailed.png","Good night."),
]

JANITOR_DIALOGUE = [

    ("Narrator",None, "In the middle of the night..."),

    ("Narrator", None,"Chloe suddenly screams."),

    ("Mia", "mia_front_detailed.png","Chloe?? Is that you?? Are you okay?"),

    ("Narrator", None,"Mia switches on the light."),

    ("Narrator", None,"Chloe is gone."),

    ("Mia", "mia_front_detailed.png","Chloe this isn't funny."),

    ("COMMAND", "move_path", [
        
    (1056, 1442), #fix coordinates
    (1420, 1439),
    (1625, 1512),
    (1498, 1910)

    ]),

    ("Narrator",None, "Mia rushes to the boys' room and knocks on the door."),

    ("Mia", "mia_front_detailed.png","Mark? James? Is Chloe in there with you?"),
    ("Mia", "mia_front_detailed.png","Jay? C'mon guys this isn't funny."),

    ("Narrator",None, "The hallway lights begin to flicker."),

    ("COMMAND", "move_path", [
        
    (1625, 1512)

    ]),


    ("Narrator", None,"Mia tries to return to her room but the door is now locked."),

    ("Narrator",None, "She notices a note on the floor."),

    ("Note",None, "If you want to see them again, find the keys. He's watching. Find the clues before he finds you."),

    ("COMMAND", "spawn_janitor", (1700, 1189)),

    ("Narrator",None, "Mia looks up and sees the janitor standing at the end of the hallway."),


    ("Janitor","janitor_detailed.png", "He's coming."),

    ("Narrator","janitor_detailed.png", "The janitor slowly walks towards Mia with a weapon in hand."),

    ("Mia", "mia_front_detailed.png", "What are you doing? Who's coming?"),

    ("Narrator",None, "The janitor suddenly starts chasing Mia."),

    ("COMMAND", "move_path", [
        
    (1872,2064),
    (2256, 2112)

    ]),



    ("Narrator", None,"Mia runs through the hallway until she finds an open room and locks the door behind her."),


    ("Objectives", None,"Find clues and keys around the hotel."),
    ("Objectives",None, "Use clues to unlock a weapon."),
    ("Objectives",None, "Rescue your friends."),
    ("Objectives", None,"Use keys to help save your friends."),
    ("Objectives", None,"Avoid and defeat the janitor."),
    ("Objectives",None, "Once the janitor is defeated, Level 2 will unlock."),

]

SAVECHLOE_DIALOGUE = [ ("Chloe", "chloe_front_detailed.png","Mia, thank god! "),
                       ("Mia", "mia_front_detailed.png", "Get to a safe room and hide. I'll save the others."),
                       ("Chloe", "chloe_front_detailed.png","Okay... "), 
                       ("Chloe", "chloe_front_detailed.png","By the way, I heard Jay's scream in a room near the gym."),
                       ("Mia", "mia_front_detailed.png", "Alright, thanks."),]

SAVEJAY_DIALOGUE = [   ("Mia", "mia_front_detailed.png", "Chloe's hiding somewhere. Go find her and hide."),
                       ("Jay", "jay_front_detailed.png", "Okay..."),
                    ]

SAVEMARK_DIALOGUE = [ ("Mark", "mark_front_detailed.png","Oh my god, mia! What's happening? "),
                       ("Mia", "mia_front_detailed.png", "Shh...get to a room and hide with the others first."),
                       ("Mia", "mia_front_detailed.png", "Once i find james, then we'll get out of here together."),
                       ("James", "james_front_detailed.png","SOMEBODY HELP!"),
                       ] 

SAVEJAMES_DIALOGUE = [ ("James", "james_front_detailed.png","Mia, im so glad youre okay! Wheres everyone else? "),
                       ("Mia", "mia_front_detailed.png", "No time to explain. "),
                       ("Mia", "mia_front_detailed.png", "We have to go right now! "),
                       ] 

ENDING_DIALOGUE = [
    ("COMMAND", "set_bg", "hotelentrance"),

    ("Mia", "mia_front_detailed.png", "H-hey… is everyone here? Please tell me we're all out."),
    ("Mark", "mark_front_detailed.png", "I'm here… I think I'm alive. I swear I'm never stepping into a place like that again."),
    ("Chloe", "chloe_front_detailed.png", "My legs are still shaking… that wasn't just a haunted hotel, that was something else."),
    ("James", "james_front_detailed.png", "We should've left the moment the lights started flickering…"),
    ("Jay", "jay_front_detailed.png", "James, don't say that now… just—just be glad we made it out."),

    ("COMMAND", "pause", 500),

    ("James", "james_front_detailed.png", "Do you guys hear that…?"),
    ("Chloe", "chloe_front_detailed.png", "Don't. Don't start that again."),
    ("Jay", "jay_front_detailed.png", "It's just the wind. It HAS to be just the wind."),

    ("Mia", "mia_front_detailed.png", "…We're not going back. Ever."),

    ("Narrator", None, "Mia and her friends escaped that haunted hotel and swore to never go there again."),
    ("Narrator", None, "Thank you for playing our game!")
]

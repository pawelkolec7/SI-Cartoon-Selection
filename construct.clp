(deftemplate UI-state
   (slot display (default none))
   (slot fact-name (default none))
   (slot response (default none))
   (multislot valid-answers)
   (slot state (default middle)))

(defrule system-start ""
  =>
  (assert (UI-state (display welcomeMessage)
                    (valid-answers welcomeAnswer)
                    (fact-name start))))

(defrule video-game-based ""
   (start welcomeAnswer)
   =>
   (assert (UI-state (display StartQuestion)
                     (valid-answers Yes No)
                     (fact-name video-game-based))))

(defrule a-celebrity ""
   (video-game-based No)
   =>
   (assert (UI-state (display CelebrityQuestion)
                     (valid-answers Yes No)
                     (fact-name celebrity))))

(defrule if-nintendo-franchise ""
   (video-game-based Yes)
   =>
   (assert (UI-state (display NintendoQuestion)
                     (valid-answers Yes No)
                     (fact-name nintendo-franchise))))


(defrule if-animal-furries-and-the-like ""
   (celebrity No)
   =>
   (assert (UI-state (display AnimalQuestion)
                     (valid-answers Yes No)
                     (fact-name animals-furries))))

(defrule if-cats ""
   (animals-furries Yes)
   =>
   (assert (UI-state (display CatsQuestion)
                     (valid-answers Yes No)
                     (fact-name cats))))

(defrule if-rodents ""
   (cats No)
   =>
   (assert (UI-state (display RodentsQuestion)
                     (valid-answers Yes No)
                     (fact-name rodents))))


(defrule if-dinosaurs ""
   (rodents No)
   =>
   (assert (UI-state (display DinosaursQuestion)
                     (valid-answers Yes No)
                     (fact-name dinosaurs))))

(defrule if-ducks ""
   (dinosaurs No)
   =>
   (assert (UI-state (display DucksQuestion)
                     (valid-answers Yes No)
                     (fact-name ducks))))

(defrule if-bears ""
   (ducks No)
   =>
   (assert (UI-state (display BearsQuestion)
                     (valid-answers Yes No)
                     (fact-name bears))))

(defrule if-monkeys ""
   (bears No)
   =>
   (assert (UI-state (display MonkeysQuestion)
                     (valid-answers Yes No)
                     (fact-name monkeys))))

(defrule if-cows ""
   (monkeys No)
   =>
   (assert (UI-state (display CowsQuestion)
                     (valid-answers Yes No)
                     (fact-name cows))))

(defrule if-godless-abominations ""
   (cows No)
   =>
   (assert (UI-state (display GAQuestion)
                     (valid-answers Yes No)
                     (fact-name godless-abominations))))

(defrule if-giant-robots ""
   (animals-furries No)
   =>
   (assert (UI-state (display RobotsQuestion)
                     (valid-answers Yes No)
                     (fact-name giant-robots))))

(defrule if-movie-based ""
   (giant-robots No)
   =>
   (assert (UI-state (display MovieQuestion)
                     (valid-answers Yes No)
                     (fact-name movie-based))))

(defrule if-r-rated ""
   (movie-based Yes)
   =>
   (assert (UI-state (display RQuestion)
                     (valid-answers Yes No)
                     (fact-name r-rated))))

(defrule if-post-apo ""
   (movie-based No)
   =>
   (assert (UI-state (display PostApoQuestion)
                     (valid-answers Yes No)
                     (fact-name post-apo))))

(defrule if-swords-sorcery ""
   (post-apo No)
   =>
   (assert (UI-state (display SwordsQuestion)
                     (valid-answers Yes No)
                     (fact-name swords-sorcery))))

(defrule if-military-law ""
   (swords-sorcery No)
   =>
   (assert (UI-state (display MilitaryQuestion)
                     (valid-answers Yes No)
                     (fact-name military-law))))

(defrule if-space ""
   (military-law No)
   =>
   (assert (UI-state (display SpaceQuestion)
                     (valid-answers Yes No)
                     (fact-name space))))

(defrule if-cowboys ""
   (space No)
   =>
   (assert (UI-state (display CowboysQuestion)
                     (valid-answers Yes No)
                     (fact-name cowboys))))

(defrule if-understand-wgo ""
   (cowboys No)
   =>
   (assert (UI-state (display WgoQuestion)
                     (valid-answers Yes No)
                     (fact-name understand-wgo))))

(defrule if-kids-stuff ""
   (understand-wgo Yes)
   =>
   (assert (UI-state (display KidsQuestion)
                     (valid-answers Yes No)
                     (fact-name kids-stuff))))

(defrule if-educational ""
   (kids-stuff Yes)
   =>
   (assert (UI-state (display EduQuestion)
                     (valid-answers Yes No)
                     (fact-name educational))))

(defrule if-awesome ""
   (understand-wgo No)
   =>
   (assert (UI-state (display AwesomeQuestion)
                     (valid-answers Yes No)
                     (fact-name awesome-way))))

(defrule if-computers ""
   (kids-stuff No)
   =>
   (assert (UI-state (display CompQuestion)
                     (valid-answers Yes No)
                     (fact-name computers))))

(defrule if-outrageous ""
   (computers No)
   =>
   (assert (UI-state (display OutrageusQuestion)
                     (valid-answers Yes No)
                     (fact-name outrageous))))

(defrule if-undead ""
   (outrageous No)
   =>
   (assert (UI-state (display UndeadQuestion)
                     (valid-answers Yes No)
                     (fact-name undead))))

(defrule response-nintendo-franchise-yes ""
  (nintendo-franchise Yes)
  =>
  (assert (UI-state (display property-nintendo-franchise-yes)
            (state final))))

(defrule response-nintendo-franchise-no ""
  (nintendo-franchise No)
  =>
  (assert (UI-state (display property-nintendo-franchise-no)
            (state final))))

(defrule response-celebrity-yes ""
  (celebrity Yes)
  =>
  (assert (UI-state (display property-celebrity-yes)
            (state final))))

(defrule response-cats-yes ""
  (cats Yes)
  =>
  (assert (UI-state (display property-cats-yes)
            (state final))))

(defrule response-rodents-yes ""
  (rodents Yes)
  =>
  (assert (UI-state (display property-rodents-yes)
            (state final))))

(defrule response-dinosaurs-yes ""
  (dinosaurs Yes)
  =>
  (assert (UI-state (display property-dinosaurs-yes)
            (state final))))

(defrule response-ducks-yes ""
  (ducks Yes)
  =>
  (assert (UI-state (display property-ducks-yes)
            (state final))))

(defrule response-bears-yes ""
  (bears Yes)
  =>
  (assert (UI-state (display property-bears-yes)
            (state final))))

(defrule response-monkeys-yes ""
  (monkeys Yes)
  =>
  (assert (UI-state (display property-monkeys-yes)
            (state final))))

(defrule response-cows-yes ""
  (cows Yes)
  =>
  (assert (UI-state (display property-cows-yes)
            (state final))))

(defrule response-godless-abominations-yes ""
  (godless-abominations Yes)
  =>
  (assert (UI-state (display property-godless-abominations-yes)
            (state final))))

(defrule response-godless-abominations-no ""
  (godless-abominations No)
  =>
  (assert (UI-state (display property-godless-abominations-no)
            (state final))))

(defrule response-giant-robots-yes ""
  (giant-robots Yes)
  =>
  (assert (UI-state (display property-giant-robots-yes)
            (state final))))

(defrule response-r-rated-yes ""
  (r-rated Yes)
  =>
  (assert (UI-state (display property-r-rated-yes)
            (state final))))

(defrule response-r-rated-no ""
  (r-rated No)
  =>
  (assert (UI-state (display property-r-rated-no)
            (state final))))

(defrule response-post-apo-yes ""
  (post-apo Yes)
  =>
  (assert (UI-state (display property-post-apo-yes)
            (state final))))

(defrule response-swords-sorcery-yes ""
  (swords-sorcery Yes)
  =>
  (assert (UI-state (display property-swords-sorcery-yes)
            (state final))))

(defrule response-military-law-yes ""
  (military-law Yes)
  =>
  (assert (UI-state (display property-military-law-yes)
            (state final))))

(defrule response-space-yes ""
  (space Yes)
  =>
  (assert (UI-state (display property-space-yes)
            (state final))))

(defrule response-cowboys-yes ""
  (cowboys Yes)
  =>
  (assert (UI-state (display property-cowboys-yes)
            (state final))))

(defrule response-educational-yes ""
  (educational Yes)
  =>
  (assert (UI-state (display property-educational-yes)
            (state final))))

(defrule response-educational-no ""
  (educational No)
  =>
  (assert (UI-state (display property-educational-no)
            (state final))))

(defrule response-computers-yes ""
  (computers Yes)
  =>
  (assert (UI-state (display property-computers-yes)
            (state final))))

(defrule response-outrageous-yes ""
  (outrageous Yes)
  =>
  (assert (UI-state (display property-outrageous-yes)
            (state final))))

(defrule response-undead-yes ""
  (undead Yes)
  =>
  (assert (UI-state (display property-undead-yes)
            (state final))))

(defrule response-undead-no ""
  (undead No)
  =>
  (assert (UI-state (display property-undead-no)
            (state final))))

(defrule response-awesome-yes ""
  (awesome-way Yes)
  =>
  (assert (UI-state (display property-awesome-yes)
            (state final))))

(defrule response-awesome-no ""
  (awesome-way No)
  =>
  (assert (UI-state (display property-awesome-no)
            (state final))))

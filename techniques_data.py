#File name techniques_data.py
#Advanced Techniques
adv_punches = ["jab", "cross", "left hook", "right hook", "body cross", "left uppercut", "right uppercut", "left body hook", "right body hook", "body jab","superman punch", "left spinning back fist", "right spinning back fist"]
adv_kicks = ["left low kick", "right low kick", "left body kick", "right body kick", "left head kick", "right head kick", "left teep (push kick)", "right teep (push kick)", "left spinning hook kick", "right spinning hook kick", "left spinning back kick", "right spinning back kick"]
adv_elbows = ["horizontal left elbow", "horizontal right elbow", "left upward elbow", "right upward elbow", "left downward elbow", "right downward elbow", "left spinning elbow", "right spinning elbow", "superman elbow"]
adv_knee = ["left knee", "right knee", "left jumping knee", "right jumping knee", "right spear knee", "left spear knee"]
fake_outs = ["feint-jab to cross", "feint-cross to left hook", "jab high punch low", "feint-jab then overhand right(or left hook)", "feint-jab to uppercut", "feint-strike to low kick",
"fake low kick to head kick", "fake low kick to hook", "fake teep (push kick) to strike", "fake roundhouse kick to teep (push kick)", "fake switch kick to cross", "jab high to kick low", "jab to the body, then hook to the head",
"level change to uppercut", "Dutch-style feinting (punch-kick,feint)", "The hesitation kick", "the kick-to-catch-and-sweep"]
#Beginner Techniques
beg_punches = ["jab","cross", "left hook", "right hook", "left uppercut", "right uppercut", "left body hook", "right body hook" ]
beg_kicks = ["left low kick", "right low kick", "left body kick", "right body kick", "left teep (push kick)", "right teep (push kick)"]
beg_elbows = ["horizontal left elbow", "horizontal right elbow"]
beg_knee = ["left horizontal knee", "right horizontal knee"]
#Mapping for customized options
specific_category_mapping = {"specific_kicks":adv_kicks, "specific_punches":adv_punches, "specific_elbows":adv_elbows, "specific_knees":adv_knee, "specific_fake_feints":fake_outs}
random_category_mapping = {"random_kicks":adv_kicks, "random_punches":adv_punches, "random_elbows":adv_elbows, "random_knees":adv_knee, "random_fake_feints":fake_outs}

#Techniques Information
technique_info = [
 {
 "name": "jab",
 "description": "Quick straight punch with lead hand",
 "tip": "Keeping your right guard up, aim at the head area and snap it back quickly back to guard position, All in one motion"
 },
 {
 "name": "cross",
 "description": "Straight power punch with rear hand",
 "tip": "Keeping you left guard up, rotate your hips, pivot your back foot and snap it back quickly back to guard position, All in one motion"

 },
 {
 "name": "left hook",
 "description": "A semicircular, looping punch thrown with the lead (left) hand. It targets the side of the opponent's head and is very powerful.",
 "tip": "Keeping your right guard up, rotate your hips, pivot your back foot and snap it back quickly back to guard position, All in one motion"
 },
 {
 "name": "right hook",
 "description": "The same semicircular, looping punch thrown with the rear (right) hand. It's often used as a finishing blow and is typically the fighter's most powerful hook.",
 "tip": "Keeping your left guard up, rotate your hips, pivot your back foot and snap it back quickly back to guard position, All in one motion"
 },
 {
 "name": "left uppercut",
 "description": "A short-range, vertical punch thrown in an upward motion with the lead (left) hand. It's used to attack the opponent's chin from below.",
 "tip": "Keeping your right guard up, shift your weight slightly to your front foot and bend your knees and waist, dropping your lead hand a little to load the punch. Explode upwards, driving through your legs, All in one motion."
 },
 {
 "name": "right uppercut",
 "description": "The same upward-angled punch thrown with the rear (right) hand. It's a devastating punch, especially in close-range exchanges.",
 "tip": "Keeping your left guard up, use the same mechanics as the left hook, but drive off your rear (right) foot, All in one motion."
 },
 {
 "name": "left body hook",
 "description": "A hook thrown with the lead (left) hand, but instead of targeting the head, it is aimed at the opponent's midsection, often at the ribs or liver area.",
 "tip": "Keeping your right guard up, crouch slightly and bend your knees and waist to change the angle of your punch, targeting the ribs or liver area. The mechanics are the same as a head hook (hip rotation, bent elbow), but the path is directed lower."
 },
 {
 "name": "right body hook",
 "description": "A hook thrown with the lead (right) hand, but instead of targeting the head, it is aimed at the opponent's midsection, often at the ribs area.",
 "tip": "Keeping your left guard up, crouch slightly and bend your knees and waist to change the angle of your punch, targeting the ribs area. The mechanics are the same as a head hook (hip rotation, bent elbow), but the path is directed lower."
 },
 {
 "name": "left low kick",
 "description": "A powerful roundhouse kick targeting the opponent's lead leg, usually the outer or inner thigh. It's thrown with the rear (left) leg.",
 "tip": "Generate power by stepping out and pivoting on your lead foot, driving your hips and shin through the target while maintaining a guard"

 },
 {
 "name": "right low kick",
 "description": "The same powerful roundhouse kick, but thrown with the rear (right) leg, targeting the opponent's lead leg.",
 "tip": "Generate power by stepping out and pivoting on your lead foot, driving your hips and shin through the target while maintaining a guard"
 },
 {
 "name": "left body kick",
 "description": " A powerful roundhouse kick targeting the opponent's torso (ribs, liver, arms). Thrown with the rear (left) leg.",
 "tip": "Focus on strong hip rotation and driving your shin through the target's torso, ensuring good balance and a strong guard."
 },
 {
 "name": "right body kick",
 "description": "The same powerful roundhouse kick, but thrown with the rear (right) leg, targeting the opponent's torso.",
 "tip": "Focus on strong hip rotation and driving your shin through the target's torso, ensuring good balance and a strong guard."
 },
 {
 "name": "left teep (push kick)",
 "description": "A straight push kick thrown with the lead (left) leg, often targeting the opponent's midsection or solar plexus.",
 "tip": "Shift weight back, chamber the knee high, and thrust the ball of the foot or heel directly forward into the target, retracting quickly"
 },
 {
 "name": "right teep (push kick)",
 "description": "A powerful push kick thrown with the rear (right) leg, targeting the midsection, hips, or even the face.",
 "tip": "Drive off the rear foot, bring the knee up, and thrust forward with the hip, aiming the ball of the foot or heel at the target."
 },
 {
 "name": "horizontal left elbow",
 "description": "A horizontal, slashing elbow strike thrown with the lead (left) hand, parallel to the ground. Often used to cut the opponent's brow or forehead, or target the jaw/temple.",
 "tip": " Rotate your hips and pivot on your lead foot to deliver a sharp, horizontal elbow strike, keeping the movement compact and your opposite hand up for defense."
 },
 {
 "name": "horizontal right elbow",
 "description": "A powerful horizontal elbow strike thrown with the rear (right) hand, parallel to the ground. Targets include the chin, temples, brow, or nose.",
 "tip": "Use strong hip rotation and a pivot on your rear foot to throw a powerful, horizontal elbow, maintaining a tight guard with your opposite hand"
 },
 {
 "name": "left horizontal knee",
 "description": "A powerful close-range knee strike, using the lead (left) leg",
 "tip": "Lift the knee, thrust it forward using hip and calf drive into the midsection or ribs, and push off the ball of the standing foot for power."
 },
 {
 "name": "right horizontal knee",
 "description": "A powerful close-range knee strike, similar to the lead horizontal knee but thrown with the rear (right) leg.",
 "tip": "Drive off the lead foot, lifting and thrusting the rear knee forward/upward, engaging the hip for power while maintaining a tight guard."
 },
 {
 "name": "body cross",
 "description": "A powerful punch thrown with the rear hand that crosses the body, generating force from the hips and torso and traveling in a straight line towards the opponent's body or midsection.",
 "tip": "Rotate your hips and pivot your rear foot to drive power through your core and into the punch. While keeping a tight guard"
 },
 {
 "name": "body jab",
 "description": "A quick, straight punch with the lead hand directed at the opponent's torso.",
 "tip": "Bend your knees and get low to shift your weight forward, using the jab to create an opening or wear down your opponent"
 },
 {
 "name": "superman punch",
 "description": "An explosive, flying punch where a fighter fakes a kick by lifting their knee, then quickly hops forward off the standing leg while extending a punch with the rear hand.",
 "tip": "Generate momentum and close the distance by jumping forward off your back leg as you throw the punch"
 },
 {
 "name": "left spinning back fist",
 "description": "A strike where a fighter turns their back towards the opponent and whips their left hand around, hitting with the back of the fist or forearm.",
 "tip": "Step across your body to create momentum, look over your shoulder at the target, and strike with the back of your left hand."
 },
 {
 "name": "right spinning back fist",
 "description": "Similar to the left spinning back fist, this strike uses the momentum of a turn to deliver a powerful blow with the back of the right fist.",
 "tip": "Take a step to the side with your left foot to initiate the spin and use the rotation of your torso to whip your right fist around"
 },
 {
 "name": "left spinning hook kick",
 "description": "A dynamic and powerful kick where a fighter spins on their standing foot, turning their back to the opponent, and whips their left leg in a horizontal hooking motion to strike with the heel. It is typically aimed at the head or temple.",
 "tip": "Focus on speed by turning your head quickly over your right shoulder to spot the target before snapping your left leg around."
 },
 {
 "name": "right spinning hook kick",
 "description": "Similar to the left version, this is a powerful spinning kick that uses the heel of the right foot to strike the opponent, often targeting the head.",
 "tip": "After turning your body, drive through with your hips as you extend your right leg in a hooking motion towards the target."
 },
 {
 "name": "left spinning back kick",
 "description": "A knockout technique where a fighter spins and extends their left leg straight back, driving their heel into the opponent. It is often aimed at the opponent's midsection or liver",
 "tip": "Drive your left heel straight back towards the target, leading the motion with your hips and keeping your toes pointed down."
 },
 {
 "name": "right spinning back kick",
 "description": "Similar to the left, this is a powerful kick where a fighter spins and thrusts their right heel straight back into the opponent's body.",
 "tip": "Initiate the spin by turning your body in one smooth motion, driving your heel directly into the target."
 },
 {
 "name": "left downward elbow",
 "description": "A short-range strike where the fighter brings their left elbow down in a vertical, chopping motion from 12 to 6 o'clock. It is often aimed at the top of the opponent's head or collarbone",
 "tip": "Chop your left elbow down with force, rotating your body to put more power behind the strike."
 },
 {
 "name": "right downward elbow",
 "description": "This is the same vertical, chopping elbow strike as the left downward elbow, but performed with the right arm.",
 "tip": "Elevate your right elbow by retracting your shoulder blade and turning your palm up to deliver a powerful, vertical strike."
 },
 {
 "name": "left spinning elbow",
 "description": "A strike where a fighter performs a full body spin and lands with the left elbow. The rotational force makes it an extremely powerful and surprising attack",
 "tip": "Use a step and body rotation to generate maximum momentum, hitting with the point of your left elbow."
 },
 {
 "name": "right spinning elbow",
 "description": "Similar to the left, this is a spinning elbow strike delivered with the right elbow. It requires careful timing but can be a devastating knockout blow",
 "tip": "Step across with your left foot to initiate the spin, turn your head to spot the target, and then unleash the rotating right elbow."
 },
 {
 "name": "superman elbow",
 "description": "An advanced, powerful elbow strike delivered by jumping forward, similar to a superman punch. It is used to close distance and deliver a cutting elbow strike to the opponent's head.",
 "tip": "Jump forward and land a slicing elbow as you close the distance, aiming for your opponent's eyebrow or forehead."
 },
 {
 "name": "left jumping knee",
 "description": "A knee strike where a fighter jumps with both feet and drives their left knee forward and up into the opponent's body or head. It can be used to catch an opponent off-guard or as a powerful finishing move",
 "tip": "Drive your hips and torso forward and jump explosively, pulling your left knee up towards your chest to generate force."
 },
 {
 "name": "right jumping knee",
 "description": "This is a jumping knee strike performed with the right knee, used to close distance and land a powerful strike. It is a high-risk, high-reward technique.",
 "tip": "Push off the ground explosively and drive your right knee upward, leaning your torso forward for balance and power."
 },
 {
 "name": "right spear knee",
 "description": "Also known as a stuffing knee, this is a powerful, straight-line knee strike where the fighter thrusts their right knee forward into the opponent's midsection. The hips drive the strike, making it a piercing blow.",
 "tip": "Thrust your hips forward powerfully as you drive your right knee straight into your opponent's midsection."
 },
 {
 "name": "left spear knee",
 "description": "The same powerful, straight-line knee strike as the right spear knee, but delivered with the left knee. It is an effective close-range technique for damaging an opponent's body",
 "tip": "Keep your heel directly under your knee as you drive it straight into your opponent, using your hips for maximum piercing force."
 },
#FAKE OUT and FEINTS TECHNIQUES
 {
 "name": "feint-jab to cross",
 "description": "A deceptive combination where you throw a quick, light jab feint to draw a reaction, then immediately follow with a powerful cross punch.",
 "tip": "Make the feint jab convincing by extending it halfway, then quickly retract and throw the cross while your opponent is reacting to the fake jab."
 },
 {
 "name": "feint-cross to left hook",
 "description": "A feinting technique where you start to throw a cross punch to draw your opponent's guard to one side, then quickly pivot and deliver a left hook.",
 "tip": "Begin the cross motion to get your opponent to move their guard, then immediately rotate your hips and deliver the left hook to the opening created."
 },
 {
 "name": "jab high punch low",
 "description": "A level-changing combination where you throw a jab to the head to raise your opponent's guard, then immediately follow with a punch to the body.",
 "tip": "After throwing the high jab, quickly bend your knees and lower your stance to deliver a powerful body shot while their guard is up high."
 },
 {
 "name": "feint-jab then overhand right(or left hook)",
 "description": "A setup where you throw a feint jab to occupy your opponent's attention, then deliver either an overhand right or left hook depending on their reaction.",
 "tip": "Use the feint jab to gauge your opponent's defensive reaction, then choose the overhand right if they duck or the left hook if they move their guard."
 },
 {
 "name": "feint-jab to uppercut",
 "description": "A deceptive boxing combination where you throw a fake jab to raise the opponent's guard, then immediately follow with an uppercut from underneath.",
 "tip": "Make the jab feint convincing to bring their hands up, then quickly drop your level and drive an uppercut through the gap underneath their guard."
 },
 {
 "name": "feint-strike to low kick",
 "description": "A setup technique where you feint a punch or elbow to occupy your opponent's upper body defense, then quickly transition to a low kick attack.",
 "tip": "Use any striking feint to draw their attention and guard upward, then immediately pivot and deliver a powerful low kick to their legs."
 },
 {
 "name": "fake low kick to head kick (question mark kick)",
 "description": "A deceptive kicking combination where you start a low kick motion to draw the opponent's attention downward, then quickly snap the same leg up for a head kick.",
 "tip": "Begin the low kick chamber and motion, then when your opponent drops their guard or tries to check, quickly redirect the kick upward to the head."
 },
 {
 "name": "fake low kick to hook",
 "description": "A combination that starts with a fake low kick to get your opponent to react or drop their hands, then quickly step in with a hook punch.",
 "tip": "Use the fake low kick to create a distraction and opening, then quickly plant your kicking leg and pivot into a powerful hook."
 },
 {
 "name": "fake teep (push kick) to strike",
 "description": "A feinting technique where you chamber for a teep kick to create distance or a reaction, then quickly plant and deliver a punch or different strike.",
 "tip": "Lift your knee as if throwing a teep to make your opponent back up or react, then quickly step down and close distance with a strike."
 },
 {
 "name": "fake roundhouse kick to teep (push kick)",
 "description": "A kicking feint where you start a roundhouse motion to get your opponent to react or move, then quickly change to a straight teep kick.",
 "tip": "Begin the roundhouse chamber and hip rotation, then quickly straighten your leg and drive forward with a teep when your opponent reacts."
 },
 {
 "name": "fake switch kick to cross",
 "description": "A technique where you fake a switch kick (stepping and kicking with the opposite leg) then quickly plant and throw a cross punch.",
 "tip": "Start the switch step motion to make your opponent expect a kick, then quickly plant your feet and drive through with a cross punch."
 },
 {
 "name": "jab high to kick low",
 "description": "A high-low combination that uses a jab to the head to raise the opponent's guard, then follows with a low kick to attack the legs.",
 "tip": "Throw the jab to bring their hands up and their attention to head level, then immediately follow with a low kick while their legs are unprotected."
 },
 {
 "name": "jab to the body, then hook to the head",
 "description": "A level-changing combination that starts with a body jab to lower the opponent's guard, then follows with a hook to the head.",
 "tip": "Drive the body jab low to make your opponent bring their guard down, then quickly come back up with a hook to the head opening."
 },
 {
 "name": "level change to uppercut",
 "description": "A boxing technique where you drop your level as if going for a takedown or body shot, then explode upward with an uppercut.",
 "tip": "Bend your knees and lower your stance to make your opponent expect a body attack, then drive up explosively through your legs into the uppercut."
 },
 {
 "name": "Dutch-style feinting (punch-kick,feint)",
 "description": "A Dutch kickboxing approach that uses continuous feinting between punches and kicks to keep opponents guessing and create openings.",
 "tip": "Flow between punch and kick feints in combination, using the constant motion and threats to overwhelm your opponent's defense."
 },
 {
 "name": "The hesitation kick",
 "description": "A timing-based technique where you pause or hesitate mid-kick motion to throw off your opponent's timing, then complete the kick.",
 "tip": "Start your kick normally, then pause for a split second when your opponent begins to react, then complete the kick with full commitment."
 },
 {
 "name": "the kick-to-catch-and-sweep",
 "description": "An advanced technique where you throw a kick that your opponent catches, then immediately sweep their supporting leg or transition to another attack.",
 "tip": "When throwing the kick, be ready for the catch and immediately attack their base by sweeping their standing leg or grabbing their head for a knee."
 }
]
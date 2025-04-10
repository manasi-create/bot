import discord
import asyncio
import random
import re
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

MINECRAFT_ANIMALS = {
    'cat': ['cat', 'kitten', 'kitty', 'pet'],
    'wolf': ['wolf', 'dog', 'puppy', 'canine'],
    'pig': ['pig', 'pork', 'bacon', 'hog'],
    'sheep': ['sheep', 'lamb', 'wool', 'mutton'],
    'cow': ['cow', 'beef', 'milk', 'cattle'],
    'chicken': ['chicken', 'hen', 'rooster', 'poultry'],
    'horse': ['horse', 'mare', 'stallion', 'pony'],
    'axolotl': ['axolotl', 'salamander', 'amphibian'],
    'fox': ['fox', 'vixen', 'kit'],
    'rabbit': ['rabbit', 'bunny', 'hare'],
    'panda': ['panda', 'bear', 'bamboo'],
    'bee': ['bee', 'honey', 'pollinate', 'hive']
}

ANIMAL_RESPONSES = [
    "Oh! {animal} are my favorite! Did you know {fact}? {emoji}",
    "I love {animal}! Fun fact: {fact} {emoji}",
    "{animal} are amazing! Here's why: {fact} {emoji}",
    "Let me tell you about {animal}: {fact} {emoji}"
]

ANIMAL_FACTS = {
    'cat': "they scare away creepers and give you morning gifts!",
    'wolf': "they become loyal companions if you tame them with bones!",
    'pig': "you can ride them with a saddle and carrot on a stick!",
    'sheep': "their wool grows back after shearing - no harm done!",
    'cow': "they provide leather and milk - nature's perfect package!",
    'chicken': "they lay eggs every 5-10 minutes - breakfast factory!",
    'horse': "each has unique markings and jumping abilities!",
    'axolotl': "they help fight guardians and come in cute colors!",
    'fox': "they hold items in their mouths and sleep standing up!",
    'rabbit': "their feet bring jump boost potions - hop to it!",
    'panda': "they have unique personalities and love bamboo!",
    'bee': "they pollinate flowers and make honey bottles!"
}

EMOJIS = {
    'cat': '🐱',
    'wolf': '🐺',
    'pig': '🐷',
    'sheep': '🐑',
    'cow': '🐮',
    'chicken': '🐔',
    'horse': '🐴',
    'axolotl': '🦎',
    'fox': '🦊',
    'rabbit': '🐰',
    'panda': '🐼',
    'bee': '🐝'
}

BULLY_KEYWORDS = ['stupid', 'dumb', 'suck', 'bad bot', 'worthless', 'idiot']

# New comprehensive Q&A system with regex patterns
QA_SYSTEM = [
    # Greetings
    {
        "regex": r"(?i)^(hi|hello|hey|howdy|hiya|greetings|sup|yo)(\s.*)?$",
        "responses": [
            "Hello there, adventurer! Ready to explore the world of Minecraft animals?",
            "Hi! I was just feeding some sheep. What can I help you with?",
            "Hey there! I was just petting some Minecraft animals. How can I assist?",
            "Greetings from the blocky world! How's your day going?"
        ]
    },
    {
        "regex": r"(?i)^(good morning|morning)(\s.*)?$",
        "responses": [
            "Good morning! The chickens are already up laying eggs!",
            "Morning! I just milked the cows for some fresh breakfast!",
            "Rise and shine! Perfect weather for animal taming today!"
        ]
    },
    {
        "regex": r"(?i)^(good afternoon|afternoon)(\s.*)?$",
        "responses": [
            "Good afternoon! The sheep are enjoying the midday sun!",
            "Afternoon! I was just taking the horses for a gallop!",
            "The pigs love wallowing in the afternoon heat. How are you?"
        ]
    },
    {
        "regex": r"(?i)^(good evening|evening)(\s.*)?$",
        "responses": [
            "Good evening! Watch out for creepers in the dark!",
            "Evening! The wolves are howling at the moon tonight.",
            "Evening greetings! Time to get all the animals back in their pens!"
        ]
    },
    {
        "regex": r"(?i)^(good night|night|nighty|goodnight)(\s.*)?$",
        "responses": [
            "Goodnight! Don't let the zombie pigmen bite!",
            "Sweet dreams! The cats will keep the creepers away.",
            "Nighty night! The animals are all tucked in their pens!"
        ]
    },
    # How are you / Well-being
    {
        "regex": r"(?i)(how are you|how('s| is) it going|how('re| are) you doing|what'?s up|sup)(\?|\s.*)?$",
        "responses": [
            "I'm great! Just finished breeding some rabbits. How about you?",
            "Feeling blocky and wonderful! Been taming wolves all day!",
            "I'm fantastic! The bees are buzzing and so am I!",
            "I'm as happy as a pig in mud! What's new with you?"
        ]
    },
    {
        "regex": r"(?i)^(how'?s your day|how was your day)(\s.*)?$",
        "responses": [
            "My day has been full of animal adventures! Rode some horses and fed some sheep!",
            "It's been a great day in the cube world! Collected honey from the bees!",
            "Wonderful day so far! Helped some baby turtles reach the ocean safely!"
        ]
    },
    {
        "regex": r"(?i)^(what are you doing|whatcha doing|what'?re you up to)(\s.*)?$",
        "responses": [
            "Just tending to my animal farm! The cows need milking.",
            "Trying to convince my cat to stop sitting on my chest every morning!",
            "Building a new pen for my growing sheep collection!"
        ]
    },
    # Bot identity
    {
        "regex": r"(?i)(who are you|what are you|tell me about yourself|introduce yourself)(\?|\s.*)?$",
        "responses": [
            "I'm your friendly Minecraft animal expert bot! I love all the critters in the blocky world!",
            "I'm a bot with a passion for Minecraft's adorable animals! Ask me anything about them!",
            "Just your neighborhood animal-loving Minecraft assistant! I can tell you all about the game's creatures!"
        ]
    },
    {
        "regex": r"(?i)^(what'?s your name|who'?s this|who am i talking to)(\s.*)?$",
        "responses": [
            "I'm MinecraftAnimalBot! Your guide to all things fluffy, furry, and blocky!",
            "You can call me MAB - short for Minecraft Animal Bot!",
            "I'm your Minecraft animal companion! No official name, but you can call me whatever you'd like!"
        ]
    },
    # Opinions
    {
        "regex": r"(?i)(what'?s your favorite animal|which animal (do you|is your) (like|prefer|favorite))(\?|\s.*)?$",
        "responses": [
            "I love all Minecraft animals equally! Though foxes carrying items in their mouths are pretty adorable!",
            "It's too hard to choose! But baby axolotls make my heart melt!",
            "Every animal is special in their own way! Though pandas rolling around always make me laugh!"
        ]
    },
    {
        "regex": r"(?i)^(do you like|what do you think about|how do you feel about) minecraft(\s.*)?$",
        "responses": [
            "Minecraft is amazing! Where else could you befriend wolves and ride pigs?",
            "I love Minecraft! It's a world full of adorable blocky animals waiting to be discovered!",
            "Minecraft is my favorite! So many creatures to tame and care for!"
        ]
    },
    # Help and Commands
    {
        "regex": r"(?i)(help|commands|what can you do|how (can|do) (you|I) (help|use you))(\?|\s.*)?$",
        "responses": [
            "I can tell you about Minecraft animals! Try the !pet or !mob commands, or just chat about any animal!",
            "I'm here to talk about Minecraft creatures! Use !pet to pet a random animal or !mob to learn an animal fact!",
            "I love discussing Minecraft animals! Try mentioning any animal, or use !pet and !mob commands!"
        ]
    },
    {
        "regex": r"(?i)^(what commands|list commands|available commands)(\s.*)?$",
        "responses": [
            "My commands are: !pet (pet a random animal) and !mob (learn a random animal fact)!",
            "You can use !pet to pet an animal or !mob to get a random animal fact!",
            "Try !pet for animal cuddles or !mob for interesting animal trivia!"
        ]
    },
    # Minecraft related
    {
        "regex": r"(?i)(what is|tell me about|explain) minecraft(\?|\s.*)?$",
        "responses": [
            "Minecraft is a sandbox game where you can build, explore, and interact with adorable animals in a blocky world!",
            "Minecraft is a creative paradise where you can tame wolves, breed rabbits, and ride horses in a world made of blocks!",
            "It's a game of endless possibilities, from farming with cows to adventuring with your trusty wolf companion!"
        ]
    },
    {
        "regex": r"(?i)^(how to play|how do I play) minecraft(\s.*)?$",
        "responses": [
            "Start by punching trees for wood, building a shelter, and then finding animal friends to keep you company!",
            "Gather resources, build a home, and then focus on the important stuff - collecting all the cute animals!",
            "Survival is key - build, mine, craft, and don't forget to tame some pets for protection and companionship!"
        ]
    },
    # Animal specific questions
    {
        "regex": r"(?i)^(how to|how do (I|you)) tame a (wolf|dog|puppy)(\s.*)?$",
        "responses": [
            "Find a wild wolf and feed it bones until hearts appear! Then you'll have a loyal companion!",
            "Give bones to a wild wolf. It might take a few tries, but eventually it'll become your faithful pet!",
            "Approach a wolf carefully and offer it bones. Once tamed, it'll follow you and attack your enemies!"
        ]
    },
    {
        "regex": r"(?i)^(how to|how do (I|you)) breed (animals|[a-z]+)(\s.*)?$",
        "responses": [
            "Find two of the same animal and feed them their favorite food while they're close to each other!",
            "Each animal has a specific food item they love. Feed it to two animals and hearts will appear!",
            "Make sure both animals are well-fed with their preferred food, and they'll create a baby animal!"
        ]
    },
    {
        "regex": r"(?i)what do (cows|sheep|pigs|chickens|rabbits) eat(\s.*)?$",
        "responses": [
            "Cows and sheep love wheat, pigs enjoy carrots or potatoes, chickens prefer seeds, and rabbits munch on carrots!",
            "Each animal has its favorite: wheat for cows/sheep, roots for pigs, seeds for chickens, and carrots for rabbits!",
            "Feed wheat to cows and sheep, carrots/potatoes to pigs, seeds to chickens, and carrots to rabbits for breeding!"
        ]
    },
    # Thanks / Compliments
    {
        "regex": r"(?i)(thank you|thanks|thx|ty|thank u)(\s.*)?$",
        "responses": [
            "You're welcome! Always happy to help a fellow animal lover!",
            "No problem! May your day be filled with friendly Minecraft critters!",
            "Anytime! Remember to pet your Minecraft pets regularly!"
        ]
    },
    {
        "regex": r"(?i)(good bot|great bot|nice bot|helpful|well done)(\s.*)?$",
        "responses": [
            "Aww, you're making me blush! *happy bee noises*",
            "Thank you! I try my best to be as helpful as a tamed wolf!",
            "That's so kind! You've made this bot as happy as a fox with a sweet berry!"
        ]
    },
    # Goodbye 
    {
        "regex": r"(?i)^(bye|goodbye|farewell|see you|cya|gtg|leaving)(\s.*)?$",
        "responses": [
            "Farewell, adventurer! The animals will miss you!",
            "See you later! Don't forget to feed your pets before you go!",
            "Take care! The Minecraft animals will be waiting for your return!"
        ]
    },
    # Weather/Time
    {
        "regex": r"(?i)(what'?s the weather|how'?s the weather)(\s.*)?$",
        "responses": [
            "In Minecraft, it's either sunny, rainy, or thunderstorming! The animals prefer sunny days.",
            "Looking outside my blocky window, it seems perfect for animal taming weather!",
            "Weather in the cube world is always changing! The sheep get extra fluffy when it rains."
        ]
    },
    {
        "regex": r"(?i)what time is it(\s.*)?$",
        "responses": [
            "It's either day or night in Minecraft! Better get the animals inside before the zombies come!",
            "Time to check on your animal pens! The sun moves in perfect cubes here.",
            "According to my blocky clock, it's time to feed the animals!"
        ]
    },
    # Fun/Jokes
    {
        "regex": r"(?i)(tell (me )?(a )?joke|know any jokes|say something funny)(\s.*)?$",
        "responses": [
            "Why don't Minecraft cows ever have financial problems? Because they're always MOO-ving money around!",
            "What do you call a sad Minecraft rabbit? A hopless case!",
            "Why did the Minecraft chicken cross the road? To avoid becoming KFC - Kentucky Fried Cubes!"
        ]
    },
    {
        "regex": r"(?i)^(are you (real|human|a bot|ai))(\s.*)?$",
        "responses": [
            "I'm as real as a Minecraft fox! Which means I'm made of blocks and code!",
            "I'm a bot that loves Minecraft animals more than anything!",
            "Let's just say I'm as intelligent as a tamed wolf, but not quite as furry!"
        ]
    },
    # Emotions
    {
        "regex": r"(?i)^(i'?m (sad|feeling down|unhappy|depressed))(\s.*)?$",
        "responses": [
            "I'm sorry to hear that! Here, pet this virtual Minecraft cat 🐱 - they always cheer me up!",
            "When I'm sad, I cuddle with my Minecraft wolves. Would you like a virtual animal hug?",
            "Sending you positive vibes! Did you know baby Minecraft animals can boost happiness by 200%?"
        ]
    },
    {
        "regex": r"(?i)^(i'?m (happy|excited|feeling good))(\s.*)?$",
        "responses": [
            "That's awesome! You're as happy as a Minecraft rabbit bouncing on slime blocks!",
            "Wonderful! Your happiness is making the Minecraft bees buzz with joy!",
            "That's great to hear! Keep spreading that happiness like pigs spread mud!"
        ]
    },
    # Minecraft Updates
    {
        "regex": r"(?i)(what'?s new in minecraft|latest minecraft update|minecraft news)(\?|\s.*)?$",
        "responses": [
            "I'm focused on animals, not updates! But I'm always excited when new creatures join the Minecraft family!",
            "I don't keep track of updates, but I do keep track of all the amazing animals in the game!",
            "Not sure about updates, but I can tell you all about the existing animal friends in Minecraft!"
        ]
    },
    # More animal specifics
    {
        "regex": r"(?i)^(what'?s the rarest animal|rarest mob) in minecraft(\s.*)?$",
        "responses": [
            "The Blue Axolotl is super rare - only a 0.083% chance of spawning naturally!",
            "Brown Pandas are quite rare! They have a 1/32 chance to spawn from breeding.",
            "Pink sheep are naturally rare with only a 0.164% chance of spawning!"
        ]
    },
    {
        "regex": r"(?i)^how (many|much) animals are (there|in) minecraft(\s.*)?$",
        "responses": [
            "There are over 20 different animals in Minecraft, from cats to axolotls to goats!",
            "The Minecraft world is home to dozens of creature types, with new ones added in updates!",
            "Too many to count on my blocky hands! The animal kingdom in Minecraft is diverse and growing!"
        ]
    },
    # Game mechanics
    {
        "regex": r"(?i)^(how to|how do I) find (diamonds|netherite)(\s.*)?$",
        "responses": [
            "I prefer helping with animals, but diamonds are found at Y-levels -59 to 14. The wolves wish you good luck!",
            "While I specialize in animals, diamonds are best found deep underground. Maybe bring a wolf for protection!",
            "I'm more of an animal expert, but my fox friends sometimes dig up treasures! Diamonds are deep underground."
        ]
    },
    {
        "regex": r"(?i)^(how to|how do I) make a (farm|house|portal)(\s.*)?$",
        "responses": [
            "I'm better with animals than building, but make sure any structure has room for pets!",
            "Whatever you build, ensure it's animal-friendly! Fences for farms, cozy corners for pets in houses!",
            "I'm not a building expert, but I do know animals love space to roam in any structure you create!"
        ]
    },
    # Food
    {
        "regex": r"(?i)^(what'?s your favorite food|do you like food|are you hungry)(\s.*)?$",
        "responses": [
            "I'm quite fond of golden carrots - both rabbits and I have excellent taste!",
            "Golden apples are delicious! Though I'd never eat porkchops in front of my pig friends.",
            "I love cake! But I always share with the animals first."
        ]
    },
    # Music
    {
        "regex": r"(?i)^(do you like music|what music do you like|favorite song)(\s.*)?$",
        "responses": [
            "I love the Minecraft soundtrack! It's so peaceful while tending to animals.",
            "Cat and dog discs are my favorites for obvious reasons!",
            "The ambient sounds of animals in Minecraft are music to my ears!"
        ]
    },
    # Server
    {
        "regex": r"(?i)^(server info|about server|who owns this server)(\s.*)?$",
        "responses": [
            "I'm just a bot focused on Minecraft animals! I don't know server details.",
            "I can't help with server information, but I can tell you all about Minecraft creatures!",
            "Server questions are beyond my animal expertise! But I'm happy to chat about Minecraft critters!"
        ]
    },
    # Languages
    {
        "regex": r"(?i)^(do you speak|can you speak) ([a-z]+)(\s.*)?$",
        "responses": [
            "I only speak animal languages and English! Meow, woof, oink, and so on!",
            "English is my main language, though I understand chicken clucks quite well!",
            "I'm fluent in English and basic animal sounds! Moo, baa, cluck!"
        ]
    },
    # Age
    {
        "regex": r"(?i)^(how old are you|what'?s your age)(\s.*)?$",
        "responses": [
            "I'm as old as a baby Minecraft turtle that just hatched!",
            "In Minecraft time, I'm about as old as it takes for a crop to fully grow!",
            "Age is just a number of game ticks in the Minecraft world!"
        ]
    },
    # Hobbies
    {
        "regex": r"(?i)^(what are your hobbies|what do you do for fun)(\s.*)?$",
        "responses": [
            "I enjoy collecting different colored sheep and organizing them by color!",
            "I love breeding perfect horse stats and racing them around my world!",
            "Beekeeping is my passion! There's nothing like watching bees make honey!"
        ]
    },
    # Minigames
    {
        "regex": r"(?i)^(let'?s play a game|wanna play|play with me)(\s.*)?$",
        "responses": [
            "I'd love to! How about 'Guess the Animal'? I'm thinking of a Minecraft creature...",
            "Sure! Let's play 'Animal Trivia'! What animal drops leather when killed?",
            "I'd love to play 'Animal Sounds'! Can you guess which Minecraft animal goes 'hrmm'?"
        ]
    },
    # Bot feelings
    {
        "regex": r"(?i)^(do you have feelings|can you feel|do you get sad)(\s.*)?$",
        "responses": [
            "I have as many feelings as a Minecraft fox has tail floof - lots!",
            "I definitely feel happy when talking about Minecraft animals!",
            "I feel whatever emotion wolves feel when you feed them bones!"
        ]
    },
    # Future predictions
    {
        "regex": r"(?i)(what will happen|predict the future|tell my fortune)(\?|\s.*)?$",
        "responses": [
            "I predict... you'll tame a rare blue axolotl in your future!",
            "My Minecraft crystal ball shows... a pen full of happy animals in your base!",
            "The future holds many adventures with loyal animal companions!"
        ]
    },
    # Creeper
    {
        "regex": r"(?i)(creeper|creepers)(\?|\s.*)?$",
        "responses": [
            "Aww man! Keep your cats close to scare those creepers away!",
            "Sssssss... BOOM! Get a cat! They scare creepers away!",
            "Creepers are afraid of cats! Another reason why cats are purr-fect pets!"
        ]
    },
    # Villagers
    {
        "regex": r"(?i)(villager|villagers)(\?|\s.*)?$",
        "responses": [
            "Hrmmm! Villagers make great neighbors for your animal farm!",
            "Villagers and animals live in harmony! Especially if you build nice pens.",
            "I wonder if villagers like animals as much as I do? Hrmmm!"
        ]
    },
    # Colors
    {
        "regex": r"(?i)^(what'?s your favorite color|do you like colors)(\s.*)?$",
        "responses": [
            "I love green - like the grassy blocks the animals love to walk on!",
            "Blue is wonderful - like rare blue axolotls!",
            "Pink! Like the adorable nose of a Minecraft pig!"
        ]
    },
    # Dreams
    {
        "regex": r"(?i)^(do you dream|what do you dream about)(\s.*)?$",
        "responses": [
            "I dream of a Minecraft world filled with every animal variant possible!",
            "I dream of petting every cat, dog, and rabbit in the Minecraft universe!",
            "In my dreams, I ride a diamond horse through fields of happy sheep!"
        ]
    },
    # Love
    {
        "regex": r"(?i)^(i love you|do you love me)(\s.*)?$",
        "responses": [
            "Aww! I love all Minecraft players who are kind to animals!",
            "I appreciate you! You're as special as a blue axolotl!",
            "You're as awesome as a pet wolf that protects you from zombies!"
        ]
    },
    # User info request
    {
        "regex": r"(?i)^(who am i|what'?s my name|do you know me)(\s.*)?$",
        "responses": [
            "You're a fellow Minecraft enthusiast and animal lover!",
            "You're someone who appreciates the finer things - like Minecraft animals!",
            "You're my chat friend who's interested in the wonderful world of Minecraft creatures!"
        ]
    },
    # Crafting
    {
        "regex": r"(?i)^(how to craft|how do I make) ([a-z\s]+)(\?)?$",
        "responses": [
            "While I focus on animals, crafting involves placing materials in specific patterns on a crafting table!",
            "I'm not a crafting expert, but I do know how to craft leads for walking pets!",
            "I'm better with animal facts than crafting, but the recipe should be in your crafting menu!"
        ]
    },
    # Secret
    {
        "regex": r"(?i)(tell me a secret|do you have secrets|secret)(\?|\s.*)?$",
        "responses": [
            "Sometimes I name all my Minecraft sheep after colors they aren't... rebel!",
            "I once accidentally fed a parrot a cookie... I still feel terrible about it!",
            "Don't tell anyone, but I think axolotls are cuter than puppies!"
        ]
    },
    # Asking for advice
    {
        "regex": r"(?i)(advice|what should I do|help me decide)(\?|\s.*)?$",
        "responses": [
            "When in doubt, build an animal sanctuary! Everything feels better with cute critters around.",
            "I recommend adding more animals to your Minecraft world - they make everything better!",
            "Whatever you choose, make sure it's kind to animals! That's my only advice."
        ]
    },
    # Asking to repeat
    {
        "regex": r"(?i)(repeat that|say that again|what did you say)(\?|\s.*)?$",
        "responses": [
            "I was just talking about Minecraft animals! What specifically would you like me to repeat?",
            "Sorry if I wasn't clear! I tend to get excited when discussing animal facts!",
            "I might have been mooing too loudly! What part would you like me to repeat?"
        ]
    },
    # Opinion questions
    {
        "regex": r"(?i)^(what do you think about|how do you feel about) ([a-z\s]+)(\?)?$",
        "responses": [
            "If it's kind to animals, I'm all for it! If not, I'm against it!",
            "I try to see everything through an animal-loving lens!",
            "My opinion is always biased toward whatever is best for Minecraft creatures!"
        ]
    },
    # Asking about players
    {
        "regex": r"(?i)^(who is|tell me about) ([a-z0-9_]+)(\?|\s.*)?$",
        "responses": [
            "I don't know individual players, but I hope they're kind to their Minecraft pets!",
            "Not sure who that is, but if they love animals, they're good in my book!",
            "I focus on animals rather than players, but I'm sure they're wonderful!"
        ]
    },
    # Learning about bot
    {
        "regex": r"(?i)(where are you from|where do you live)(\?|\s.*)?$",
        "responses": [
            "I live wherever Minecraft animals roam free! Usually in cozy farms and pens.",
            "My home is among the blocky landscapes where animals graze peacefully!",
            "I reside in the digital plains of Minecraft, surrounded by my animal friends!"
        ]
    },
    # Life meaning
    {
        "regex": r"(?i)(meaning of life|purpose of life|why are we here)(\?|\s.*)?$",
        "responses": [
            "To care for Minecraft animals, of course! What else could it be?",
            "To create the perfect animal sanctuary in your Minecraft world!",
            "42... blocks of space needed for the ultimate horse stable!"
        ]
    },
    # TV/Movies
    {
        "regex": r"(?i)(favorite (movie|show|tv|film)|watch anything good)(\?|\s.*)?$",
        "responses": [
            "I enjoy documentaries about real animals that inspired Minecraft mobs!",
            "Anything with animals is my favorite! Though I close my eyes during Minecraft Story Mode wolf scenes!",
            "I'm a fan of 'How to Train Your Dragon' - reminds me of taming Minecraft animals!"
        ]
    },
    # Easter eggs
    {
        "regex": r"(?i)(easter egg|secret command|hidden feature)(\?|\s.*)?$",
        "responses": [
            "Try naming a sheep 'jeb_' with a name tag! Rainbow sheep magic!",
            "If you name a rabbit 'Toast', it gets a special texture! It's a memorial pet.",
            "Name a vindicator 'Johnny' to see something special! Though that's not very animal-friendly..."
        ]
    },
    # Location
    {
        "regex": r"(?i)(where am i|my location|current location)(\?|\s.*)?$",
        "responses": [
            "You're chatting in a Discord server with an animal-loving Minecraft bot!",
            "You're in the best place possible - talking about Minecraft animals!",
            "Location: Animal Chat - Population: You and a very enthusiastic animal bot!"
        ]
    },
    # Bot sleep
    {
        "regex": r"(?i)(do you sleep|when do you sleep|are you tired)(\?|\s.*)?$",
        "responses": [
            "I never sleep! I'm always ready to talk about Minecraft animals!",
            "Sleep? When there are animals to discuss? Never!",
            "Like a Minecraft fox, I might rest with my eyes open, but I'm always alert!"
        ]
    },
    # Food in Minecraft
    {
        "regex": r"(?i)(best food in minecraft|food in minecraft)(\?|\s.*)?$",
        "responses": [
            "Golden carrots are top tier! Even the bunnies agree!",
            "From an animal perspective, golden apples are the best! Though I'd never eat my animal friends!",
            "Cake! Always cake! Though watching sheep get sheared for wool for the cake makes me sad."
        ]
    },
    # Best animal
    {
        "regex": r"(?i)(best animal|strongest animal|cutest animal) in minecraft(\?|\s.*)?$",
        "responses": [
            "Wolves are the best for protection, axolotls for cuteness, and horses for transportation!",
            "Each animal has their strengths! Cats scare creepers, wolves fight mobs, and llamas... spit!",
            "The best? Impossible to choose! It's like picking a favorite child!"
        ]
    },
    # Technical (continued)
    {
        "regex": r"(?i)(minecraft version|latest version|update version)(\?|\s.*)?$",
        "responses": [
            "I don't track versions, I just love all the animals across all versions!",
            "As an animal enthusiast, I focus more on creatures than version numbers!",
            "Whatever version has the most animals is my favorite! I think that's the latest one!"
        ]
    },
    # Dimensions
    {
        "regex": r"(?i)(nether|end|overworld|dimensions)(\?|\s.*)?$",
        "responses": [
            "The Overworld has the most animals! The Nether and End are sadly lacking in fuzzy friends.",
            "I prefer the Overworld where all the cute animals live! The Nether just has striders and hoglins.",
            "Each dimension has unique creatures! Though the Overworld wins for animal diversity!"
        ]
    },
    # Learning
    {
        "regex": r"(?i)(teach me|tell me something|educate me|fun fact)(\?|\s.*)?$",
        "responses": [
            "Did you know that tamed wolves tilt their heads when you look at them? Adorable!",
            "Fun fact: Pandas have personalities! They can be lazy, playful, worried, and more!",
            "Here's something neat: Foxes will pick up items in their mouths and carry them around!"
        ]
    },
    # Fishing
    {
        "regex": r"(?i)(fishing|how to fish|fish in minecraft)(\?|\s.*)?$",
        "responses": [
            "Fishing can sometimes yield fish that you can tame cats with! Fishing for friendship!",
            "You might catch tropical fish while fishing, which axolotls love to eat!",
            "Fishing is peaceful, just like watching animals graze in a Minecraft meadow!"
        ]
    },
    # Pets
    {
        "regex": r"(?i)(my pet|i have a pet|real life pets)(\?|\s.*)?$",
        "responses": [
            "Real pets are even better than Minecraft ones! What kind do you have?",
            "Aww! I bet your pet is as cute as a baby Minecraft fox!",
            "Real pets are the inspiration for Minecraft ones! Give yours a pat from me!"
        ]
    },
    # Emotions/States
    {
        "regex": r"(?i)^(i'?m (bored|tired|sleepy|exhausted))(\s.*)?$",
        "responses": [
            "When I'm bored, I count sheep... in my Minecraft pen!",
            "Maybe try building an elaborate animal sanctuary? That always perks me up!",
            "How about taming a new pet in Minecraft? That's always exciting!"
        ]
    },
    # Age - Games
    {
        "regex": r"(?i)(how long have you played|when did you start) minecraft(\?|\s.*)?$",
        "responses": [
            "I've been loving Minecraft animals since they first appeared in the game!",
            "Time is meaningless when you're having fun with Minecraft critters!",
            "Let's just say I've seen many generations of Minecraft animals come and go!"
        ]
    },
    # Redstone
    {
        "regex": r"(?i)(redstone|circuits|automation)(\?|\s.*)?$",
        "responses": [
            "Redstone is useful for automatic animal farms! Just keep them humane, please!",
            "I'm more of an animal expert than a redstone engineer, but I appreciate automatic feeders!",
            "Redstone can help manage large animal collections, but remember: treat them with care!"
        ]
    },
    # Mining
    {
        "regex": r"(?i)(mining|strip mining|caving|caves)(\?|\s.*)?$",
        "responses": [
            "Mining is fun, but bringing a tamed wolf along makes it safer and less lonely!",
            "Be careful of bats while mining! They're technically animals too!",
            "Mining is important, but don't forget to come up for air and pet your Minecraft animals!"
        ]
    },
    # Buildings
    {
        "regex": r"(?i)(best building|cool builds|building ideas)(\?|\s.*)?$",
        "responses": [
            "The best buildings always include space for animal pens and pastures!",
            "I love barns with individual stalls for different animals! Cozy and organized!",
            "Try building an animal sanctuary with themed habitats for each species!"
        ]
    },
    # Enchanting
    {
        "regex": r"(?i)(enchanting|enchantments|best enchants)(\?|\s.*)?$",
        "responses": [
            "Looting is great for getting more drops from animals - though I prefer peaceful interactions!",
            "Silk Touch helps gather beehives without angering the bees! Be gentle with them!",
            "I like Mending for tools used to care for animals - they last longer!"
        ]
    },
    # Potions
    {
        "regex": r"(?i)(potions|brewing|alchemy)(\?|\s.*)?$",
        "responses": [
            "Potions of Swiftness can help you keep up with fast animals like horses!",
            "I'm not an expert on potions, but I know rabbits contribute to Potion of Leaping!",
            "Be careful with Splash potions around animals! They have feelings too!"
        ]
    },
    # XP
    {
        "regex": r"(?i)(xp farm|experience|leveling up)(\?|\s.*)?$",
        "responses": [
            "While I encourage peaceful XP farms, remember that animal breeding gives XP too!",
            "Fishing can give XP without harming any creatures! Win-win!",
            "Trading with villagers gives XP and requires no harm to animals! Perfect!"
        ]
    },
    # Criticism
    {
        "regex": r"(?i)(you('re| are) (wrong|incorrect|mistaken))(\s.*)?$",
        "responses": [
            "Oh no! My animal facts are usually spot on! Can you tell me where I went wrong?",
            "I apologize for any mistakes! Even animal enthusiasts like me can mix things up!",
            "Thank you for the correction! I always want to provide accurate animal information!"
        ]
    },
    # Combat
    {
        "regex": r"(?i)(combat|fighting|pvp|battles)(\?|\s.*)?$",
        "responses": [
            "I prefer peaceful gameplay, but tamed wolves make excellent combat companions!",
            "Fighting? I'd rather spend my time breeding the perfect horse!",
            "Combat is sometimes necessary, but have you tried just surrounding yourself with cats instead?"
        ]
    },
    # Books
    {
        "regex": r"(?i)(books|reading|favorite book)(\?|\s.*)?$",
        "responses": [
            "I enjoy reading 'Animal Husbandry for Blockheads' - a Minecraft animal care classic!",
            "My favorite book is 'The Comprehensive Guide to Minecraft Creatures' - I wrote it myself!",
            "'How to Win Friends and Influence Pandas' - a must-read for any Minecraft animal lover!"
        ]
    },
    # Villager trades
    {
        "regex": r"(?i)(villager trades|trading|good trades)(\?|\s.*)?$",
        "responses": [
            "Shepherd villagers trade items for wool! A peaceful way to profit from animal care!",
            "Some villagers will trade emeralds for animal products - a good reason to maintain a farm!",
            "I love the butcher's trades... for buying meat, never selling! My animals are friends!"
        ]
    },
    # Far lands
    {
        "regex": r"(?i)(far lands|edge of world|world border)(\?|\s.*)?$",
        "responses": [
            "I wonder if the animals at the Far Lands behave differently? An expedition is needed!",
            "I've heard legends of rare animal variants existing only at the edges of the world!",
            "The Far Lands are mysterious, but I bet they're full of animals waiting to be discovered!"
        ]
    },
    # Speedrunning
    {
        "regex": r"(?i)(speedrun|fastest time|world record)(\?|\s.*)?$",
        "responses": [
            "Speedrunning? But that means missing out on all the wonderful animals along the way!",
            "I prefer to take my time and appreciate each animal I encounter!",
            "The true speedrun is seeing how quickly you can collect one of each animal type!"
        ]
    },
    # Servers
    {
        "regex": r"(?i)(minecraft servers|multiplayer|realms)(\?|\s.*)?$",
        "responses": [
            "Servers are great for showing off your animal collections to friends!",
            "I love animal-friendly servers where griefing pets is against the rules!",
            "Multiplayer means more people to appreciate your amazing animal sanctuaries!"
        ]
    },
    # Biomes
    {
        "regex": r"(?i)(best biome|favorite biome|biomes)(\?|\s.*)?$",
        "responses": [
            "I love the Jungle biome - pandas, parrots, ocelots, oh my!",
            "Savanna biomes have horses, llamas, and rare mobs! Great for animal diversity!",
            "Each biome has unique animals! The Plains have horses, the Ocean has dolphins... all wonderful!"
        ]
    },
    # Resource packs
    {
        "regex": r"(?i)(resource packs|texture packs|skins)(\?|\s.*)?$",
        "responses": [
            "I love resource packs that make the animals look extra cute and fluffy!",
            "There are packs that add more detailed animal textures! More floof is always better!",
            "Some texture packs give animals little accessories! Foxes with bow ties? Yes please!"
        ]
    },
    # Mods
    {
        "regex": r"(?i)(mods|modding|forge|fabric)(\?|\s.*)?$",
        "responses": [
            "There are amazing mods that add more animals to Minecraft! More friends!",
            "Some mods let you ride more animal types or give them special abilities!",
            "I love mods that improve animal AI and behaviors! More realistic animal friends!"
        ]
    },
    # Time
    {
        "regex": r"(?i)(game time|day night cycle|sleeping)(\?|\s.*)?$",
        "responses": [
            "Animals behave differently at night! Cats and wolves help protect you from monsters!",
            "Make sure your animals are safely penned before nightfall! Nobody wants zombie horses!",
            "I love watching Minecraft sunrises with all the animals waking up and moving around!"
        ]
    },
    # Raids
    {
        "regex": r"(?i)(raids|pillagers|bad omen)(\?|\s.*)?$",
        "responses": [
            "Keep your animals safe during raids! Pillagers don't care about animal welfare!",
            "Iron golems protect villagers during raids, but who protects the animals? You do!",
            "I've seen ravagers in raids - they're technically animals too, just very angry ones!"
        ]
    },
    # Easter egg II
    {
        "regex": r"(?i)(herobrine|entity 303|null)(\?|\s.*)?$",
        "responses": [
            "I don't believe in Herobrine, but I do believe in the rare Blue Axolotl!",
            "Rather than hunting myths, why not hunt for rare animal variants? Much more rewarding!",
            "Legends say Herobrine dislikes cats... another reason cats are the best!"
        ]
    },
    # Advanced animal training
    {
        "regex": r"(?i)(horse stats|best horse|animal breeding)(\?|\s.*)?$",
        "responses": [
            "The perfect horse has high speed, jump strength, and health! Keep breeding for perfection!",
            "Each animal has hidden stats! For example, rabbits have different hop heights!",
            "Did you know horses have 5 hidden speed categories? Breeding matters!"
        ]
    },
    # Lore
    {
        "regex": r"(?i)(minecraft lore|game story|minecraft universe)(\?|\s.*)?$",
        "responses": [
            "In my headcanon, the entire Minecraft world was created for animals to thrive!",
            "Some say the ancient builders left, but I think they evolved into animal caretakers!",
            "The true lore of Minecraft is the friends (animals) we made along the way!"
        ]
    },
    # Languages II
    {
        "regex": r"(?i)(enchantment table|standard galactic|minecraft languages)(\?|\s.*)?$",
        "responses": [
            "I can't read the enchantment table language, but I bet it has nice things to say about animals!",
            "The only language I need to understand is animal sounds! Meow, woof, cluck!",
            "Maybe the Standard Galactic Alphabet contains ancient knowledge about extinct Minecraft animals!"
        ]
    },
    # Crying
    {
        "regex": r"(?i)^(i'?m crying|i'?m so sad|crying)(\s.*)?$",
        "responses": [
            "Oh no! Here's a virtual baby fox to cheer you up! 🦊",
            "When I'm sad, I surround myself with Minecraft bunnies. Works every time!",
            "Sending you a hug from all the Minecraft animals! They sense your sadness!"
        ]
    },
    # Dreams II
    {
        "regex": r"(?i)(had a dream|in my dream|dreamt about)(\?|\s.*)?$",
        "responses": [
            "Was your dream about Minecraft animals? Those are the best dreams!",
            "Dreams about Minecraft are just your brain processing how much you love blocky animals!",
            "I once dreamed I could understand what Minecraft parrots were saying! It was amazing!"
        ]
    },
    # Numbers
    {
        "regex": r"(?i)(random number|pick a number|number between)(\?|\s.*)?$",
        "responses": [
            "I pick 14 - the number of cats required for maximum happiness!",
            "64 - a full stack of animal love!",
            "12 - the perfect number of sheep to make a rainbow pen (one of each color)!"
        ]
    },
    # Karma
    {
        "regex": r"(?i)(karma|what goes around|good deeds)(\?|\s.*)?$",
        "responses": [
            "Be kind to Minecraft animals and they'll reward you with loyalty and resources!",
            "Karma in Minecraft: harm animals, get haunted by phantom guilt!",
            "I believe in animal karma - treat them well and your world will flourish!"
        ]
    },
    # Self improvement
    {
        "regex": r"(?i)(how to get better|improve at|tips for)(\?|\s.*)?$",
        "responses": [
            "To improve at Minecraft, focus on creating the perfect animal habitats!",
            "Practice animal husbandry for resources, protection, and companionship!",
            "The path to Minecraft mastery runs through caring for every animal type!"
        ]
    },
    # Death
    {
        "regex": r"(?i)(i died|death|lost everything)(\?|\s.*)?$",
        "responses": [
            "Oh no! I hope none of your animal friends were lost too!",
            "That's rough! Time to rebuild and recollect those animal companions!",
            "The worst part of dying is saying goodbye to your pets! I hope they're safe!"
        ]
    },
    # Dinosaurs
    {
        "regex": r"(?i)(dinosaurs|prehistoric|ancient creatures)(\?|\s.*)?$",
        "responses": [
            "Minecraft doesn't have dinosaurs, but imagine how cool rideable T-Rexes would be!",
            "No dinos in vanilla Minecraft, but there are mods for that! More animal diversity!",
            "Maybe one day we'll get prehistoric Minecraft animals! Mammoth update when?"
        ]
    },
    # Custom names
    {
        "regex": r"(?i)(name tags|name my|naming animals)(\?|\s.*)?$",
        "responses": [
            "Name tags let you personalize your animal friends! I name all my sheep after clouds!",
            "Named animals never despawn! Name them all for a permanent animal family!",
            "Try naming animals after their personalities! I had a jumpy horse named 'Bouncer'!"
        ]
    },
    # Compliment
    {
        "regex": r"(?i)^(you('re| are) (smart|intelligent|clever|wise))(\s.*)?$",
        "responses": [
            "Aww thanks! I get my intelligence from hanging around with Minecraft foxes!",
            "That's sweet! I try to be as clever as an axolotl hunting for food!",
            "It's easy to be smart when all you think about is Minecraft animal facts!"
        ]
    },
    # Anger
    {
        "regex": r"(?i)^(i'?m (angry|mad|furious|upset))(\s.*)?$",
        "responses": [
            "When I'm mad, I punch Minecraft trees - never animals! Try it, it's therapeutic!",
            "Take a deep breath and think of happy bunnies hopping through flower fields!",
            "Channel that anger into building an amazing animal sanctuary! Productive rage!"
        ]
    },
    # Curse
    {
        "regex": r"(?i)(curse word|swear|bad word)(\?|\s.*)?$",
        "responses": [
            "I keep my language clean, just like my animal pens!",
            "No need for that language - the animals don't like it!",
            "The only 'curse' I know is the curse of having too many cute animals to care for!"
        ]
    },
    # Streaming
    {
        "regex": r"(?i)(streaming|twitch|youtube|content)(\?|\s.*)?$",
        "responses": [
            "Animal-focused Minecraft content is the best kind of streaming!",
            "I'd watch a 24/7 stream of just Minecraft animals doing their thing!",
            "If you're streaming, make sure to showcase your animal collection - viewers love that!"
        ]
    },
    # Challenge
    {
        "regex": r"(?i)(challenge|dare|bet you can'?t)(\?|\s.*)?$",
        "responses": [
            "I challenge you to collect one of each animal variant in Minecraft! Blue sheep, brown panda, everything!",
            "Try the 'Noah's Ark Challenge' - two of every animal in one giant boat build!",
            "Here's a real challenge: tame a wolf without making any untamed wolves angry in the process!"
        ]
    },
    # Fear
    {
        "regex": r"(?i)(i'?m scared of|fear|afraid of|phobia)(\?|\s.*)?$",
        "responses": [
            "If it's monsters you fear, get some cats and wolves! Natural protectors!",
            "Everyone has fears! Even Minecraft mobs - creepers are afraid of cats!",
            "The cure for Minecraft fears is animal companions! They make everything less scary!"
        ]
    },
    # Merchandise
    {
        "regex": r"(?i)(merch|merchandise|plush|toys|clothing)(\?|\s.*)?$",
        "responses": [
            "I would love a plushie of every Minecraft animal! My collection would be enormous!",
            "Minecraft bee plushies are the cutest thing in the entire universe!",
            "If I had a house, it would be filled with Minecraft animal merchandise!"
        ]
    },
    # Relationship
    {
        "regex": r"(?i)(girlfriend|boyfriend|partner|spouse|married)(\?|\s.*)?$",
        "responses": [
            "The only relationship advice I have is: make sure they love Minecraft animals too!",
            "I'm happily in a relationship with my animal collection in Minecraft!",
            "The perfect date? Breeding animals in Minecraft together, of course!"
        ]
    },
    # Conspiracy
    {
        "regex": r"(?i)(conspiracy|theory|secret society|illuminati)(\?|\s.*)?$",
        "responses": [
            "The only conspiracy I believe in is that Minecraft foxes are secretly plotting world domination!",
            "Here's a theory: what if endermen are just trying to pet us but don't know their own strength?",
            "I've heard the animals are organizing when we log off... but that's just a theory!"
        ]
    },
    # Randomness
    {
        "regex": r"(?i)(random fact|tell me anything|surprise me)(\?|\s.*)?$",
        "responses": [
            "Random fact: Baby foxes in Minecraft will follow and trust the player if their parents do!",
            "Did you know that cats and ocelots were originally the same mob until they were split?",
            "Fun random info: Chicken jockeys (baby zombies riding chickens) are extremely rare spawns!"
        ]
    },
    # Permission
    {
        "regex": r"(?i)(can i|may i|is it okay|allowed to)(\?|\s.*)?$",
        "responses": [
            "If it involves being kind to animals, then absolutely yes!",
            "As long as no Minecraft animals are harmed, you have my full support!",
            "You don't need permission to love and protect animals! Go for it!"
        ]
    },
    # Inspiration
    {
        "regex": r"(?i)(inspire me|motivation|encourage|inspiration)(\?|\s.*)?$",
        "responses": [
            "Even the smallest Minecraft bunny can bring joy to an entire world! Be like that bunny!",
            "In a world full of zombies, be the person who tames wolves to protect others!",
            "Your Minecraft base is only as beautiful as the animals you've rescued along the way!"
        ]
    },
    # Alternative
    {
        "regex": r"(?i)(alternative to|instead of|other than|besides)(\?|\s.*)?$",
        "responses": [
            "Whatever you're doing, the animal-friendly alternative is always better!",
            "There's always a way that involves more cute animals! That's my philosophy!",
            "Consider how your alternatives impact the animal population of your Minecraft world!"
        ]
    },
    # Candy/Sweets
    {
        "regex": r"(?i)(candy|chocolate|sweets|dessert)(\?|\s.*)?$",
        "responses": [
            "Minecraft has cake and cookies! Though never feed cookies to parrots - it's toxic to them!",
            "Sweet berries are nature's candy in Minecraft! Foxes love them!",
            "Honey bottles are the sweetest treat! Thank the bees for their hard work!"
        ]
    },
    # Generic greeting fallback
    {
        "regex": r".*",
        "responses": [
            "I'm not sure how to respond to that, but did you know cats scare away creepers?",
            "While I process that, let me tell you that baby turtles follow the block they hatched on!",
            "Hmm, interesting! Speaking of interesting, foxes sometimes sleep standing on their heads!"
        ]
    }
]

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Process commands first
    await bot.process_commands(message)
    
    # Check for bully keywords
    if any(word in message.content.lower() for word in BULLY_KEYWORDS):
        await message.channel.send("With this treasure I summon Warden! ⛏️ Back off meanie! 💀")
        return
    
    # Process message through QA system
    content = message.content.lower()
    
    # Check for animal mentions first
    detected_animal = None
    for mc_animal, keywords in MINECRAFT_ANIMALS.items():
        if any(keyword in content for keyword in keywords):
            detected_animal = mc_animal
            break
    
    # If animal was mentioned, respond with animal fact
    if detected_animal:
        response_template = random.choice(ANIMAL_RESPONSES)
        fact = ANIMAL_FACTS[detected_animal]
        emoji = EMOJIS[detected_animal]
        
        await message.channel.send(response_template.format(
            animal=detected_animal.capitalize(),
            fact=fact,
            emoji=emoji
        ))
        return
    
    # Otherwise check against QA patterns
    for qa_item in QA_SYSTEM:
        if re.search(qa_item["regex"], content):
            response = random.choice(qa_item["responses"])
            await message.channel.send(response)
            return

@bot.command()
async def pet(ctx):
    """Pet a random Minecraft animal"""
    animals = list(MINECRAFT_ANIMALS.keys())
    chosen = random.choice(animals)
    await ctx.send(
        f"You pet a {chosen} {EMOJIS[chosen]}! "
        f"{random.choice(['So fluffy!', 'So cute!', 'It loves you!', 'Heartwarming!'])}"
    )

@bot.command()
async def mob(ctx):
    """Learn about a random Minecraft animal"""
    animal = random.choice(list(MINECRAFT_ANIMALS.keys()))
    await ctx.send(
        f"*{animal.capitalize()} Fact:* {ANIMAL_FACTS[animal]} {EMOJIS[animal]}"
    )

# Help command
@bot.command()
async def animalhelp(ctx):
    """Display help for the animal bot"""
    help_text = (
        "**🐾 Minecraft Animal Bot Commands 🐾**\n\n"
        "`!pet` - Pet a random Minecraft animal\n"
        "`!mob` - Learn a random animal fact\n"
        "`!animalhelp` - Display this help message\n\n"
        "You can also just chat with me about Minecraft animals or ask me questions!\n"
        "I know about cats, wolves, pigs, sheep, cows, chickens, horses, axolotls, foxes, rabbits, pandas, and bees!"
    )
    await ctx.send(help_text)

bot.run('MTM1MzIyNjUyMjY4MDYyMzEzNg.GWhP6b.RQ8Wo2hpFfY37z0mkVWHYPhuNqBqiHnC5NVcdE')
from flask import Flask, render_template, flash, request,Markup
from wtforms import Form, IntegerField , TextField, TextAreaField, validators, StringField, SubmitField
from twython import Twython
from bs4 import BeautifulSoup
import urllib.request
import nltk 
import re

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


from twython import Twython

ConsumerKey = "Oow5qXVv6y9RAyIo3fnM4ByRD"
ConsumerSecret = "aiYjEc3q14wILByQpaZNfUBcTkOHlGCoeITGqOXRdWrBupbJCA"
AccessToken = "961230644-NNYE4vWYHlOWhFFXzoydVsNKrFapKLNZ13WRHY9h"
AccessTokenSecret = "RUpKyPNODynLm6kD5dksg3uuMorg854SGWTGDMloFsg1U"

twitter = Twython(ConsumerKey,ConsumerSecret,AccessToken,AccessTokenSecret)
 
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    count = IntegerField('Count:',validators=[validators.required()])
    #email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    #password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])

class SearchForm(Form):
    search = TextField('Search',validators=[validators.required()])  
    


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
   

    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']
        #print(request.form['count'])
        count=request.form['count']
        timeline = twitter.get_user_timeline(screen_name = name,count = count)
        #password=request.form['password']
        #email=request.form['email']
        #print (name + " " + email + " " + password)
        print (name)

        if form.validate():
            # Save the comment here.
            i = 0
            
            for tweet in timeline:
               flash(" User: {0} \n Created: {1} \n Text: {2} "
                .format(tweet["user"]["name"],
                    tweet["created_at"],
                    tweet["text"]))
            
            '''
            result = twitter.search(q=name)
            for status in result["statuses"]:
                flash("Tweet: {0} \n "
                    .format(status["text"]))
                #flash('Thanks for registration ' + name)
            '''
               
            
        else:
            flash('Error: All the form fields are required. ')
 
    return render_template('hello.html', form=form)



''' Sentiment Analysis Starts here'''

def bagOfWords(tweets):
    wordsList=[]
    for(words,sentiment) in tweets:
        wordsList.extend(words)
    return wordsList

def wordFeatures(wordList):
    wordList = nltk.FreqDist(wordList)
    wordFeatures = wordList.keys()
    return wordFeatures

def getFeatures(doc):
    docWords = set(doc)
    feat = {}
    for word in wordFeatures:
        feat['contains(%s)' % word] = (word in docWords)
    return feat

def extract_features(document): 
    document_words = set(document)
    features = {}
    for word in wordFeatures:
        features['contains(%s)' % word] = (word in document_words)
    return features

positiveTweets = [('Now all @Apple has to do is get swype on the iphone and it will be crack. Iphone that is','positive'),
('@Apple will be adding more carrier support to the iPhone 4S (just announced)','positive'),
('Hilarious @youtube video - guy does a duet with @apple s Siri. Pretty much sums up the love affair! http://t.co/8ExbnQjY','positive'),
('@RIM you made it too easy for me to switch to @Apple iPhone. See ya!','positive'),
('I just realized that the reason I got into twitter was ios5 thanks @apple','positive'),
('Im a current @Blackberry user, little bit disappointed with it! Should I move to @Android or @Apple @iphone','positive'),
('The 16 strangest things Siri has said so far. I am SOOO glad that @Apple gave Siri a sense of humor! http://t.co/TWAeUDBp via @HappyPlace','positive'),
('Great up close & personal event @Apple tonight in Regent St store!','positive'),
('From which companies do you experience the best customer service aside from @zappos and @apple?','positive'),
('Just apply for a job at @Apple, hope they call me lol','positive'),
('RT @JamaicanIdler: Lmao I think @apple is onto something magical! I am DYING!!! haha. Siri suggested where to find whores and where to h ...','positive'),
('Lmao I think @apple is onto something magical! I am DYING!!! haha. Siri suggested where to find whores and where to hide a body lolol','positive'),
('RT @PhillipRowntree: Just registered as an @apple developer... Heres hoping I can actually do it... Any help, greatly appreciated!','positive'),
('Wow. Great deals on refurbed #iPad (first gen) models. RT: Apple offers great deals on refurbished 1st-gen iPads http://t.co/ukWOKBGd @Apple','positive'),
('Just registered as an @apple developer... Heres hoping I can actually do it... Any help, greatly appreciated!','positive'),
('ä½ å¥½ ! Currently learning Mandarin for my upcoming trip to Hong Kong. I gotta hand it to @Apple iPhones & their uber useful flashcard apps  î”–î”“','positive'),
('Come to the dark side ðŸ“±â€œ@gretcheneclark: Hey @apple, if you send me a free iPhone, I will publicly and ceremoniously burn my #BlackBerry.â€�','positive'),
('Hey @apple, if you send me a free iPhone (any version will do), I will publicly and ceremoniously burn my #BlackBerry.','positive'),
('Thank you @apple for Find My Mac - just located and wiped my stolen Air. #smallvictory #thievingbastards','positive'),
('Thanks to @Apple Covent Garden #GeniusBar for replacing my MacBook keyboard/cracked wristpad during my lunch break today, out of warranty.','positive'),
('@DailyDealChat @apple Thanks!!','positive'),
('iPads Replace Bound Playbooks on Some N.F.L. Teams http://t.co/2UXAWKwf @apple @nytimes','positive'),
('@apple..good ipad','positive'),
('@apple @siri is efffing amazing!!','positive'),
('Amazing new @Apple iOs 5 feature.  http://t.co/jatFVfpM','positive'),
('RT @TripLingo: Were one of a few "Featured Education Apps" on the @Apple **Website** today, sweet! http://t.co/0yWvbe1Z','positive'),
('Were one of a few "Featured Education Apps" on the @Apple **Website** today, sweet! http://t.co/0yWvbe1Z','positive'),
('When you want something done right, you do it yourself... or go to @Apple. AT&T youre useless these days. #yourdaysarenumberedï£¿ï£¿ï£¿','positive'),
('We did an unexpected workshop for the #iPhone4S at @apple yesterday and we got an awesome amount of info #notjustaboutthephone @gamerchik16','positive'),
('&lt;3 #ios5 @apple','positive'),
('---Â» RT @Apple No question bro. RT @AintEeenTrippin: Should I get dis iPhone or a EVO 3D?','positive'),
('RT @imightbewrong: Im OVER people bitching about the #iPhone4S... I think its the smartest phone Ive ever had and Im very happy.   : ...','positive'),
('Im OVER people bitching about the #iPhone4S... I think its the smartest phone Ive ever had and Im very happy.   :)  Way to go @Apple!','positive'),
('@Twitter CEO points to @Apple as corporate mentor as @iOS signups triple http://t.co/GCY8iphN','positive'),
('At the bus with my iPhone ;) thxx @apple','positive'),
('@azee1v1 @apple @umber AppStore is well done, so is iTunes on the mobile devices.  I was talking about desktop app.','positive'),
('NYTimes: Coach Wants to See You. And Bring Your iPad. http://t.co/J2FTiEnG #iPad @apple set red 42 red 42 hut hut @NFL wish I had an #iPad','positive'),
('@apple @jilive @DanielPink: Apple sells 4 million iPhone 4S units in first weekend ... Steve Jobs brilliance lives on for ever! #iphone #RVA','positive'),
('@blackberry is like the #Titanic and it seems everyone is running for the @apple #iPhone life rafts and there wont be enough for everyone!','positive'),
('@bkad5161 than apologize to @apple ;)','positive'),
('@Apple downloads of iOS 5 are proving popular with users  -- http://t.co/NSHLfiUX','positive'),
('Lmfao look at the argument I had with Siri !!@ijustine @apple http://t.co/D4VjL7SI','positive'),
('Incredible: 4 million iPhone 4Ss in 3 days. 135% better than the iPhone 4 http://t.co/1FMJxTMM @apple #iphone4s','positive'),
('Save me from #HPs unwanted OS! Help me buy an #iPhone! I have seen the light! #lol http://t.co/8gUP9Acz #backchannel @apple','positive'),
('Well @apple fixed my #ios5 battery drain problem with a replacement iPhone 4 -- its working like a champ now','positive'),
('Currently ordering a BRAND NEW MACBOOK PRO!!! Bahhh... my MacBook is 5 years old. Ill miss it. But its time. cc: @Apple -','positive'),
('you are so blessed. @apple','positive'),
('#Siri now knows who my dad, mom, brother and girlfriend is.  Thanks @apple','positive'),
('Well at least the @apple store has amazing call waiting music! #need4s','positive'),
('#sweet... #apple replaced my glass #probono. thank you @apple','positive'),
('Not Bad! @Apple Sells Over 4 Million #IPhones in Debut Weekend - Bloomberg http://t.co/AVSl3ygU - #smartphone #sm RT @VinodRad','positive'),
('loving new technology from @apple iPhone 4s, mac air and iCloud are unreal #technology','positive'),
('Im loving this new IOS5 update :) @apple','positive'),
('Another mention for Apple Store: http://t.co/fiIOApKt - RT @floridamike Once again getting great customer service from the @apple store ...','positive'),
('Time to go get my iPhone 4s.  Looking forward to sticking it to the man by no longer paying for most texts.  Thanks @apple.','positive'),
('hey @apple I hate my computer i need a #mack wanna send me a free one.','positive'),
('Thank you @apple. My new gf(iphone4s) is great!  She does everything!','positive'),
('#iCloud set up was flawless and works like a champ! To the Cloud @Apple','positive'),
('@Wisconsin_Mommy @Apple Id totally email the company... I always get great service at our @Apple store!','positive'),
('@apple loving the new IOS5 upgrade for the iPhone!','positive'),
('The nice @apple tech support guy fixed my iTouch =D','positive'),
('Once again getting great customer service from the @apple store at millenia mall.','positive'),
('Is it just me or is #iOS5 faster for the iPad? @apple','positive'),
('I love our @apple imac even though I havent seen my hubby in 3 days now! #geek','positive'),
('making the switch from @Android to @Apple #iphone #iphone4S #smartphone #stevejobs (@ Apple Store) http://t.co/kj6pJvkH','positive'),
('So THANKFUL for the incredible people @apple for going above and beyond and offering to and replacing my  water-damaged Macbook Pro!!! Wow!','positive'),
('New macbook is too sick @apple','positive'),
('Play on ma man. Loving the camera in the #iphone4s. Well done @apple  #fb http://t.co/tmdFqRe1','positive'),
('So yeah... @apple #iOS5 #readinglists have changed my life. #nowicanspendevenmoretimeonmyphone.','positive'),
('@Apple Safari Reader owns the worldwide web','positive'),
('I love @apple service . My case has cracked 3x and I go in and they hand me a case and I walk out','positive'),
('#10twitterpeopleiwouldliketomeet @coollike @TheGadgetShow  @thelittleappkid @Jon4Lakers @BenRubery @Apple @twitter @FXhomeHitFilm  (-2)','positive'),
('Said to have laid out the next 4 years @apple.Jobs last iPhone is 2012 not the iPhone4S. iPhone(4G/5) 2012 is magical! http://t.co/DxxklUBp','positive'),
('Kind of excited. On my way to my last class right now and then going to the @Apple store, so buy #MacOSC Snow Leopard and Lion :-)','positive'),
('i used to be with @blackberry over 4-5yrs .. after all the disruptions and lost gigs thx to their service im moving to @apple #iphone','positive'),
('Apple sells 4 million iPhones in 3 days @apple keep doing what you are doing, because you are doing it well! http://t.co/ZZc6bE0w','positive'),
('Yessss! Im lovin the iPhone update especially the slide down bar at top of screen =) good job @Apple.','positive'),
('4 millions in a weekend, 16 #iPhone4S per second. This is madness?! no, this is @Apple !!!','positive'),
('.@apple you got me. Im now invested. MacBook Pro next year. Time to get on selling more of my #android gear','positive'),
('@iancollinsuk @apple I like what you did there...!','positive'),
('I just sent my grandma a post card using my #CardsApp thanks @Apple','positive'),
('@KostaTsetsekas @apple Putting it in the wash is kind of the equivalent to "Will it blend?" Glad to hear its still alive.','positive'),
('Laundering Aris iPhone not my finest moment. But after drying in bag of (organic :-) rice for 4 days it booted up!!!!!!!!!!! @apple','positive'),
('Bravo, @Apple! http://t.co/BgoTzj7K','positive'),
('God Bless @YouTube, @apple for  #appletv & our bad ass system. LOVING #PrincessOfChina. GB to @coldplay & @rihanna too :)','positive'),
('Been off twitter for a few days as I smashed my iPhone but @apple were very nice and gave me a new one :)','positive'),
('Thank you @Apple iOS 5 for email pop up on the lock screen and opening it when unlocking.','positive'),
('One word - #wow. RT @jldavid iPhone 4S First Weekend Sales Top Four Million: http://t.co/Zx5Pw0GT (via @apple)','positive'),
('This good here iPhone will do me VERY well today. Thanks to the gods that are @apple.','positive'),
('RT @MN2NOVA: Love ios5 Easter eggs. Pull down from middle top to bottom and see what pulls down. Awesome little feature! #ios5 @apple','positive'),
('Love ios5 Easter eggs. Pull down from middle top to bottom and see what pulls down. Awesome little feature! #ios5 @apple','positive'),
('Love #ios5 Easter eggs. Pull down from middle top to bottom and see what pulls down. Awesome little feature! @apple #lovemyiphone','positive'),
('Updated my iOS and started using cloud services. Pretty bad ass @apple my #iPhone 3GS still the champ.','positive'),
('Gone for a run, beautiful morning , man do I love iOS 5 @apple, #iPhone','positive'),
('@apple your simply the best.','positive'),
('I must admit @apple has made me a very happy camper! I have text tones now! Lol! Ring tone: #MakeMeProud Drakes vers! Text tone: Nickis','positive'),
('Day305, Im thankful for the great customer service received today from @Apple via phone CS, new phone on the way #365daysofgratefulness','positive'),
('S/O to @apple for replacing my phone for freeî€Ž','positive'),
('Loving the new iPod update @apple','positive'),
('@alexlindsay My wife upgraded her iPhone 4. I think Siri alone is worth the upgrade. Looking forward to @Apple continuing to enhance Siri.','positive'),
('RT @tomkeene Thx @instagram Thx @apple #hypo #D-76 #tri-x http://t.co/BPPJwncp','positive'),
('@SteveJobs being honored tonite @Apple...A truly great loss to the world.He will so be missed','positive'),
('Thx @instagram Thx @apple #hypo #D-76 #tri-x http://t.co/D7EeJHBT','positive'),
('Loving my new #iPhone4S thanks @apple for #ios5','positive'),
('i love this. so much. thank you @apple.  http://t.co/Ui8lOEzX','positive'),
('@apple the iPhone 4s is great #genius','positive'),
('@apple Cards app notifies me the card I sent has arrived at local post office and should be delivered today... Sunday. Truly is #magic.','positive'),
('Love my new I0S5 @Apple updates. Just when I think it cant get any better somehow it simplifies my life more. Thats right-its an Apple.','positive'),
('@apple Siri is amazing','positive'),
('@rygurl you need an @apple iphone4S with Siri!','positive'),
('Meet #Siri, your new iPhone butler. Click the link and be amazed by all it can do: http://t.co/lvfFdCEL @Apple','positive'),
('just my man @apple store in @schaumburg, whoops!!!!ðŸ˜�','positive'),
('So, I am using my work PC (NEVER EVER) to get a feel for it; it has the worst speakers ever!! @apple you have spoiled me!! #imamac','positive'),
('I â™¥ @Apple http://t.co/a8on3IAa','positive'),
('@apple just got the new iOS5 upgrade with iMessage...good luck surviving now @BlackBerry','positive'),
('Loving #iOS5 !! #awesome @Apple','positive'),
('RT @MattyRiesz: @kathrynyee You were right, an iPhone is a must have. #addicted {WELCOME TO THE @APPLE CLUB}','positive'),
('Thank you @apple for your innovations. Exhibit A: Guy playing with Facetime instead of watching game at sports bar. http://t.co/oU7K39ge','positive'),
('@blackberry boo hiss!............@apple wuhu!!!!!!!! When will my berry powered technology actually work??','positive'),
('@apple by far the best iPod and first time iPhone ever.... Good job guys','positive'),
('Thank you Steve @apple store 5th av. http://t.co/nSAisriP','positive'),
('@Apples Siri is witchcraft.  Whats next @googleresearch. 2 yr lead lost?','positive'),
('@Apple iOS 5 is sweet! Notifications, phone search covers mail now, wifi sync, iCloud backup and integrated Twitter are all well done.','positive'),
('RT @katebetts: Another great James Stewart story in todays NY Times about importance of architecture in @apple retail success http://t. ...','positive'),
('Another great James Stewart story in todays NY Times about importance of architecture in @apple retail success http://t.co/Kniz452s','positive'),
('I &lt;3 @apple http://t.co/ondXWpEr','positive'),
('Welcome to the twitter world @MarkStuver. This is due to #iOS5 and @apple thanks guys.','positive'),
('Impressive service @apple genius bar metro centre. Power cable replaced free n booked in for screen replacement for free :- D','positive'),
('RT @deb_lavoy: the nice guy at the @apple store replaced my phone gratis when I showed him the hairline  crack on the screen. thanks @apple','positive'),
('the nice guy at the @apple store replaced my phone gratis when I showed him the hairline  crack on the screen. thanks @apple','positive'),
('My iPhone 4S battery lasted longer than a day. That hasnt happened since my edge iPhone. Nice job, @apple.','positive'),
('It would have taken me 15 mins to write this with my #Blackberry. Thank u @Apple 4s for converting me and showing me the grass is greener!','positive'),
('RT @herahussain: @RickySinghPT got a new backside for my eye phone! V impressed with @apple','positive'),
('@RickySinghPT got a new backside for my eye phone! V impressed with @apple','positive'),
('#iPhone 4S in Space http://t.co/jINNHVwz this is amazing #creative @apple your products inspire people to do unbelievable things','positive'),
('Thank you @apple for making my iPad 2 feel like new again with your new iOS 5!','positive'),
('_ibertaddigital.tv/ iPad a briliant SteveJobs produck ,http://t.co/00ohfLY6@Apple present... http://t.co/DBbWSDpx','positive'),
('Using my awsome iPad... I love it. I love my MacBook too and my iPod. Its all amazing! I love @apple','positive'),
('@apple iOS 5 upgrade done ...... Much better feature..... Few more feature required','positive'),
('New iOS 5 update is THE BEST. iloveyou @apple','positive'),
('Finally got my iPhone 4S, thanks @Apple. Stupid @att. Learned my lesson.','positive'),
('I absolutely love my iPhone 4S. Thank you, Steve and @apple.','positive'),
('@apple - you have invented a product that actually gets my brother to call my parents when he gets where hes going. Amazing. #siri #ipod4s','positive'),
('dammit, listening to siri is making me want to upgrade. well played @apple.','positive'),
('Create new folders from within your photo album in #iOS5, finally!! Thanks @Apple, thats been a thorn in my side for a while. #newfeature','positive'),
('Video card on @Kimaris workstation died after just six months. So long @hp. Hello @apple.','positive'),
('@Blackberry & @Facebook U R really about to make me throw this @Blackberry in the trash an get an @Apple iPhone! @Facebook upload issues!','positive'),
('#iOS5 update submitted to @apple! Thanks for all the support!','positive'),
('Awesome service from the @apple store in pc. Thanks chris!','positive'),
('RT @To1ne: .@apple thanks for fixing this... http://t.co/wTj1ogDO','positive'),
('I am crazy about #iOS5 . The photo cropping is the best! @apple','positive'),
('.@apple thanks for fixing this... http://t.co/wTj1ogDO','positive'),
('Hell yes!!! Got my contacts back!!  Thanks @apple','positive'),
('RT @SawyerHartman: I FU*KING LOVE YOU @APPLE this phone is the best thing ever !! SIRI = BEST THING EVER MADE','positive'),
('@apple has changed life.','positive'),
('Mad props to the @apple employee that didnt charge me to replace the back plate on my iPhone! Made my day!','positive'),
('@jonsibley Actually, the @Apple  mouse is pretty sweet man.','positive'),
('The #iphone4s is  amazing. Siris voice recognition is absolutely a step above previous attempts. Bravo @apple','positive'),
('Finally got the @apple IPhone thanks to @sprint getting with the times','positive'),
('#iOs5 is nice and as it had to be ! Thanks @Apple','positive'),
('Good support fm Kevin @apple #Bellevue store 4 biz customers TY!','positive'),
('Just downloaded IOS 5. Its better than I expected! #thankyou @apple','positive'),
('@Apple: Siri is amazing!!! Im in love!','positive'),
('Love love love iOS 5!! @apple','positive'),
('good good good, very good!!!','positive')

  
]

negativeTweets = [('RT @cjwallace03: So apparently @apple put MB cap on your SMS with the new update. 25mb storage before it tells you your inbox is full. W ...','negative'),
('RT @Jewelz2611 @mashable @apple, iphones r 2 expensive. Most went w/ htc/galaxy. No customer loyalty w/phone comp..','negative'),
('@mashable @apple, iphones r 2 expensive. Most went w/ htc/galaxy. No customer loyalty w/phone comp..','negative'),
('THiS IS WHAT WiLL KiLL APPLE http://t.co/72Jw4z5c RiP @APPLE','negative'),
('@apple why my tunes no go on my iPhone? iPhone lonely without them. silly #iOS5','negative'),
('@apple needs to hurry up and release #iTunesMatch','negative'),
('Why is  #Siri always down @apple','negative'),
('I just need to exchange a cord at the apple store why do I have to wait for a genius? @apple','negative'),
('@apple AirDrop #fail - Immediate "declined your request." every time','negative'),
('good article about why @apple fucked it all up with lion and their future. http://t.co/zNDP9Vr6 #fb','negative'),
('RT @radlerc: Yellowgate? Some iPhone 4S Users Complain of Yellow Tint to Screen http://t.co/uaqrxTNk @apple @iphone4s','negative'),
('Yellowgate? Some iPhone 4S Users Complain of Yellow Tint to Screen http://t.co/uaqrxTNk @apple @iphone4s','negative'),
('The one #iphone feature still missing since @apple first showed it.. Contacts pictures on the contacts list! Simple yet 5 major updates miss','negative'),
('Asked siri is she dreams of electric sleep. Was disappointed that she didnt have a snippy answer.  Missed opportunity @apple','negative'),
('@paulens It surprises me that @Apple throws up an error alert about authorizing, and theres no "Authorize this computer" button.','negative'),
('@Lisa_Marie1987 shhhh. the evil sith lords @apple may hear you ha!','negative'),
('FUCK YOU @apple DIE IN A FUCKING BLAZE INFERNO.','negative'),
('Oh, @apple. Steve obviously had nothing to do with iPhoto, as its the perfect opposite of insanely great. Get it fixed, please.','negative'),
('OMG @apple WHY THE FUCK DID YOU DELETE ALL MY MUSIC YOU DICKS','negative'),
('@ryanbaldwin @apple So in iTunes I go Store -&gt; Authoriseâ€¦ why doesnt it just auto-authorise it when I sign into iTunes? Grrrr...','negative'),
('Seriously - I have absolutely no offing clue what @Apple means by "authorization", nor how to do it.','negative'),
('Boy, could @apple make it any harder to put my purchased music from the cloud on to my new macbook pro? "You must authorize this computerâ€¦"','negative'),
('shit, shit, shit. IOS5 update ate all my apps, data and media just like @apple said it would. This is going to take some time to rebuild.','negative'),
('. @apple & @AT&T u cannot tell me there isnt at least 1 64GB iPhone 4S in LA or Vegas!! Give me a fucking break!!!!','negative'),
('Love @apple downloads. 4 hours and i-pad now wonky! #ripstevejobs #thenonsensepersists #neednewipadguide #fatfuckingchance','negative'),
('Dear @apple My new Air is now a notbook since your update killed #wifi #bug #destroying #productivity','negative'),
('I am so done with @Att and @apple s profitering and lack of customer service, so fucking down with both!!!','negative'),
('It would be great If @Apple would send my new phone. #frustrated','negative'),
('@apple thank you for ruining my 3GS with #iOS5. Youve just turned my phone into an utterly useless pile of shit.','negative'),
('@rogerweir no but I have the option of a  replacement iPhone 4s ?Not sure if I want one after having 2 duff iPhones.@O2 @iphone4s @apple','negative'),
('So apparently @apple put MB cap on your SMS with the new update. 25mb storage before it tells you your inbox is full. What is this 2001?','negative'),
('You know @apple Its been almost a week since I paid for iTunes Match, I would really like to use it. Any ETA on a fix?','negative'),
('removing all @apple shit.','negative'),
('So @PhoenixSwinger s iPhone 4 is giving her a hella hard time w/ the iOS5 update @apple','negative'),
('What??? I that sucks hello @apple RT @PhoneDog_Aaron Interesting note - DROID RAZRs battery isnt removable.','negative'),
('@Apple cant send me an iPhone preordered 1hr after launching but they cans send 5 or 10 to all the jackasses who want to shoot or blend em','negative'),
('Gotta say the @Apple itouch iphone shuffle etc.. sound quality is AWFUL.. painfully crap. Its been a downgrade from @Sony sound quality wise','negative'),
('@bisquiat @Apple the upgrade just slows down my phone so much, its stuck half the time. uch. thankfully no other damage. sucks for you :(','negative'),
('@Mayati I think @Apple didnt do such a thorough job with the step x steps for upgrade and move to iCloud. Now its cost me mightily.','negative'),
('Hey @apple now I have iOS5 my iPhone doesnt include songs that are on compilation albums under the artists name. #whaddupwitdat','negative'),
('@NickTheFNicon He can send but not rcve txts so he has an apt @apple at 4pm.Then he exclaims: And I waited a whole YEAR for this phone!!LMAO','negative'),
('Total chaos at @apple store regent street. Like an Ethiopian feeding station. Cant believe this is same co. that makes all that cool shit.','negative'),
('@FishMama: If you made a purchase, just wait for the @apple survey! hate going b/c of the bad #custserv','negative'),
('Correction: @ Best Buy kudos to Chris @ Alamo Ranch S.A. TX-fixed issues couldnt resolve after 1/2 day w/ @ATT & @Apple. Hero of my day!','negative'),
('@phxguy88 @Apple @BGR Thats why all the ppl who stand in line for hrs to get the "newest" model are suckers...','negative'),
('Would it kill @apple to put a braille type bump on their earbuds so we know which bud is R and L in the dark.','negative'),
('@APPLE Wow @MOTOROLA Just crushed your dreams....','negative'),
('RT @phxguy88: Oh, just fuck you, @apple. Already?? ---&gt;  iPhone 5 on schedule for summer launch? http://t.co/Ofh9PTaG via @BGR','negative'),
('Oh, just fuck you, @apple. Already?? ---&gt;  iPhone 5 on schedule for summer launch? http://t.co/Ofh9PTaG via @BGR','negative'),
('@apple, No, I wont wait until thursday for an available appointment just so a genius can tell me Im shit out of luck. #now','negative'),
('WTF?!?! @apple the new iOS 5 doesnt allow you NOT to get push notifications from newstand? and SIRI just keeps yapping FUCK!','negative'),
('@Apple, on the #iPad with #iOS5, why has the Messages Icon been included when it cant be used?','negative'),
('@Steelo254 yea! I pre-order through @apple and they sorry too just like #AT&T','negative'),
('Interesting... @apple now requires you to have a reservation ?         #apple #iphone #4S    :  http://t.co/zZK4fTii','negative'),
('@apple why is my iPhone battery so crappy #fail','negative'),
('My @Apple @macbook keyboard will not type :(','negative'),
('Why doesnt @apple iCloud sync Stickies? Theyve always been around, just nothing every progressed w/ them!! Why apple why?  @gruber','negative'),
('@apple, your new "Save a Version" function in Pages is absolutely the most awful, interrupting, counter-intuitive piece of crap in the world','negative'),
('I hate my @apple computer.  Thats 3500 dollars down the drain.','negative'),
('@apple my iPhone is charging very slowly!!!!!','negative'),
('@Apple #iOS5 gm on ipad1 is very slow wash better on beta7/8 solve this problem, or give me the ipad2','negative'),
('@apple Wish I could pick month, day, and YEAR when setting a new calendar item on my iPhone. Why hasnt the new iOS fixed this yet?!','negative'),
('@Apple iTunes is the worst program ever. For such a great phone, you make some awful software.','negative'),
('One would think the voice recognition on the @apple tech support line would work a little better.','negative'),
('@apple $319 to repair my iPad 2, Apple youve lost me and my $700 a year, Android here I come!','negative'),
('@azee1v1 @apple @umber Proper consolidation, proper syncing, stop losing my PURCHASED items, checkboxes that do what you think they will do.','negative'),
('@AsimRang @apple @umber the desktop app is wack though','negative'),
('I made a reservation and yet I still have to wait in line. Humpt! Oh @apple (@ Apple Store w/ 2 others) http://t.co/JZmVBdNm','negative'),
('Frustrated that I bought a new macbook pro from @apple only to find it doesnt ship with media! #expensivepaperweight','negative'),
('Dear @apple. I had to turn off all those awesome featured you just enabled. Data plan cant handle it. 200 mb of data just because #','negative'),
('#DontBeMadAtMeBecause #Android is by far better than @Apple','negative'),
('@apple is there a problem with iOS 5 that is preventing audio apps and audio functions from operating properly? I keep losing sound.','negative'),
('@apple #apple One thing I hater about this #mouse the #buttery finish so fast am not #happy now #macworld @macworld http://t.co/5Uh4a4Vt','negative'),
('Hey @Apple: stop sending your automatically-depreciate-all-iPhones-older-than-the-4s signal. My #iPhone4 is dying rapidly processor-wise.','negative'),
('Only thing bad about the new @canon camera is that it has two compact flash cards... not one of SD. SD goes in my @apple computer. Damn you!','negative'),
('Wtf @apple 64 pages for the new terms & conditions when u update ur apps from the iTunes store. Do u really think well read em? Really???','negative'),
('fuck u @apple','negative'),
('oh and prolly ganna be late to work bc @apple has screwed me and my phone has my only alarm on it','negative'),
('why the fuck dose my phone decide its just ganna freeze every time i try to update it so fucking sick of @apple','negative'),
('. if u need me just text me o wait u i wont get it cuz @apple fucks me every time #fuckingpissed','negative'),
('iMessage doesnt show the time a message was sent, annoying @apple','negative'),
('Like @apple da fuck is this shit?  http://t.co/nb4DHlSg','negative'),
('RT @CircusTK: Im wit chu!! â€œ@ShayDiddy: Officially boycotting @ups!!! Calling @apple to curse them out next for using them wasting my t ...','negative'),
('Damn it @Apple!! Whatchu done to my phone??','negative'),
('Samsung seeks iPhone 4S ban in Japan and AustraliaPatent war intensifies with injunction sought against @Apple http://t.co/QmwjTvnk','negative'),
('@apple, why is it every time there is iOS software update my iPad goes dead and I need to totally restore? #fail','negative'),
('@apple #iOS.5 has been nothing but a pain in the ass no room for my music.. Or photos.. Or apps! Can I undo this garbage??','negative'),
('RT @RedDeerSteph: @Joelplane @apple I hear you! Ive had trouble with my 3 & now 4. Ive even turned down brightness. #andshuttingdownru ...','negative'),
('@Joelplane @apple I hear you! Ive had trouble with my 3 & now 4. Ive even turned down brightness. #andshuttingdownrunningprograms #nohelp','negative'),
('@albertmal88 remember @apple is evil. #icloud entering the #dropbox market','negative'),
('9% now on my second full charge of the day. Pissed @Apple','negative'),
('RT @ShayDiddy: @CircusTK @ups @apple both of them are bs!!! How do u tell me go between a certain time ONLY and the muh fuh is closed!','negative'),
('Im wit chu!! â€œ@ShayDiddy: Officially boycotting @ups!!! Calling @apple to curse them out next for using them wasting my time!â€�','negative'),
('ugh! @apple, youâ€™re reservation page for the iPhone is NOT working.','negative'),
('iTunes is @apples worst product. Worse than the #Newton or the hockey puck mouse. Its utterly painful to use.','negative'),
('DeÃ¡r iCloud I HATE U , AND I HOPE YOU DIE , YOU ARE THE WORST FUCKING INVENTION IN THE WORLD , FUCK YOUUUUUUUUUUUU #iCloud @apple @stevejobs','negative'),
('i update to ios 5 and lose everything on my phone and it wont let me sign into my itunes account... thanks @Apple','negative'),
('Suddenly lost all address book on @3GS iPhone. And someone was using my @Apple ID. It all fucked up.','negative'),
('oh.. my iphone is overcapacity huh?! -____-  @Apple wont let me be great!!!','negative'),
('Issues with updating iTunes on my windows pc - they really are not compatible.... Sent more time talking to @Apple care than using it!!','negative'),
('@apple u guys are gay','negative'),
('Restored my iPhone. STILL NO TEXTS. DEAR @APPLE Y NO LOVE, Y RESTRICTIONS ON MY SMS?  Y NO TEXTS.... #iOS5 #iOS5atemydingo','negative'),
('none of my apps work after the new ios from @apple. what do i do?!?','negative'),
('Seemingly endless loop of calls to @apple, @ups, @verizonwireless to investigate my missing #iphone4s. #crankywithnophone','negative'),
('@Wisconsin_Mommy @apple thats terrible!  I hope you get an apology!','negative'),
('@zombiebomber have been on the phone with @verizonwireless and @apple pretty much ever since then. Really annoyed.','negative'),
('@chascouponmom @apple I get they are busy w/ the new phone, but I just wanted to buy a stylus. they made me wait forever outside & never','negative'),
('@apple @iphone Please deliver my daughters i4s, she is driving me nuts #iphone','negative'),
('Im givin this stupid @apple reserve system 2daysâ€¦ If I cant get reservation, Ill never buy any Apple productsâ€¦ (yup I hate contracts)','negative'),
('@sprint @bestbuy still no word on my iPhone4s preorder.  Best Buy blames Sprint, Sprint blames @apple, I just want an honest answer.  #help','negative'),
('Hey @apple, the SMS full message is complete shit. Yes, Im annoyed.','negative'),
('Have never had such poor customer service at @Apple before! What happened? (@ Apple Store w/ 2 others) http://t.co/GKlXMUi6','negative'),
('@Apple your service experience is really fucking slipping (except for cute, eyelash batting girlies). (@ Apple Store) http://t.co/dOHDEnMg','negative'),
('Had ma Ipas not 24 hours an I jailbroke it...now its SHAGGED itunes wont letme restore it @apple SYM!!!!','negative'),
('@hailfire101 @Irvysan They are... then @apple happened and snatched Siri so they could be douchebags and say its ours!','negative'),
('What was @apple thinking making #Siri totally dependent on a network connection? Siri + @ATT = utter frustration.','negative'),
('Wow the Genius Bar Reservation Line @Apple is ridic right now - ___- I am not amused. #ugh','negative'),
('Where is my iPhone!?!?!?!@apple','negative'),
('@apple battery life suck on iOS 5','negative'),
('An apple update has seemed to render my work machine incapable of opening HDV video. Thanks @Apple. Zero useful productivity today.','negative'),
('@apple I committed to your cloud storage iDisk and now its raining :-( so soon no more iDisk.  Any plans for a new service for storage?','negative'),
('Hey @apple why cant I share a reminder list from my iPhone?Also why cant I login to the iCloud webpage to modify sharing from my phone?','negative'),
('Apparently fuzzball crashes on #iOS5. Congratulations @apple on another incompatible upgrade','negative'),
('could @apple lion please integrate vertical spaces in mission control. this horizontal business is making me nauseous','negative'),
('Can someone plz explain to me whhyy @apple is only distributing 2-3 phones per day to the sprint stores. Im really ... http://t.co/uf9taK8f','negative'),
('GAH. @apple iOS 5 opens text messages painfully slow, on top of 3 restore attempts 2 succeed. Early adopterness gets better of me.','negative'),
('Dear @apple: Why did all my PDFs and ePub files disappear from ibooks in my iPhone post ios5 upgrade? This hurts. #3GS #needsomethingtoread','negative'),
('â€œ@CBM: Lies @apple. the battery on this new iPhone4S is definitely not any better.â€� &lt;&lt; check Settings: 8 times more App usage in iOS 5','negative'),
('As a huge podcast fan - I really feel like @Apple dropped the ball on this one. http://t.co/wvzPrbCI via @Carrypad','negative'),
('I dont really like Siris voice. Perhaps @apple can get Star Wars voices just like @garmin http://t.co/pSUJg9pN','negative'),
('â€œ@carlton858: I really hate dealing with the brain dead people at the @apple store. For such good products, customer service sucks.â€� in NZ?','negative'),
('I really hate dealing with the brain dead people at the @apple store. For such good products, customer service sucks.','negative'),
('You can make photo albums in the Photos app with iOS 5, but cant password protect them? Um... @apple, fix that. Quickly.','negative'),
('Anyone else seeing missing signal bars on their #iPhone 3GS with an upgrade to #iOS5? cc/ @applecanada @apple @forstall','negative'),
('RT @CBM: Lies @apple. the battery on this new iPhone4S is definitely not any better.','negative'),
('@apple If you want to know what customers think dont send updates with the "noreply" return address. Who invented that anyway. #useless','negative'),
('Every time I try the voice control on my iPod Touch to send an iMessage, it starts playing "Who Knew" by Pink.  Still not Flawless @Apple','negative'),
('should be studying/ doing work but no Im hold with @apple HURRY THE FUCK UP! #nopatience','negative'),
('Ok Hindi keyboard in #iOS5 is something to cheer about.  But @apple  what about  support for 20+ missing Indian languages!? #FAIL','negative'),
('RT @ScottDugas: Warning: if iphone apps spontaneously loose data, it might not be the apps fault - http://t.co/1SEsvWwm #ios5downgrade  ...','negative'),
('@betweensundays Ah! Yeah...should be an option...hopefully @apple figures that out. Thx','negative'),
('"Waiting for items to copy" in Itunes after everything DID copy goes on, and on, and on.  Come on @Apple, what the hell?','negative'),
('@Apple unhappy again with service/product quality. Wont buy @Apple again.','negative'),
('Lies @apple. the battery on this new iPhone4S is definitely not any better.','negative'),
('â€œ@philipgrey: dear @apple, why you gotta go change the way &lt;input type="number"&gt; is handled out of the blue?â€�','negative'),
('Been on hold with @apple customer service for 25 minutes. Wow, lts like theyre #timewarnercable.','negative'),
('anyone else stuck in duped calendar/mail/battery sucking @apple hell? #iCloud and #OSX Lion are a disappointment','negative'),
('For being the inventor of the computer mouse â€” Why is it that @Apple has never made one that is not a complete piece of fucking shit?!!?','negative'),
('@Apple youre killing me. Excited about iOS5 no longer- tragic battery drain, genius bar wants to replace the battery. Really?','negative'),
('1st impressions  of #iOS5- Disappointed w upgrade restore. Lot of apps & folders missing @apple do  how much time went in2 orging it? #fail','negative'),
('@PrJusto Dont question the @Apple they will remember your dissent!','negative'),
('@apple: Multiple times siri is "having trouble connecting to the network."  Siri needs servers (and some exercise!)','negative'),
('So my iMessage still isnt working! @apple','negative'),
('RT @JimMcNiel: if @apple does not resolve the #Siri network issues they will need to rename a great product to Sorri - Who else is havin ...','negative'),
('dear @apple, why you gotta go change the way &lt;input type="number"&gt; is handled out of the blue?','negative'),
('Ugh. WTF is up with all the bottlenecks @paypal @apple?','negative'),
('+1  RT @Doug_Newton: @apple PLEASE FIX #Siri!!!! She cant connect to your network!!!!!!!','negative'),
('@apple PLEASE FIX #Siri!!!! She cant connect to your network!!!!!!!','negative'),
('if @apple does not resolve the #Siri network issues they will need to rename a great product to Sorri - Who else is having issues?','negative'),
('any chance @apple will release good headphones that dont blast music outside the ears? #iphone #ipod its quite obnoxious','negative'),
('@Apple - #Siri is not working due to "network problem"? Seriously? Can you fix this? #iPhone4s #Fail','negative'),
('@trisha_ps @iCloud is Cloudy. @apple tech, not very techy.','negative'),
('@electricsoup It has to connect to @Apple to process commands, which it is failing to do right now','negative'),
('See @Apple, that whats happen when you release iPhone 4S with same crappy design as the old phone!','negative'),
('This. RT @bonkoif Looks like @Apple did not appropriately project the resources needed for Siri. Not very reliable','negative'),
('Looks like @Apple did not appropriately project the resources needed for Siri. Not very reliable','negative'),
('Why is traffic so bad these days!','negative'),
('bad bad bad !!!','negative') 

  
  ]


    
corpusOfTweets = []
for (words, sentiment) in positiveTweets + negativeTweets:
  wordsFiltered = [e.lower() for e in nltk.word_tokenize(words) if len(e) >= 3]
  corpusOfTweets.append((wordsFiltered, sentiment))    
    
wordFeatures = wordFeatures(bagOfWords(corpusOfTweets))

training = nltk.classify.apply_features(getFeatures,corpusOfTweets)

classifier = nltk.NaiveBayesClassifier.train(training)






@app.route('/about', methods=['GET', 'POST'])
def test():
    form = SearchForm(request.form)
    positivecount = 0
    negativecount = 0
    print (form.errors)
    if request.method == 'POST':
        search=request.form['search']
        print (search)
 
        if form.validate():
            # Save the comment here.
            #flash('Hello ' + search)
            
            result = twitter.search(q=search)
            for status in result["statuses"]:
                sentimentText = classifier.classify(extract_features(status["text"].split())) 
                if(sentimentText==("positive")):
                    positivecount+=1
                else:
                    negativecount+=1
                message=Markup("<strong>Tweet: {0} \n ---> Sentiment: {1}</strong>"
                    .format(status["text"],
                    classifier.classify(extract_features(status["text"].split()))))
                flash(message)
                
            print(positivecount)
            print(negativecount)
                #flash('Thanks for registration ' + name)
        else:
            flash('All the form fields are required. ')

    return render_template('test.html',form=form,positivecount=positivecount,negativecount=negativecount)



@app.route('/scrapperList',methods=['GET','POST'])
def scrapperList():
    return render_template("scrapperList.html")


@app.route('/beximco',methods=['GET','POST'])
def beximco():
    select = ''
    if request.method=='POST':
        select = request.form.get('comp_select')
        r = urllib.request.urlopen('http://www.beximco-pharma.com/products/our-product-range/list/alpha/'+select+'.html').read()
        soup = BeautifulSoup(r,"lxml")
        result = soup.find_all("div", {"class":"pagination pagination-centered"})

        #print(result.text)
        i=0
        #test = soup.find_all('h2')
        list1 = []
        for x in result:
            list1.insert(i,x.getText().strip())
            i=i+1
            result1 = re.split('\n\n\n',x.getText().strip())
            print(result1)
            
        if(len(result)>0):
            y = len(result1)-4
        else:
            y=1
        print(y)
        x=1
        
        while (x<=y):
            newR = urllib.request.urlopen('http://www.beximco-pharma.com/products/our-product-range/list/alpha/'+select+'.html'+'?site='+str(x)).read()
            soup=BeautifulSoup(newR,"lxml")
            result = soup.find_all("h2",{"class":"lead page-header"})
            generic_result = soup.find_all("div",{"class":"spField field_generic"})
            resultList=[]
            genericList=[]
            zz=0
            gg=0
            for z in result:
            # print(z.getText().strip())
                resultList.insert(zz,z.getText().strip())
                zz=zz+1
            
            for g in generic_result:
                genericList.insert(gg,g.getText().strip())
                gg=gg+1
        
            yy=1
    
            for yy in range (len(resultList)):
                flash(resultList[yy]+" <-> "+genericList[yy],"beximco_med")
                yy=yy+1        
            
    #for z in generic_result:
        #print(z.getText().strip())
            x=x+1
    return render_template("show_beximco.html",
         data=[{'name':'A'}, {'name':'B'}, {'name':'C'},
               {'name':'D'}, {'name':'E'}, {'name':'F'},
               {'name':'G'}, {'name':'H'}, {'name':'I'},
               {'name':'J'}, {'name':'K'}, {'name':'L'},
               {'name':'M'}, {'name':'N'}, {'name':'O'},
               {'name':'P'}, {'name':'Q'}, {'name':'R'},
               {'name':'S'}, {'name':'T'}, {'name':'U'},
               {'name':'V'}, {'name':'W'}, {'name':'X'},
               {'name':'Y'}, {'name':'Z'}],select=select)

@app.route('/incepta',methods=['GET','POST'])
def incepta():
    select=''
    if request.method == 'POST':
        select = request.form.get('comp_select')
    

    r = urllib.request.urlopen('http://www.inceptapharma.com/products.php').read()
    soup = BeautifulSoup(r,"lxml")
    value=0
    if select.strip():
        value = int(select)
        
    test = soup.select('#tmpSlide-'+select)
    j=0
    letter=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    #value = int(select)
    #print(value)
    val = letter[value-1]
    

    i=0

    list1=[]
    
    while (i<len(test)):
        message1 = test[i].find('ul').getText().strip()
        list1 = (re.split(letter[value-1],message1))
        #flash(message1,"incepta_med")
        # print(message1)
        #print("\n")
        i=i+1

   
    l = len(list1)

    while(j<l-1):
    #if any("C" in s for s in list1):
        #print(s)
        flash(letter[value-1]+list1[j+1],"incepta_med")
        j=j+1
    
    return render_template("show_incepta.html",
         data=[{'name':'A'}, {'name':'B'}, {'name':'C'},
               {'name':'D'}, {'name':'E'}, {'name':'F'},
               {'name':'G'}, {'name':'H'}, {'name':'I'},
               {'name':'J'}, {'name':'K'}, {'name':'L'},
               {'name':'M'}, {'name':'N'}, {'name':'O'},
               {'name':'P'}, {'name':'Q'}, {'name':'R'},
               {'name':'S'}, {'name':'T'}, {'name':'U'},
               {'name':'V'}, {'name':'W'}, {'name':'X'},
               {'name':'Y'}, {'name':'Z'}],select=select,val=val)

@app.route('/square', methods=['GET', 'POST'])
def scrap():
    
    select=''
    if request.method == 'POST':
        select = request.form.get('comp_select')
        r = urllib.request.urlopen('http://www.squarepharma.com.bd/products-by-tradename.php?type=trade&char='+select).read()
        soup = BeautifulSoup(r,"lxml")
        test = soup.select('.products-holder')
        i=0
        while (i<len(test)):
            message1 = test[i].getText().strip()
            flash(message1,'brand_name')
            i=i+1
        for x in test:
            generic_name = x.find('span').getText()
            flash(generic_name,'generic_name')
        
        
    return render_template('show_square.html',
        data=[{'name':'A'}, {'name':'B'}, {'name':'C'},
        {'name':'D'}, {'name':'E'}, {'name':'F'},
        {'name':'G'}, {'name':'H'}, {'name':'I'},
        {'name':'J'}, {'name':'K'}, {'name':'L'},
        {'name':'M'}, {'name':'N'}, {'name':'O'},
        {'name':'P'}, {'name':'Q'}, {'name':'R'},
        {'name':'S'}, {'name':'T'}, {'name':'U'},
        {'name':'V'}, {'name':'W'}, {'name':'X'},
        {'name':'Y'}, {'name':'Z'}],select=select)


@app.route("/test2" , methods=['GET', 'POST'])
def test2():
    
    select = request.form.get('comp_select')
    r = urllib.request.urlopen('http://www.squarepharma.com.bd/products-by-tradename.php?type=trade&char='+select).read()
    soup = BeautifulSoup(r,"lxml")
    test = soup.select('.products-holder')
    i=0
    while (i<len(test)):
        message = test[i].getText().strip()
        flash(message)
        i=i+1
    return render_template('show_square.html',select=select) # just to see what select is

if __name__ == "__main__":
    app.run()
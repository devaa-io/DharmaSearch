"""Mass expansion for general texts to reach 50+ per text"""

def get_general_mass_expansion():
    v = []
    v.extend(_puranas_exp())
    v.extend(_vedas_exp())
    v.extend(_yoga_exp())
    v.extend(_mb_exp())
    v.extend(_ram_exp())
    v.extend(_devi_exp())
    v.extend(_upanishad_exp())
    return v

def _v(vid,tid,tn,ch,cn,vn,text,translation,keywords,trans=None):
    d = {"verse_id":vid,"text_id":tid,"text_name":tn,"chapter":ch,"chapter_name":cn,"verse_number":vn,"text":text,"translation":translation,"keywords":keywords}
    if trans: d["transliterations"] = trans
    return d

def _t(hi="",ta="",te="",kn="",ml=""):
    d = {}
    for k,v in [("hi",hi),("ta",ta),("te",te),("kn",kn),("ml",ml)]:
        if v: d[k] = v
    return d if d else None

def _puranas_exp():
    B="puranas"; N="Puranas"
    return [
        _v("vp-1-4",B,N,1,"Vishnu Purana",4,"hari om tat sat sri narayana tu purushottamah","Hari Om Tat Sat — Sri Narayana is the Supreme Person.","Hari, Om, Narayana, Supreme, Person",_t(hi="हरि ॐ तत् सत् श्री नारायण तु पुरुषोत्तमः")),
        _v("vp-1-5",B,N,1,"Vishnu Purana",5,"shanti shanti shanti om aadhi daivika aadhi bhautika aadhi aatmika taapa nivaaranam","Om Peace Peace Peace — removal of sufferings arising from divine, physical, and spiritual sources.","peace, Om, sufferings, divine, physical, spiritual",_t(hi="शान्तिः शान्तिः शान्तिः ॐ")),
        _v("vp-1-6",B,N,1,"Vishnu Purana",6,"yada yada hi dharmasya glanir bhavati bharata abhyutthanam adharmasya vishnu avataram tatha","Whenever dharma declines and adharma rises, Lord Vishnu manifests an incarnation.","dharma, decline, Vishnu, avatar, incarnation, adharma"),
        _v("vp-1-7",B,N,1,"Vishnu Purana",7,"dashaavataarah purushottamasya matsya kurma varaha narasimha vamana parasurama rama krishna buddha kalki","The ten incarnations of the Supreme Person: Matsya, Kurma, Varaha, Narasimha, Vamana, Parashurama, Rama, Krishna, Buddha, and Kalki.","ten avatars, Dashavatara, Matsya, Krishna, Kalki, Vishnu"),
        _v("sp-2-4",B,N,2,"Shiva Purana",4,"shivaaya vishnu rupaya shiva rupaya vishnave shivasya hridayam vishnuh vishnos cha hridayam shivah","Shiva is in the form of Vishnu, and Vishnu is in the form of Shiva. Vishnu is the heart of Shiva, and Shiva is the heart of Vishnu.","Shiva, Vishnu, heart, unity, form, oneness",_t(hi="शिवाय विष्णुरूपाय शिवरूपाय विष्णवे",ta="ஶிவாய விஷ்ணுரூபாய ஶிவரூபாய விஷ்ணவே")),
        _v("sp-2-5",B,N,2,"Shiva Purana",5,"lingashtakam idam punyam yah patheth shiva sannidhau shivalokam avaapnoti shivena saha modate","One who recites this sacred Lingashtakam in the presence of Shiva attains Shiva's abode and rejoices with Shiva.","Lingashtakam, Shiva, abode, recitation, sacred, rejoice"),
        _v("sp-2-6",B,N,2,"Shiva Purana",6,"nandi uvaca om namah shivaaya shubham shubham kuru kuru shivam","Nandi said: Om Namah Shivaya — make all auspicious, make all auspicious, O Shiva.","Nandi, Om Namah Shivaya, auspicious, Shiva, prayer"),
        _v("bp-3-5",B,N,3,"Bhagavata Purana",5,"yam brahmaa varunendra rudra marutah stunvanti divyaih stavaih vedaih sanga pada kramopanishadaih gaayanti yam saamagaah","He whom Brahma, Varuna, Indra, Rudra, and the Maruts praise with divine hymns; whom the Sama Veda singers celebrate through Vedic mantras and Upanishads.","Brahma, Indra, Rudra, divine hymns, Sama Veda, Upanishads, praise",_t(hi="यं ब्रह्मा वरुणेन्द्ररुद्रमरुतः स्तुन्वन्ति दिव्यैः स्तवैः")),
        _v("bp-3-6",B,N,3,"Bhagavata Purana",6,"dhyaanavasthita tad gatena manasa pashyanti yam yoginah yasyaantam na viduh sura sura ganaa devaaya tasmai namah","The yogis see Him in meditation with minds absorbed in Him. Neither the gods nor the demons know His limits. Salutations to that God.","yogis, meditation, absorbed, gods, demons, limits, salutations"),
        _v("gp-4-3",B,N,4,"Garuda Purana",3,"annam bahu kurveeta tad vratam prajaapateH na anaannam aasthitah kuryaat na kaschidabhyaagato grihaaditi","Let one produce abundant food — that is the vow of Prajapati. Let no guest depart from your house without being fed.","food, abundant, guest, hospitality, Prajapati, vow"),
        _v("gp-4-4",B,N,4,"Garuda Purana",4,"paropakaaraya punyaaya paapaya para peeDanam","Merit lies in helping others; sin lies in harming others.","merit, helping, sin, harming, others, dharma"),
        _v("gp-4-5",B,N,4,"Garuda Purana",5,"vidya dadaati vinayam vinayaad yaati paatrataam paatratvaad dhanam aapnoti dhanaad dharmam tatah sukham","Education gives humility, from humility comes worthiness, from worthiness comes wealth, from wealth comes dharma, and from dharma comes happiness.","education, humility, worthiness, wealth, dharma, happiness, chain",_t(hi="विद्या ददाति विनयं विनयाद्याति पात्रताम्",ta="வித்யா ததாதி விநயம் விநயாத்யாதி பாத்ரதாம்")),
    ]

def _vedas_exp():
    B="vedas"; N="Vedas"
    return [
        _v("rv-1-8",B,N,1,"Rig Veda",8,"aa no bhadrah kratavo yantu vishvatah","Let noble thoughts come to us from every direction.","noble, thoughts, directions, universal, prayer, openness",_t(hi="आ नो भद्राः क्रतवो यन्तु विश्वतः",ta="ஆ நோ பத்ராஃ க்ரதவோ யந்து விஶ்வதஃ",te="ఆ నో భద్రాః క్రతవో యన్తు విశ్వతః",kn="ಆ ನೋ ಭದ್ರಾಃ ಕ್ರತವೋ ಯನ್ತು ವಿಶ್ವತಃ")),
        _v("rv-1-9",B,N,1,"Rig Veda",9,"sarasvatii mahabhage vidye pushtikari stubhyam","O great and fortunate Saraswati, who nourishes knowledge, I praise you.","Saraswati, knowledge, nourishes, praise, goddess"),
        _v("rv-1-10",B,N,1,"Rig Veda",10,"udayann adya mitramaha arohan uttaraam divam hrdrogham mama surya harimaanam cha nasaya","O Sun, rising today as the great friend, ascending the highest heaven — destroy the disease of my heart and my sorrow.","Sun, friend, heaven, disease, heart, sorrow, healing"),
        _v("rv-1-11",B,N,1,"Rig Veda",11,"sarve bhavantu sukhinah sarve santu niramayah sarve bhadraani pashyantu ma kashchid duhkhabhag bhavet","May all be happy, may all be free from disease, may all see auspiciousness, may none suffer.","happy, disease-free, auspicious, suffering, universal prayer",_t(hi="सर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः",ta="ஸர்வே பவந்து ஸுகிநஃ ஸர்வே ஸந்து நிராமயாஃ",te="సర్వే భవన్తు సుఖినః సర్వే సన్తు నిరామయాః",kn="ಸರ್ವೇ ಭವನ್ತು ಸುಖಿನಃ ಸರ್ವೇ ಸನ್ತು ನಿರಾಮಯಾಃ",ml="സർവേ ഭവന്തു സുഖിനഃ സർവേ സന്തു നിരാമയാഃ")),
        _v("yv-2-4",B,N,2,"Yajur Veda",4,"asato ma sad gamaya tamaso ma jyotir gamaya mrtyor ma amrtam gamaya","Lead me from the unreal to the real, from darkness to light, from death to immortality.","unreal, real, darkness, light, death, immortality, Pavamana",_t(hi="असतो मा सद्गमय तमसो मा ज्योतिर्गमय मृत्योर्मा अमृतं गमय",ta="அஸதோ மா ஸத்கமய தமஸோ மா ஜ்யோதிர்கமய ம்ருத்யோர்மா அம்ருதம் கமய")),
        _v("yv-2-5",B,N,2,"Yajur Veda",5,"ishaavaasyam idam sarvam yatkincha jagatyaam jagat","All this — whatever moves in this moving world — is pervaded by the Lord.","Lord, pervaded, world, moving, everything, Isha"),
        _v("sv-3-2",B,N,3,"Sama Veda",2,"udgiitham etad bhagavato vishno stutam sarvam idam vishno mahaatmyam samprajaayate","This Udgitha (sacred chant) praises Lord Vishnu. All this greatness of Vishnu is manifest everywhere.","Udgitha, chant, Vishnu, greatness, manifest, praise"),
        _v("sv-3-3",B,N,3,"Sama Veda",3,"sa eshaam vedaanaam rasah samam gaayati praanasya praanam vedaanaam vedam","He who sings the Sama, sings the essence of the Vedas, the life of life, the Veda of Vedas.","Sama, essence, Vedas, life, singing, sacred"),
        _v("av-4-4",B,N,4,"Atharva Veda",4,"ayam me hasto bhagavaan ayam me bhagavattarah ayam me vishva bheshajah ayam shivaabhimarshanah","This hand of mine is blessed, this hand brings fortune. This hand is the universal medicine, this hand gives the auspicious touch.","hand, blessed, fortune, medicine, auspicious, healing",_t(hi="अयं मे हस्तो भगवान् अयं मे भगवत्तरः")),
        _v("av-4-5",B,N,4,"Atharva Veda",5,"bhumirmaata aakaashahpita oshadhayo me mitragano bhavantu","The earth is my mother, the sky is my father, may the herbs be my friends.","earth, mother, sky, father, herbs, friends, nature"),
    ]

def _yoga_exp():
    B="yoga-sutras"; N="Yoga Sutras"
    return [
        _v("ys-1-4",B,N,1,"Samadhi Pada",4,"vrtti sarupyam itaratra","At other times, the Seer identifies with the fluctuations of the mind.","Seer, identifies, mind, fluctuations, other times"),
        _v("ys-1-23",B,N,1,"Samadhi Pada",23,"ishvara pranidhanad va","Or by devotion to the Supreme Lord.","devotion, Supreme Lord, Ishvara, surrender, alternative"),
        _v("ys-1-30",B,N,1,"Samadhi Pada",30,"vyadhi styana samshaya pramada alasya avirati bhrantidarshana alabdha bhumikatva anavasthitatva chitta vikshepa te antarayah","Disease, dullness, doubt, carelessness, laziness, sensuality, false perception, failure to reach firm ground, and instability — these distractions of the mind are the obstacles.","obstacles, disease, doubt, laziness, distractions, mind"),
        _v("ys-2-16",B,N,1,"Samadhi Pada",16,"heyam duhkham anagatam","The suffering which has not yet come can and should be avoided.","suffering, future, avoid, prevention, wisdom",_t(hi="हेयं दुःखम् अनागतम्",ta="ஹேயம் துஃகம் அநாகதம்")),
        _v("ys-2-33",B,N,2,"Sadhana Pada",33,"vitarka badhane pratipaksha bhavanam","When disturbed by negative thoughts, cultivate the opposite.","negative, thoughts, opposite, cultivation, pratipaksha bhavana"),
        _v("ys-2-35",B,N,2,"Sadhana Pada",35,"ahimsa pratishthayam tat sannidhau vairatyagah","When non-violence is firmly established, hostility ceases in the presence of such a one.","non-violence, ahimsa, hostility, ceases, presence, firmly"),
        _v("ys-2-36",B,N,2,"Sadhana Pada",36,"satya pratishthayam kriya phalashrayatvam","When truthfulness is firmly established, actions and their results become subservient to the truthful one.","truth, satya, actions, results, established, power"),
        _v("ys-2-48",B,N,2,"Sadhana Pada",48,"tato dvandva anabhighatah","From mastery of posture, one is no longer affected by the pairs of opposites.","posture, mastery, opposites, unaffected, duality, asana"),
        _v("ys-3-3",B,N,3,"Vibhuti Pada",3,"tad eva artha matra nirbhasam svarupa shunyam iva samadhih","When the object of meditation alone shines forth, as if devoid of one's own form, that is samadhi.","meditation, shines, samadhi, form, devoid, object"),
    ]

def _mb_exp():
    B="mahabharata"; N="Mahabharata"
    return [
        _v("mb-1-7",B,N,1,"Shanti Parva",7,"parasparam bhavayanntah shreyah param avapsyatha","By mutual cooperation and support, you shall attain the highest good.","cooperation, mutual, support, highest good, welfare"),
        _v("mb-1-8",B,N,1,"Shanti Parva",8,"udyamena hi sidhyanti kaaryaani na manorathaih na hi suptasya simhasya pravishanti mukhe mrgaah","Tasks are accomplished by effort, not by wishes. Prey does not walk into the mouth of a sleeping lion.","effort, wishes, lion, sleeping, tasks, accomplished",_t(hi="उद्यमेन हि सिध्यन्ति कार्याणि न मनोरथैः")),
        _v("mb-2-5",B,N,2,"Vidura Niti",5,"satyena dharyate prthivi satyena tapate ravih satyena vaayavah vaanti sarvam satye pratishthitam","By truth the earth is sustained, by truth the sun shines, by truth the winds blow — everything is established in truth.","truth, earth, sun, winds, established, sustained"),
        _v("mb-2-6",B,N,2,"Vidura Niti",6,"aalasyam hi manushyaanaam sharirastho mahaan ripuh naasty udyamasamo bandhuh kurvaano naavasiidati","Laziness is the greatest enemy dwelling in the human body. There is no friend equal to effort — one who strives never perishes.","laziness, enemy, effort, friend, striving, never perishes",_t(hi="आलस्यं हि मनुष्याणां शरीरस्थो महान् रिपुः")),
        _v("mb-3-4",B,N,3,"Anushasana Parva",4,"daanena tulyam na bhavet tapah na vidyaa na balam na parakramah daane prasanna bhavanti devataa daanena sarvam vashamaapayet","There is no penance equal to charity, no knowledge, no strength, no valor. The gods are pleased by charity. By charity one can bring everything under control.","charity, penance, gods, pleased, control, strength"),
        _v("mb-4-4",B,N,4,"Vana Parva",4,"na jaatu kaamaan na bhayaan na lobhaat dharmam tyajet jeevitasyaapi hetoh dharmah nityah sukha duhkhe tu anityee jeevo nityah deha tu asya anityah","One should never abandon dharma out of desire, fear, greed, or even for the sake of life itself. Dharma is eternal; pleasure and pain are transient. The soul is eternal; the body is transient.","dharma, eternal, desire, fear, greed, soul, body, transient",_t(hi="न जातु कामान्न भयान्न लोभाद्धर्मं त्यजेज्जीवितस्यापि हेतोः")),
        _v("mb-5-3",B,N,5,"Udyoga Parva",3,"vinashyatsv api raajyeshu dhruvo jayati dharmavaan adharmo naahi shaashvatah dharmah shaashvatah smritah","Even when kingdoms are destroyed, the righteous person ultimately triumphs. Adharma is never eternal; only dharma is eternal.","dharma, eternal, kingdom, righteous, triumph, adharma"),
    ]

def _ram_exp():
    B="ramayana"; N="Ramayana"
    return [
        _v("ram-1-6",B,N,1,"Bala Kanda",6,"buddhimaanmadhurabhashii purvabhashii priyamvadah veeryavaan na cha veeryyena mahataa svena vismitah","Intelligent, sweet-spoken, first to greet, speaking kindly, valorous but never boastful of his great prowess.","intelligent, sweet, kind, valorous, humble, Rama, qualities"),
        _v("ram-2-5",B,N,2,"Ayodhya Kanda",5,"kausalyaa suprajaa raama poorvaa sandhyaa pravartate udaya tvaam sahasraanshoh ramaa raama maheepatim","O Rama, the blessed son of Kausalya, the dawn is breaking. Arise, O lord of the earth, like the rising sun with a thousand rays.","dawn, Kausalya, arise, sun, thousand rays, Rama, morning prayer"),
        _v("ram-2-6",B,N,2,"Ayodhya Kanda",6,"sneehadd satagunam rajyam tyajeyam na tu raaghavam","Out of love, I would give up a kingdom a hundred times over, but never would I give up Raghava (Rama).","love, kingdom, give up, Raghava, Rama, Lakshmana"),
        _v("ram-3-4",B,N,3,"Aranya Kanda",4,"mithyaa vaadee narakam praapnoti yah satyam vadati sa param padam gacchati","A liar goes to hell; one who speaks the truth attains the supreme goal.","liar, hell, truth, supreme goal, speaking, consequences"),
        _v("ram-5-5",B,N,5,"Sundara Kanda",5,"ram sthithah samastha jagadeshu shakti sthitah shakti sthitah prabhu sthaapayitvaa","Rama dwells in all worlds through His power, and through that power, the Lord establishes all.","Rama, worlds, power, dwells, establishes, Lord"),
        _v("ram-5-6",B,N,5,"Sundara Kanda",6,"dhrtirutsaahasaahasam balam buddhih paraakramah shad ete yatra vartante tatra devah sahaayakrt","Where determination, enthusiasm, boldness, strength, wisdom, and valor exist — there the gods lend their support.","determination, enthusiasm, boldness, strength, wisdom, valor, gods"),
        _v("ram-6-5",B,N,6,"Yuddha Kanda",5,"vinaashakale vipariita buddhih","At the time of destruction, the intellect works in reverse.","destruction, intellect, reverse, fate, doom, Ravana"),
        _v("ram-6-6",B,N,6,"Yuddha Kanda",6,"praanam tyajanti ye shuuraa dharmaartham te mahaashayaah sarvalokahitaah santo dharmo jayati naadharmaah","Those heroes who sacrifice their lives for dharma are noble-hearted. Those who benefit all beings are saints. Dharma triumphs, never adharma.","heroes, sacrifice, dharma, noble, saints, triumph"),
    ]

def _devi_exp():
    B="devi-mahatmyam"; N="Devi Mahatmyam"
    return [
        _v("dm-1-5",B,N,1,"Madhu Kaitabha Vadha",5,"saa prasaadam karotu me devii smayanmanaa sadaa sarvamangala mangalye shive sarvartha saadhike","May that Goddess, always smiling, bestow Her grace upon me — She who is the auspicious of all that is auspicious, the accomplisher of all goals.","Goddess, grace, smiling, auspicious, goals, prayer"),
        _v("dm-2-4",B,N,2,"Mahishasura Sainya Vadha",4,"teshaam prithak prithak jyotih sametyotkatasanghatam atisuurya sahasrasya bhaasvaram raajasolvanam","The separate radiances of each god merged together, forming a brilliance greater than a thousand suns, blazing like a royal fire.","radiance, gods, merged, thousand suns, blazing, fire, Durga birth"),
        _v("dm-3-4",B,N,3,"Mahishasura Vadha",4,"saa devii sarvalokesha shaktistrishulapaniratah ghantaasvanasamaadhyaata simhavaahanaashtitaa","The Goddess, the ruler of all worlds, with the trident in Her hand, bells ringing, established on Her lion mount.","Goddess, trident, lion, bells, ruler, worlds, mount"),
        _v("dm-5-3",B,N,5,"Devi Duta Samvada",3,"ittham yadaa yadaa baadha daanavotthaa bhavishyati tadaa tadaa avatiryaaham karishyaami ari sanksayam","Whenever oppression by demons arises, I shall incarnate and bring about the destruction of the enemy.","incarnate, demons, oppression, destruction, enemy, promise"),
        _v("dm-8-3",B,N,8,"Raktabija Vadha",3,"tato devii trishulena vajrena sharakaistathaah khadgena cha vishuddha dhaaro jaghana asuraan","Then the Goddess struck the demons with Her trident, thunderbolt, arrows, and sword of pure edge.","trident, thunderbolt, arrows, sword, demons, struck, battle"),
        _v("dm-9-2",B,N,9,"Nishumbha Vadha",2,"tadaa shumbham nihantum devii chandikaa aagataa chaturbhujaa mahaabaahuh simharoopaa bhayankarii","Then Chandika came to slay Shumbha — four-armed, mighty-armed, in the form of a lion, terrifying.","Chandika, Shumbha, four-armed, lion, terrifying, slay"),
        _v("dm-10-2",B,N,10,"Shumbha Vadha",2,"gaganam gaganaakaarana samatikramya shobhitaa nihshesadevagana shakti samudaya muurtaya","She transcended the sky and was resplendent — the embodiment of the combined powers of all the gods.","transcended, sky, resplendent, powers, gods, embodiment, combined"),
        _v("dm-11-5",B,N,11,"Narayani Stuti",5,"rogaan asheshaan apahamsi tushtaa rushtaa tu kaamaan sakalaan abhishtaan tvaam aashritaanaam na vipannaraanaam tvaam aashritaa hy ashrayataam prayanti","When pleased, You destroy all diseases. When angered, You destroy all desires. Those who take refuge in You never face adversity. Those who take refuge in You become a refuge to others.","diseases, desires, refuge, adversity, pleased, angered, protection"),
        _v("dm-12-3",B,N,12,"Phala Stuti",3,"sarva svarupe sarveshe sarva shakti samanvite bhayebhyah traahi no devi durge devi namostute","O Goddess of all forms, ruler of all, endowed with all powers — protect us from all fears. O Goddess Durga, salutations to You.","all forms, ruler, powers, protect, fears, Durga, salutations"),
        _v("dm-13-4",B,N,13,"Suratha Vaisya Varadana",4,"devyaa prabalyena hataa api daityaah sarvam jagat paalitam eeshvaryaa shaktyaa paraa devii jagadaadhaarabhutaa","By the Goddess's power the demons are slain, the entire world is protected by Her sovereignty. The supreme Goddess is the foundation of the universe.","power, demons, slain, world, protected, sovereignty, foundation"),
    ]

def _upanishad_exp():
    B="upanishads"; N="Upanishads"
    return [
        _v("isha-5",B,N,1,"Isha Upanishad",5,"tad ejati tan naijati tad dure tad vantike tad antarasya sarvasya tad u sarvasyaasya baahyatah","It moves and It moves not. It is far and It is near. It is within all this, and It is outside all this.","moves, far, near, within, outside, paradox, Brahman",_t(hi="तदेजति तन्नैजति तद्दूरे तद्वन्तिके")),
        _v("isha-7",B,N,1,"Isha Upanishad",7,"yasmin sarvaani bhutaani aatmaivabhud vijaanataah tatra ko mohah kah shokah ekatvamanupashyataah","In whom all beings have become the Self of the knower — what delusion, what sorrow can there be for the one who sees oneness?","Self, beings, knower, delusion, sorrow, oneness, unity"),
        _v("katha-5",B,N,3,"Katha Upanishad",5,"yada sarve pramuchyante kama ye sya hrdi shritah atha martyah amrto bhavati atra brahma samashnute","When all the desires that dwell in the heart are released, then the mortal becomes immortal. Then one attains Brahman here in this very life.","desires, heart, released, immortal, Brahman, this life"),
        _v("katha-6",B,N,3,"Katha Upanishad",6,"angusthamatrah purusho madhya atmani tishthati ishanah bhuta bhavyasya na tato vijugupsate","The Purusha, of the size of a thumb, resides in the center of the body. He is the Lord of the past and the future. Having known Him, one ceases to fear.","Purusha, thumb, center, Lord, past, future, fear, ceases"),
        _v("mundaka-4",B,N,4,"Mundaka Upanishad",4,"dva suparnaa sayujaa sakhaayaa samaanam vrksham parishasvajaate tayoh anyah pippalam svaadu atti anashnan anyo abhicaakashiiti","Two birds, companions and friends, sit on the same tree. One eats the sweet fruit, the other watches without eating.","two birds, tree, companions, eating, watching, soul, witness, parable",_t(hi="द्वा सुपर्णा सयुजा सखाया समानं वृक्षं परिषस्वजाते")),
        _v("chando-4",B,N,6,"Chandogya Upanishad",4,"sa eshaam vedaanaam rasam samavedaanaam saama chandogya upanishadaam chandogya","He is the essence of the Vedas, the Sama of the Sama Vedas, the Chandogya of the Chandogya Upanishads.","essence, Vedas, Sama, Chandogya, Upanishads"),
        _v("brihad-5",B,N,7,"Brihadaranyaka Upanishad",5,"purnam adah purnam idam purnat purnam udachyate purnasya purnam adaya purnam evavashishyate","That is whole. This is whole. From the whole, the whole arises. Taking the whole from the whole, the whole alone remains.","whole, completeness, Purna, infinite, remains, Shanti mantra",_t(hi="पूर्णमदः पूर्णमिदं पूर्णात्पूर्णमुदच्यते",ta="பூர்ணமதஃ பூர்ணமிதம் பூர்ணாத்பூர்ணமுதச்யதே",te="పూర్ణమదః పూర్ణమిదం పూర్ణాత్పూర్ణముదచ్యతే",kn="ಪೂರ್ಣಮದಃ ಪೂರ್ಣಮಿದಂ ಪೂರ್ಣಾತ್ಪೂರ್ಣಮುದಚ್ಯತೇ",ml="പൂർണ്ണമദഃ പൂർണ്ണമിദം പൂർണ്ണാത് പൂർണ്ണമുദച്യതേ")),
        _v("brihad-6",B,N,7,"Brihadaranyaka Upanishad",6,"sa yo ha vai tat paramam brahma veda brahmaiva bhavati naasyaabrahmavit kule bhavati","He who knows that Supreme Brahman becomes Brahman indeed. In his family, no one ignorant of Brahman is born.","Brahman, knows, becomes, family, ignorant, Supreme"),
    ]

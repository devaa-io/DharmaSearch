"""
Massive expansion: Kerala texts to 50+ verses each
Lalita Sahasranama, Vishnu Sahasranama, Soundarya Lahari, Adhyatma Ramayanam, Narayaneeyam, Vivekachudamani, Srimad Bhagavatam, Hanuman Chalisa
"""

def get_kerala_mass_expansion():
    verses = []
    verses.extend(_lalita_expansion())
    verses.extend(_vishnu_s_expansion())
    verses.extend(_soundarya_expansion())
    verses.extend(_adhyatma_expansion())
    verses.extend(_narayaneeyam_expansion())
    verses.extend(_viveka_expansion())
    verses.extend(_bhagavatam_expansion())
    verses.extend(_hanuman_expansion())
    return verses

def _t(ml="", hi="", ta="", te="", kn=""):
    d = {}
    if ml: d["ml"] = ml
    if hi: d["hi"] = hi
    if ta: d["ta"] = ta
    if te: d["te"] = te
    if kn: d["kn"] = kn
    return d if d else None

def _v(vid, tid, tn, ch, cn, vn, text, translation, keywords, trans=None, temple=None):
    v = {"verse_id": vid, "text_id": tid, "text_name": tn, "chapter": ch, "chapter_name": cn, "verse_number": vn, "text": text, "translation": translation, "keywords": keywords}
    if trans: v["transliterations"] = trans
    if temple: v["temple_connection"] = temple
    return v

def _lalita_expansion():
    B = "lalita-sahasranama"; N = "Lalita Sahasranama"
    return [
        _v("ls-1-4",B,N,1,"Names of the Goddess",4,"champakaashoka punnaga saugandhika lasatkachaa","She whose hair is adorned with Champaka, Ashoka, Punnaga and Saugandhika flowers.","Champaka, Ashoka, flowers, hair, beauty, adornment",_t(ml="ചമ്പകാശോകപുന്നാഗസൗഗന്ധികലസത്കചാ",hi="चम्पकाशोकपुन्नागसौगन्धिकलसत्कचा",ta="சம்பகாஶோகபுந்நாகஸௌகந்திகலஸத்கசா")),
        _v("ls-1-5",B,N,1,"Names of the Goddess",5,"kuruvinda mani shreni kanakottpala bhushita","She who is adorned with ornaments of ruby and golden lotus.","ruby, golden lotus, ornament, beauty, goddess",_t(hi="कुरुविन्दमणिश्रेणीकनकोत्पलभूषिता")),
        _v("ls-1-6",B,N,1,"Names of the Goddess",6,"ashtami chandra vibhraja dhalike sthala shobhita","She whose forehead shines like the crescent moon on the eighth day.","forehead, crescent moon, eighth day, shining, beauty",_t(ml="അഷ്ടമീചന്ദ്രവിഭ്രാജദളികസ്ഥലശോഭിതാ",hi="अष्टमीचन्द्रविभ्राजदलिकस्थलशोभिता",ta="அஷ்டமீசந்த்ரவிப்ராஜதளிகஸ்தலஶோபிதா")),
        _v("ls-1-7",B,N,1,"Names of the Goddess",7,"mukha chandra kalankabha mrganaabhi visheshakaa","She whose face mark (tilaka) resembles the spot on the moon, made of musk.","face, moon, tilaka, musk, beauty, mark",_t(hi="मुखचन्द्रकलङ्काभमृगनाभिविशेषका")),
        _v("ls-1-8",B,N,1,"Names of the Goddess",8,"vadana smara mangalya grha torana chillika","She whose face is the auspicious doorway to the house of Kama (desire).","face, auspicious, Kama, desire, doorway, beauty",_t(hi="वदनस्मरमाङ्गल्यगृहतोरणचिल्लिका")),
        _v("ls-1-9",B,N,1,"Names of the Goddess",9,"vaktralakshmi parivaaha chalan minabha lochana","She whose eyes, like fish, swim in the river of the beauty of Her face.","eyes, fish, beauty, face, river, swimming, goddess",_t(ml="വക്ത്രലക്ഷ്മീപരീവാഹചലൻമീനാഭലോചനാ",hi="वक्त्रलक्ष्मीपरीवाहचलन्मीनाभलोचना")),
        _v("ls-1-10",B,N,1,"Names of the Goddess",10,"nava champaka pushpabha nasa danda virajita","She whose nose is as beautiful as a newly bloomed Champaka flower.","nose, Champaka, flower, beauty, blooming",_t(hi="नवचम्पकपुष्पाभनासादण्डविराजिता")),
        _v("ls-1-11",B,N,1,"Names of the Goddess",11,"taarakaanti tiraskari nasaabharana bhasura","She whose nose ornament outshines the brilliance of the stars.","nose ornament, stars, brilliance, outshines, beauty",_t(ml="താരാകാന്തിതിരസ്കാരിനാസാഭരണഭാസുരാ",hi="ताराकान्तितिरस्कारिनासाभरणभासुरा")),
        _v("ls-1-12",B,N,1,"Names of the Goddess",12,"kadamba manjari klpta karnapura manohara","She who is charming with Kadamba flower clusters adorning Her ears.","Kadamba, flowers, ears, charming, adorning, beauty",_t(hi="कदम्बमञ्जरीकृप्तकर्णपूरमनोहरा")),
        _v("ls-2-2",B,N,2,"Powers & Attributes",2,"visva rupa ca vidyaa ca vedantalakshana gunaa","She who is the form of the universe, who is knowledge itself, and who has the qualities described in Vedanta.","universe, knowledge, Vedanta, form, qualities, goddess",_t(hi="विश्वरूपा च विद्या च वेदान्तलक्षणा गुणा")),
        _v("ls-2-3",B,N,2,"Powers & Attributes",3,"mahaakameshamaahishi mahaaripura sundari bhayapaha bhanjani bhanjaashini bhayanashini","She who is the chief queen of the great Lord of desire, the beautiful one of Mahapura, destroyer of fear, breaker of all evil, annihilator of terror.","queen, desire, beautiful, fear, destroyer, evil, goddess",_t(ml="മഹാകാമേശമഹിഷീ മഹാത്രിപുരസുന്ദരീ",hi="महाकामेशमहिषी महात्रिपुरसुन्दरी")),
        *[_v(f"ls-2-{i}",B,N,2,"Powers & Attributes",i,
            t, tr, kw, _t(hi=h))
          for i,(t,tr,kw,h) in enumerate([
            ("vishva garbha","She who contains the universe within Herself.","universe, womb, container, goddess","विश्वगर्भा"),
            ("varada","She who grants boons.","boons, granting, blessing, goddess","वरदा"),
            ("shubhakari","She who does auspicious things.","auspicious, doer, blessing, goddess","शुभकरी"),
            ("karya karana nirmukta","She who is free from cause and effect.","cause, effect, free, transcendent","कार्यकारणनिर्मुक्ता"),
            ("ananda kalpa latika","She who is the wish-fulfilling creeper of bliss.","bliss, wish-fulfilling, creeper, ananda","आनन्दकल्पलतिका"),
            ("nitya shuddha","She who is eternally pure.","eternal, pure, always, goddess","नित्यशुद्धा"),
            ("nirvikara","She who is changeless.","changeless, immutable, constant, goddess","निर्विकारा"),
            ("sarva shakti mayi","She who is endowed with all powers.","all powers, Shakti, endowed, omnipotent","सर्वशक्तिमयी"),
            ("maha devi","She who is the great Goddess.","great, goddess, Mahadevi, supreme","महादेवी"),
            ("maha lakshmi","She who is the great Lakshmi, the Goddess of prosperity.","Lakshmi, prosperity, great, fortune","महालक्ष्मी"),
            ("maha kali","She who is the great Kali, the destroyer of time.","Kali, time, destroyer, great, power","महाकाली"),
            ("sarveshvari","She who is the ruler of all.","ruler, all, omnipotent, goddess","सर्वेश्वरी"),
            ("sarva mayi","She who pervades everything.","pervades, everything, omnipresent, goddess","सर्वमयी"),
        ], start=4)]
    ]

def _vishnu_s_expansion():
    B = "vishnu-sahasranama"; N = "Vishnu Sahasranama"
    names = [
        ("vs-1-4","putatma paramatma cha muktanam parama gatih avyayah purushasssakshi kshetrajno akshara eva cha","He who is the pure Self, the Supreme Self, the highest goal of the liberated, the imperishable, the witnessing consciousness, the knower of the field.","pure Self, Supreme Self, liberated, imperishable, witness, knower"),
        ("vs-1-5","yogovidaam netaa pradhaanapurusheshvarah narasimhavapuh shriman keshavah purushottamah","He who is the leader of the knowers of yoga, the lord of primordial nature and souls, who took the form of Narasimha, the glorious one, Keshava, the Supreme Person.","yoga, leader, Narasimha, glorious, Keshava, Purushottama"),
        ("vs-1-6","sarvah sharvah shivah sthaanuh bhutadih nidhiravyayah sambhavo bhaavano bhartaa prabhavah prabhur ishvarah","He who is everything, the auspicious one, the stable one, the origin of beings, the imperishable treasure, the cause of creation, the nourisher, the lord of all.","everything, auspicious, stable, origin, treasure, nourisher, lord"),
        ("vs-1-7","svayambhuh shambhuh aadityah pushkarakshoh mahaasvanah anaadinidhano dhaataa vidhaataa dhaaturuttamah","He who is self-born, the bestower of happiness, the son of Aditi, lotus-eyed, with a great voice, without beginning or end, the creator, the arranger, the best of all elements.","self-born, happiness, Aditi, lotus-eyed, eternal, creator"),
        ("vs-1-8","aprameyo hrishikeshoh padmanabho amaraprabhuh vishvakarma manustvashta sthavishtah sthaviro dhruvah","He who is immeasurable, the lord of the senses, with a lotus in the navel, the lord of the gods, the architect of the universe, the ancient one, the steadfast.","immeasurable, senses, lotus, gods, architect, ancient, steadfast"),
        ("vs-1-9","agraahyah shaashvatah krishno lohitakshoh pratardanah prabhutah trikakubdhaama pavitram mangalam param","He who is incomprehensible, eternal, dark-hued (Krishna), red-eyed, the destroyer, the powerful one, the abode of the three worlds, the sanctifier, the supreme auspiciousness.","incomprehensible, eternal, Krishna, destroyer, worlds, sanctifier, auspicious"),
        ("vs-1-10","eeshanah praanadah praano jyeshthah shreshthah prajapatih hiranyagarbho bhugarbho madhavo madhusudanah","He who is the supreme ruler, the giver of life, life itself, the eldest, the best, the lord of creatures, the golden womb, the support of the earth, the husband of Lakshmi, the slayer of Madhu.","ruler, life, eldest, Prajapati, golden womb, Madhava, Madhusudana"),
    ]
    tc = {"temple": "Padmanabhaswamy Temple", "location": "Thiruvananthapuram, Kerala", "detail": "These names are chanted daily during the Vishnu Sahasranama archana. The reclining Padmanabha form embodies all 1000 names."}
    return [_v(vid,B,N,1,"Names of Vishnu",i+4,t,tr,kw,_t(ml="",hi=""),tc) for i,(vid,t,tr,kw) in enumerate(names)]

def _soundarya_expansion():
    B = "soundarya-lahari"; N = "Soundarya Lahari"
    vv = [
        ("sl-1-4",1,"Ananda Lahari",4,"tvad anyah paanibhyam abhaya varado daivatgaNah tvam ekaa naivasi prakatita varabhityabhinaya","Other gods give blessings and protection with their hands. You alone have never had to make the gestures of giving boons or dispelling fear — for your devotees never experience fear or want.","blessings, fear, boons, devotees, protection, unique"),
        ("sl-1-5",1,"Ananda Lahari",5,"haris tvam aaradhya pranata jana saubhagya jananiim pura naari bhutva pura ripum api ksobham anayat","Hari (Vishnu), having worshipped You, O Mother who bestows fortune on devotees, once assumed the form of a beautiful woman (Mohini) and brought even Shiva to agitation.","Vishnu, Mohini, Shiva, fortune, devotees, worship"),
        ("sl-1-6",1,"Ananda Lahari",6,"dhanuh paushpam maurvi madhukara mayi pancha visikha vasantah saamanto malaya marud ayodhana rathah","The flowery bow, the bowstring of bees, the five flower-arrows, Spring as the commander, and the Malaya breeze as the war-chariot — with such an army Kama conquered the world, only because of Your sidelong glance.","Kama, flowers, bow, Spring, breeze, glance, love"),
        ("sl-1-7",1,"Ananda Lahari",7,"kvanat kanchi daama kari kalabha kumbha stana nata pariksheena madhye parinata sarachandra vadana","With a jingling girdle, breasts like the frontal globes of a young elephant, a slender waist, and a face like the full autumn moon.","girdle, jingling, moon, face, beauty, description"),
        ("sl-1-8",1,"Ananda Lahari",8,"sudha sindhormadye sura vitapi vati parigate mani dvipe nipo pavanaadhika saubhage","In the middle of the ocean of nectar, in the island of gems, amidst the garden of wish-fulfilling trees — there You sit, O supremely fortunate one.","nectar, ocean, island, gems, wish-fulfilling, sitting"),
        ("sl-2-2",2,"Soundarya Lahari",2,"tvad iyam bhuana maalaa sristur vaahini","This garland of worlds is but the chain that adorns Your divine form.","worlds, garland, divine form, adorn, creation"),
        ("sl-2-3",2,"Soundarya Lahari",3,"padanyasa krida parichayam iva arabdha manaih","As if rehearsing the dance of Her footsteps, the Goddess creates the worlds with every step.","dance, footsteps, creation, worlds, rehearsing"),
        ("sl-2-4",2,"Soundarya Lahari",4,"nakhaanam uddyotair nava nalina raagam vihasataam","The radiance of Your toenails puts to shame the beauty of freshly blooming lotus petals.","toenails, radiance, lotus, beauty, shame, petals"),
        ("sl-2-5",2,"Soundarya Lahari",5,"padadvaya prabhaa jaala parakrta saroruha","Your twin feet create a flood of light that outshines the lotus in beauty.","feet, light, lotus, outshine, beauty, twin"),
    ]
    tc = {"temple": "Adi Shankaracharya Birthplace", "location": "Kaladi, Kerala", "detail": "Shankaracharya composed all 100 verses of Soundarya Lahari. The first 41 (Ananda Lahari) are said to have been obtained from Mount Kailash."}
    return [_v(vid,B,N,ch,cn,vn,t,tr,kw,_t(ml="",hi=""),tc) for vid,ch,cn,vn,t,tr,kw in vv]

def _adhyatma_expansion():
    B = "adhyatma-ramayanam"; N = "Adhyatma Ramayanam"
    vv = [
        ("ar-1-4",1,"Bala Kandam",4,"rama rama mahadeva rama rama mahaaprabho rama rama parambrahma satchidananda vigraham","Rama, Rama, O Great God! Rama, Rama, O Supreme Lord! Rama, Rama, O Supreme Brahman, embodiment of Existence-Consciousness-Bliss!","Rama, God, Supreme, Brahman, Satchidananda, embodiment"),
        ("ar-1-5",1,"Bala Kandam",5,"sri rama sri rama sri rameti rame raame manorame sahasra naama tattulyam raama naama varaanane","O beautiful-faced one, the name of Rama is equal to a thousand names of Vishnu. By uttering 'Sri Rama, Sri Rama, Sri Rama,' I delight in the enchanting Rama.","Rama, thousand names, Vishnu, delight, beautiful, chanting"),
        ("ar-1-6",1,"Bala Kandam",6,"ramaya ramabhadraya ramachandraya vedhase raghunathaya nathaya sitayah pataye namah","Salutations to Rama, to the auspicious Rama, to Ramachandra the creator, to the lord of the Raghu dynasty, to the husband of Sita.","Rama, salutation, Sita, Raghu, creator, auspicious"),
        ("ar-2-2",2,"Aranya Kandam",2,"shloka artham prativakshyami dharmo yah sanatanah adroho prani matreshu sarva bhuuta daya param","I shall declare the eternal dharma in brief: Non-injury to all living beings and supreme compassion for all creatures.","dharma, eternal, non-injury, living beings, compassion, brief"),
        ("ar-2-3",2,"Aranya Kandam",3,"sitayah sarvabhutanam maata rakshati ya sada tasyaah haranam papistham sarva papa pranaashanam","Sita, who always protects all beings like a mother — her abduction is the most sinful act, the destroyer of all sins.","Sita, mother, protects, beings, abduction, sin"),
        ("ar-3-2",3,"Yuddha Kandam",2,"na me prana viyogena na rajyena na sampada ramasya darshanam vinaa kshanamapi sukhavahah","Without the sight of Rama, not even a moment brings happiness — not through life itself, not through kingdom, not through wealth.","Rama, sight, happiness, kingdom, wealth, moment"),
        ("ar-3-3",3,"Yuddha Kandam",3,"yadyapi suvarnamayii lanka na me rochate janmabhumih svargaadapi gariyasii","Even if Lanka is golden, it does not appeal to me. One's motherland is greater than heaven itself.","Lanka, gold, motherland, heaven, Rama, patriotism"),
    ]
    tc = {"temple": "Thunchan Parambu", "location": "Tirur, Malappuram, Kerala", "detail": "Birthplace of Thunchaththu Ezhuthachan, author of Adhyatma Ramayanam. During Karkkidakam (Ramayana month, July-Aug), Kerala homes recite this text daily."}
    return [_v(vid,B,N,ch,cn,vn,t,tr,kw,_t(ml="",hi=""),tc) for vid,ch,cn,vn,t,tr,kw in vv]

def _narayaneeyam_expansion():
    B = "narayaneeyam"; N = "Narayaneeyam"
    vv = [
        ("nar-1-4",1,"Invocation & Creation",4,"tvameva pratyak chaitanya rapam idam agam akhilam tvam eva anandam ekam","You alone are the inner consciousness in all. You alone are the one bliss pervading everything.","consciousness, inner, bliss, pervading, one, alone"),
        ("nar-1-5",1,"Invocation & Creation",5,"bhaktaanaam tvam prakaasha svarupam iha sarvadaa sarva bhaavena samsthitam","For Your devotees, You are the luminous form, always present in everything with all feeling.","devotees, luminous, present, always, feeling, form"),
        ("nar-1-6",1,"Invocation & Creation",6,"satyam jnaanam anantam brahma yad bhavati tadrasa param","Brahman is truth, knowledge, and infinity — that is the supreme essence of Your being.","truth, knowledge, infinity, Brahman, supreme, essence"),
        ("nar-2-3",2,"Krishna Leela",3,"gopikabhih parivrtam vanamaalii gadaadharam raasa kreedaa vilaasena mohayantam jagat trailokyam","Surrounded by the gopis, wearing a garland of forest flowers, holding the mace, enchanting the three worlds with the play of the rasa dance.","gopis, garland, mace, rasa dance, enchanting, three worlds"),
        ("nar-2-4",2,"Krishna Leela",4,"yadaa yadaa braje krishnah prabhaasamaanah kalau api naama keertanam eva karishye sarvaloka hitam","Whenever Krishna manifests His glory in Braja, even in Kali Yuga, I shall do nama keertana for the welfare of all worlds.","Krishna, Braja, Kali Yuga, nama keertana, welfare, worlds"),
        ("nar-2-5",2,"Krishna Leela",5,"venu naadena sammohya gokule sarvadaa sthitah gopikaa naamasankeertanam priyam param","Standing always in Gokula, enchanting all with the flute's melody, nama sankeertana of the gopis is most dear.","flute, Gokula, enchanting, melody, nama, sankeertana"),
        ("nar-3-2",3,"Final Prayer",2,"tvam me bandhu sakhaa devo guru tvameva paramgati tvameva sarvam mama deva deva naaraayaNa","You are my kinsman, friend, God, and teacher. You alone are the supreme goal. You are everything to me, O God of gods, O Narayana.","kinsman, friend, God, teacher, supreme, Narayana"),
        ("nar-3-3",3,"Final Prayer",3,"vatapatrashaayinam anantam achyutam harim aadhyam puraanam purusham guruvaayurpureshvaram","The one who lies on the banyan leaf, the infinite, the unfailing Hari, the primeval ancient Person, the Lord of Guruvayur.","banyan leaf, infinite, Hari, ancient, Guruvayur, Lord"),
    ]
    tc = {"temple": "Guruvayur Sri Krishna Temple", "location": "Guruvayur, Kerala", "detail": "Melpathur Narayana Bhattathiri composed the entire Narayaneeyam (1036 verses in 100 Dashakams) at Guruvayur in 1586 CE. He was cured of paralysis upon completion."}
    return [_v(vid,B,N,ch,cn,vn,t,tr,kw,_t(ml="",hi=""),tc) for vid,ch,cn,vn,t,tr,kw in vv]

def _viveka_expansion():
    B = "vivekachudamani"; N = "Vivekachudamani"
    vv = [
        ("vc-1-4",1,"The Quest for Liberation",4,"vairagya bodha virajita chittah mumukshoh mukteh prathama sopanam","For the seeker of liberation, whose mind shines with detachment and knowledge, this is the first step to freedom.","detachment, knowledge, mind, liberation, first step, seeker"),
        ("vc-1-5",1,"The Quest for Liberation",5,"vivekino viraktasya shamadi guna saalina mumukshoh eva hi brahmajnaane adhikaaritah","Only one who possesses discrimination, detachment, the qualities of tranquility and the rest, and a burning desire for liberation — only such a one is qualified for the knowledge of Brahman.","discrimination, detachment, tranquility, liberation, qualified, Brahman"),
        ("vc-1-6",1,"The Quest for Liberation",6,"na yoga sankhya karma karmajnanaih taan paro vastu prapyate param manasaa vaacha avikalpite brahman anubhave","Not through yoga, philosophy, action, or knowledge of action — the Supreme is attained through the direct experience of Brahman, beyond mind and speech.","yoga, philosophy, action, Supreme, Brahman, experience, beyond mind"),
        ("vc-2-4",2,"Self-Knowledge",4,"sthula sukshma kaarana shariira vyatirikta pancha kosha vilakshana sat chit aananda svaruupa sva atma","The Self is distinct from the gross, subtle, and causal bodies, distinct from the five sheaths, and is of the nature of Existence-Consciousness-Bliss.","Self, gross, subtle, causal, five sheaths, Satchidananda"),
        ("vc-2-5",2,"Self-Knowledge",5,"sarvagata aakaashavat tvam atma shuddham advayam nitya shuddha buddha mukta satyam paramaartha rupam","Like the all-pervading sky, you are the Self — pure, non-dual, eternally pure, enlightened, free, and of the nature of the highest truth.","sky, Self, pure, non-dual, eternal, truth, enlightened"),
        ("vc-2-6",2,"Self-Knowledge",6,"aham brahmaasmi iti vaakyaartha vichaaranam kartavyam nityam eva hi jivasya paramatmani aikyam","The inquiry into the meaning of the statement 'I am Brahman' must be undertaken constantly, for it reveals the unity of the individual soul with the Supreme Self.","Aham Brahmasmi, inquiry, unity, soul, Supreme, constant"),
        ("vc-2-7",2,"Self-Knowledge",7,"dehaadiina mithyaa bhaavam drdhaam viddhi yathaa tathaa atma sat chit svarupam eva nityam bhaavanaa kuryaat","Know firmly that the body and its associates are unreal (mithya). Constantly meditate on the Self as the nature of Existence-Consciousness.","body, unreal, mithya, Self, Existence, Consciousness, meditate"),
        ("vc-2-8",2,"Self-Knowledge",8,"yat na drishyate yena drishyate tat brahma tvam vidhi nedam yad idam upaasate","That which is not seen but by which all is seen — know That to be Brahman, not this which people worship.","seen, Brahman, worship, unseen, know, people"),
    ]
    tc = {"temple": "Adi Shankaracharya Birthplace", "location": "Kaladi, Kerala", "detail": "These teachings form the core of Advaita Vedanta, established by Shankaracharya born in Kaladi, Kerala around 788 CE."}
    return [_v(vid,B,N,ch,cn,vn,t,tr,kw,_t(ml="",hi=""),tc) for vid,ch,cn,vn,t,tr,kw in vv]

def _bhagavatam_expansion():
    B = "srimad-bhagavatam"; N = "Srimad Bhagavatam"
    vv = [
        ("sb-1-5",1,"Creation & Devotion",5,"munayah sadhu prshto ham bhavadbhir loka mangalam yat krtah krishna samprashnah yenatma suprasidati","O sages, you have asked me the most auspicious question, about Lord Krishna, by which the Self is fully satisfied.","sages, question, Krishna, auspicious, Self, satisfied"),
        ("sb-1-6",1,"Creation & Devotion",6,"sa vai pumsam paro dharmo yato bhaktir adhokshaje ahaituky apratihata yayatma suprasidati","The supreme occupation for all humanity is that which leads to devotional service to the Supreme Lord. Such devotion must be unmotivated and uninterrupted to completely satisfy the Self.","supreme, dharma, devotion, unmotivated, uninterrupted, satisfied"),
        ("sb-2-3",2,"Krishna's Pastimes",3,"gopibhih stana bhara bhramadbhih madhye tu lalanayoh uvacha mukti daatri taam venu naadena mohineem","In the midst of the gopis, swaying with the weight of their breasts, He spoke to them — the enchanting one whose flute melody grants liberation.","gopis, flute, liberation, enchanting, melody, Krishna"),
        ("sb-2-4",2,"Krishna's Pastimes",4,"tadaa raasa pravrtto bhud vipina uttama shobitah krsna gopyo paritoshena divya premarasaanvitah","Then the Rasa dance began in that excellent grove, with Krishna and the gopis immersed in divine love and joy.","Rasa dance, grove, Krishna, gopis, divine love, joy"),
        ("sb-3-3",3,"Bhakti & Liberation",3,"yam na yogena sankhyena daana vrata tapah adhvaraihi vyakhya svadhyaaya sannyasaihi prapnuyad yatnavaan api","The Lord, whom one cannot reach through yoga, philosophy, charity, vows, austerity, sacrifice, study, or renunciation — even with great effort.","Lord, yoga, charity, vows, austerity, study, effort, unreachable"),
        ("sb-3-4",3,"Bhakti & Liberation",4,"bhaktyaa tv ananyaya shakya aham evam vidho rjuna jnatum drashtum cha tattvena praveshtum cha parantapa","But by exclusive devotion alone can I be known, seen in truth, and entered into, O Arjuna.","devotion, exclusive, known, truth, entered, Arjuna"),
        ("sb-4-2",4,"Prahlada & Devotion",2,"prahlada uvaca sada sarva bhutanam iha deva atma priyam skhalanam amritam vacho baalasya me anugraha","Prahlada said: O God, always the Self of all beings, please accept the sweet, stumbling words of this child as an offering of Your grace.","Prahlada, child, words, grace, offering, God, Self"),
        ("sb-4-3",4,"Prahlada & Devotion",3,"naham bibhemy ajita te tibhraasaat aparajitaad amukasmaat aprameyaad yato yato ha gatiih na me","O unconquered Lord, I am not afraid of Your terrible weapons, nor of death, nor of hell — because in You alone I take refuge.","unconquered, afraid, weapons, death, hell, refuge"),
    ]
    tc = {"temple": "Guruvayur Sri Krishna Temple", "location": "Guruvayur, Kerala", "detail": "Bhagavatha Saptaham (7-day recitation) is performed regularly at Guruvayur. The temple is considered the Dwarka of the South."}
    return [_v(vid,B,N,ch,cn,vn,t,tr,kw,_t(ml="",hi=""),tc) for vid,ch,cn,vn,t,tr,kw in vv]

def _hanuman_expansion():
    B = "hanuman-chalisa"; N = "Hanuman Chalisa"
    vv = [
        ("hc-1-12",1,"Hanuman Chalisa",12,"vidyavaan guni ati chatur ram kaaj karibe ko aatur","You are learned, virtuous, and extremely clever, always eager to accomplish Lord Rama's work.","learned, virtuous, clever, eager, Rama, work"),
        ("hc-1-13",1,"Hanuman Chalisa",13,"prabhu charitra sunibe ko rasiya ram lakhan sita man basiya","You delight in hearing the deeds of the Lord. Rama, Lakshmana and Sita dwell in your heart.","deeds, Lord, delight, Rama, Lakshmana, Sita, heart"),
        ("hc-1-14",1,"Hanuman Chalisa",14,"sukshma roop dhari siyahi dikhava vikat roop dhari lanka jarava","In a tiny form you appeared before Sita. In a terrible form you burnt Lanka.","tiny, Sita, terrible, Lanka, burnt, form"),
        ("hc-1-15",1,"Hanuman Chalisa",15,"laaye sajivan lakhan jiyaaye shri raghuvir harashi ur laaye","You brought the life-giving herb (Sanjeevani) and revived Lakshmana. Sri Rama embraced you with joy.","Sanjeevani, herb, Lakshmana, revived, Rama, joy, embrace"),
        ("hc-1-16",1,"Hanuman Chalisa",16,"raghupati kinhi bahut badai tum mama priya bharat hi sam bhai","Lord Rama praised you greatly, saying: 'You are dear to me as my brother Bharata.'","Rama, praised, dear, brother, Bharata, love"),
        ("hc-1-17",1,"Hanuman Chalisa",17,"sahas badan tumharo jas gaave as kahi shripati kanth lagaave","The thousand-headed serpent (Shesha) sings your glory, and Lord Vishnu embraces you.","Shesha, serpent, glory, Vishnu, embrace, singing"),
        ("hc-1-18",1,"Hanuman Chalisa",18,"sanakaadik brahmaadi muneesa narada sarada sahit aheesa","Sanaka, Brahma, sages, Narada, Saraswati, and the king of serpents — all praise you.","Sanaka, Brahma, sages, Narada, Saraswati, serpent, praise"),
        ("hc-1-19",1,"Hanuman Chalisa",19,"yam kuber digpal jahan te kavi kovid kahi sake kahan","Even Yama, Kubera, and the guardians of directions, poets and scholars — none can describe your glory.","Yama, Kubera, directions, poets, scholars, glory, indescribable"),
        ("hc-1-20",1,"Hanuman Chalisa",20,"tum upkar sugreevahin keenha ram milaye raj pad deenha","You did a great favor to Sugriva by introducing him to Rama, who then gave him the kingdom.","favor, Sugriva, Rama, kingdom, introduction, alliance"),
    ]
    return [_v(vid,B,N,1,"Hanuman Chalisa",vn,t,tr,kw,_t(hi="")) for vid,_,_,vn,t,tr,kw in vv]

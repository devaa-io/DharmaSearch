"""
Kerala-specific Hindu scriptures with transliterations and temple connections:
- Srimad Bhagavatam
- Narayaneeyam
- Adhyatma Ramayanam
- Lalita Sahasranama
- Vishnu Sahasranama
- Soundarya Lahari
- Vivekachudamani
"""

def get_kerala_metadata():
    return [
        {
            "text_id": "srimad-bhagavatam",
            "name": "Srimad Bhagavatam",
            "description": "The most beloved Purana in Kerala, narrating the life and pastimes of Lord Krishna. Recited during Bhagavatha Saptaham in temples across Kerala, it is central to the devotional life of Malayali Hindus.",
            "total_chapters": 4,
            "language": "Sanskrit",
            "region": "Kerala",
            "image": ""
        },
        {
            "text_id": "narayaneeyam",
            "name": "Narayaneeyam",
            "description": "Composed by Melpathur Narayana Bhattathiri at the Guruvayur Temple in 1586 CE. A condensed poetic retelling of the Srimad Bhagavatam in 1036 verses, written as a prayer to Lord Guruvayurappan to cure his paralysis.",
            "total_chapters": 3,
            "language": "Sanskrit",
            "region": "Kerala",
            "image": ""
        },
        {
            "text_id": "adhyatma-ramayanam",
            "name": "Adhyatma Ramayanam",
            "description": "The Malayalam Ramayana by Thunchaththu Ezhuthachan, the father of Malayalam literature. Written in the 16th century, it brought the Ramayana into every Kerala home and is considered the foundation of modern Malayalam.",
            "total_chapters": 3,
            "language": "Malayalam/Sanskrit",
            "region": "Kerala",
            "image": ""
        },
        {
            "text_id": "lalita-sahasranama",
            "name": "Lalita Sahasranama",
            "description": "The thousand names of Goddess Lalita (Tripurasundari), from the Brahmanda Purana. Widely recited in Kerala Devi temples, especially during Navaratri, it is a profound meditation on the Divine Feminine.",
            "total_chapters": 2,
            "language": "Sanskrit",
            "region": "Kerala",
            "image": ""
        },
        {
            "text_id": "vishnu-sahasranama",
            "name": "Vishnu Sahasranama",
            "description": "The thousand names of Lord Vishnu, from the Anushasana Parva of the Mahabharata. Daily recitation is a cornerstone of worship in Kerala Vishnu temples like Padmanabhaswamy and Guruvayur.",
            "total_chapters": 2,
            "language": "Sanskrit",
            "region": "Kerala",
            "image": ""
        },
        {
            "text_id": "soundarya-lahari",
            "name": "Soundarya Lahari",
            "description": "The 'Waves of Beauty' — a masterpiece by Adi Shankaracharya (born in Kaladi, Kerala). 100 verses praising Goddess Parvati, combining tantric worship with sublime poetry. A jewel of Advaita and Shakta traditions.",
            "total_chapters": 2,
            "language": "Sanskrit",
            "region": "Kerala",
            "image": ""
        },
        {
            "text_id": "vivekachudamani",
            "name": "Vivekachudamani",
            "description": "The 'Crest-Jewel of Discrimination' by Adi Shankaracharya. A treatise on Advaita Vedanta philosophy explaining the path to self-realization. Shankaracharya, born in Kaladi, Kerala, remains one of India's greatest philosophers.",
            "total_chapters": 2,
            "language": "Sanskrit",
            "region": "Kerala",
            "image": ""
        }
    ]


def get_kerala_verses():
    verses = []
    verses.extend(_bhagavatam_verses())
    verses.extend(_narayaneeyam_verses())
    verses.extend(_adhyatma_ramayanam_verses())
    verses.extend(_lalita_sahasranama_verses())
    verses.extend(_vishnu_sahasranama_verses())
    verses.extend(_soundarya_lahari_verses())
    verses.extend(_vivekachudamani_verses())
    return verses


def _bhagavatam_verses():
    return [
        {"verse_id": "sb-1-1", "text_id": "srimad-bhagavatam", "text_name": "Srimad Bhagavatam", "chapter": 1, "chapter_name": "Creation & Devotion", "verse_number": 1,
         "text": "janmady asya yato nvayad itaratas cartheshv abhijnah svarat tene brahma hrda ya adi-kavaye muhyanti yat surayah",
         "translation": "I meditate upon Lord Sri Krishna, from whom all creation emanates, by whom it is sustained, and into whom it dissolves. He is the omniscient one who imparted Vedic knowledge into the heart of Brahma, the first being.",
         "keywords": "Krishna, creation, omniscient, Brahma, Vedas, meditation",
         "transliterations": {"ml": "ജന്മാദ്യസ്യ യതോ ന്വയാദ് ഇതരതഃ ചാർഥേഷ്വ് അഭിജ്ഞഃ സ്വരാട്", "hi": "जन्माद्यस्य यतो न्वयाद् इतरतः चार्थेष्वभिज्ञः स्वराट्", "ta": "ஜன்மாத்யஸ்ய யதோ ந்வயாத் இதரதஃ சார்த்தேஷ்வபிஜ்ஞஃ ஸ்வராட்"},
         "temple_connection": {"temple": "Guruvayur Sri Krishna Temple", "location": "Guruvayur, Kerala", "detail": "The Bhagavatam is the central text of Guruvayur temple worship. Bhagavatha Saptaham (7-day recitation) is performed here regularly."}},

        {"verse_id": "sb-1-2", "text_id": "srimad-bhagavatam", "text_name": "Srimad Bhagavatam", "chapter": 1, "chapter_name": "Creation & Devotion", "verse_number": 2,
         "text": "dharmah projjhita-kaitavo tra paramo nirmatsaranam satam vedyam vastavam atra vastu sivadam tapa-trayonmulanam",
         "translation": "Completely rejecting all religious activities which are materially motivated, this Bhagavata Purana propounds the highest truth, which is understandable by those devotees who are fully pure in heart.",
         "keywords": "truth, devotion, purity, heart, highest, Bhagavata",
         "transliterations": {"ml": "ധർമഃ പ്രോജ്ഝിതകൈതവോ ത്ര പരമോ നിർമത്സരാണാം സതാം", "hi": "धर्मः प्रोज्झितकैतवो त्र परमो निर्मत्सराणां सताम्"},
         "temple_connection": {"temple": "Padmanabhaswamy Temple", "location": "Thiruvananthapuram, Kerala", "detail": "Daily Bhagavatam recitation is a tradition at this ancient Vishnu temple, one of the richest temples in the world."}},

        {"verse_id": "sb-2-1", "text_id": "srimad-bhagavatam", "text_name": "Srimad Bhagavatam", "chapter": 2, "chapter_name": "Krishna's Pastimes", "verse_number": 1,
         "text": "krsnam enam avehi tvam atmanam akhilatmanam jagad-dhitaya so py atra dehivabhati mayaya",
         "translation": "Know Krishna to be the Supreme Soul of all souls. For the welfare of the world, He appears here through His divine maya in a human-like form.",
         "keywords": "Krishna, Supreme Soul, maya, welfare, world, incarnation",
         "transliterations": {"ml": "കൃഷ്ണം ഏനം അവേഹി ത്വം ആത്മാനം അഖിലാത്മനാം", "hi": "कृष्णं एनं अवेहि त्वं आत्मानं अखिलात्मनाम्"}},

        {"verse_id": "sb-2-2", "text_id": "srimad-bhagavatam", "text_name": "Srimad Bhagavatam", "chapter": 2, "chapter_name": "Krishna's Pastimes", "verse_number": 2,
         "text": "vasudevah sarvam iti sa mahatma su-durlabhah",
         "translation": "One who knows that Vasudeva (Krishna) is everything — such a great soul is extremely rare.",
         "keywords": "Vasudeva, Krishna, everything, great soul, rare, devotion",
         "transliterations": {"ml": "വാസുദേവഃ സർവം ഇതി സ മഹാത്മാ സുദുർലഭഃ", "hi": "वासुदेवः सर्वं इति स महात्मा सुदुर्लभः"}},

        {"verse_id": "sb-3-1", "text_id": "srimad-bhagavatam", "text_name": "Srimad Bhagavatam", "chapter": 3, "chapter_name": "Bhakti & Liberation", "verse_number": 1,
         "text": "kaler dosa-nidhe rajann asti hy eko mahan gunah kirtanad eva krsnasya mukta-sangah param vrajet",
         "translation": "In this age of Kali, which is an ocean of faults, there is one great virtue: simply by chanting the holy names of Krishna, one can become free from bondage and attain the supreme destination.",
         "keywords": "Kali Yuga, chanting, Krishna, liberation, bondage, nama japa",
         "transliterations": {"ml": "കലേർ ദോഷനിധേ രാജൻ അസ്തി ഹ്യേകോ മഹാൻ ഗുണഃ", "hi": "कलेर्दोषनिधे राजन् अस्ति ह्येको महान् गुणः"},
         "temple_connection": {"temple": "Sabarimala Ayyappa Temple", "location": "Pathanamthitta, Kerala", "detail": "The Bhagavatam's teachings on devotion and surrender are central to the Ayyappa pilgrimage tradition."}},

        {"verse_id": "sb-3-2", "text_id": "srimad-bhagavatam", "text_name": "Srimad Bhagavatam", "chapter": 3, "chapter_name": "Bhakti & Liberation", "verse_number": 2,
         "text": "akamah sarva-kamo va moksha-kama udara-dhih tivrena bhakti-yogena yajeta purusham param",
         "translation": "Whether one desires everything or nothing, or desires liberation, if one is truly intelligent, one should worship the Supreme Person with intense devotional service.",
         "keywords": "desire, liberation, worship, bhakti yoga, intelligence, Supreme",
         "transliterations": {"ml": "അകാമഃ സർവകാമോ വാ മോക്ഷകാമ ഉദാരധീഃ", "hi": "अकामः सर्वकामो वा मोक्षकाम उदारधीः"}},

        {"verse_id": "sb-4-1", "text_id": "srimad-bhagavatam", "text_name": "Srimad Bhagavatam", "chapter": 4, "chapter_name": "Prahlada & Devotion", "verse_number": 1,
         "text": "sravanam kirtanam visnoh smaranam pada-sevanam arcanam vandanam dasyam sakhyam atma-nivedanam",
         "translation": "The nine forms of devotional service are: hearing about the Lord, chanting His glories, remembering Him, serving His feet, worshipping, praying, serving, befriending, and surrendering everything to Him.",
         "keywords": "nine forms, devotion, bhakti, hearing, chanting, remembering, Prahlada, navavidha bhakti",
         "transliterations": {"ml": "ശ്രവണം കീർത്തനം വിഷ്ണോഃ സ്മരണം പാദസേവനം", "hi": "श्रवणं कीर्तनं विष्णोः स्मरणं पादसेवनम्"},
         "temple_connection": {"temple": "Guruvayur Sri Krishna Temple", "location": "Guruvayur, Kerala", "detail": "All nine forms of bhakti are practiced daily at Guruvayur. The Vilakkunnetthi and Usha Pooja embody these forms."}},
    ]


def _narayaneeyam_verses():
    return [
        {"verse_id": "nar-1-1", "text_id": "narayaneeyam", "text_name": "Narayaneeyam", "chapter": 1, "chapter_name": "Invocation & Creation", "verse_number": 1,
         "text": "sandrananda avabodhatmakam anupamitam kala desha avadhibhyam niruktam nityam nirgunam api",
         "translation": "I meditate on the Supreme Being who is of the nature of concentrated bliss and pure consciousness, who is beyond comparison, unlimited by time and space, eternal and beyond all qualities.",
         "keywords": "bliss, consciousness, eternal, unlimited, meditation, Guruvayurappan",
         "transliterations": {"ml": "സാന്ദ്രാനന്ദാവബോധാത്മകം അനുപമിതം കാലദേശാവധിഭ്യാം", "hi": "सान्द्रानन्दावबोधात्मकं अनुपमितं कालदेशावधिभ्याम्"},
         "temple_connection": {"temple": "Guruvayur Sri Krishna Temple", "location": "Guruvayur, Kerala", "detail": "The entire Narayaneeyam was composed here by Melpathur in 1586. He was cured of paralysis upon completing the 100th Dashakam. The last verse was composed on the 28th day of Vrischikam (Nov-Dec)."}},

        {"verse_id": "nar-1-2", "text_id": "narayaneeyam", "text_name": "Narayaneeyam", "chapter": 1, "chapter_name": "Invocation & Creation", "verse_number": 2,
         "text": "agre pasyami tejo nibiditam sakalam pratyag atma svarupam",
         "translation": "Before me I see a mass of radiance, the complete form of the inner Self, the all-pervading light of consciousness.",
         "keywords": "radiance, self, consciousness, light, vision, divine form",
         "transliterations": {"ml": "അഗ്രേ പശ്യാമി തേജോ നിബിഡിതം സകലം പ്രത്യഗാത്മസ്വരൂപം", "hi": "अग्रे पश्यामि तेजो निबिडितं सकलं प्रत्यगात्मस्वरूपम्"}},

        {"verse_id": "nar-2-1", "text_id": "narayaneeyam", "text_name": "Narayaneeyam", "chapter": 2, "chapter_name": "Krishna Leela", "verse_number": 1,
         "text": "ayam tu sakshad bhagavan svayam harer avataro narakantako harim",
         "translation": "This child (Krishna) is the direct incarnation of Lord Hari Himself, the Supreme Lord who destroys all evil and suffering.",
         "keywords": "Krishna, incarnation, Hari, Supreme Lord, evil, suffering",
         "transliterations": {"ml": "അയം തു സാക്ഷാദ് ഭഗവാൻ സ്വയം ഹരേർ അവതാരോ നരകാന്തകോ ഹരിം", "hi": "अयं तु साक्षाद् भगवान् स्वयं हरेर् अवतारो नरकान्तको हरिम्"},
         "temple_connection": {"temple": "Guruvayur Sri Krishna Temple", "location": "Guruvayur, Kerala", "detail": "The Krishna Leela sections describe the deity form worshipped at Guruvayur — the child Krishna (Unni Kannan) holding conch, discus, mace and lotus."}},

        {"verse_id": "nar-3-1", "text_id": "narayaneeyam", "text_name": "Narayaneeyam", "chapter": 3, "chapter_name": "Final Prayer", "verse_number": 1,
         "text": "agre pashyami tejo nibiditam akhilam tatva muktyai bhajami tvam vatalyalayesham",
         "translation": "I behold before me a brilliant form of concentrated radiance. For the attainment of liberation, I worship You, O Lord of Guruvayur (the temple surrounded by the wind).",
         "keywords": "radiance, liberation, worship, Guruvayur, Lord, vision, final verse",
         "transliterations": {"ml": "അഗ്രേ പശ്യാമി തേജോ നിബിഡിതം അഖിലം തത്ത്വമുക്ത്യൈ ഭജാമി", "hi": "अग्रे पश्यामि तेजो निबिडितं अखिलं तत्त्वमुक्त्यै भजामि"},
         "temple_connection": {"temple": "Guruvayur Sri Krishna Temple", "location": "Guruvayur, Kerala", "detail": "This is the climactic verse of the Narayaneeyam — the 100th Dashakam. Upon writing it, Melpathur had a vision of Lord Vishnu and was cured of his paralysis. It is recited daily at Guruvayur."}},
    ]


def _adhyatma_ramayanam_verses():
    return [
        {"verse_id": "ar-1-1", "text_id": "adhyatma-ramayanam", "text_name": "Adhyatma Ramayanam", "chapter": 1, "chapter_name": "Bala Kandam", "verse_number": 1,
         "text": "sriramo jayaramo jayajaya rama srirama jayarama jayajaya rama",
         "translation": "Victory to Lord Sri Rama! Victory, victory to Rama! Sri Rama is victorious, victory, victory to Rama!",
         "keywords": "Rama, victory, chanting, invocation, Ezhuthachan",
         "transliterations": {"ml": "ശ്രീരാമോ ജയരാമോ ജയജയ രാമ ശ്രീരാമ ജയരാമ ജയജയ രാമ", "hi": "श्रीरामो जयरामो जयजय राम श्रीराम जयराम जयजय राम"}},

        {"verse_id": "ar-1-2", "text_id": "adhyatma-ramayanam", "text_name": "Adhyatma Ramayanam", "chapter": 1, "chapter_name": "Bala Kandam", "verse_number": 2,
         "text": "harinamakirttanam nalla matham ini enikkum nishchayam harismaranam ennum ekkaalathum venda marannu pokalaarumee janmam",
         "translation": "Chanting the name of Hari is the best path — of this I am now certain. Remembrance of Hari at all times is needed; let no one forget this throughout their life.",
         "keywords": "Hari, chanting, remembrance, path, life, devotion, Malayalam",
         "transliterations": {"ml": "ഹരിനാമകീർത്തനം നല്ല മതം ഇനി എനിക്കും നിശ്ചയം ഹരിസ്മരണം എന്നും എക്കാലത്തും വേണ്ട മറന്നുപോകല്ലാരുമീ ജന്മം", "hi": "हरिनामकीर्तनं नल्ल मतम् इनि एनिक्कुम् निश्चयम्"}},

        {"verse_id": "ar-2-1", "text_id": "adhyatma-ramayanam", "text_name": "Adhyatma Ramayanam", "chapter": 2, "chapter_name": "Aranya Kandam", "verse_number": 1,
         "text": "ramayanam jagatinum veda saaram athin ullil ariyaam param poruL",
         "translation": "The Ramayana is the essence of the Vedas for the entire world. Within it lies the supreme meaning that can be known.",
         "keywords": "Ramayana, Vedas, essence, supreme meaning, world",
         "transliterations": {"ml": "രാമായണം ജഗതിനും വേദസാരം അതിൻ ഉള്ളിൽ അറിയാം പരം പൊരുൾ", "hi": "रामायणं जगतिनुम् वेदसारम् अतिन् उल्लिल् अरियाम् परम् पोरुळ्"},
         "temple_connection": {"temple": "Thunchan Parambu", "location": "Tirur, Malappuram, Kerala", "detail": "This is the birthplace of Thunchaththu Ezhuthachan, author of the Adhyatma Ramayanam. The site is now a memorial and cultural center. Ramayana month (Karkkidakam) recitations happen across Kerala."}},

        {"verse_id": "ar-3-1", "text_id": "adhyatma-ramayanam", "text_name": "Adhyatma Ramayanam", "chapter": 3, "chapter_name": "Yuddha Kandam", "verse_number": 1,
         "text": "api svarnamayii lanka na me lakshmana rochate jananii janma bhuumishcha svargaadapi gariiyasii",
         "translation": "Even this golden Lanka does not charm me, O Lakshmana. One's mother and motherland are greater than heaven itself.",
         "keywords": "Lanka, gold, motherland, mother, heaven, Rama, Lakshmana, patriotism",
         "transliterations": {"ml": "അപി സ്വർണ്ണമയീ ലങ്കാ ന മേ ലക്ഷ്മണ രോചതേ ജനനീ ജന്മഭൂമിശ്ച സ്വർഗ്ഗാദപി ഗരീയസീ", "hi": "अपि स्वर्णमयी लङ्का न मे लक्ष्मण रोचते जननी जन्मभूमिश्च स्वर्गादपि गरीयसी"}},
    ]


def _lalita_sahasranama_verses():
    return [
        {"verse_id": "ls-1-1", "text_id": "lalita-sahasranama", "text_name": "Lalita Sahasranama", "chapter": 1, "chapter_name": "Names of the Goddess", "verse_number": 1,
         "text": "sri mata sri maha rajni srimat simhasanesvari chidagni kunda sambhuta deva karya samudyata",
         "translation": "She who is the auspicious Mother, the great Empress, who sits on the lion throne. She who was born from the fire of pure consciousness, who arose to accomplish the purpose of the gods.",
         "keywords": "Mother, Empress, consciousness, fire, gods, Lalita, Tripurasundari",
         "transliterations": {"ml": "ശ്രീമാതാ ശ്രീമഹാരാജ്ഞീ ശ്രീമത്സിംഹാസനേശ്വരീ ചിദഗ്നികുണ്ഡസംഭൂതാ ദേവകാര്യസമുദ്യതാ", "hi": "श्रीमाता श्रीमहाराज्ञी श्रीमत्सिंहासनेश्वरी चिदग्निकुण्डसम्भूता देवकार्यसमुद्यता"},
         "temple_connection": {"temple": "Chottanikkara Bhagavathy Temple", "location": "Ernakulam, Kerala", "detail": "Lalita Sahasranama is recited daily here. The temple worships the Goddess in three forms — Saraswati (morning), Lakshmi (noon), and Durga (evening)."}},

        {"verse_id": "ls-1-2", "text_id": "lalita-sahasranama", "text_name": "Lalita Sahasranama", "chapter": 1, "chapter_name": "Names of the Goddess", "verse_number": 2,
         "text": "udyadbhanu sahasrabha chaturbaahu samanvita ragha svarupa pashadhya krodhakara ankusojjvala",
         "translation": "She who has the radiance of a thousand rising suns, who has four arms, who holds the noose of desire and the goad of anger, radiating brilliance.",
         "keywords": "radiance, suns, four arms, noose, goad, desire, anger, brilliance",
         "transliterations": {"ml": "ഉദ്യദ്ഭാനുസഹസ്രാഭാ ചതുർബാഹുസമന്വിതാ രാഗസ്വരൂപപാശാഢ്യാ ക്രോധാകാരാങ്കുശോജ്ജ്വലാ", "hi": "उद्यद्भानुसहस्राभा चतुर्बाहुसमन्विता रागस्वरूपपाशाढ्या क्रोधाकाराङ्कुशोज्ज्वला"}},

        {"verse_id": "ls-2-1", "text_id": "lalita-sahasranama", "text_name": "Lalita Sahasranama", "chapter": 2, "chapter_name": "Powers & Attributes", "verse_number": 1,
         "text": "sarva mangala mangalye sive sarvartha sadhike sharanye tryambake gauri narayani namostute",
         "translation": "O auspicious of all that is auspicious, O Shiva, O accomplisher of all goals, O refuge, O three-eyed Gauri, O Narayani — salutations to You.",
         "keywords": "auspicious, Shiva, Gauri, Narayani, refuge, salutations, prayer",
         "transliterations": {"ml": "സർവമംഗളമാംഗല്യേ ശിവേ സർവാർഥസാധികേ ശരണ്യേ ത്ര്യംബകേ ഗൗരി നാരായണി നമോസ്തുതേ", "hi": "सर्वमङ्गलमाङ्गल्ये शिवे सर्वार्थसाधिके शरण्ये त्र्यम्बके गौरि नारायणि नमोस्तुते"},
         "temple_connection": {"temple": "Attukal Bhagavathy Temple", "location": "Thiruvananthapuram, Kerala", "detail": "Known for the Attukal Pongala, the largest gathering of women for a religious festival (Guinness record). Lalita Sahasranama is central to worship here."}},
    ]


def _vishnu_sahasranama_verses():
    return [
        {"verse_id": "vs-1-1", "text_id": "vishnu-sahasranama", "text_name": "Vishnu Sahasranama", "chapter": 1, "chapter_name": "Names of Vishnu", "verse_number": 1,
         "text": "visvam vishnur vashatkaro bhuta bhavya bhavat prabhuh bhutakrit bhutabhrit bhavo bhutatma bhutabhavanah",
         "translation": "He who is the universe, who is all-pervading, who controls all, who is the Lord of past, present and future. He who creates, sustains, and is the soul and nourisher of all beings.",
         "keywords": "Vishnu, universe, all-pervading, Lord, past, future, creator, sustainer",
         "transliterations": {"ml": "വിശ്വം വിഷ്ണുർ വഷട്കാരോ ഭൂതഭവ്യഭവത്പ്രഭുഃ ഭൂതകൃദ് ഭൂതഭൃദ് ഭാവോ ഭൂതാത്മാ ഭൂതഭാവനഃ", "hi": "विश्वं विष्णुर्वषट्कारो भूतभव्यभवत्प्रभुः भूतकृद् भूतभृद् भावो भूतात्मा भूतभावनः"},
         "temple_connection": {"temple": "Padmanabhaswamy Temple", "location": "Thiruvananthapuram, Kerala", "detail": "One of the 108 Divya Desams. The reclining Vishnu (Padmanabha) form here is one of the most sacred in Hinduism. Vishnu Sahasranama is recited daily."}},

        {"verse_id": "vs-1-2", "text_id": "vishnu-sahasranama", "text_name": "Vishnu Sahasranama", "chapter": 1, "chapter_name": "Names of Vishnu", "verse_number": 2,
         "text": "om namo bhagavate vasudevaya",
         "translation": "Om, salutations to the Supreme Lord Vasudeva (Krishna).",
         "keywords": "Om, salutations, Vasudeva, Krishna, mantra, devotion",
         "transliterations": {"ml": "ഓം നമോ ഭഗവതേ വാസുദേവായ", "hi": "ॐ नमो भगवते वासुदेवाय"},
         "temple_connection": {"temple": "Guruvayur Sri Krishna Temple", "location": "Guruvayur, Kerala", "detail": "This mantra is the heart of worship at Guruvayur. Devotees chant it while circumambulating the temple."}},

        {"verse_id": "vs-2-1", "text_id": "vishnu-sahasranama", "text_name": "Vishnu Sahasranama", "chapter": 2, "chapter_name": "Phala Shruti", "verse_number": 1,
         "text": "iteedam keertaneeyasya keshavasya mahaatmanah naamnam sahasram divyaanaam aseshena prakeertitam",
         "translation": "Thus have been sung the complete thousand divine names of Keshava, the great-souled one, which are worthy of being recited.",
         "keywords": "thousand names, Keshava, divine, recitation, complete, great soul",
         "transliterations": {"ml": "ഇതീദം കീർത്തനീയസ്യ കേശവസ്യ മഹാത്മനഃ നാമ്നാം സഹസ്രം ദിവ്യാനാം അശേഷേണ പ്രകീർത്തിതം", "hi": "इतीदं कीर्तनीयस्य केशवस्य महात्मनः नाम्नां सहस्रं दिव्यानां अशेषेण प्रकीर्तितम्"}},
    ]


def _soundarya_lahari_verses():
    return [
        {"verse_id": "sl-1-1", "text_id": "soundarya-lahari", "text_name": "Soundarya Lahari", "chapter": 1, "chapter_name": "Ananda Lahari", "verse_number": 1,
         "text": "sivah saktya yukto yadi bhavati saktah prabhavitum na cedevam devo na khalu kusalah spanditumapi",
         "translation": "Only when Shiva is united with Shakti does He have the power to create. Without Her, He cannot even move. How then can one who has not acquired merit worship You, who are adored even by Brahma, Vishnu and Shiva?",
         "keywords": "Shiva, Shakti, creation, power, worship, Brahma, Vishnu, merit, Shankaracharya",
         "transliterations": {"ml": "ശിവഃ ശക്ത്യാ യുക്തോ യദി ഭവതി ശക്തഃ പ്രഭവിതും ന ചേദേവം ദേവോ ന ഖലു കുശലഃ സ്പന്ദിതുമപി", "hi": "शिवः शक्त्या युक्तो यदि भवति शक्तः प्रभवितुं न चेदेवं देवो न खलु कुशलः स्पन्दितुमपि"},
         "temple_connection": {"temple": "Adi Shankaracharya Birthplace", "location": "Kaladi, Kerala", "detail": "Shankaracharya was born here around 788 CE. This verse establishes the Shakta-Advaita philosophy — Shiva and Shakti are inseparable. The memorial temple at Kaladi celebrates his legacy."}},

        {"verse_id": "sl-1-2", "text_id": "soundarya-lahari", "text_name": "Soundarya Lahari", "chapter": 1, "chapter_name": "Ananda Lahari", "verse_number": 2,
         "text": "taniyamsam pamsum tava carana pankeruha-bhavam virincih sanchinvan virachayati lokan avikalam",
         "translation": "Brahma collects a tiny particle of dust from Your lotus feet and creates the entire universe without any deficiency.",
         "keywords": "Brahma, lotus feet, dust, creation, universe, Goddess, devotion",
         "transliterations": {"ml": "തനീയാംസം പാംശും തവ ചരണപങ്കേരുഹഭവം വിരിഞ്ചിഃ സഞ്ചിൻവൻ വിരചയതി ലോകാൻ അവികലം", "hi": "तनीयांसं पांशुं तव चरणपङ्केरुहभवं विरिञ्चिः सञ्चिन्वन् विरचयति लोकान् अविकलम्"}},

        {"verse_id": "sl-2-1", "text_id": "soundarya-lahari", "text_name": "Soundarya Lahari", "chapter": 2, "chapter_name": "Soundarya Lahari", "verse_number": 1,
         "text": "gatair manikyatvam gagana-manibhih sandraghatitam kiritam te haimam himagiri sute kirttayati yah",
         "translation": "O daughter of the Himalayas, Your golden crown studded with gems that were once the stars of the sky — he who praises it becomes the crown-jewel among poets.",
         "keywords": "crown, gems, stars, Himalayas, daughter, poet, praise, beauty",
         "transliterations": {"ml": "ഗതൈർ മാണിക്യത്വം ഗഗനമണിഭിഃ സാന്ദ്രഘടിതം കിരീടം തേ ഹൈമം ഹിമഗിരിസുതേ കീർത്തയതി യഃ", "hi": "गतैर्माणिक्यत्वं गगनमणिभिः सान्द्रघटितं किरीटं ते हैमं हिमगिरिसुते कीर्तयति यः"}},
    ]


def _vivekachudamani_verses():
    return [
        {"verse_id": "vc-1-1", "text_id": "vivekachudamani", "text_name": "Vivekachudamani", "chapter": 1, "chapter_name": "The Quest for Liberation", "verse_number": 1,
         "text": "sarva vedanta siddhanta gocharamtam agocharam govindamparamanandam sad gurum pranatosmy aham",
         "translation": "I prostrate before Govinda, the supreme teacher, who is the embodiment of supreme bliss, who is the goal of all Vedanta, yet remains beyond the reach of words and mind.",
         "keywords": "Govinda, guru, bliss, Vedanta, prostrate, liberation, Shankaracharya",
         "transliterations": {"ml": "സർവവേദാന്തസിദ്ധാന്തഗോചരം തം അഗോചരം ഗോവിന്ദം പരമാനന്ദം സദ്ഗുരും പ്രണതോസ്മ്യഹം", "hi": "सर्ववेदान्तसिद्धान्तगोचरं तं अगोचरं गोविन्दं परमानन्दं सद्गुरुं प्रणतोस्म्यहम्"},
         "temple_connection": {"temple": "Sringeri Sharada Peetham", "location": "Karnataka (founded by Shankaracharya from Kerala)", "detail": "Shankaracharya, born in Kaladi, Kerala, established four mathas including Sringeri. His Vivekachudamani teachings continue through the Shankaracharya lineage."}},

        {"verse_id": "vc-1-2", "text_id": "vivekachudamani", "text_name": "Vivekachudamani", "chapter": 1, "chapter_name": "The Quest for Liberation", "verse_number": 2,
         "text": "jantunam nara janma durlabham atah pumsatvam tatah viprata tasmad vaidikadharmamargaparata vidvattvamasmat param",
         "translation": "For all beings, human birth is rare to obtain. Even rarer is being born as a man, rarer still a Brahmana, and rarest of all is the desire for liberation through the path of Vedic wisdom.",
         "keywords": "human birth, rare, liberation, wisdom, Vedic, path, discrimination",
         "transliterations": {"ml": "ജന്തൂനാം നരജന്മ ദുർലഭം അതഃ പുംസ്ത്വം തതഃ വിപ്രതാ", "hi": "जन्तूनां नरजन्म दुर्लभं अतः पुंस्त्वं ततः विप्रता"}},

        {"verse_id": "vc-2-1", "text_id": "vivekachudamani", "text_name": "Vivekachudamani", "chapter": 2, "chapter_name": "Self-Knowledge", "verse_number": 1,
         "text": "brahma satyam jagan mithya jivo brahmaiva naparah",
         "translation": "Brahman alone is real, the world is an appearance (mithya), and the individual self (jiva) is none other than Brahman.",
         "keywords": "Brahman, real, world, mithya, illusion, self, Advaita, mahavakya",
         "transliterations": {"ml": "ബ്രഹ്മ സത്യം ജഗൻ മിഥ്യാ ജീവോ ബ്രഹ്മൈവ നാപരഃ", "hi": "ब्रह्म सत्यं जगन् मिथ्या जीवो ब्रह्मैव नापरः"},
         "temple_connection": {"temple": "Adi Shankaracharya Birthplace", "location": "Kaladi, Kerala", "detail": "This is the core teaching of Advaita Vedanta. The temple at Kaladi has shrines for both Shankara and his guru Govindapada. The Shankaracharya lineage continues to this day."}},

        {"verse_id": "vc-2-2", "text_id": "vivekachudamani", "text_name": "Vivekachudamani", "chapter": 2, "chapter_name": "Self-Knowledge", "verse_number": 2,
         "text": "slokaardhena pravakshyaami yad uktam granthakotibhih brahma satyam jagan mithya jivo brahmaiva naparah",
         "translation": "I shall state in half a verse what has been said in crores of scriptures: Brahman is real, the world is appearance, the individual soul is Brahman alone and nothing else.",
         "keywords": "half verse, scriptures, Brahman, reality, appearance, soul, summary",
         "transliterations": {"ml": "ശ്ലോകാർധേന പ്രവക്ഷ്യാമി യദ് ഉക്തം ഗ്രന്ഥകോടിഭിഃ", "hi": "श्लोकार्धेन प्रवक्ष्यामि यदुक्तं ग्रन्थकोटिभिः"}},
    ]

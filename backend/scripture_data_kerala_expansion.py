"""
Additional Kerala verses + transliterations for all Kerala texts in Tamil, Telugu, Kannada
"""

def get_kerala_expansion_verses():
    return [
        # More Srimad Bhagavatam
        {"verse_id": "sb-1-3", "text_id": "srimad-bhagavatam", "text_name": "Srimad Bhagavatam", "chapter": 1, "chapter_name": "Creation & Devotion", "verse_number": 3,
         "text": "nigama-kalpa-taror galitam phalam shuka-mukhad amrita-drava-samyutam pibata bhagavatam rasam alayam muhur aho rasika bhuvi bhavukah",
         "translation": "O thoughtful men, relish the Srimad Bhagavatam, the ripe fruit of the Vedic tree, dripping with nectar from the lips of Shuka. Drink deeply of this immortal essence again and again.",
         "keywords": "Bhagavatam, fruit, Vedic tree, nectar, Shuka, relish, immortal",
         "transliterations": {"ml": "നിഗമകല്പതരോർ ഗലിതം ഫലം ശുകമുഖാദ് അമൃതദ്രവസംയുതം", "hi": "निगमकल्पतरोर्गलितं फलं शुकमुखादमृतद्रवसंयुतम्", "ta": "நிகமகல்பதரோர்கலிதம் பலம் ஶுகமுகாதம்ருததிரவஸம்யுதம்", "te": "నిగమకల్పతరోర్గలితం ఫలం శుకముఖాదమృతద్రవసంయుతమ్", "kn": "ನಿಗಮಕಲ್ಪತರೋರ್ಗಲಿತಂ ಫಲಂ ಶುಕಮುಖಾದಮೃತದ್ರವಸಂಯುತಮ್"},
         "temple_connection": {"temple": "Guruvayur Sri Krishna Temple", "location": "Guruvayur, Kerala", "detail": "This verse is recited at the beginning of every Bhagavatha Saptaham (7-day recitation) at Guruvayur and across Kerala temples."}},

        {"verse_id": "sb-1-4", "text_id": "srimad-bhagavatam", "text_name": "Srimad Bhagavatam", "chapter": 1, "chapter_name": "Creation & Devotion", "verse_number": 4,
         "text": "nasta prayeshv abhadreshu nityam bhagavata sevaya bhagavaty uttama shloke bhaktir bhavati naishthiki",
         "translation": "By regularly hearing the Bhagavatam and rendering service to the pure devotee, all that is troublesome to the heart is almost completely destroyed, and loving service unto the Supreme Lord, who is praised with transcendental songs, is established as an irrevocable fact.",
         "keywords": "hearing, service, devotee, heart, loving service, Supreme Lord",
         "transliterations": {"ml": "നഷ്ടപ്രായേഷ്വഭദ്രേഷു നിത്യം ഭാഗവതസേവയാ", "hi": "नष्टप्रायेष्वभद्रेषु नित्यं भागवतसेवया", "ta": "நஷ்டப்ராயேஷ்வபத்ரேஷு நித்யம் பாகவதஸேவயா", "te": "నష్టప్రాయేష్వభద్రేషు నిత్యం భాగవతసేవయా", "kn": "ನಷ್ಟಪ್ರಾಯೇಷ್ವಭದ್ರೇಷು ನಿತ್ಯಂ ಭಾಗವತಸೇವಯಾ"}},

        # More Narayaneeyam
        {"verse_id": "nar-1-3", "text_id": "narayaneeyam", "text_name": "Narayaneeyam", "chapter": 1, "chapter_name": "Invocation & Creation", "verse_number": 3,
         "text": "sarveshaam aadhaaram aadhaaraheenm sarveshaam chaalanam chaalanam achalyam sarveshaam karanam kaaranamesha param",
         "translation": "He is the support of all, yet has no support. He is the mover of all, yet is immovable. He is the cause of all causes, the supreme ultimate.",
         "keywords": "support, immovable, cause, supreme, ultimate, paradox",
         "transliterations": {"ml": "സർവേഷാം ആധാരം ആധാരഹീനം സർവേഷാം ചാലനം ചാലനം അചല്യം", "hi": "सर्वेषां आधारं आधारहीनं सर्वेषां चालनं चालनं अचल्यम्", "ta": "ஸர்வேஷாம் ஆதாரம் ஆதாரஹீநம் ஸர்வேஷாம் சாலநம் சாலநம் அசல்யம்", "te": "సర్వేషాం ఆధారం ఆధారహీనం సర్వేషాం చాలనం చాలనం అచల్యమ్"},
         "temple_connection": {"temple": "Guruvayur Sri Krishna Temple", "location": "Guruvayur, Kerala", "detail": "This philosophical verse describes the nature of Lord Vishnu as worshipped at Guruvayur — the paradox of the Absolute being both the foundation and the transcendent."}},

        {"verse_id": "nar-2-2", "text_id": "narayaneeyam", "text_name": "Narayaneeyam", "chapter": 2, "chapter_name": "Krishna Leela", "verse_number": 2,
         "text": "krishnam vande jagadgurum",
         "translation": "I salute Krishna, the teacher of the entire universe.",
         "keywords": "Krishna, salutation, teacher, universe, guru, jagadguru",
         "transliterations": {"ml": "കൃഷ്ണം വന്ദേ ജഗദ്ഗുരും", "hi": "कृष्णं वन्दे जगद्गुरुम्", "ta": "க்ருஷ்ணம் வந்தே ஜகத்குரும்", "te": "కృష్ణం వన్దే జగద్గురుమ్", "kn": "ಕೃಷ್ಣಂ ವನ್ದೇ ಜಗದ್ಗುರುಂ"}},

        # More Soundarya Lahari
        {"verse_id": "sl-1-3", "text_id": "soundarya-lahari", "text_name": "Soundarya Lahari", "chapter": 1, "chapter_name": "Ananda Lahari", "verse_number": 3,
         "text": "avidyanam antas timira mihira dvipanagari jadanam chaitanya stabaka makaranda shruti jhari",
         "translation": "For those enveloped in the darkness of ignorance, You are the island city of the Sun. For the dull-witted, You are the cluster of blossoms showering the nectar of consciousness.",
         "keywords": "ignorance, darkness, Sun, consciousness, nectar, blossoms, Shankaracharya",
         "transliterations": {"ml": "അവിദ്യാനാം അന്തസ്തിമിരമിഹിരദ്വീപനഗരീ ജഡാനാം ചൈതന്യസ്തബകമകരന്ദശ്രുതിഝരീ", "hi": "अविद्यानां अन्तस्तिमिरमिहिरद्वीपनगरी जडानां चैतन्यस्तबकमकरन्दश्रुतिझरी", "ta": "அவித்யாநாம் அந்தஸ்திமிரமிஹிரத்வீபநகரீ ஜடாநாம் சைதந்யஸ்தபகமகரந்தஶ்ருதிஜரீ"}},

        # More Vivekachudamani
        {"verse_id": "vc-1-3", "text_id": "vivekachudamani", "text_name": "Vivekachudamani", "chapter": 1, "chapter_name": "The Quest for Liberation", "verse_number": 3,
         "text": "durlabham trayam evaitad devanugraha hetukam manushyatvam mumukshutvam mahapurusha samsrayah",
         "translation": "Three things are rare indeed and are due to the grace of God: a human birth, the longing for liberation, and the protecting care of a perfected sage.",
         "keywords": "rare, human birth, liberation, sage, grace of God, longing",
         "transliterations": {"ml": "ദുർലഭം ത്രയമേവൈതദ് ദേവാനുഗ്രഹഹേതുകം മനുഷ്യത്വം മുമുക്ഷുത്വം മഹാപുരുഷസംശ്രയഃ", "hi": "दुर्लभं त्रयमेवैतद्देवानुग्रहहेतुकम् मनुष्यत्वं मुमुक्षुत्वं महापुरुषसंश्रयः", "ta": "துர்லபம் த்ரயமேவைதத்தேவாநுக்ரஹஹேதுகம் மநுஷ்யத்வம் முமுக்ஷுத்வம் மஹாபுருஷஸம்ஶ்ரயஃ"}},

        {"verse_id": "vc-2-3", "text_id": "vivekachudamani", "text_name": "Vivekachudamani", "chapter": 2, "chapter_name": "Self-Knowledge", "verse_number": 3,
         "text": "na yogena na sankhyena karmana no na vidyaya brahmatmaikatva bodhena moksah sidhyati nanyatha",
         "translation": "Neither by yoga, nor by sankhya, nor by works, nor by learning, but by the realization of the identity of Brahman and Atman is liberation possible, and by no other means.",
         "keywords": "yoga, sankhya, works, learning, Brahman, Atman, liberation, identity, Advaita",
         "transliterations": {"ml": "ന യോഗേന ന സാംഖ്യേന കർമണാ നോ ന വിദ്യയാ ബ്രഹ്മാത്മൈകത്വബോധേന മോക്ഷഃ സിധ്യതി നാന്യഥാ", "hi": "न योगेन न सांख्येन कर्मणा नो न विद्यया ब्रह्मात्मैकत्वबोधेन मोक्षः सिध्यति नान्यथा", "ta": "ந யோகேந ந ஸாம்க்யேந கர்மணா நோ ந வித்யயா ப்ரஹ்மாத்மைகத்வபோதேந மோக்ஷஃ ஸித்யதி நாந்யதா", "te": "న యోగేన న సాంఖ్యేన కర్మణా నో న విద్యయా బ్రహ్మాత్మైకత్వబోధేన మోక్షః సిధ్యతి నాన్యథా"}},

        # More Vishnu Sahasranama
        {"verse_id": "vs-1-3", "text_id": "vishnu-sahasranama", "text_name": "Vishnu Sahasranama", "chapter": 1, "chapter_name": "Names of Vishnu", "verse_number": 3,
         "text": "achyutah prathitah pranah pranadah vasavanujah apam nidhir adhishthanam apramattah pratishtitah",
         "translation": "He who never falls (Achyuta), who is well-known, who is the life-breath, who gives life-breath, who is the brother of Indra, the ocean, the substratum, the vigilant one, the well-established.",
         "keywords": "Achyuta, never falls, life-breath, ocean, vigilant, established, Vishnu",
         "transliterations": {"ml": "അച്യുതഃ പ്രഥിതഃ പ്രാണഃ പ്രാണദഃ വാസവാനുജഃ", "hi": "अच्युतः प्रथितः प्राणः प्राणदः वासवानुजः", "ta": "அச்யுதஃ ப்ரதிதஃ ப்ராணஃ ப்ராணதஃ வாஸவாநுஜஃ", "te": "అచ్యుతః ప్రథితః ప్రాణః ప్రాణదః వాసవానుజః"},
         "temple_connection": {"temple": "Padmanabhaswamy Temple", "location": "Thiruvananthapuram, Kerala", "detail": "Achyuta is one of the principal names chanted during the daily Vishnu Sahasranama recitation at Padmanabhaswamy. The temple's reclining Vishnu form embodies these qualities."}},

        # More Lalita Sahasranama
        {"verse_id": "ls-1-3", "text_id": "lalita-sahasranama", "text_name": "Lalita Sahasranama", "chapter": 1, "chapter_name": "Names of the Goddess", "verse_number": 3,
         "text": "mano rupekshu kodanda pancha tanmatra sayaka nijanuna prabha pura majjat brahmanda mandala",
         "translation": "She who holds the sugarcane bow of the mind, whose arrows are the five subtle elements, and in the flood of whose beauty all the worlds are immersed.",
         "keywords": "sugarcane bow, mind, five elements, arrows, beauty, worlds, immersed",
         "transliterations": {"ml": "മനോരൂപേക്ഷുകോദണ്ഡാ പഞ്ചതന്മാത്രസായകാ", "hi": "मनोरूपेक्षुकोदण्डा पञ्चतन्मात्रसायका", "ta": "மநோரூபேக்ஷுகோதண்டா பஞ்சதந்மாத்ரஸாயகா"},
         "temple_connection": {"temple": "Kodungallur Bhagavathy Temple", "location": "Thrissur, Kerala", "detail": "One of the most ancient Devi temples in Kerala. Lalita Sahasranama is chanted during the famous Bharani festival."}},

        # More Adhyatma Ramayanam
        {"verse_id": "ar-1-3", "text_id": "adhyatma-ramayanam", "text_name": "Adhyatma Ramayanam", "chapter": 1, "chapter_name": "Bala Kandam", "verse_number": 3,
         "text": "ramanama japam ente jeeva raksha mantra kayum athmavil enikku aarumillatha naalaanu ee lokathil",
         "translation": "The chanting of Rama's name is my life-protecting mantra. In this world where I have no one else in my soul, this alone sustains me.",
         "keywords": "Rama nama, chanting, life, protection, mantra, soul, sustain, Malayalam",
         "transliterations": {"ml": "രാമനാമ ജപം എന്റെ ജീവരക്ഷാ മന്ത്രകായും ആത്മാവിൽ എനിക്ക് ആരുമില്ലാത്ത നാളാണ് ഈ ലോകത്തിൽ", "hi": "रामनाम जपम् एन्ते जीवरक्षा मन्त्रकायुम्"}},

        # More Hanuman Chalisa
        {"verse_id": "hc-1-10", "text_id": "hanuman-chalisa", "text_name": "Hanuman Chalisa", "chapter": 1, "chapter_name": "Hanuman Chalisa", "verse_number": 10,
         "text": "jai jai jai hanuman gosain krupa karahu gurudev ki naain",
         "translation": "Victory, victory, victory to Lord Hanuman! Bestow your grace upon us as our supreme teacher.",
         "keywords": "victory, Hanuman, grace, teacher, guru, blessing",
         "transliterations": {"ml": "ജയ് ജയ് ജയ് ഹനുമാൻ ഗോസാഈൻ കൃപാ കരഹു ഗുരുദേവ് കീ നായിൻ", "hi": "जय जय जय हनुमान गोसाईं कृपा करहु गुरुदेव की नाईं", "ta": "ஜய் ஜய் ஜய் ஹநுமான் கோஸாயீன் க்ருபா கரஹு குருதேவ் கீ நாயீன்"}},

        {"verse_id": "hc-1-11", "text_id": "hanuman-chalisa", "text_name": "Hanuman Chalisa", "chapter": 1, "chapter_name": "Hanuman Chalisa", "verse_number": 11,
         "text": "jo sat baar paath kar koi chhutahi bandi maha sukh hoi",
         "translation": "Whoever recites this a hundred times is released from bondage and attains great bliss.",
         "keywords": "recitation, hundred, bondage, released, bliss, merit",
         "transliterations": {"ml": "ജോ സത് ബാർ പാഠ് കർ കോയീ ഛൂടഹി ബന്ദി മഹാ സുഖ് ഹോയി", "hi": "जो सत बार पाठ कर कोई छूटहि बन्दि महा सुख होई", "ta": "ஜோ ஸத் பார் பாட் கர் கோயீ சூடஹி பந்தி மஹா ஸுக் ஹோயீ"}},

        # More Puranas
        {"verse_id": "bp-3-4", "text_id": "puranas", "text_name": "Puranas", "chapter": 3, "chapter_name": "Bhagavata Purana", "verse_number": 4,
         "text": "yad anudhyasinah yukta karmana anusmara tyo pi hrida purushottamam",
         "translation": "By constantly meditating with a disciplined mind upon the Supreme Being in one's heart, even while performing prescribed duties, one attains perfection.",
         "keywords": "meditation, heart, Supreme Being, duties, perfection, discipline"},

        {"verse_id": "sp-2-3", "text_id": "puranas", "text_name": "Puranas", "chapter": 2, "chapter_name": "Shiva Purana", "verse_number": 3,
         "text": "mahamrityunjaya mantra: tryambakam yajamahe sugandhim pushtivardhanam urvarukamiva bandhanan mrityor mukshiya maamritat",
         "translation": "We worship the three-eyed Lord (Shiva) who nourishes all and increases sweetness. As the cucumber is freed from its bondage to the vine, may we be liberated from death, not from immortality.",
         "keywords": "Mahamrityunjaya, Shiva, three-eyed, liberation, death, immortality, mantra, healing",
         "transliterations": {"ml": "ത്ര്യംബകം യജാമഹേ സുഗന്ധിം പുഷ്ടിവർദ്ധനം ഉർവ്വാരുകമിവ ബന്ധനാൻ മൃത്യോർ മുക്ഷീയ മാമൃതാത്", "hi": "त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम् उर्वारुकमिव बन्धनान्मृत्योर्मुक्षीय मामृतात्", "ta": "த்ர்யம்பகம் யஜாமஹே ஸுகந்திம் புஷ்டிவர்தநம் உர்வாருகமிவ பந்தநான்ம்ருத்யோர்முக்ஷீய மாம்ருதாத்", "te": "త్ర్యంబకం యజామహే సుగన్ధిం పుష్టివర్ధనమ్ ఉర్వారుకమివ బన్ధనాన్మృత్యోర్ముక్షీయ మామృతాత్", "kn": "ತ್ರ್ಯಂಬಕಂ ಯಜಾಮಹೇ ಸುಗಂಧಿಂ ಪುಷ್ಟಿವರ್ಧನಮ್ ಉರ್ವಾರುಕಮಿವ ಬಂಧನಾನ್ಮೃತ್ಯೋರ್ಮುಕ್ಷೀಯ ಮಾಮೃತಾತ್"}},
    ]

"""
Extended Hindu scriptures: Upanishads, Yoga Sutras, Mahabharata, Vedas, Hanuman Chalisa, Vishnu Sahasranama
"""

def get_extended_metadata():
    return [
        {
            "text_id": "upanishads",
            "name": "Upanishads",
            "description": "The philosophical heart of the Vedas. These mystical texts explore the nature of Brahman, Atman, and the ultimate reality through dialogues between teachers and seekers.",
            "total_chapters": 8,
            "language": "Sanskrit",
            "image": "https://images.unsplash.com/photo-1643300788512-64b38ad876c6?w=400"
        },
        {
            "text_id": "yoga-sutras",
            "name": "Yoga Sutras of Patanjali",
            "description": "The foundational text of Raja Yoga, consisting of 196 sutras organized into four chapters. A systematic guide to the science of yoga and meditation.",
            "total_chapters": 4,
            "language": "Sanskrit",
            "image": "https://images.unsplash.com/photo-1488875482628-eee706cbfad5?w=400"
        },
        {
            "text_id": "mahabharata",
            "name": "Mahabharata",
            "description": "The longest epic poem in the world with over 100,000 verses. Beyond the Bhagavad Gita, it contains profound wisdom on dharma, statecraft, philosophy, and human nature.",
            "total_chapters": 5,
            "language": "Sanskrit",
            "image": "https://images.unsplash.com/photo-1617904472808-7e038208077a?w=400"
        },
        {
            "text_id": "vedas",
            "name": "Vedas",
            "description": "The oldest sacred texts of Hinduism, composed between 1500-1200 BCE. The four Vedas - Rig, Yajur, Sama, and Atharva - contain hymns, rituals, and philosophical insights.",
            "total_chapters": 4,
            "language": "Sanskrit",
            "image": "https://images.unsplash.com/photo-1643300788512-64b38ad876c6?w=400"
        },
        {
            "text_id": "hanuman-chalisa",
            "name": "Hanuman Chalisa",
            "description": "A devotional hymn of 40 verses composed by Tulsidas in praise of Lord Hanuman. One of the most recited prayers in Hinduism, celebrating devotion, strength, and courage.",
            "total_chapters": 1,
            "language": "Awadhi",
            "image": "https://images.unsplash.com/photo-1617904472808-7e038208077a?w=400"
        },
        {
            "text_id": "puranas",
            "name": "Puranas",
            "description": "Ancient encyclopedic texts covering cosmology, genealogies, mythology, and dharma. The 18 Mahapuranas include the Vishnu Purana, Shiva Purana, and Bhagavata Purana.",
            "total_chapters": 4,
            "language": "Sanskrit",
            "image": "https://images.unsplash.com/photo-1488875482628-eee706cbfad5?w=400"
        }
    ]


def get_extended_verses():
    verses = []
    verses.extend(_upanishad_verses())
    verses.extend(_yoga_sutra_verses())
    verses.extend(_mahabharata_verses())
    verses.extend(_veda_verses())
    verses.extend(_hanuman_chalisa_verses())
    verses.extend(_purana_verses())
    return verses


def _upanishad_verses():
    return [
        # Isha Upanishad
        {"verse_id": "isha-1", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 1, "chapter_name": "Isha Upanishad", "verse_number": 1, "text": "isavasyam idam sarvam yat kinca jagatyam jagat tena tyaktena bhunjitha ma grdhah kasya svid dhanam", "translation": "All this — whatever exists in this changing universe — should be covered by the Lord. Protect yourself through detachment. Do not covet anybody's wealth.", "keywords": "God, universe, detachment, renunciation, covetousness, Isha"},
        {"verse_id": "isha-2", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 1, "chapter_name": "Isha Upanishad", "verse_number": 2, "text": "kurvann eveha karmani jijivisec chatam samah evam tvayi nanyatheto'sti na karma lipyate nare", "translation": "By performing karma in this world, one should wish to live a hundred years. Thus, and in no other way, can man be free from the taint of karma.", "keywords": "karma, life, action, freedom, hundred years"},
        {"verse_id": "isha-6", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 1, "chapter_name": "Isha Upanishad", "verse_number": 6, "text": "yas tu sarvani bhutany atmany evanupasyati sarva-bhutesu catmanam tato na vijugupsate", "translation": "He who sees all beings in his own Self, and his own Self in all beings, loses all fear and hatred.", "keywords": "self, all beings, unity, fear, hatred, oneness"},

        # Kena Upanishad
        {"verse_id": "kena-1", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 2, "chapter_name": "Kena Upanishad", "verse_number": 1, "text": "keneshitam patati preshitam manah kena pranah prathamah praiti yuktah keneshitam vacam imam vadanti cakshuh shrotram ka u devo yunakti", "translation": "By whom directed does the mind go towards its objects? Commanded by whom does the life-force proceed? At whose will do men utter speech? What power directs the eye and the ear?", "keywords": "mind, life-force, speech, senses, inquiry, Brahman"},
        {"verse_id": "kena-2", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 2, "chapter_name": "Kena Upanishad", "verse_number": 2, "text": "shrotrasya shrotram manaso mano yad vaco ha vacam sa u pranasya pranah caksusas caksur atimucya dhirah pretya asmal lokat amrta bhavanti", "translation": "It is the Ear of the ear, the Mind of the mind, the Speech of speech, the Life of life, the Eye of the eye. Having detached the Self from the senses, the wise become immortal.", "keywords": "ear, mind, speech, senses, immortal, Brahman, detachment"},

        # Katha Upanishad
        {"verse_id": "katha-1", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 3, "chapter_name": "Katha Upanishad", "verse_number": 1, "text": "uttishthata jagrata prapya varan nibodhata ksurasya dhara nisita duratyaya durgam pathas tat kavayo vadanti", "translation": "Arise! Awake! Approach the great masters and learn. The path is sharp as a razor's edge, difficult to traverse — the wise say.", "keywords": "arise, awake, wisdom, razor, path, difficult, master, Nachiketa"},
        {"verse_id": "katha-2", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 3, "chapter_name": "Katha Upanishad", "verse_number": 2, "text": "atmanam rathinam viddhi shariram ratham eva tu buddhim tu sarathim viddhi manah pragraham eva ca", "translation": "Know the Self as the lord of the chariot, the body as the chariot. Know the intellect as the charioteer, and the mind as the reins.", "keywords": "self, chariot, body, intellect, mind, metaphor, Yama, soul"},
        {"verse_id": "katha-3", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 3, "chapter_name": "Katha Upanishad", "verse_number": 3, "text": "na jayate mriyate va vipascin nayam kutascin na babhuva kascit ajo nityah sasvato yam purano na hanyate hanyamane sarire", "translation": "The wise Self is not born, nor does it die. It did not spring from anything, nor did anything spring from it. Unborn, eternal, everlasting, ancient — it is not slain when the body is slain.", "keywords": "self, eternal, unborn, death, immortal, soul, ancient"},

        # Mundaka Upanishad
        {"verse_id": "mundaka-1", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 4, "chapter_name": "Mundaka Upanishad", "verse_number": 1, "text": "dve vidye veditavye iti ha sma yad brahmavido vadanti para caivapara ca", "translation": "Two kinds of knowledge must be known — this is what the knowers of Brahman say — the higher and the lower.", "keywords": "knowledge, higher, lower, Brahman, wisdom, vidya"},
        {"verse_id": "mundaka-2", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 4, "chapter_name": "Mundaka Upanishad", "verse_number": 2, "text": "satyameva jayate nanrtam satyena pantha vitato devayanah yenakramanty rsayo hy aptakama yatra tat satyasya paramam nidhanam", "translation": "Truth alone triumphs, not falsehood. Through truth the divine path is spread out by which the sages whose desires have been completely fulfilled reach where that supreme treasure of Truth resides.", "keywords": "truth, triumphs, divine path, sages, supreme treasure, satya"},

        # Mandukya Upanishad
        {"verse_id": "mandukya-1", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 5, "chapter_name": "Mandukya Upanishad", "verse_number": 1, "text": "om ity etad aksharam idam sarvam tasyopavyakhyanam bhutam bhavad bhavishyad iti sarvam aumkara eva", "translation": "Om — this syllable is all this. All that is past, present, and future is truly Om. And whatever transcends the three periods of time, that too is truly Om.", "keywords": "Om, syllable, past, present, future, Aum, Brahman, transcendence"},

        # Chandogya Upanishad
        {"verse_id": "chando-1", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 6, "chapter_name": "Chandogya Upanishad", "verse_number": 1, "text": "tat tvam asi shvetaketo", "translation": "That thou art, O Shvetaketu. You are that ultimate reality, that Brahman.", "keywords": "tat tvam asi, you are that, Brahman, identity, self-realization, Shvetaketu, mahavakya"},
        {"verse_id": "chando-2", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 6, "chapter_name": "Chandogya Upanishad", "verse_number": 2, "text": "sarvam khalvidam brahma tajjalan iti santa upasita", "translation": "All this is indeed Brahman. From Brahman everything is born, into Brahman everything dissolves, and by Brahman everything is sustained.", "keywords": "Brahman, everything, creation, dissolution, sustenance, universe"},

        # Brihadaranyaka Upanishad
        {"verse_id": "brihad-1", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 7, "chapter_name": "Brihadaranyaka Upanishad", "verse_number": 1, "text": "asato ma sadgamaya tamaso ma jyotirgamaya mrtyorma amrtam gamaya", "translation": "Lead me from the unreal to the real, lead me from darkness to light, lead me from death to immortality.", "keywords": "lead me, unreal, real, darkness, light, death, immortality, prayer, Pavamana Mantra"},
        {"verse_id": "brihad-2", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 7, "chapter_name": "Brihadaranyaka Upanishad", "verse_number": 2, "text": "aham brahmasmi", "translation": "I am Brahman. The individual self and the universal Self are one.", "keywords": "aham brahmasmi, I am Brahman, mahavakya, self-realization, identity, oneness"},
        {"verse_id": "brihad-3", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 7, "chapter_name": "Brihadaranyaka Upanishad", "verse_number": 3, "text": "na va are patyuh kamaya patih priyo bhavaty atmanas tu kamaya patih priyo bhavati", "translation": "It is not for the sake of the husband that the husband is dear, but for the sake of the Self. It is not for the sake of anything else, but for the sake of the Self that everything is dear.", "keywords": "self, love, dear, Yajnavalkya, Maitreyi, atman"},

        # Taittiriya Upanishad
        {"verse_id": "taitt-1", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 8, "chapter_name": "Taittiriya Upanishad", "verse_number": 1, "text": "satyam vada dharmam cara svadhyayan ma pramadah acarya priyam dhanam ahrtya prajatantum ma vyavacchetsih", "translation": "Speak the truth. Practice dharma. Do not neglect study. Having brought the teacher's fee, do not cut off the line of progeny.", "keywords": "truth, dharma, study, teacher, duty, convocation"},
        {"verse_id": "taitt-2", "text_id": "upanishads", "text_name": "Upanishads", "chapter": 8, "chapter_name": "Taittiriya Upanishad", "verse_number": 2, "text": "anando brahmeti vyajanat anandadhyeva khalvimani bhutani jayante anandena jatani jivanti anandam prayanty abhisamvisanti", "translation": "He knew that Brahman is bliss. From bliss all beings are born, by bliss they are sustained, and into bliss they return and merge.", "keywords": "bliss, Brahman, ananda, born, sustained, merge, joy"},
    ]


def _yoga_sutra_verses():
    return [
        # Samadhi Pada
        {"verse_id": "ys-1-1", "text_id": "yoga-sutras", "text_name": "Yoga Sutras", "chapter": 1, "chapter_name": "Samadhi Pada", "verse_number": 1, "text": "atha yoganushasanam", "translation": "Now begins the exposition of yoga.", "keywords": "yoga, beginning, discipline, exposition"},
        {"verse_id": "ys-1-2", "text_id": "yoga-sutras", "text_name": "Yoga Sutras", "chapter": 1, "chapter_name": "Samadhi Pada", "verse_number": 2, "text": "yogash chitta vrtti nirodhah", "translation": "Yoga is the cessation of the fluctuations of the mind.", "keywords": "yoga, mind, cessation, fluctuations, chitta, vritti, definition"},
        {"verse_id": "ys-1-3", "text_id": "yoga-sutras", "text_name": "Yoga Sutras", "chapter": 1, "chapter_name": "Samadhi Pada", "verse_number": 3, "text": "tada drashtuh svarupe avasthanam", "translation": "Then the Seer abides in its own true nature.", "keywords": "seer, true nature, self, witness, consciousness"},
        {"verse_id": "ys-1-12", "text_id": "yoga-sutras", "text_name": "Yoga Sutras", "chapter": 1, "chapter_name": "Samadhi Pada", "verse_number": 12, "text": "abhyasa vairagyabhyam tannirodhah", "translation": "The cessation of mental fluctuations is brought about by persistent practice and non-attachment.", "keywords": "practice, non-attachment, vairagya, abhyasa, cessation, discipline"},
        {"verse_id": "ys-1-33", "text_id": "yoga-sutras", "text_name": "Yoga Sutras", "chapter": 1, "chapter_name": "Samadhi Pada", "verse_number": 33, "text": "maitri karuna mudita upekshanam sukha duhkha punya apunya vishayanam bhavanatah chitta prasadanam", "translation": "By cultivating attitudes of friendliness toward the happy, compassion for the unhappy, delight in the virtuous, and equanimity toward the non-virtuous, the mind retains its undisturbed calmness.", "keywords": "friendliness, compassion, delight, equanimity, calmness, mind, virtue"},

        # Sadhana Pada
        {"verse_id": "ys-2-1", "text_id": "yoga-sutras", "text_name": "Yoga Sutras", "chapter": 2, "chapter_name": "Sadhana Pada", "verse_number": 1, "text": "tapah svadhyaya ishvarapranidhanani kriya yogah", "translation": "Austerity, self-study, and surrender to God constitute the yoga of action (Kriya Yoga).", "keywords": "austerity, self-study, surrender, God, kriya yoga, tapas"},
        {"verse_id": "ys-2-3", "text_id": "yoga-sutras", "text_name": "Yoga Sutras", "chapter": 2, "chapter_name": "Sadhana Pada", "verse_number": 3, "text": "avidya asmita raga dvesha abhiniveshaha pancha kleshah", "translation": "Ignorance, egoism, attachment, aversion, and clinging to life are the five afflictions.", "keywords": "ignorance, ego, attachment, aversion, fear, klesha, afflictions"},
        {"verse_id": "ys-2-29", "text_id": "yoga-sutras", "text_name": "Yoga Sutras", "chapter": 2, "chapter_name": "Sadhana Pada", "verse_number": 29, "text": "yama niyama asana pranayama pratyahara dharana dhyana samadhayo ashtau angani", "translation": "The eight limbs of yoga are: restraints, observances, posture, breath control, sense withdrawal, concentration, meditation, and absorption.", "keywords": "eight limbs, ashtanga, yama, niyama, asana, pranayama, meditation, samadhi"},
        {"verse_id": "ys-2-46", "text_id": "yoga-sutras", "text_name": "Yoga Sutras", "chapter": 2, "chapter_name": "Sadhana Pada", "verse_number": 46, "text": "sthira sukham asanam", "translation": "Posture should be steady and comfortable.", "keywords": "posture, steady, comfortable, asana, stability"},

        # Vibhuti Pada
        {"verse_id": "ys-3-1", "text_id": "yoga-sutras", "text_name": "Yoga Sutras", "chapter": 3, "chapter_name": "Vibhuti Pada", "verse_number": 1, "text": "desha bandhah chittasya dharana", "translation": "Concentration is fixing the mind on a single point or region.", "keywords": "concentration, mind, focus, dharana, single point"},
        {"verse_id": "ys-3-2", "text_id": "yoga-sutras", "text_name": "Yoga Sutras", "chapter": 3, "chapter_name": "Vibhuti Pada", "verse_number": 2, "text": "tatra pratyaya ekatanata dhyanam", "translation": "Meditation is the continuous flow of awareness toward that point.", "keywords": "meditation, continuous, flow, awareness, dhyana"},

        # Kaivalya Pada
        {"verse_id": "ys-4-34", "text_id": "yoga-sutras", "text_name": "Yoga Sutras", "chapter": 4, "chapter_name": "Kaivalya Pada", "verse_number": 34, "text": "purusha artha shunyanam gunanam pratiprasavah kaivalyam svarupa pratishtha va chiti shaktir iti", "translation": "Liberation (Kaivalya) is the state when the gunas cease serving the purpose of the Self. The power of pure consciousness becomes established in its own nature.", "keywords": "liberation, kaivalya, gunas, consciousness, freedom, self"},
    ]


def _mahabharata_verses():
    return [
        # Shanti Parva (Book of Peace)
        {"verse_id": "mb-1-1", "text_id": "mahabharata", "text_name": "Mahabharata", "chapter": 1, "chapter_name": "Shanti Parva", "verse_number": 1, "text": "ahimsa paramo dharmah dharma himsa tathaiva cha", "translation": "Non-violence is the highest dharma, and so too is all justified violence in service of dharma.", "keywords": "ahimsa, non-violence, dharma, violence, highest law"},
        {"verse_id": "mb-1-2", "text_id": "mahabharata", "text_name": "Mahabharata", "chapter": 1, "chapter_name": "Shanti Parva", "verse_number": 2, "text": "na hi satyat paro dharmah", "translation": "There is no dharma higher than truth.", "keywords": "truth, dharma, highest, satya"},
        {"verse_id": "mb-1-3", "text_id": "mahabharata", "text_name": "Mahabharata", "chapter": 1, "chapter_name": "Shanti Parva", "verse_number": 3, "text": "dharma eva hato hanti dharmo rakshati rakshitah tasmat dharmo na hantavyah ma no dharmo hato vadhit", "translation": "Dharma destroys those who destroy it. Dharma protects those who protect it. Therefore dharma should not be destroyed, lest destroyed dharma destroy us.", "keywords": "dharma, protection, destruction, law, righteousness"},
        {"verse_id": "mb-1-4", "text_id": "mahabharata", "text_name": "Mahabharata", "chapter": 1, "chapter_name": "Shanti Parva", "verse_number": 4, "text": "yatha sarvasya bhuutasya pitaa maata ca madhavah tatha tisthema bhutanam hitam carantah", "translation": "As Madhava is the father and mother of all beings, so should we conduct ourselves for the welfare of all creatures.", "keywords": "welfare, all beings, compassion, duty, Madhava"},
        {"verse_id": "mb-1-5", "text_id": "mahabharata", "text_name": "Mahabharata", "chapter": 1, "chapter_name": "Shanti Parva", "verse_number": 5, "text": "shreyah svadharmo vigunah paradharmat svanushthitat sva dharme nidhanam shreyah paradharmo bhayavahah", "translation": "Better is one's own dharma, though imperfect, than the dharma of another well discharged. Better is death in one's own dharma; the dharma of another brings danger.", "keywords": "svadharma, own duty, another's duty, danger, death, better"},

        # Vidura Niti
        {"verse_id": "mb-2-1", "text_id": "mahabharata", "text_name": "Mahabharata", "chapter": 2, "chapter_name": "Vidura Niti", "verse_number": 1, "text": "vidura uvaca atmanam prthivim patnim putran bandhums tathaa suhrt shad etan samyag avekseta na pramatted dhanaanvitah", "translation": "Vidura said: A wise man should carefully attend to six things: his own self, his country, his wife, his children, his relatives, and his friends. He should never be negligent about wealth.", "keywords": "wisdom, Vidura, six things, self, family, wealth, negligence"},
        {"verse_id": "mb-2-2", "text_id": "mahabharata", "text_name": "Mahabharata", "chapter": 2, "chapter_name": "Vidura Niti", "verse_number": 2, "text": "panca panchabhir utthaya bhutva sthira shayanam cha shama dama ahimsa satya arjavam dharma lakshanam", "translation": "Tranquility, self-control, non-violence, truthfulness, and simplicity — these are the marks of dharma.", "keywords": "tranquility, self-control, non-violence, truth, simplicity, dharma, marks"},
        {"verse_id": "mb-2-3", "text_id": "mahabharata", "text_name": "Mahabharata", "chapter": 2, "chapter_name": "Vidura Niti", "verse_number": 3, "text": "krodhah pranashanam dattam mano bhedo ripo jayah aashvasah sarva satveshu daanam ishtam dvija archana", "translation": "Anger leads to ruin, a composed mind conquers enemies. Compassion to all beings, generosity, and reverence for the learned — these are the highest virtues.", "keywords": "anger, ruin, mind, enemies, compassion, generosity, virtues"},

        # Anushasana Parva
        {"verse_id": "mb-3-1", "text_id": "mahabharata", "text_name": "Mahabharata", "chapter": 3, "chapter_name": "Anushasana Parva", "verse_number": 1, "text": "sarve bhavantu sukhinah sarve santu niramayah sarve bhadrani pashyantu ma kashcit duhkha bhag bhavet", "translation": "May all be happy, may all be free from illness. May all see what is auspicious, may no one suffer.", "keywords": "happiness, health, auspicious, suffering, universal prayer, blessing"},
        {"verse_id": "mb-3-2", "text_id": "mahabharata", "text_name": "Mahabharata", "chapter": 3, "chapter_name": "Anushasana Parva", "verse_number": 2, "text": "shruuyataam dharma sarvasvam shrutvaa caiva anuvartate aatmanah pratikuulaani pareshaam na samacharet", "translation": "Listen to the essence of dharma and having listened, follow it: Do not do unto others what you would not have them do unto you.", "keywords": "golden rule, dharma, essence, others, reciprocity, ethics"},

        # Vana Parva
        {"verse_id": "mb-4-1", "text_id": "mahabharata", "text_name": "Mahabharata", "chapter": 4, "chapter_name": "Vana Parva", "verse_number": 1, "text": "sukhasya muulam dharmo dharmasyaiva krpa mulam krpayaash cha gurum sevaa tato daivam prasidati", "translation": "The root of happiness is dharma, the root of dharma is compassion, the root of compassion is service to the guru; thereby the divine is pleased.", "keywords": "happiness, dharma, compassion, guru, service, divine, root"},
        {"verse_id": "mb-4-2", "text_id": "mahabharata", "text_name": "Mahabharata", "chapter": 4, "chapter_name": "Vana Parva", "verse_number": 2, "text": "vinasho naasti daivena na cha bhagyena cha kvachit karmanaam phala samyogaat praarabdham phalam aapnuyaat", "translation": "Destruction comes not by fate alone, nor by destiny. Through the connection of one's own actions, one obtains the results of what was begun.", "keywords": "fate, destiny, actions, results, karma, self-determination"},

        # Udyoga Parva
        {"verse_id": "mb-5-1", "text_id": "mahabharata", "text_name": "Mahabharata", "chapter": 5, "chapter_name": "Udyoga Parva", "verse_number": 1, "text": "yatra yogeshvarah krishno yatra partho dhanurdharah tatra shrir vijayo bhutir dhruva nitir matir mama", "translation": "Where there is Krishna, the Lord of Yoga, and where there is Arjuna, the wielder of the bow — there will be fortune, victory, prosperity, and firm righteousness.", "keywords": "Krishna, Arjuna, victory, fortune, prosperity, righteousness"},
        {"verse_id": "mb-5-2", "text_id": "mahabharata", "text_name": "Mahabharata", "chapter": 5, "chapter_name": "Udyoga Parva", "verse_number": 2, "text": "kale kale hi dharmasya pravrttih cha pravartate kalah sarvesham bhutanam pravrttim cha nivarttanam", "translation": "From age to age, dharma manifests and evolves. Time governs the rise and fall of all beings.", "keywords": "time, dharma, age, evolution, rise, fall, beings"},
    ]


def _veda_verses():
    return [
        # Rig Veda
        {"verse_id": "rv-1-1", "text_id": "vedas", "text_name": "Vedas", "chapter": 1, "chapter_name": "Rig Veda", "verse_number": 1, "text": "agnim ile purohitam yajnasya devam ritvijam hotaram ratnadhatamam", "translation": "I praise Agni, the chosen Priest, God, minister of sacrifice, the hotar, lavishest of wealth.", "keywords": "Agni, fire, praise, sacrifice, priest, wealth, Rig Veda, first hymn"},
        {"verse_id": "rv-1-2", "text_id": "vedas", "text_name": "Vedas", "chapter": 1, "chapter_name": "Rig Veda", "verse_number": 2, "text": "ekam sad vipra bahudha vadanty agnim yamam matarishvanam ahuh", "translation": "Truth is One; the wise call it by many names — they call it Agni, Yama, Matarishvan.", "keywords": "truth, one, many names, Agni, Yama, unity, diversity, ekam sat"},
        {"verse_id": "rv-1-3", "text_id": "vedas", "text_name": "Vedas", "chapter": 1, "chapter_name": "Rig Veda", "verse_number": 3, "text": "nasadiya sukta: nasad asin no sad asit tadanim nasid rajo no vyoma paro yat", "translation": "Then there was neither existence nor non-existence; there was no atmosphere, no sky beyond. What covered it? Where was it? In whose protection?", "keywords": "creation, hymn, existence, non-existence, Nasadiya Sukta, origin, cosmos"},
        {"verse_id": "rv-1-4", "text_id": "vedas", "text_name": "Vedas", "chapter": 1, "chapter_name": "Rig Veda", "verse_number": 4, "text": "om purnamadah purnamidam purnat purnamudachyate purnasya purnamadaya purnamevavashishyate", "translation": "That is whole, this is whole. From the whole, the whole arises. Taking the whole from the whole, only the whole remains.", "keywords": "whole, completeness, infinite, purna, Brahman, fullness, Shanti mantra"},
        {"verse_id": "rv-1-5", "text_id": "vedas", "text_name": "Vedas", "chapter": 1, "chapter_name": "Rig Veda", "verse_number": 5, "text": "gayatri mantra: tat savitur varenyam bhargo devasya dhimahi dhiyo yo nah prachodayat", "translation": "We meditate on the divine light of the radiant Sun. May it inspire our understanding and illuminate our intellect.", "keywords": "Gayatri mantra, Sun, meditation, light, intellect, prayer, Savitri"},

        # Yajur Veda
        {"verse_id": "yv-2-1", "text_id": "vedas", "text_name": "Vedas", "chapter": 2, "chapter_name": "Yajur Veda", "verse_number": 1, "text": "om sahana vavatu sahanau bhunaktu saha viryam karavavahai tejasvi navadhitamastu ma vidvishavahai", "translation": "May we be protected together, may we be nourished together. May we work together with great energy. May our studies be brilliant. May we never quarrel.", "keywords": "protection, nourishment, energy, study, peace, Shanti mantra, teacher, student"},
        {"verse_id": "yv-2-2", "text_id": "vedas", "text_name": "Vedas", "chapter": 2, "chapter_name": "Yajur Veda", "verse_number": 2, "text": "om bhadram karnebhih shrunuyaama devaa bhadram pashyema akshabhir yajatraah sthirair angais tushtuvaamsas tanuubhih vyashema devahitam yad aayuh", "translation": "O Gods, may we hear with our ears what is auspicious. May we see what is auspicious. May we enjoy the life allotted by the gods with strong and healthy bodies.", "keywords": "ears, eyes, auspicious, health, body, life, gods, blessing"},

        # Sama Veda
        {"verse_id": "sv-3-1", "text_id": "vedas", "text_name": "Vedas", "chapter": 3, "chapter_name": "Sama Veda", "verse_number": 1, "text": "agna a yahi vitaye grnano havya dhataye ni hota satsi barhishi", "translation": "O Agni, come to the feast, praised one, to the offering. Sit as the priest upon the sacred grass.", "keywords": "Agni, fire, feast, priest, offering, sacred, Sama Veda"},

        # Atharva Veda
        {"verse_id": "av-4-1", "text_id": "vedas", "text_name": "Vedas", "chapter": 4, "chapter_name": "Atharva Veda", "verse_number": 1, "text": "prthivim shantam dyo shantam shantam idam urv antariksham shantah samudroh salilam shantam nah santvoshadhayah", "translation": "May the earth be peaceful, may the sky be peaceful. May the vast space between be peaceful. May the waters be peaceful, and may the herbs be peaceful for us.", "keywords": "peace, earth, sky, waters, herbs, prayer, Shanti, nature"},
        {"verse_id": "av-4-2", "text_id": "vedas", "text_name": "Vedas", "chapter": 4, "chapter_name": "Atharva Veda", "verse_number": 2, "text": "mata bhumih putro aham prthivyah parjanyah pita sa u nah pipartu", "translation": "Earth is my mother, I am her son. Parjanya (the rain god) is my father — may he nourish us.", "keywords": "earth, mother, son, rain, father, nourish, nature, Prithvi"},
    ]


def _hanuman_chalisa_verses():
    return [
        {"verse_id": "hc-1-1", "text_id": "hanuman-chalisa", "text_name": "Hanuman Chalisa", "chapter": 1, "chapter_name": "Hanuman Chalisa", "verse_number": 1, "text": "shri guru charan saroj raj nij manu mukuru sudhari baranaun raghubar bimal jasu jo dayaku phal chari", "translation": "Cleansing the mirror of my mind with the pollen-dust of the lotus feet of the Guru, I describe the untarnished glory of Rama, which bestows the four fruits of life.", "keywords": "guru, Rama, glory, four fruits, cleansing, mind, Tulsidas"},
        {"verse_id": "hc-1-2", "text_id": "hanuman-chalisa", "text_name": "Hanuman Chalisa", "chapter": 1, "chapter_name": "Hanuman Chalisa", "verse_number": 2, "text": "buddhihina tanu jaanike sumiraun pavan kumar bal buddhi vidya dehu mohi harahu kalesa vikaar", "translation": "Knowing myself to be ignorant, I pray to you, O Hanuman, son of the Wind God: Grant me strength, wisdom and knowledge, and remove my afflictions and impurities.", "keywords": "Hanuman, wisdom, strength, knowledge, prayer, afflictions, Pavan Kumar"},
        {"verse_id": "hc-1-3", "text_id": "hanuman-chalisa", "text_name": "Hanuman Chalisa", "chapter": 1, "chapter_name": "Hanuman Chalisa", "verse_number": 3, "text": "jai hanuman gyan gun sagar jai kapis tihun lok ujagar", "translation": "Victory to Hanuman, the ocean of wisdom and virtue. Victory to the Lord of monkeys, illuminator of the three worlds.", "keywords": "Hanuman, victory, wisdom, virtue, ocean, three worlds, illuminator"},
        {"verse_id": "hc-1-4", "text_id": "hanuman-chalisa", "text_name": "Hanuman Chalisa", "chapter": 1, "chapter_name": "Hanuman Chalisa", "verse_number": 4, "text": "ram doot atulit bal dhama anjani putra pavan sut nama", "translation": "You are the messenger of Rama, the abode of matchless strength, the son of Anjani and the Wind God.", "keywords": "Hanuman, Rama, messenger, strength, Anjani, Wind God, Vayu"},
        {"verse_id": "hc-1-5", "text_id": "hanuman-chalisa", "text_name": "Hanuman Chalisa", "chapter": 1, "chapter_name": "Hanuman Chalisa", "verse_number": 5, "text": "mahabir bikram bajrangi kumati nivar sumati ke sangi", "translation": "O great hero, valiant and strong as a thunderbolt, you dispel evil intellect and are the companion of those with good sense.", "keywords": "hero, valiant, thunderbolt, evil, intellect, companion, wisdom"},
        {"verse_id": "hc-1-6", "text_id": "hanuman-chalisa", "text_name": "Hanuman Chalisa", "chapter": 1, "chapter_name": "Hanuman Chalisa", "verse_number": 6, "text": "kanchan baran biraj subesa kanan kundal kunchit kesa", "translation": "Your golden-hued body is resplendent, wearing beautiful garments, with earrings and curly hair.", "keywords": "golden, body, resplendent, beautiful, Hanuman, description"},
        {"verse_id": "hc-1-7", "text_id": "hanuman-chalisa", "text_name": "Hanuman Chalisa", "chapter": 1, "chapter_name": "Hanuman Chalisa", "verse_number": 7, "text": "bhima roop dhari asur samhare ramachandra ke kaaj sanvare", "translation": "Assuming a fearsome form, you destroyed the demons and accomplished all the tasks of Lord Rama.", "keywords": "fearsome, demons, destruction, Rama, tasks, accomplished"},
        {"verse_id": "hc-1-8", "text_id": "hanuman-chalisa", "text_name": "Hanuman Chalisa", "chapter": 1, "chapter_name": "Hanuman Chalisa", "verse_number": 8, "text": "sankat kate mite sab pira jo sumirai hanuman balbira", "translation": "All difficulties are removed and all pain ends for those who remember the mighty Hanuman.", "keywords": "difficulties, pain, remember, Hanuman, mighty, protection"},
        {"verse_id": "hc-1-9", "text_id": "hanuman-chalisa", "text_name": "Hanuman Chalisa", "chapter": 1, "chapter_name": "Hanuman Chalisa", "verse_number": 9, "text": "pavan tanay sankat haran mangal murati roop ram laxman sita sahit hriday basahu sur bhoop", "translation": "O son of the Wind, remover of calamities, embodiment of auspiciousness — together with Rama, Lakshmana, and Sita, dwell forever in my heart, O king of gods.", "keywords": "Hanuman, Wind, calamity, auspicious, Rama, Sita, Lakshmana, heart, blessing"},
    ]


def _purana_verses():
    return [
        # Vishnu Purana
        {"verse_id": "vp-1-1", "text_id": "puranas", "text_name": "Puranas", "chapter": 1, "chapter_name": "Vishnu Purana", "verse_number": 1, "text": "sarvam vishnumayam jagat", "translation": "The entire universe is pervaded by Vishnu.", "keywords": "Vishnu, universe, pervaded, all-encompassing, divine"},
        {"verse_id": "vp-1-2", "text_id": "puranas", "text_name": "Puranas", "chapter": 1, "chapter_name": "Vishnu Purana", "verse_number": 2, "text": "janma karma ca me divyam evam yo vetti tattvatah tyaktva deham punar janma naiti mam eti so arjuna", "translation": "One who truly understands My divine birth and activities, upon leaving the body, is not born again but comes to Me, O Arjuna.", "keywords": "divine birth, liberation, rebirth, Vishnu, knowledge, moksha"},
        {"verse_id": "vp-1-3", "text_id": "puranas", "text_name": "Puranas", "chapter": 1, "chapter_name": "Vishnu Purana", "verse_number": 3, "text": "yasya prasaadad bhagavat prasaado yasya aprasaadaan na gatih kuto api dhyaayan stuvams tasya yashas trisandhyam", "translation": "By whose grace one attains divine grace, without whose grace there is no progress — one should meditate on and praise his glory at the three junctions of the day.", "keywords": "grace, divine, guru, meditation, praise, progress"},

        # Shiva Purana
        {"verse_id": "sp-2-1", "text_id": "puranas", "text_name": "Puranas", "chapter": 2, "chapter_name": "Shiva Purana", "verse_number": 1, "text": "om namah shivaya shantaya karanah traya hetave nivedayami chatmanam tvam gatih parameshvara", "translation": "Om, salutations to Shiva, the peaceful one, the cause of the three worlds. I surrender myself to you. You are the supreme refuge, O Lord.", "keywords": "Shiva, salutation, peaceful, three worlds, surrender, refuge, Om Namah Shivaya"},
        {"verse_id": "sp-2-2", "text_id": "puranas", "text_name": "Puranas", "chapter": 2, "chapter_name": "Shiva Purana", "verse_number": 2, "text": "karpur gauram karunavataram sansara saram bhujagendra haaram sada vasantam hridayaravinde bhavam bhavani sahitam namami", "translation": "I bow to Lord Shiva, who is white as camphor, the incarnation of compassion, the essence of the world, who wears the king of serpents as a garland, and who always dwells in the lotus of the heart along with Goddess Bhavani.", "keywords": "Shiva, camphor, compassion, serpent, heart, Bhavani, prayer"},

        # Bhagavata Purana
        {"verse_id": "bp-3-1", "text_id": "puranas", "text_name": "Puranas", "chapter": 3, "chapter_name": "Bhagavata Purana", "verse_number": 1, "text": "janmady asya yatah anvayad itaratas ca arthesv abhijnah svarat tene brahma hrda ya adi kavaye", "translation": "I meditate upon Him from whom this universe originates, by whom it is sustained, and in whom it is dissolved — He who is the omniscient, self-luminous being who revealed the Vedas to the first poet.", "keywords": "Brahman, universe, origin, sustenance, dissolution, omniscient, Vedas"},
        {"verse_id": "bp-3-2", "text_id": "puranas", "text_name": "Puranas", "chapter": 3, "chapter_name": "Bhagavata Purana", "verse_number": 2, "text": "vasudevah sarvam iti sa mahatma sudurlabhah", "translation": "One who knows that Vasudeva (Krishna) is everything — such a great soul is very rare to find.", "keywords": "Vasudeva, Krishna, everything, great soul, rare, devotion"},
        {"verse_id": "bp-3-3", "text_id": "puranas", "text_name": "Puranas", "chapter": 3, "chapter_name": "Bhagavata Purana", "verse_number": 3, "text": "kaler dosha nidhe rajann asti hy eko mahan gunah kirtanad eva krishnasya mukta sangah param vrajet", "translation": "O King, in this age of Kali, which is an ocean of faults, there is one great quality: simply by chanting the names of Krishna, one can become free from all bondage and attain the supreme goal.", "keywords": "Kali Yuga, chanting, Krishna, liberation, nama, bondage, supreme goal"},

        # Garuda Purana
        {"verse_id": "gp-4-1", "text_id": "puranas", "text_name": "Puranas", "chapter": 4, "chapter_name": "Garuda Purana", "verse_number": 1, "text": "na hi deha bhrto shakyam tyaktum karmany asheshatah yas tu karma phala tyagi sa tyagi ity abhidhiyate", "translation": "It is not possible for an embodied being to abandon all actions entirely. But one who renounces the fruits of action is truly said to be a renunciant.", "keywords": "renunciation, action, fruits, embodied, tyagi, karma"},
        {"verse_id": "gp-4-2", "text_id": "puranas", "text_name": "Puranas", "chapter": 4, "chapter_name": "Garuda Purana", "verse_number": 2, "text": "shariram aadyam khalu dharma saadhanam", "translation": "The body is indeed the primary instrument for the practice of dharma.", "keywords": "body, dharma, instrument, health, practice"},
    ]

from list_utils import find

LANGUAGE_PAIRS_TUPLE = (
    ("angle", "угол, поворачивать"),
    ("ant", "муравей"),
    ("apple", "яблоко"),
    ("arch", "арка, дуга, выгибать"),
    ("arm", "рука, вооружать"),
    ("army", "армия"),
    ("bag", "сумка"),
    ("ball", "мяч"),
    ("bank", "банк"),
    ("basin", "бассейн"),
    ("basket", "корзина"),
    ("bath", "ванна, купаться"),
    ("bed", "кровать"),
    ("bee", "пчела"),
    ("bell", "колокольчик"),
    ("berry", "ягода"),
    ("bird", "птица"),
    ("blade", "лезвие"),
    ("board", "доска"),
    ("boat", "лодка, судно"),
    ("bone", "кость"),
    ("book", "книга"),
    ("boot", "ботинок, загружать"),
    ("bottle", "бутылка"),
    ("box", "коробка"),
    ("boy", "мальчик"),
    ("brain", "мозг"),
    ("brake", "тормоз, тормозить"),
    ("branch", "ветвь, отделение"),
    ("brick", "кирпич"),
    ("bridge", "мост"),
    ("brush", "щётка, кисть"),
    ("bucket", "ведро, черпать"),
    ("bulb", "луковица, выпирать"),
    ("button", "кнопка, застёгивать"),
    ("baby", "ребёнок, младенец"),
    ("cake", "пирог"),
    ("camera", "камера"),
    ("card", "карта, чесать"),
    ("cart", "везти"),
    ("carriage", "вагон"),
    ("cat", "кот"),
    ("chain", "цепь, сеть"),
    ("cheese", "сыр"),
    ("chest", "грудь, сундук"),
    ("chin", "подбородок"),
    ("church", "церковь"),
    ("circle", "круг"),
    ("clock", "часы"),
    ("cloud", "облако"),
    ("coat", "пальто, покрывать"),
    ("collar", "воротник, хватать"),
    ("comb", "расчёсывать"),
    ("cord", "шнур, связывать"),
    ("cow", "корова"),
    ("cup", "чашка"),
    ("curtain", "занавес, штора, занавешивать"),
    ("cushion", "подушка, смягчать"),
    ("dog", "собака"),
    ("door", "дверь"),
    ("drain", "утечка, истощать"),
    ("drawer", "ящик"),
    ("dress", "платье, одевать"),
    ("drop", "капля, опускать"),
    ("ear", "ухо"),
    ("egg", "яйцо"),
    ("engine", "двигатель"),
    ("eye", "глаз"),
    ("face", "лицо"),
    ("farm", "ферма"),
    ("feather", "перо, украшать"),
    ("finger", "палец"),
    ("fish", "рыба"),
    ("flag", "флаг, сигнализировать"),
    ("floor", "пол, этаж, дно"),
    ("fly", "муха, лететь"),
    ("foot", "нога"),
    ("fork", "вилка"),
    ("fowl", "домашняя птица"),
    ("frame", "структура, рамка, создавать"),
    ("garden", "сад"),
    ("girl", "девочка"),
    ("glove", "перчатка"),
    ("goat", "коза"),
    ("gun", "оружие"),
    ("hair", "волосы"),
    ("hammer", "молоток"),
    ("hand", "рука"),
    ("hat", "шляпа"),
    ("head", "голова"),
    ("heart", "сердце"),
    ("hook", "крюк, вербовать"),
    ("horn", "рожок"),
    ("horse", "лошадь"),
    ("hospital", "больница"),
    ("house", "дом"),
    ("island", "остров"),
    ("jewel", "драгоценный камень"),
    ("kettle", "чайник"),
    ("key", "ключ"),
    ("knee", "колено"),
    ("knife", "нож"),
    ("knot", "узел"),
    ("leaf", "лист, покрывать листвой"),
    ("leg", "нога"),
    ("library", "библиотека"),
    ("line", "линия, очередь, выравнивать"),
    ("lip", "губа"),
    ("lock", "замок"),
    ("map", "карта"),
    ("match", "спичка, сделки, соответствовать"),
    ("monkey", "обезьяна"),
    ("moon", "луна"),
    ("mouth", "рот, жевать"),
    ("muscle", "мускул"),
    ("nail", "ноготь"),
    ("neck", "шея, обниматься"),
    ("needle", "игла"),
    ("nerve", "нерв"),
    ("net", "чистый, сеть"),
    ("nose", "нос"),
    ("nut", "орех"),
    ("office", "офис"),
    ("orange", "апельсин, оранжевый"),
    ("oven", "духовка, печь"),
    ("parcel", "пакет, распределять"),
    ("pen", "ручка"),
    ("pencil", "карандаш"),
    ("picture", "картина"),
    ("pig", "свинья"),
    ("pin", "булавка, прикреплять"),
    ("pipe", "труба"),
    ("plane", "самолёт"),
    ("plate", "пластина"),
    ("plow", "плуг, пахать"),
    ("pocket", "карман, присваивать"),
    ("pot", "горшок"),
    ("potato", "картофель"),
    ("prison", "тюрьма"),
    ("pump", "насос, качать"),
    ("rail", "рельс, перевозить поездом"),
    ("rat", "крыса"),
    ("receipt", "квитанция"),
    ("ring", "кольцо, звонить"),
    ("rod", "прут"),
    ("roof", "крыша"),
    ("root", "корень"),
    ("sail", "парус"),
    ("school", "школа"),
    ("scissors", "ножницы"),
    ("screw", "винт"),
    ("seed", "семя"),
    ("sheep", "овцы"),
    ("shelf", "полка"),
    ("ship", "корабль"),
    ("shirt", "рубашка"),
    ("shoe", "ботинок"),
    ("skin", "кожа, очищать"),
    ("skirt", "юбка"),
    ("snake", "змея"),
    ("sock", "носок"),
    ("spade", "лопата"),
    ("sponge", "губка"),
    ("spoon", "ложка"),
    ("spring", "весна"),
    ("square", "квадрат"),
    ("stamp", "печать, марка, отпечатывать"),
    ("star", "звезда"),
    ("station", "станция"),
    ("stem", "стебель, происходить"),
    ("stick", "палка, прикреплять"),
    ("stocking", "снабжать"),
    ("stomach", "живот, смелость, переваривать"),
    ("store", "магазин, запас"),
    ("street", "улица"),
    ("sun", "солнце"),
    ("table", "стол"),
    ("tail", "хвост, выслеживать"),
    ("thread", "нить, пронизывать"),
    ("throat", "горло"),
    ("thumb", "листать, большой палец"),
    ("ticket", "билет"),
    ("toe", "палец ноги"),
    ("tongue", "язык"),
    ("tooth", "зуб"),
    ("town", "город"),
    ("train", "поезд"),
    ("tray", "поднос"),
    ("tree", "дерево"),
    ("trousers", "брюки"),
    ("umbrella", "зонт"),
    ("wall", "стена"),
    ("watch", "часы"),
    ("wheel", "колесо, вертеть"),
    ("whip", "кнут, хлестать"),
    ("whistle", "свист, свистеть"),
    ("window", "окно"),
    ("wing", "крыло"),
    ("wire", "провод"),
    ("worm", "червь"),
    ("come", "приходить, приезжать"),
    ("get", "получать, заставлять"),
    ("give", "давать"),
    ("go", "ходить, идти"),
    ("keep", "продолжать, держать, оставлять, не допускать"),
    ("let", "позволять"),
    ("make", "делать/сделать, заставлять"),
    ("put", "помещать"),
    ("seem", "казаться, представляться"),
    ("take", "брать/взять"),
    ("be", "быть"),
    ("do", "делать"),
    ("have", "иметь, съесть, знать"),
    ("say", "говорить"),
    ("see", "видеть"),
    ("send", "посылать"),
    ("may", "мочь"),
    ("will", "быть хотеть"),
    ("about", "о"),
    ("across", "через"),
    ("after", "после"),
    ("against", "против"),
    ("among", "среди"),
    ("before", "перед"),
    ("between", "между"),
    ("by", "к, в соответствии с, за, на"),
    ("down", "вниз"),
    ("from", "из"),
    ("in", "в"),
    ("off", "прочь, от"),
    ("on", "на"),
    ("over", "по"),
    ("through", "через"),
    ("under", "под"),
    ("up", "вверх"),
    ("with", "с"),
    ("as", "поскольку, как"),
    ("for", "для"),
    ("of", "из, о, от"),
    ("till", "пока, до"),
    ("than", "чем"),
    ("all", "все, весь"),
    ("any", "любой, никто"),
    ("every", "каждый"),
    ("no", "никакой, нет"),
    ("other", "другой"),
    ("some", "некоторый, немного"),
    ("such", "такой, таким образом"),
    ("that", "что"),
    ("this", "это, этот"),
    ("i", "я"),
    ("he", "он"),
    ("you", "ты, вы"),
    ("who", "кто"),
    ("and", "и"),
    ("because", "потому что"),
    ("but", "а, но"),
    ("or", "или"),
    ("if", "если"),
    ("though", "хотя"),
    ("while", "в то время как"),
    ("how", "как"),
    ("when", "когда"),
    ("where", "где, куда, откуда"),
    ("why", "почему"),
    ("again", "снова"),
    ("ever", "когда-либо, никогда"),
    ("far", "самый дальний"),
    ("forward", "отправлять, вперед"),
    ("here", "здесь, сюда"),
    ("near", "рядом, около"),
    ("now", "теперь, сейчас"),
    ("out", "вне, снаружи"),
    ("still", "все еще"),
    ("then", "тогда"),
    ("there", "там, туда"),
    ("together", "вместе"),
    ("well", "хорошо, намного"),
    ("almost", "почти"),
    ("enough", "достаточно"),
    ("even", "еще, даже"),
    ("little", "маленький"),
    ("much", "много"),
    ("not", "не"),
    ("only", "только"),
    ("quite", "весьма"),
    ("so", "так"),
    ("very", "очень"),
    ("tomorrow", "завтра"),
    ("yesterday", "вчера"),
    ("north", "север"),
    ("south", "юг"),
    ("east", "восток"),
    ("west", "запад"),
    ("please", "пожалуйста"),
    ("yes", "да"),
    ("able", "способный, быть в состоянии"),
    ("acid", "кислота, кислый"),
    ("angry", "сердитый"),
    ("beautiful", "красивый"),
    ("black", "чёрный"),
    ("boiling", "кипение"),
    ("bright", "яркий, умный"),
    ("broken", "сломанный"),
    ("brown", "коричневый"),
    ("cheap", "дешёвый"),
    ("chemical", "химикат"),
    ("chief", "главный"),
    ("clean", "чистый, чистить"),
    ("clear", "ясный, очищать, оправдываться"),
    ("common", "общий"),
    ("complex", "комплекс"),
    ("conscious", "сознательный"),
    ("cut", "резать"),
    ("deep", "глубокий, глубоко"),
    ("dependent", "зависимый"),
    ("early", "рано, ранний"),
    ("elastic", "эластичный"),
    ("equal", "равный, равняться"),
    ("fat", "толстый, жир"),
    ("fertile", "плодородный"),
    ("first", "первый"),
    ("fixed", "неподвижный, неизменный"),
    ("flat", "плоский, квартира, плоскость"),
    ("free", "свобода, бесплатный"),
    ("frequent", "частый, часто посещать"),
    ("full", "полный"),
    ("general", "общий, генерал"),
    ("good", "хороший"),
    ("great", "великий, великолепный"),
    ("grey|gray", "серый"),
    ("hanging", "вывешивание, висение"),
    ("happy", "счастье"),
    ("hard", "трудный, тяжёлый, твёрдый"),
    ("healthy", "здоровый"),
    ("high", "высокий, высоко"),
    ("hollow", "пустота"),
    ("important", "важный"),
    ("jewel", "драгоценный камень"),
    ("kind", "добрый, вид"),
    ("like", "подобный, любить, нравиться"),
    ("living", "проживаниe"),
    ("long", "долго, длинный"),
    ("male", "мужской, мужчина"),
    ("married", "женатый, замужем"),
    ("material", "материал"),
    ("medical", "медицинский"),
    ("military", "военный"),
    ("natural", "натуральный"),
    ("necessary", "необходимый"),
    ("new", "новый"),
    ("normal", "нормальный"),
    ("open", "открытый, открывать"),
    ("parallel", "параллельный, находить что-либо подобное"),
    ("past", "мимо, прошлый"),
    ("physical", "физический"),
    ("political", "политический"),
    ("poor", "бедный, плохой, слабый"),
    ("possible", "возможный"),
    ("present", "существующий, подарок"),
    ("private", "личный, приватный"),
    ("probable", "вероятный"),
    ("quick", "быстрый"),
    ("quiet", "тихий, успокаивать"),
    ("ready", "готовый, готов"),
    ("read", "читать"),
    ("regular", "регулярный"),
    ("responsible", "ответственный"),
    ("right", "верный, право"),
    ("round", "вокруг, круглый, раунд"),
    ("same", "то же самое"),
    ("second", "секунда, второй"),
    ("separate", "отдельный, отделять"),
    ("serious", "серьёзный"),
    ("sharp", "острый"),
    ("smooth", "гладкий, мягкий, приглаживать"),
    ("sticky", "липкий"),
    ("stiff", "жесткий"),
    ("straight", "прямой"),
    ("strong", "сильный"),
    ("sudden", "внезапный"),
    ("sweet", "сладкий"),
    ("tall", "высокий"),
    ("thick", "толстый, густой"),
    ("tight", "трудный"),
    ("tired", "усталый"),
    ("true", "правда, правдивый"),
    ("violent", "сильный, жестокий"),
    ("waiting", "ожидание"),
    ("warm", "теплый, нагревать"),
    ("wet", "влажный"),
    ("wide", "широкий"),
    ("wise", "мудрый"),
    ("yellow", "жёлтый"),
    ("young", "молодой"),
    ("awake", "активный, пробуждать, просыпаться"),
    ("bad", "плохой"),
    ("bent", "склонность, сгибать"),
    ("bitter", "горький, ожесточенный"),
    ("blue", "синий"),
    ("certain", "уверенный, определенный"),
    ("cold", "холодный"),
    ("complete", "полный, заканчивать"),
    ("cruel", "жестокий"),
    ("dark", "темнота, темный"),
    ("dead", "мёртвый"),
    ("dear", "дорогой"),
    ("delicate", "тонкий, деликатный"),
    ("different", "различный, другой"),
    ("dirty", "грязный"),
    ("dry", "сухой, сушить"),
    ("false", "фальшивый"),
    ("feeble", "слабый"),
    ("female", "женский"),
    ("foolish", "глупый"),
    ("future", "будущий, будущее"),
    ("green", "зелёный"),
    ("ill", "плохо, болеть"),
    ("last", "последний, длиться"),
    ("late", "опаздывать"),
    ("left", "лево, левый"),
    ("loose", "свободный, освобождать"),
    ("loud", "громкий"),
    ("low", "низкий"),
    ("mixed", "перемешанный"),
    ("narrow", "узкий, сужаться"),
    ("old", "старый"),
    ("opposite", "напротив, противоположный"),
    ("public", "публичный"),
    ("rough", "грубый"),
    ("sad", "расстроенный"),
    ("safe", "безопасный"),
    ("secret", "секретный"),
    ("short", "короткий"),
    ("simple", "простой"),
    ("slow", "медленный"),
    ("small", "маленький"),
    ("soft", "мягкий"),
    ("solid", "твёрдый, солидный"),
    ("special", "специальный"),
    ("strange", "странный"),
    ("thin", "худой, тонкий, жидкий"),
    ("white", "белый"),
    ("wrong", "неправильный, несправедливость"),
)

LANGUAGE_PAIRS = [
    {
        "english_word": item[0],
        "russian_word": item[1],
    }
    for item in LANGUAGE_PAIRS_TUPLE
]


def get_pair_by_russian_word(word: str) -> dict:
    return find(LANGUAGE_PAIRS, lambda pair: pair["russian_word"] == word)


def get_pair_by_english_word(word: str) -> dict:
    return find(LANGUAGE_PAIRS, lambda pair: pair["english_word"] == word)

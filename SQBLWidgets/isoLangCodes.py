# -*- coding: utf-8 -*-

def languageCodeListPairs():
    common = []
    for code,data in popularcodes.items():
        common.append((code,"%s - %s / %s "%(code,data['name'],data['native'])))
    common.sort()
    allLangs = []
    for code,data in langcodes.items():
        try:
            allLangs.append((code,"%s - %s / %s "%(code,data['name'],data['native'])))
        except:
            allLangs.append((code,"%s - %s"%(code,data['name'])))
    allLangs.sort()
    return common + allLangs

def languageCodeList():
    common = []
    for code,data in popularcodes.items():
        common.append(code + " - " + data['name'] + " / " + data['native'])
    common.sort()
    allLangs = []
    for code,data in langcodes.items():
        try:
            allLangs.append("" + code + " - " + data['name'] + " / " + data['native'])
        except:
            allLangs.append("" + code + " - ")
    allLangs.sort()
    return common + allLangs

def iso639CodeToString(code):
    lang = knowncodes[code.lower()]
    return "%s / %s"%(lang['native'],lang['name'])

# Following list taken from [http://en.wikipedia.org/wiki/Global_Internet_usage#Internet_users_by_language]
popularcodes = {
"en":       {"name": "English"              ,"native":    u"British / Standard English" },
"zh":       {"name": "Chinese (Mandarin)"   ,"native":    u"官話/官话"                   },
"es":       {"name": "Spanish"              ,"native":    u"Español"                    },
"ja":       {"name": "Japanese"             ,"native":    u"日本語"                      },
"pt":       {"name": "Portuguese"           ,"native":    u"Português"                  },
"de":       {"name": "German"               ,"native":    u"Deutsch"                    },
"ar":       {"name": "Arabic"               ,"native":    u"العربية/عربي/عربىī"         }, 
"fr":       {"name": "French"               ,"native":    u"français"                   },
"ru":       {"name": "Russian"              ,"native":    u"русский язык"               },
"ko":       {"name": "Korean"               ,"native":    u"한국어, 조선말"               },
"en-us":    {"name": "American English"     ,"native":    u"American English"           },  # The difference means it is important enough to be added
}

# These languages don't have flags associated... yet
langcodes = {
"aa":    {"name": "Afaraf", "native" : u"Afar"}, 
"af":    {"name": "Afrikaans", "native" : u"Afrikaans"}, 
"ak":    {"name": "Akan", "native" : u"Akan"}, 
"sq":    {"name": "Albanian", "native" : u"Shqip"}, 
"am":    {"name": "Amharic", "native" : u"አማርኛ"}, 
"ar":    {"name": "Arabic", "native" : u"العربية"}, 
"an":    {"name": "Aragonese", "native" : u"Aragonés"}, 
"hy":    {"name": "Armenian", "native" : u"Հայերեն"}, 
"as":    {"name": "Assamese", "native" : u"অসমীয়া"}, 
"av":    {"name": "Avaric", "native" : u"авар мацӀ, магӀарул мацӀ"}, 
"ae":    {"name": "Avestan", "native" : u"avesta"}, 
"ay":    {"name": "Aymara", "native" : u"aymar aru"}, 
"az":    {"name": "Azerbaijani", "native" : u"azərbaycan dili"}, 
"bm":    {"name": "Bambara", "native" : u"bamanankan"}, 
"ba":    {"name": "Bashkir", "native" : u"башҡорт теле"}, 
"eu":    {"name": "Basque", "native" : u"euskara, euskera"}, 
"be":    {"name": "Belarusian", "native" : u"Беларуская"}, 
"bn":    {"name": "Bengali", "native" : u"বাংলা"}, 
"bh":    {"name": "Bihari", "native" : u"भोजपुरी"}, 
"bi":    {"name": "Bislama", "native" : u"Bislama"}, 
"bs":    {"name": "Bosnian", "native" : u"bosanski jezik"}, 
"br":    {"name": "Breton", "native" : u"brezhoneg"}, 
"bg":    {"name": "Bulgarian", "native" : u"български език"}, 
"my":    {"name": "Burmese", "native" : u"ဗမာစာ"}, 
"ca":    {"name": "Catalan; Valencian", "native" : u"Català"}, 
"ch":    {"name": "Chamorro", "native" : u"Chamoru"}, 
"ce":    {"name": "Chechen", "native" : u"нохчийн мотт"}, 
"ny":    {"name": "Chichewa; Chewa; Nyanja", "native" : u"chiCheŵa, chinyanja"}, 
"zh":    {"name": "Chinese", "native" : u"中文 (Zhōngwén), 汉语, 漢語"}, 
"cv":    {"name": "Chuvash", "native" : u"чӑваш чӗлхи"}, 
"kw":    {"name": "Cornish", "native" : u"Kernewek"}, 
"co":    {"name": "Corsican", "native" : u"corsu, lingua corsa"}, 
"cr":    {"name": "Cree", "native" : u"ᓀᐦᐃᔭᐍᐏᐣ"}, 
"hr":    {"name": "Croatian", "native" : u"hrvatski"}, 
"cs":    {"name": "Czech", "native" : u"česky, čeština"}, 
"da":    {"name": "Danish", "native" : u"dansk"}, 
"dv":    {"name": "Divehi; Dhivehi; Maldivian;", "native" : u"ދިވެހި"}, 
"nl":    {"name": "Dutch", "native" : u"Nederlands, Vlaams"}, 
"dz":    {"name": "Dzongkha", "native" : u"རྫོང་ཁ"}, 
"en":    {"name": "English", "native" : u"English"}, 
"eo":    {"name": "Esperanto", "native" : u"Esperanto"}, 
"et":    {"name": "Estonian", "native" : u"eesti, eesti keel"}, 
"ee":    {"name": "Ewe", "native" : u"Eʋegbe"}, 
"fo":    {"name": "Faroese", "native" : u"føroyskt"}, 
"fj":    {"name": "Fijian", "native" : u"vosa Vakaviti"}, 
"fi":    {"name": "Finnish", "native" : u"suomi, suomen kieli"}, 
"fr":    {"name": "French", "native" : u"français, langue française"}, 
"ff":    {"name": "Fula; Fulah; Pulaar; Pular", "native" : u"Fulfulde, Pulaar, Pular"}, 
"gl":    {"name": "Galician", "native" : u"Galego"}, 
"ka":    {"name": "Georgian", "native" : u"ქართული"}, 
"de":    {"name": "German", "native" : u"Deutsch"}, 
"el":    {"name": "Greek, Modern", "native" : u"Ελληνικά"}, 
"gu":    {"name": "Gujarati", "native" : u"ગુજરાતી"}, 
"ht":    {"name": "Haitian; Haitian Creole", "native" : u"Kreyòl ayisyen"}, 
"ha":    {"name": "Hausa", "native" : u"Hausa, هَوُسَ"}, 
"he":    {"name": "Hebrew(modern)", "native" : u"עברית"}, 
"hz":    {"name": "Herero", "native" : u"Otjiherero"}, 
"hi":    {"name": "Hindi", "native" : u"हिन्दी, हिंदी"}, 
"ho":    {"name": "Hiri Motu", "native" : u"Hiri Motu"}, 
"hu":    {"name": "Hungarian", "native" : u"Magyar"}, 
"id":    {"name": "Indonesian", "native" : u"Bahasa Indonesia"}, 
"ga":    {"name": "Irish", "native" : u"Gaeilge"}, 
"ig":    {"name": "Igbo", "native" : u"Asụsụ Igbo"}, 
"ik":    {"name": "Inupiaq", "native" : u"Iñupiaq, Iñupiatun"}, 
"is":    {"name": "Icelandic", "native" : u"Íslenska"}, 
"it":    {"name": "Italian", "native" : u"Italiano"}, 
"iu":    {"name": "Inuktitut", "native" : u"ᐃᓄᒃᑎᑐᑦ"}, 
"ja":    {"name": "Japanese", "native" : u"日本語 (にほんご)"}, 
"jv":    {"name": "Javanese", "native" : u"basa Jawa"}, 
"kl":    {"name": "Kalaallisut, Greenlandic", "native" : u"kalaallisut, kalaallit oqaasii"}, 
"kn":    {"name": "Kannada", "native" : u"ಕನ್ನಡ"}, 
"kr":    {"name": "Kanuri", "native" : u"Kanuri"}, 
"ks":    {"name": "Kashmiri", "native" : u"कश्मीरी, كشميري"}, 
"kk":    {"name": "Kazakh", "native" : u"Қазақ тілі"}, 
"km":    {"name": "Khmer", "native" : u"ខ្មែរ, ខេមរភាសា, ភាសាខ្មែរ"}, 
"ki":    {"name": "Kikuyu, Gikuyu", "native" : u"Gĩkũyũ"}, 
"rw":    {"name": "Kinyarwanda", "native" : u"Ikinyarwanda"}, 
"ky":    {"name": "Kirghiz, Kyrgyz", "native" : u"кыргыз тили"}, 
"kv":    {"name": "Komi", "native" : u"коми кыв"}, 
"kg":    {"name": "Kongo", "native" : u"KiKongo"}, 
"ko":    {"name": "Korean", "native" : u"한국어 (韓國語), 조선어 (朝鮮語)"}, 
"ku":    {"name": "Kurdish", "native" : u"Kurdî, كوردی"}, 
"kj":    {"name": "Kwanyama, Kuanyama", "native" : u"Kuanyama"}, 
"la":    {"name": "Latin", "native" : u"latine, lingua latina"}, 
"lb":    {"name": "Luxembourgish, Letzeburgesch", "native" : u"Lëtzebuergesch"}, 
"lg":    {"name": "Luganda", "native" : u"Luganda"}, 
"li":    {"name": "Limburgish, Limburgan, Limburger", "native" : u"Limburgs"}, 
"ln":    {"name": "Lingala", "native" : u"Lingála"}, 
"lo":    {"name": "Lao", "native" : u"ພາສາລາວ"}, 
"lt":    {"name": "Lithuanian", "native" : u"lietuvių kalba"}, 
"lu":    {"name": "Luba-Katanga", "native" : u""}, 
"lv":    {"name": "Latvian", "native" : u"latviešu valoda"}, 
"gv":    {"name": "Manx", "native" : u"Gaelg, Gailck"}, 
"mk":    {"name": "Macedonian", "native" : u"македонски јазик"}, 
"mg":    {"name": "Malagasy", "native" : u"Malagasy fiteny"}, 
"ms":    {"name": "Malay", "native" : u"bahasa Melayu, بهاس ملايو"}, 
"ml":    {"name": "Malayalam", "native" : u"മലയാളം"}, 
"mt":    {"name": "Maltese", "native" : u"Malti"}, 
"mi":    {"name": "Māori", "native" : u"te reo Māori"}, 
"mr":    {"name": "Marathi (Marāṭhī)", "native" : u"मराठी"}, 
"mh":    {"name": "Marshallese", "native" : u"Kajin M̧ajeļ"}, 
"mn":    {"name": "Mongolian", "native" : u"монгол"}, 
"na":    {"name": "Nauru", "native" : u"Ekakairũ Naoero"}, 
"nv":    {"name": "Navajo, Navaho", "native" : u"Diné bizaad, Dinékʼehǰí"}, 
"nb":    {"name": "Norwegian Bokmål", "native" : u"Norsk bokmål"}, 
"nd":    {"name": "North Ndebele", "native" : u"isiNdebele"}, 
"ne":    {"name": "Nepali", "native" : u"नेपाली"}, 
"ng":    {"name": "Ndonga", "native" : u"Owambo"}, 
"nn":    {"name": "Norwegian Nynorsk", "native" : u"Norsk nynorsk"}, 
"no":    {"name": "Norwegian", "native" : u"Norsk"}, 
"ii":    {"name": "Nuosu", "native" : u"ꆈꌠ꒿ Nuosuhxop"}, 
"nr":    {"name": "South Ndebele", "native" : u"isiNdebele"}, 
"oc":    {"name": "Occitan", "native" : u"Occitan"}, 
"oj":    {"name": "Ojibwe, Ojibwa", "native" : u"ᐊᓂᔑᓈᐯᒧᐎᓐ"}, 
"cu":    {"name": "Old Church Slavonic, Church Slavic, Church Slavonic, Old Bulgarian, Old Slavonic", "native" : u"ѩзыкъ словѣньскъ"}, 
"om":    {"name": "Oromo", "native" : u"Afaan Oromoo"}, 
"or":    {"name": "Oriya", "native" : u"ଓଡ଼ିଆ"}, 
"os":    {"name": "Ossetian, Ossetic", "native" : u"ирон æвзаг"}, 
"pa":    {"name": "Panjabi, Punjabi", "native" : u"ਪੰਜਾਬੀ, پنجابی"}, 
"pi":    {"name": "Pāli", "native" : u"पाऴि"}, 
"fa":    {"name": "Persian", "native" : u"فارسی"}, 
"pl":    {"name": "Polish", "native" : u"polski"}, 
"ps":    {"name": "Pashto, Pushto", "native" : u"پښتو"}, 
"pt":    {"name": "Portuguese", "native" : u"Português"}, 
"qu":    {"name": "Quechua", "native" : u"Runa Simi, Kichwa"}, 
"rm":    {"name": "Romansh", "native" : u"rumantsch grischun"}, 
"rn":    {"name": "Kirundi", "native" : u"Ikirundi"}, 
"ro":    {"name": "Romanian, Moldavian, Moldovan", "native" : u"română"}, 
"ru":    {"name": "Russian", "native" : u"русский язык"}, 
"sa":    {"name": "Sanskrit (Saṁskṛta)", "native" : u"संस्कृतम्"}, 
"sc":    {"name": "Sardinian", "native" : u"sardu"}, 
"sd":    {"name": "Sindhi", "native" : u">सिन्धी, <سنڌي، سندھی"}, 
"se":    {"name": "Northern Sami", "native" : u"Davvisámegiella"}, 
"sm":    {"name": "Samoan", "native" : u"gagana fa'a Samoa"}, 
"sg":    {"name": "Sango", "native" : u"yângâ tî sängö"}, 
"sr":    {"name": "Serbian", "native" : u"српски језик"}, 
"gd":    {"name": "Scottish Gaelic; Gaelic", "native" : u"Gàidhlig"}, 
"sn":    {"name": "Shona", "native" : u"chiShona"}, 
"si":    {"name": "Sinhala, Sinhalese", "native" : u"සිංහල"}, 
"sk":    {"name": "Slovak", "native" : u"slovenčina"}, 
"sl":    {"name": "Slovene", "native" : u"slovenščina"}, 
"so":    {"name": "Somali", "native" : u"Soomaaliga, af Soomaali"}, 
"st":    {"name": "Southern Sotho", "native" : u"Sesotho"}, 
"es":    {"name": "Spanish; Castilian", "native" : u"español, castellano"}, 
"su":    {"name": "Sundanese", "native" : u"Basa Sunda"}, 
"sw":    {"name": "Swahili", "native" : u"Kiswahili"}, 
"ss":    {"name": "Swati", "native" : u"SiSwati"}, 
"sv":    {"name": "Swedish", "native" : u"svenska"}, 
"ta":    {"name": "Tamil", "native" : u"தமிழ்"}, 
"te":    {"name": "Telugu", "native" : u"తెలుగు"}, 
"tg":    {"name": "Tajik", "native" : u"тоҷикӣ, toğikī, تاجیکی"}, 
"th":    {"name": "Thai", "native" : u"ไทย"}, 
"ti":    {"name": "Tigrinya", "native" : u"ትግርኛ"}, 
"bo":    {"name": "Tibetan Standard, Tibetan, Central", "native" : u"བོད་ཡིག"}, 
"tk":    {"name": "Turkmen", "native" : u"Türkmen, Түркмен"}, 
"tl":    {"name": "Tagalog", "native" : u"Wikang Tagalog, ᜏᜒᜃᜅ᜔ ᜆᜄᜎᜓᜄ᜔"}, 
"tn":    {"name": "Tswana", "native" : u"Setswana"}, 
"to":    {"name": "Tonga(Tonga Islands)", "native" : u"faka Tonga"}, 
"tr":    {"name": "Turkish", "native" : u"Türkçe"}, 
"ts":    {"name": "Tsonga", "native" : u"Xitsonga"}, 
"tt":    {"name": "Tatar", "native" : u"татарча, tatarça, تاتارچا"}, 
"tw":    {"name": "Twi", "native" : u"Twi"}, 
"ty":    {"name": "Tahitian", "native" : u"Reo Tahiti"}, 
"ug":    {"name": "Uighur, Uyghur", "native" : u"Uyƣurqə, ئۇيغۇرچە"}, 
"uk":    {"name": "Ukrainian", "native" : u"українська"}, 
"ur":    {"name": "Urdu", "native" : u"اردو"}, 
"uz":    {"name": "Uzbek", "native" : u"O'zbek, Ўзбек, أۇزبېك<"}, 
"ve":    {"name": "Venda", "native" : u"Tshivenḓa"}, 
"vi":    {"name": "Vietnamese", "native" : u"Tiếng Việt"}, 
"wa":    {"name": "Walloon", "native" : u"Walon"}, 
"cy":    {"name": "Welsh", "native" : u"Cymraeg"}, 
"wo":    {"name": "Wolof", "native" : u"Wollof"}, 
"fy":    {"name": "Western Frisian", "native" : u"Frysk"}, 
"xh":    {"name": "Xhosa", "native" : u"isiXhosa"}, 
"yi":    {"name": "Yiddish", "native" : u"ייִדיש"}, 
"yo":    {"name": "Yoruba", "native" : u"Yorùbá"}, 
"za":    {"name": "Zhuang, Chuang", "native" : u"Saɯ cueŋƅ, Saw cuengh"}, 
"zu":    {"name": "Zulu", "native" : u"isiZulu"}
}

knowncodes = {}
knowncodes.update(langcodes)
knowncodes.update(popularcodes)

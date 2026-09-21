#!/usr/bin/env python3
"""
BHASHASETU handwriting worksheets - generator.

Builds print-ready A4 HTML workbooks that teach a Bengali speaker to WRITE
Devanagari, in the order the bengali_to_hindi course teaches it:
letters -> vowel signs -> words -> sentences.

Every instruction is in Bengali. Output: worksheets/<pair>/*.html
PDFs are produced from those with headless Chrome (see build_pdfs.sh).

Tunables live in CSS custom properties at the top of STYLE so the ruling and
glyph placement can be adjusted in one place after looking at a printed page.
"""
import os, html, json

PAIR = "bengali_to_hindi"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), PAIR)

# ---------------------------------------------------------------- data
# (devanagari, bengali equivalent, transliteration, example word, example gloss)
VOWELS = [
    ("अ",  "অ",  "a",   "अब",     "এখন"),
    ("आ",  "আ",  "ā",   "आम",     "আম"),
    ("इ",  "ই",  "i",   "इधर",    "এদিকে"),
    ("ई",  "ঈ",  "ī",   "ईख",     "আখ"),
    ("उ",  "উ",  "u",   "उधर",    "ওদিকে"),
    ("ऊ",  "ঊ",  "ū",   "ऊन",     "উল"),
    ("ऋ",  "ঋ",  "ṛ",   "ऋषि",    "ঋষি"),
    ("ए",  "এ",  "e",   "एक",     "এক"),
    ("ऐ",  "ঐ",  "ai",  "ऐनक",    "চশমা"),
    ("ओ",  "ও",  "o",   "ओर",     "দিক"),
    ("औ",  "ঔ",  "au",  "औषधि",   "ঔষধ"),
    ("अं", "অং", "aṃ",  "हंस",     "রাজহাঁস"),
    ("अः", "অঃ", "aḥ",  "दुःख",    "দুঃখ"),
]

CONSONANTS = [
    # (deva, bangla, translit, example, gloss, varga label)
    ("क","ক","ka","कमल","কমল","কণ্ঠ্য বর্গ (কবর্গ)"),
    ("ख","খ","kha","खग","পাখি","কণ্ঠ্য বর্গ (কবর্গ)"),
    ("ग","গ","ga","गगन","আকাশ","কণ্ঠ্য বর্গ (কবর্গ)"),
    ("घ","ঘ","gha","घर","ঘর","কণ্ঠ্য বর্গ (কবর্গ)"),
    ("ङ","ঙ","ṅa","रंग","রং","কণ্ঠ্য বর্গ (কবর্গ)"),
    ("च","চ","ca","चंद्र","চন্দ্র","তালব্য বর্গ (চবর্গ)"),
    ("छ","ছ","cha","छत्र","ছাতা","তালব্য বর্গ (চবর্গ)"),
    ("ज","জ","ja","जल","জল","তালব্য বর্গ (চবর্গ)"),
    ("झ","ঝ","jha","झरना","ঝরনা","তালব্য বর্গ (চবর্গ)"),
    ("ञ","ঞ","ña","ज्ञान","জ্ঞান","তালব্য বর্গ (চবর্গ)"),
    ("ट","ট","ṭa","टमाटर","টম্যাটো","মূর্ধন্য বর্গ (টবর্গ)"),
    ("ठ","ঠ","ṭha","ठंड","ঠান্ডা","মূর্ধন্য বর্গ (টবর্গ)"),
    ("ड","ড","ḍa","डंडा","লাঠি","মূর্ধন্য বর্গ (টবর্গ)"),
    ("ढ","ঢ","ḍha","ढोल","ঢোল","মূর্ধন্য বর্গ (টবর্গ)"),
    ("ण","ণ","ṇa","प्राण","প্রাণ","মূর্ধন্য বর্গ (টবর্গ)"),
    ("त","ত","ta","तारा","তারা","দন্ত্য বর্গ (তবর্গ)"),
    ("थ","থ","tha","थाली","থালা","দন্ত্য বর্গ (তবর্গ)"),
    ("द","দ","da","दिन","দিন","দন্ত্য বর্গ (তবর্গ)"),
    ("ध","ধ","dha","धन","ধন","দন্ত্য বর্গ (তবর্গ)"),
    ("न","ন","na","नाम","নাম","দন্ত্য বর্গ (তবর্গ)"),
    ("प","প","pa","पुस्तक","পুস্তক","ওষ্ঠ্য বর্গ (পবর্গ)"),
    ("फ","ফ","pha","फल","ফল","ওষ্ঠ্য বর্গ (পবর্গ)"),
    ("ब","ব","ba","बाबा","বাবা","ওষ্ঠ্য বর্গ (পবর্গ)"),
    ("भ","ভ","bha","भाषा","ভাষা","ওষ্ঠ্য বর্গ (পবর্গ)"),
    ("म","ম","ma","माँ","মা","ওষ্ঠ্য বর্গ (পবর্গ)"),
    ("य","য","ya","यह","এটা","অন্তঃস্থ ও ঊষ্ম"),
    ("र","র","ra","राम","রাম","অন্তঃস্থ ও ঊষ্ম"),
    ("ल","ল","la","लाल","লাল","অন্তঃস্থ ও ঊষ্ম"),
    ("व","ব / ৱ","va","वन","বন","অন্তঃস্থ ও ঊষ্ম"),
    ("श","শ","śa","शांति","শান্তি","অন্তঃস্থ ও ঊষ্ম"),
    ("ष","ষ","ṣa","षट्","ছয়","অন্তঃস্থ ও ঊষ্ম"),
    ("स","স","sa","सत्य","সত্য","অন্তঃস্থ ও ঊষ্ম"),
    ("ह","হ","ha","हाथ","হাত","অন্তঃস্থ ও ঊষ্ম"),
]

NUKTA = [
    ("ड़","ড়","ṛa","पढ़ना","পড়া","নুক্তা - বাংলার ড় ঢ় এখানেই"),
    ("ढ़","ঢ়","ṛha","बूढ़ा","বুড়ো","নুক্তা - বাংলার ড় ঢ় এখানেই"),
    ("क़","ক়","qa","क़ानून","আইন","নুক্তা - ফার্সি-আরবি ধ্বনি"),
    ("ख़","খ়","kha","ख़त","চিঠি","নুক্তা - ফার্সি-আরবি ধ্বনি"),
    ("ग़","গ়","ġa","ग़ज़ल","গজল","নুক্তা - ফার্সি-আরবি ধ্বনি"),
    ("ज़","জ়","za","ज़रूर","অবশ্যই","নুক্তা - ফার্সি-আরবি ধ্বনি"),
    ("फ़","ফ়","fa","फ़ोन","ফোন","নুক্তা - ফার্সি-আরবি ধ্বনি"),
]

# barakhadi: (form, bengali equivalent, translit, note)
MATRA = [
    ("क","ক","ka","অন্তর্নিহিত 'অ' - কোনো চিহ্ন নেই"),
    ("का","কা","kā","আ-কার: ডানদিকে একটি দাঁড়ি"),
    ("कि","কি","ki","ই-কার: বাঁদিকে বসে, কিন্তু পড়া হয় পরে"),
    ("की","কী","kī","ঈ-কার: ডানদিকে"),
    ("कु","কু","ku","উ-কার: নিচে"),
    ("कू","কূ","kū","ঊ-কার: নিচে"),
    ("कृ","কৃ","kṛ","ঋ-কার: নিচে"),
    ("के","কে","ke","এ-কার: শিরোরেখার উপরে"),
    ("कै","কৈ","kai","ঐ-কার: উপরে দুটি"),
    ("को","কো","ko","ও-কার: দাঁড়ি + উপরে এক"),
    ("कौ","কৌ","kau","ঔ-কার: দাঁড়ি + উপরে দুই"),
    ("कं","কং","kaṃ","অনুস্বার"),
    ("कः","কঃ","kaḥ","বিসর্গ"),
]


# Conjuncts. Devanagari builds these four ways; the book is grouped by the rule,
# not alphabetically, because the rule is what generalises to pairs not listed.
#   (conjunct, first-with-virama, second, example, bengali gloss, group)
CONJUNCTS = [
    # 1. doubled - the easiest, and the rule is visible: drop the stem, repeat
    ("क्क","क्","क","पक्का","পাকা","দ্বিত্ব - একই অক্ষর দুবার"),
    ("च्च","च्","च","बच्चा","বাচ্চা","দ্বিত্ব - একই অক্ষর দুবার"),
    ("च्छ","च्","छ","अच्छा","ভালো","দ্বিত্ব - একই অক্ষর দুবার"),
    ("ज्ज","ज्","ज","सज्जन","ভদ্রলোক","দ্বিত্ব - একই অক্ষর দুবার"),
    ("त्त","त्","त","पत्ता","পাতা","দ্বিত্ব - একই অক্ষর দুবার"),
    ("द्द","द्","द","गद्दा","গদি","দ্বিত্ব - একই অক্ষর দুবার"),
    ("न्न","न्","न","अन्न","অন্ন","দ্বিত্ব - একই অক্ষর দুবার"),
    ("प्प","प्","प","चप्पल","চপ্পল","দ্বিত্ব - একই অক্ষর দুবার"),
    ("ब्ब","ब्","ब","डिब्बा","কৌটো","দ্বিত্ব - একই অক্ষর দুবার"),
    ("म्म","म्","म","चम्मच","চামচ","দ্বিত্ব - একই অক্ষর দুবার"),
    ("ल्ल","ल्","ल","बिल्ली","বিড়াল","দ্বিত্ব - একই অক্ষর দুবার"),
    ("स्स","स्","स","रस्सी","দড়ি","দ্বিত্ব - একই অক্ষর দুবার"),
    # 2. half-form: the left letter loses its vertical stem
    ("स्त","स्","त","पुस्तक","পুস্তক","আধা অক্ষর - দাঁড়ি কেটে"),
    ("स्थ","स्","थ","स्थान","স্থান","আধা অক্ষর - দাঁড়ি কেটে"),
    ("स्न","स्","न","स्नान","স্নান","আধা অক্ষর - দাঁড়ি কেটে"),
    ("स्व","स्","व","स्वर","স্বর","আধা অক্ষর - দাঁড়ি কেটে"),
    ("स्म","स्","म","स्मरण","স্মরণ","আধা অক্ষর - দাঁড়ি কেটে"),
    ("स्क","स्","क","स्कूल","স্কুল","আধা অক্ষর - দাঁড়ি কেটে"),
    ("श्व","श्","व","विश्व","বিশ্ব","আধা অক্ষর - দাঁড়ি কেটে"),
    ("श्य","श्","य","दृश्य","দৃশ্য","আধা অক্ষর - দাঁড়ি কেটে"),
    ("ष्ट","ष्","ट","कष्ट","কষ্ট","আধা অক্ষর - দাঁড়ি কেটে"),
    ("ष्ठ","ष्","ठ","श्रेष्ठ","শ্রেষ্ঠ","আধা অক্ষর - দাঁড়ি কেটে"),
    # 3a. ra on top - the reph
    ("र्म","र्","म","धर्म","ধর্ম","রেফ - র উপরে বসে"),
    ("र्क","र्","क","तर्क","তর্ক","রেফ - র উপরে বসে"),
    ("र्य","र्","य","सूर्य","সূর্য","রেফ - র উপরে বসে"),
    ("र्ष","र्","ष","वर्ष","বর্ষ","রেফ - র উপরে বসে"),
    ("र्थ","र्","थ","अर्थ","অর্থ","রেফ - র উপরে বসে"),
    ("र्ण","र्","ण","वर्ण","বর্ণ","রেফ - র উপরে বসে"),
    # 3b. ra underneath
    ("प्र","प्","र","प्रेम","প্রেম","পায়ে র - নিচে হেলানো দাগ"),
    ("क्र","क्","र","क्रम","ক্রম","পায়ে র - নিচে হেলানো দাগ"),
    ("ग्र","ग्","र","ग्राम","গ্রাম","পায়ে র - নিচে হেলানো দাগ"),
    ("द्र","द्","र","चंद्र","চন্দ্র","পায়ে র - নিচে হেলানো দাগ"),
    ("ब्र","ब्","र","ब्रज","ব্রজ","পায়ে র - নিচে হেলানো দাগ"),
    ("त्र","त्","र","पत्र","চিঠি","পায়ে র - নিচে হেলানো দাগ"),
    ("श्र","श्","र","श्रम","শ্রম","পায়ে র - নিচে হেলানো দাগ"),
    ("स्त्र","स्त्","र","वस्त्र","বস্ত্র","পায়ে র - তিন অক্ষরের জোড়"),
    # 4. irregular ligatures - must be memorised, the shape hides the parts
    ("क्ष","क्","ष","क्षमा","ক্ষমা","বিশেষ রূপ - মুখস্থ করতে হয়"),
    ("ज्ञ","ज्","ञ","ज्ञान","জ্ঞান","বিশেষ রূপ - মুখস্থ করতে হয়"),
    ("द्य","द्","य","विद्या","বিদ্যা","বিশেষ রূপ - মুখস্থ করতে হয়"),
    ("द्व","द्","व","द्वार","দ্বার","বিশেষ রূপ - মুখস্থ করতে হয়"),
    ("द्ध","द्","ध","बुद्ध","বুদ্ধ","বিশেষ রূপ - মুখস্থ করতে হয়"),
    ("द्म","द्","म","पद्म","পদ্ম","বিশেষ রূপ - মুখস্থ করতে হয়"),
    ("ह्म","ह्","म","ब्रह्म","ব্রহ্ম","বিশেষ রূপ - মুখস্থ করতে হয়"),
    ("ह्य","ह्","य","सह्य","সহ্য","বিশেষ রূপ - মুখস্থ করতে হয়"),
    ("ह्न","ह्","न","चिह्न","চিহ্ন","বিশেষ রূপ - মুখস্থ করতে হয়"),
    ("ट्ठ","ट्","ठ","चिट्ठी","চিঠি","বিশেষ রূপ - মুখস্থ করতে হয়"),
    # 5. y-forms
    ("क्य","क्","य","क्या","কী","য-ফলা"),
    ("ख्य","ख्","य","मुख्य","মুখ্য","য-ফলা"),
    ("त्य","त्","य","सत्य","সত্য","য-ফলা"),
    ("थ्य","थ्","य","तथ्य","তথ্য","য-ফলা"),
    ("ध्य","ध्","य","ध्यान","ধ্যান","য-ফলা"),
    ("न्य","न्","य","अन्य","অন্য","য-ফলা"),
    ("म्य","म्","य","रम्य","রম্য","য-ফলা"),
    ("व्य","व्","य","व्यक्ति","ব্যক্তি","য-ফলা"),
    # 6. v-forms
    ("त्व","त्","व","तत्व","তত্ত্ব","ব-ফলা"),
    ("ध्व","ध्","व","ध्वनि","ধ্বনি","ব-ফলা"),
    ("ज्व","ज्","व","ज्वर","জ্বর","ব-ফলা"),
    ("क्व","क्","व","पक्व","পক্ব","ব-ফলা"),
    # 7. nasal + consonant (often written with anusvara instead - both shown)
    ("न्त","न्","त","अन्त / अंत","অন্ত","নাসিক্য জোড় - অনুস্বারেও লেখা চলে"),
    ("न्द","न्","द","वन्दे / वंदे","বন্দে","নাসিক্য জোড় - অনুস্বারেও লেখা চলে"),
    ("न्ध","न्","ध","अन्धा / अंधा","অন্ধ","নাসিক্য জোড় - অনুস্বারেও লেখা চলে"),
    ("म्प","म्","प","कम्पन / कंपन","কম্পন","নাসিক্য জোড় - অনুস্বারেও লেখা চলে"),
    ("म्ब","म्","ब","अम्बर / अंबर","অম্বর","নাসিক্য জোড় - অনুস্বারেও লেখা চলে"),
    ("म्भ","म्","भ","स्तम्भ / स्तंभ","স্তম্ভ","নাসিক্য জোড় - অনুস্বারেও লেখা চলে"),
    ("ण्ड","ण्","ड","दण्ड / दंड","দণ্ড","নাসিক্য জোড় - অনুস্বারেও লেখা চলে"),
    ("ञ्च","ञ्","च","पञ्च / पंच","পঞ্চ","নাসিক্য জোড় - অনুস্বারেও লেখা চলে"),
]

WORDS1 = {
    "সর্বনাম": [("मैं","আমি"),("तू","তুই"),("तुम","তুমি"),("आप","আপনি"),
                 ("वह","সে"),("यह","এটা"),("हम","আমরা"),("वे","তারা")],
    "নিত্য বিশেষ্য": [("घर","ঘর"),("पानी","জল"),("नाम","নাম"),("दिन","দিন"),
                      ("रात","রাত"),("दूध","দুধ"),("चावल","চাল"),("रोटी","রুটি"),
                      ("हवा","হাওয়া"),("आग","আগুন"),("फूल","ফুল"),("फल","ফল")],
    "শরীর": [("हाथ","হাত"),("पैर","পা"),("सिर","মাথা"),("मुँह","মুখ"),
             ("नाक","নাক"),("कान","কান"),("आँख","চোখ"),("दाँत","দাঁত")],
    "পরিবার": [("माँ","মা"),("पिता","বাবা"),("भाई","ভাই"),("बहन","বোন"),
               ("बेटा","ছেলে"),("बेटी","মেয়ে"),("दादा","ঠাকুরদা"),("नाना","দাদামশাই")],
    "রং ও গুণ": [("लाल","লাল"),("काला","কালো"),("हरा","সবুজ"),("पीला","হলুদ"),
                 ("नीला","নীল"),("छोटा","ছোট"),("गरम","গরম"),("ठीक","ঠিক")],
    "সংখ্যা": [("एक","এক"),("दो","দুই"),("तीन","তিন"),("चार","চার"),("पाँच","পাঁচ"),
               ("छह","ছয়"),("सात","সাত"),("आठ","আট"),("नौ","নয়"),("दस","দশ")],
    "সাধারণ ক্রিয়া": [("आना","আসা"),("जाना","যাওয়া"),("खाना","খাওয়া"),("पीना","পান করা"),
                       ("देखना","দেখা"),("सुनना","শোনা"),("बोलना","বলা"),("चलना","চলা"),
                       ("उठना","ওঠা"),("सोना","ঘুমানো")],
}

WORDS2 = {
    "যুক্তাক্ষর - সংস্কৃত সেতু": [("पुस्तक","পুস্তক"),("सत्य","সত্য"),("विद्या","বিদ্যা"),
                                  ("शिक्षा","শিক্ষা"),("ज्ञान","জ্ঞান"),("मित्र","মিত্র"),
                                  ("चंद्र","চন্দ্র"),("शब्द","শব্দ")],
    "যুক্তাক্ষর - আরও": [("प्रेम","প্রেম"),("स्वप्न","স্বপ্ন"),("वस्त्र","বস্ত্র"),("धर्म","ধর্ম"),
                          ("कर्म","কর্ম"),("पत्र","চিঠি"),("कक्षा","শ্রেণি"),("श्रम","শ্রম")],
    "নুক্তা - বাংলার ড় ঢ়": [("पढ़ना","পড়া"),("बड़ा","বড়"),("पेड़","গাছ"),("लड़का","ছেলে"),
                              ("लड़की","মেয়ে"),("चढ़ना","চড়া"),("बढ़ना","বাড়া")],
    "নুক্তা - ফার্সি ধ্বনি": [("ज़मीन","জমি"),("ज़रूर","অবশ্যই"),("फ़ोन","ফোন"),("क़ानून","আইন"),
                              ("ग़ज़ल","গজল"),("बाज़ार","বাজার"),("मेज़","টেবিল")],
    "ফার্সি-আরবি শব্দ": [("किताब","বই"),("कमरा","ঘর / কামরা"),("दुकान","দোকান"),("कुर्सी","চেয়ার"),
                         ("कपड़ा","কাপড়"),("दोस्त","বন্ধু"),("हिसाब","হিসাব")],
    "দীর্ঘ শব্দ": [("नमस्ते","নমস্কার"),("धन्यवाद","ধন্যবাদ"),("विद्यालय","বিদ্যালয়"),
                   ("अस्पताल","হাসপাতাল"),("विद्यार्थी","বিদ্যার্থী"),("समाचार","সংবাদ"),
                   ("स्वतंत्रता","স্বাধীনতা")],
    "কঠিন ক্রিয়া": [("समझना","বোঝা"),("सीखना","শেখা"),("पहुँचना","পৌঁছানো"),("छोड़ना","ছাড়া"),
                     ("खरीदना","কেনা"),("बेचना","বেচা"),("मिलना","দেখা করা")],
    "ভাব ও গুণ": [("सुंदर","সুন্দর"),("लंबा","লম্বা"),("मुश्किल","কঠিন"),("आसान","সহজ"),
                  ("ज़रूरी","দরকারি"),("खुश","খুশি"),("दुखी","দুঃখী")],
}

SENTENCES1 = [
    ("मेरा नाम राम है।","আমার নাম রাম।"),
    ("यह मेरा घर है।","এটা আমার ঘর।"),
    ("मैं पानी पीता हूँ।","আমি জল খাই।"),
    ("वह रोटी खाता है।","সে রুটি খায়।"),
    ("तुम कहाँ हो?","তুমি কোথায়?"),
    ("मैं घर जाता हूँ।","আমি ঘরে যাই।"),
    ("यह फूल लाल है।","এই ফুল লাল।"),
    ("मेरी माँ आती है।","আমার মা আসেন।"),
    ("वह मेरा भाई है।","সে আমার ভাই।"),
    ("आपका नाम क्या है?","আপনার নাম কী?"),
    ("दूध गरम है।","দুধ গরম।"),
    ("वह नहीं आता।","সে আসে না।"),
    ("मुझे पानी दो।","আমাকে জল দাও।"),
    ("यहाँ आओ।","এখানে এসো।"),
    ("वहाँ मत जाओ।","ওখানে যেও না।"),
    ("मेरे दो भाई हैं।","আমার দুই ভাই।"),
    ("हम सुबह आते हैं।","আমরা সকালে আসি।"),
    ("तुम भी चलो।","তুমিও চলো।"),
    ("मेरा हाथ छोटा है।","আমার হাত ছোট।"),
    ("पानी ठंडा है।","জল ঠান্ডা।"),
    ("बेटा सोता है।","ছেলে ঘুমোয়।"),
    ("यह मेरा फल है।","এটা আমার ফল।"),
    ("आज रात है।","আজ রাত।"),
    ("वह गाना गाती है।","সে গান গায়।"),
    ("मैं हिंदी सीखता हूँ।","আমি হিন্দি শিখি।"),
    ("यह घर नया है।","এই ঘর নতুন।"),
    ("हवा ठंडी है।","হাওয়া ঠান্ডা।"),
    ("मैं आज नहीं जाऊँगा।","আমি আজ যাব না।"),
]

SENTENCES2 = [
    ("मैं कोलकाता से हूँ।","আমি কলকাতা থেকে।"),
    ("मैं रोज़ किताब पढ़ता हूँ।","আমি রোজ বই পড়ি।"),
    ("वह विद्यालय में पढ़ती है।","সে বিদ্যালয়ে পড়ে।"),
    ("क्या आप हिंदी बोलते हैं?","আপনি কি হিন্দি বলেন?"),
    ("मुझे यह शहर पसंद है।","আমার এই শহর ভালো লাগে।"),
    ("कृपया थोड़ा पानी दीजिए।","অনুগ্রহ করে একটু জল দিন।"),
    ("आज मौसम अच्छा है।","আজ আবহাওয়া ভালো।"),
    ("मेरे मित्र का नाम अर्जुन है।","আমার বন্ধুর নাম অর্জুন।"),
    ("हम कल बाज़ार जाएँगे।","আমরা কাল বাজার যাব।"),
    ("उसने मुझे पत्र लिखा।","সে আমাকে চিঠি লিখেছে।"),
    ("यह पुस्तक सुंदर है।","এই বই সুন্দর।"),
    ("क्या तुमने खाना खाया?","তুমি কি খেয়েছ?"),
    ("वह अस्पताल में काम करता है।","সে হাসপাতালে কাজ করে।"),
    ("मुझे हिंदी सीखनी है।","আমাকে হিন্দি শিখতে হবে।"),
    ("तुम्हारा घर कहाँ है?","তোমার ঘর কোথায়?"),
    ("वे मिलकर काम करते हैं।","তারা একসাথে কাজ করে।"),
    ("इस कमरे में तीन कुर्सियाँ हैं।","এই ঘরে তিনটি চেয়ার আছে।"),
    ("बच्चे बगीचे में खेल रहे हैं।","বাচ্চারা বাগানে খেলছে।"),
    ("मैंने समाचार नहीं पढ़ा।","আমি খবর পড়িনি।"),
    ("उसे संगीत सुनना पसंद है।","তার গান শুনতে ভালো লাগে।"),
    ("हमें समय पर पहुँचना चाहिए।","আমাদের সময়মতো পৌঁছাতে হবে।"),
    ("यह प्रश्न मुश्किल है।","এই প্রশ্ন কঠিন।"),
    ("दुकान नौ बजे खुलती है।","দোকান নয়টায় খোলে।"),
    ("मेरी बहन डॉक्टर है।","আমার বোন ডাক্তার।"),
    ("स्वतंत्रता हमारा अधिकार है।","স্বাধীনতা আমাদের অধিকার।"),
    ("धन्यवाद, आपकी बहुत कृपा।","ধন্যবাদ, আপনার অনেক কৃপা।"),
    ("मैं आपसे बाद में मिलूँगा।","আমি আপনার সাথে পরে দেখা করব।"),
    ("क्षमा कीजिए, मुझे देर हुई।","ক্ষমা করবেন, আমার দেরি হল।"),
]

# ---------------------------------------------------------------- css
STYLE = """
:root{
  /* --- ruling geometry: change these to retune every sheet --- */
  --head:  9mm;        /* SHIRO-REKHA - letters hang from here   */
  --base:  19mm;       /* baseline - letters sit here            */
  /* Noto Serif Devanagari metrics, measured with canvas TextMetrics
     (see calibrate_font.html). Fractions of the font size, from the baseline:
       bare letter  shirorekha ....... 0.642 up
       matras above (ि ी े ै) ........ 0.925 up
       matras below (ु ू ृ) .......... 0.290 down
     Only --head and --base are set by hand; everything else derives. */
  --asc-ratio:  0.642;
  --top-ratio:  0.283; /* 0.925 - 0.642: how far matras clear the headline */
  --bot-ratio:  0.290;

  --ink:#1C1611; --faded:#6B5B48; --sindoor:#A83024; --ochre:#B8802D; --teal:#1F4D4A;
  --line:#9aa8b8;      /* solid ruling                           */
  --line-soft:#c7d0da; /* dashed ruling                          */
  --trace:#c9c9c9;     /* filled grey glyph, trace over it       */
  --outline:#bdbdbd;   /* hollow outline glyph                   */
  --faint:#e3e3e3;
}
@page{ size:A4; margin:11mm 10mm 12mm 10mm; }
*{ box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
html,body{ margin:0; padding:0; background:#fff; }
body{
  font-family:'Noto Serif Bengali','Noto Sans Bengali',serif;
  color:var(--ink);
  font-size:10pt;
}
.deva{ font-family:'Noto Serif Devanagari','Devanagari Sangam MN','Kohinoor Devanagari',serif; }

.sheet{ page-break-after:always; break-after:page; position:relative; min-height:262mm; }
.sheet:last-child{ page-break-after:auto; break-after:auto; }

/* ---------- page head ---------- */
.ph{ display:flex; align-items:flex-end; justify-content:space-between;
     border-bottom:0.5mm solid var(--ink); padding-bottom:2mm; margin-bottom:3mm; }
.ph-l{ display:flex; align-items:flex-end; gap:5mm; }
.ph .big{ font-size:22mm; line-height:0.95; }
.ph .meta{ padding-bottom:1.5mm; }
.ph .eq{ font-size:13pt; color:var(--ink); }
.ph .eq b{ color:var(--sindoor); }
.ph .tr{ font-family:'JetBrains Mono',monospace; font-size:9pt; color:var(--sindoor); letter-spacing:.04em; }
.ph .ex{ font-size:10pt; color:var(--faded); margin-top:1mm; }
.ph-r{ text-align:right; padding-bottom:1.5mm; }
.ph-r .grp{ font-size:9pt; color:var(--faded); }
.ph-r .num{ font-family:'JetBrains Mono',monospace; font-size:8pt; color:var(--faded); letter-spacing:.14em; }

/* ---------- two-step shirorekha illustration ---------- */
.steps{ display:flex; gap:4mm; align-items:flex-end; margin:0 0 3mm; }
.step{ border:0.3mm dashed var(--line-soft); border-radius:1mm; padding:1.5mm 3mm 1mm;
       text-align:center; position:relative; }
.step .g{ font-size:16mm; line-height:1.05; position:relative; display:inline-block; }
.step .mask{ position:absolute; left:-1mm; right:-1mm; top:0; height:2.6mm; background:#fff; }
.step .cap{ font-size:8pt; color:var(--faded); margin-top:0.5mm; }
.step .cap b{ color:var(--teal); }
.steps .note{ font-size:9pt; color:var(--ink); line-height:1.5; padding-bottom:2mm; flex:1; }
.steps .note b{ color:var(--sindoor); }

/* ---------- practice rows ---------- */
.rowlabel{ font-size:8.5pt; color:var(--faded); margin:0 0 0.8mm; display:flex;
           justify-content:space-between; align-items:baseline; }
.rowlabel b{ color:var(--teal); font-weight:600; }
/* Only --head and --base differ between row types; the glyph size, the two
   dashed guide lines and the row height all derive from them. */
.row{ position:relative; margin-bottom:2.2mm;
      --gs:   calc((var(--base) - var(--head)) / var(--asc-ratio));
      --asc:  calc(var(--head) - var(--top-ratio) * var(--gs));
      --desc: calc(var(--base) + var(--bot-ratio) * var(--gs));
      height: calc(var(--desc) + 1.5mm); }
.row .ln{ position:absolute; left:0; right:0; height:0; }
.ln.a{ top:var(--asc);  border-top:0.25mm dashed var(--line-soft); }
.ln.h{ top:var(--head); border-top:0.4mm solid var(--line); }
.ln.b{ top:var(--base); border-top:0.4mm solid var(--line); }
.ln.d{ top:var(--desc); border-top:0.25mm dashed var(--line-soft); }
/* The strut is an inline-block whose bottom edge sits on the text baseline,
   so the baseline lands exactly on --base whatever the font's line metrics. */
.row .cells{ position:absolute; left:0; right:0; top:0;
             display:flex; justify-content:flex-start; line-height:0; }
.st{ display:inline-block; width:0; height:var(--base); vertical-align:baseline; }
.row .c{ font-size:var(--gs); line-height:0; flex:0 0 auto; width:24mm; text-align:center; }

/* word and sentence rows: tighter band so long strings fit the page width */
.row.words{ --head:6.5mm; --base:14mm; }
.row.words .c{ width:auto; padding-right:10mm; text-align:left; }
.row.sent{ --head:5.5mm; --base:11.5mm; }
.row.sent .cells{ display:block; }
.row.sent .c{ display:block; width:auto; text-align:left; }

.t-model{ color:var(--ink); }
.t-trace{ color:var(--trace); }
.t-out{ color:transparent; -webkit-text-stroke:0.28mm var(--outline); }
.t-faint{ color:var(--faint); }

/* vertical start ticks in blank rows */
.row.blank .cells .c{ color:transparent; }
.tick{ position:absolute; top:var(--head); height:calc(var(--base) - var(--head));
       border-left:0.25mm dotted var(--line-soft); }

/* ---------- cover ---------- */
.cover{ text-align:center; padding-top:22mm; }
.cover .kicker{ font-family:'JetBrains Mono',monospace; font-size:9pt; letter-spacing:.3em;
                text-transform:uppercase; color:var(--sindoor); }
.cover h1{ font-size:30pt; margin:6mm 0 2mm; line-height:1.25; }
.cover h1 .deva{ display:block; font-size:34pt; color:var(--ink); margin-bottom:3mm; }
.cover .sub{ font-size:12pt; color:var(--faded); max-width:135mm; margin:0 auto; line-height:1.7; }
.rules{ text-align:left; max-width:150mm; margin:12mm auto 0; }
.rules h2{ font-size:12pt; margin:0 0 3mm; color:var(--sindoor); }
.rules ol{ padding-left:6mm; margin:0; }
.rules li{ margin-bottom:3mm; line-height:1.65; font-size:10.5pt; }
.rules li b{ color:var(--teal); }
.legend{ margin:10mm auto 0; max-width:150mm; border:0.3mm solid var(--line-soft);
         border-radius:1.5mm; padding:4mm 5mm; }
.legend h3{ margin:0 0 2.5mm; font-size:10pt; color:var(--teal); }
.legend .lg{ display:flex; gap:7mm; align-items:flex-end; }
.legend .lg div{ text-align:center; font-size:8.5pt; color:var(--faded); }
.legend .lg .s{ font-size:13mm; line-height:1.1; display:block; }
.cover .foot{ position:absolute; bottom:6mm; left:0; right:0; text-align:center;
              font-family:'JetBrains Mono',monospace; font-size:8pt; letter-spacing:.16em;
              text-transform:uppercase; color:var(--sindoor); }

/* ---------- running footer ---------- */
.pf{ position:absolute; bottom:0; left:0; right:0; display:flex; justify-content:space-between;
     border-top:0.25mm solid var(--line-soft); padding-top:1.5mm;
     font-size:8pt; color:var(--faded); }
.pf .r{ font-family:'JetBrains Mono',monospace; letter-spacing:.1em; }
"""

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Noto+Serif+Bengali:wght@400;500;600;700"
         "&family=Noto+Serif+Devanagari:wght@400;500;600;700"
         "&family=JetBrains+Mono:wght@400;500&display=swap")

def page_head(title):
    return f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8"/>
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="{FONTS}" rel="stylesheet"/>
<style>{STYLE}</style>
</head>
<body>
"""

def row(cells_html, label_left, label_right="", cls=""):
    return f"""<div class="rowlabel"><span>{label_left}</span><span>{label_right}</span></div>
<div class="row {cls}">
  <div class="ln a"></div><div class="ln h"></div><div class="ln b"></div><div class="ln d"></div>
  <div class="cells">{cells_html}</div>
</div>"""

def cells(glyph, n, cls):
    return "".join(f'<span class="c deva {cls}"><i class="st"></i>{glyph}</span>' for _ in range(n))

def footer(book, n):
    return (f'<div class="pf"><span>{html.escape(book)}</span>'
            f'<span class="r">BHASHASETU &middot; বাংলা থেকে হিন্দি &middot; {n}</span></div>')

def cover(book_no, deva_title, bn_title, sub, rules, extra_legend=True):
    lg = ""
    if extra_legend:
        lg = """<div class="legend"><h3>এই বইয়ে চার রকম লেখা</h3><div class="lg">
        <div><span class="s deva t-model">क</span>নমুনা - দেখে নাও</div>
        <div><span class="s deva t-trace">क</span>ধূসর - উপর দিয়ে টানো</div>
        <div><span class="s deva t-out">क</span>ফাঁপা - ভেতরটা ভরো</div>
        <div><span class="s deva t-faint">क</span>ক্ষীণ - প্রায় একা</div>
        </div></div>"""
    ol = "".join(f"<li>{r}</li>" for r in rules)
    return f"""<div class="sheet cover">
  <div class="kicker">খাতা {book_no}</div>
  <h1><span class="deva">{deva_title}</span>{bn_title}</h1>
  <p class="sub">{sub}</p>
  <div class="rules"><h2>লেখার আগে পাঁচটি কথা</h2><ol>{ol}</ol></div>
  {lg}
  <div class="foot">made by Nil &middot; using Claude</div>
</div>"""


CONJUNCT_RULES = [
    "<b>নিয়ম শেখো, তালিকা নয়।</b> দেবনাগরীতে ৩৩টি ব্যঞ্জনের জোড়া হাজারের বেশি হতে পারে - সব লেখা অসম্ভব, দরকারও নেই। এই খাতায় চারটি <b>নিয়ম</b> আর তাদের প্রতিটি চালু জোড় আছে। নিয়ম ধরলে বাকিগুলো নিজেই আসবে।",
    "<b>এক: দাঁড়ি কেটে (আধা অক্ষর)।</b> বাঁদিকের অক্ষরের খাড়া দাঁড়িটা কেটে দাও, তারপর পরেরটা জুড়ে দাও - স + ত = স্ত। যাদের দাঁড়ি নেই (ট, ড, ঠ), তারা একটার নিচে আরেকটা বসে।",
    "<b>দুই: র-এর দুই চেহারা।</b> র <i>আগে</i> থাকলে পরের অক্ষরের মাথায় উঠে যায় - ধর্ম। র <i>পরে</i> থাকলে আগের অক্ষরের পায়ে হেলানো দাগ হয় - প্রেম।",
    "<b>তিন: কয়েকটা মুখস্থ।</b> ক্ষ, জ্ঞ, ত্র, শ্র, দ্য, দ্ধ - এদের চেহারায় টুকরো দুটো আর চেনা যায় না। বাংলাতেও ঠিক তাই: ক্ষ দেখে ক আর ষ আলাদা বোঝা যায় না।",
    "<b>চার: বাংলা তোমাকে এগিয়ে রেখেছে।</b> যুক্তাক্ষর বাংলারও আছে, আর অনেকগুলো <i>একই জোড়</i> - ক্ষ = ক্ষ, জ্ঞ = জ্ঞ, স্ত = স্ত। ধারণা এক, শুধু আঁকার ভঙ্গি আলাদা।",
]

COMMON_RULES = [
    "<b>শিরোরেখা সবার শেষে।</b> বাংলায় তুমি যেমন আগে অক্ষরের শরীর লেখো, তারপর মাথায় মাত্রা টানো - দেবনাগরীতেও ঠিক তাই। অভ্যাসটা তোমার আগে থেকেই আছে।",
    "<b>অক্ষর ঝোলে, বসে না।</b> মোটা উপরের রেখা থেকে অক্ষর <i>ঝুলে</i> থাকে, আর নিচের রেখায় পা রাখে। দুই রেখার মাঝখানটুকুই অক্ষরের শরীর।",
    "<b>উপরের-নিচের ছেঁড়া রেখা মাত্রার জন্য।</b> কি, কী, কে, কৈ উপরে যায়; কু, কূ, কৃ নিচে নামে। ওই দুটি ছেঁড়া রেখা তাদের সীমানা।",
    "<b>ধীরে। দিনে এক পাতা যথেষ্ট।</b> হাত শেখে পুনরাবৃত্তিতে, তাড়াহুড়োয় নয়। প্রতিটি সারি শেষ করে একবার জোরে উচ্চারণ করো।",
    "<b>পেনসিল দিয়ে শুরু করো।</b> ধূসর অক্ষরের উপর দিয়ে টানার সময় চাপ কম রাখো; ফাঁপা অক্ষরের ভেতরটা ভরার সময় প্রান্ত ছুঁয়ে থাকো।",
]


# Rough advance width of Devanagari in Noto Serif Devanagari, as a fraction of
# the font size. Used only to warn when a sentence would overrun the ruling.
ADVANCE = 0.55
def check_width(text, band_mm, label):
    gs = band_mm / 0.642            # same derivation the CSS uses
    est = len(text) * ADVANCE * gs
    if est > 185:
        print(f"  !! too wide ({est:.0f}mm > 185mm): {label} :: {text}")
        return False
    return True

# ---------------------------------------------------------------- pages
def letter_sheet(book, n, deva, bn, tr, ex, exgloss, group, note=None):
    steps_note = note or ("বাংলার মতোই: আগে অক্ষরের <b>শরীর</b>, সবার শেষে মাথার "
                          "<b>শিরোরেখা</b>। ডানদিকের দুটি বাক্স সেই ক্রম দেখাচ্ছে।")
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l">
      <div class="big deva">{deva}</div>
      <div class="meta">
        <div class="eq">= <b>{bn}</b></div>
        <div class="tr">{tr}</div>
        <div class="ex"><span class="deva">{ex}</span> &middot; {exgloss}</div>
      </div>
    </div>
    <div class="ph-r"><div class="grp">{group}</div><div class="num">{n:02d}</div></div>
  </div>

  <div class="steps">
    <div class="step"><span class="g deva">{deva}<span class="mask"></span></span>
      <div class="cap"><b>১</b> শরীর</div></div>
    <div class="step"><span class="g deva">{deva}</span>
      <div class="cap"><b>২</b> শিরোরেখা</div></div>
    <div class="note">{steps_note}</div>
  </div>

  {row(cells(deva,7,'t-trace'), 'ধূসর অক্ষরের <b>উপর দিয়ে</b> টানো', 'সাত বার')}
  {row(cells(deva,7,'t-out'), 'ফাঁপা অক্ষরের <b>ভেতরটা ভরো</b>', 'সাত বার')}
  {row('<span class="c deva t-model"><i class="st"></i>'+deva+'</span><span class="c deva t-faint"><i class="st"></i>'+deva+'</span>',
       'শুরুটা দেওয়া আছে - <b>বাকিটা নিজে</b>', 'সারি শেষ করো')}
  {row('', 'নিজে লেখো', 'সারি ভরাও')}
  {row('', 'নিজে লেখো', '')}

  {row('<span class="c deva t-model"><i class="st"></i>'+ex+'</span><span class="c deva t-trace"><i class="st"></i>'+ex+'</span>'+('<span class="c deva t-out"><i class="st"></i>'+ex+'</span>' if len(ex)<=4 else ''),
       f'শব্দে বসাও - <span class="deva">{ex}</span> ({exgloss})', 'তারপর নিজে', 'words')}
  {footer(book, n)}
</div>"""

def matra_sheet(book, n, form, bn, tr, note):
    others = ["ख","ग","म","स"]
    base = form[0]
    sign = form[1:]
    applied = "".join(f'<span class="c deva t-model"><i class="st"></i>{c}{sign}</span>'
                      f'<span class="c deva t-trace"><i class="st"></i>{c}{sign}</span>'
                      f'<span class="c deva t-out"><i class="st"></i>{c}{sign}</span>' for c in others[:2])
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l">
      <div class="big deva">{form}</div>
      <div class="meta">
        <div class="eq">= <b>{bn}</b></div>
        <div class="tr">{tr}</div>
        <div class="ex">{note}</div>
      </div>
    </div>
    <div class="ph-r"><div class="grp">মাত্রা / বারাখড়ি</div><div class="num">{n:02d}</div></div>
  </div>

  <div class="steps">
    <div class="step"><span class="g deva">{base}</span><div class="cap"><b>১</b> ব্যঞ্জন</div></div>
    <div class="step"><span class="g deva">{form}</span><div class="cap"><b>২</b> + চিহ্ন</div></div>
    <div class="note">বাংলায় ক + া = কা। হিন্দিতে <span class="deva">{base}</span> + চিহ্ন =
      <span class="deva">{form}</span>। <b>নিয়মটা তোমার জানা</b> - শুধু চেহারা নতুন।</div>
  </div>

  {row(cells(form,7,'t-trace'), 'ধূসরের <b>উপর দিয়ে</b>', 'সাত বার')}
  {row(cells(form,7,'t-out'), '<b>ভেতরটা ভরো</b>', 'সাত বার')}
  {row('<span class="c deva t-model"><i class="st"></i>'+form+'</span><span class="c deva t-faint"><i class="st"></i>'+form+'</span>',
       'শুরুটা দেওয়া আছে - <b>বাকিটা নিজে</b>', 'সারি শেষ করো')}
  {row(applied, 'একই চিহ্ন <b>অন্য ব্যঞ্জনে</b>', 'তারপর নিজে')}
  {row('', 'নিজে লেখো', '')}
  {footer(book, n)}
</div>"""


def conjunct_sheet(book, n, items):
    blocks = ""
    for cj, a, bpart, ex, gloss, grp in items:
        check_width(ex, 7.5, f"যুক্তাক্ষর {n}")
        label = (f'<span class="deva" style="font-size:13pt">{a}</span> + '
                 f'<span class="deva" style="font-size:13pt">{bpart}</span> = '
                 f'<span class="deva" style="font-size:15pt"><b>{cj}</b></span>'
                 f' &nbsp;&middot;&nbsp; <span class="deva">{ex}</span> ({gloss})')
        blocks += row(cells(cj, 7, 't-trace'), label, 'ধূসরের উপর দিয়ে')
        blocks += row(cells(cj, 4, 't-out') +
                      '<span class="c deva t-model"><i class="st"></i>' + cj + '</span>',
                      'ভেতরটা ভরো, তারপর নিজে', '')
        blocks += row('<span class="c deva t-model"><i class="st"></i>' + ex + '</span>'
                      '<span class="c deva t-trace"><i class="st"></i>' + ex + '</span>',
                      f'শব্দে বসাও', 'তারপর নিজে', 'words')
        blocks += row('', '', 'নিজে লেখো', 'words')
    grp = items[0][5]
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:15pt"><b>{grp}</b></div>
      <div class="ex">বাংলাতেও যুক্তাক্ষর আছে - ক্ষ = ক + ষ, জ্ঞ = জ + ঞ। ধারণাটা তোমার জানা; এখানে শুধু চেহারা নতুন।</div>
    </div></div>
    <div class="ph-r"><div class="grp">যুক্তাক্ষর</div><div class="num">{n:02d}</div></div>
  </div>
  {blocks}
  {footer(book, n)}
</div>"""

def words_sheet(book, n, group, items):
    blocks = ""
    for w, g in items:
        blocks += row(f'<span class="c deva t-model"><i class="st"></i>{w}</span>'
                      f'<span class="c deva t-trace"><i class="st"></i>{w}</span>',
                      f'<span class="deva" style="font-size:12pt">{w}</span> &nbsp; = &nbsp; <b>{g}</b>',
                      'শুরুটা দেওয়া আছে', 'words')
        blocks += row('', '', 'নিজে লেখো', 'words')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:16pt"><b>{group}</b></div>
      <div class="ex">প্রথম দুটি দেওয়া আছে - নমুনা আর ধূসর। তারপর সারির বাকিটা তোমার।</div>
    </div></div>
    <div class="ph-r"><div class="grp">শব্দ</div><div class="num">{n:02d}</div></div>
  </div>
  {blocks}
  {footer(book, n)}
</div>"""

def sentence_sheet(book, n, items):
    blocks = ""
    for hi, bn in items:
        check_width(hi, 6.0, f"বাক্য {n}")   # .row.sent band = 11.5 - 5.5 mm
        blocks += f'<div class="rowlabel"><span><b>{bn}</b></span><span>নমুনা &rarr; ধূসর &rarr; নিজে</span></div>'
        blocks += row(f'<span class="c deva t-model"><i class="st"></i>{hi}</span>', '', '', 'sent')
        blocks += row(f'<span class="c deva t-trace"><i class="st"></i>{hi}</span>', 'ধূসরের উপর দিয়ে', '', 'sent')
        blocks += row('', 'নিজে লেখো', '', 'sent')
        blocks += row('', '', '', 'sent')
        blocks += row('', '', '', 'sent')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:16pt"><b>বাক্য লেখা</b></div>
      <div class="ex">একটানা শিরোরেখা শব্দের শেষ পর্যন্ত - তারপর ফাঁক। ওটাই দেবনাগরীর ছন্দ।</div>
    </div></div>
    <div class="ph-r"><div class="grp">বাক্য</div><div class="num">{n:02d}</div></div>
  </div>
  {blocks}
  {footer(book, n)}
</div>"""

# ---------------------------------------------------------------- books
def build():
    os.makedirs(OUT, exist_ok=True)
    made = []

    # ---- book 1: vowels
    b = "খাতা ১ · স্বরবর্ণ"
    p = [cover("১", "स्वर", "স্বরবর্ণ",
               "তেরোটি স্বরবর্ণ। বাংলায় তুমি এগুলো চেনো - এখানে শুধু নতুন চেহারা। "
               "প্রতিটি পাতায় একটি অক্ষর, ছয়টি সারি।", COMMON_RULES)]
    for i, (d, bn, tr, ex, g) in enumerate(VOWELS, 1):
        p.append(letter_sheet(b, i, d, bn, tr, ex, g, "স্বরবর্ণ"))
    made.append(("01_svarabarna", "স্বরবর্ণ", p))

    # ---- book 2: consonants
    b = "খাতা ২ · ব্যঞ্জনবর্ণ"
    p = [cover("২", "व्यंजन", "ব্যঞ্জনবর্ণ",
               "তেত্রিশটি ব্যঞ্জন, বর্গ অনুসারে - ঠিক বর্ণপরিচয়ের ক্রমে। "
               "শেষে সাতটি নুক্তা-অক্ষর, যার দুটি তোমার চেনা ড় আর ঢ়।", COMMON_RULES)]
    for i, (d, bn, tr, ex, g, varga) in enumerate(CONSONANTS, 1):
        p.append(letter_sheet(b, i, d, bn, tr, ex, g, varga))
    for j, (d, bn, tr, ex, g, varga) in enumerate(NUKTA, len(CONSONANTS)+1):
        note = ("বাংলার <b>ড়</b> / <b>ঢ়</b> হিন্দিতে নিচে একটি বিন্দু দিয়ে লেখা হয় - "
                "<b>নুক্তা</b>। বিন্দুটি সবার শেষে বসাও।") if d in ("ड़","ढ़") else \
               ("নুক্তা = নিচে একটি বিন্দু। শরীর আগে, শিরোরেখা তারপর, <b>বিন্দু সবার শেষে</b>।")
        p.append(letter_sheet(b, j, d, bn, tr, ex, g, varga, note))
    made.append(("02_byanjanbarna", "ব্যঞ্জনবর্ণ", p))

    # ---- book 3: matra
    b = "খাতা ৩ · মাত্রা"
    p = [cover("৩", "मात्रा", "স্বরচিহ্ন / বারাখড়ি",
               "বিদ্যাসাগরের চাল: বারোটি চিহ্ন শিখলে তেত্রিশটি ব্যঞ্জনে বসিয়ে "
               "চারশোর বেশি অক্ষর পাওয়া যায়। এখানে ক-এর বারাখড়ি।", COMMON_RULES)]
    for i, (f, bn, tr, note) in enumerate(MATRA, 1):
        p.append(matra_sheet(b, i, f, bn, tr, note))
    made.append(("03_matra", "মাত্রা", p))

    # ---- book 4: conjuncts, grouped by the rule that forms them
    b = "খাতা ৪ · যুক্তাক্ষর"
    p = [cover("৪", "संयुक्ताक्षर", "যুক্তাক্ষর",
               "দুই ব্যঞ্জন এক শ্বাসে - অচ্ছা-র চ্ছ, ক্ষমা-র ক্ষ। ছেষট্টিটি জোড়, "
               "নিয়ম অনুসারে সাজানো। নিয়মটা ধরতে পারলে তালিকায় না-থাকা জোড়ও লিখতে পারবে।",
               CONJUNCT_RULES)]
    i = 1
    grouped = {}
    for c in CONJUNCTS:
        grouped.setdefault(c[5], []).append(c)
    for grp, items in grouped.items():
        for k in range(0, len(items), 2):
            p.append(conjunct_sheet(b, i, items[k:k+2])); i += 1
    made.append(("04_juktakshar", "যুক্তাক্ষর", p))

    # ---- books 5 and 6: words, easy then hard
    word_books = [
        ("05_shabda_1", "শব্দ ১", "৫", WORDS1,
         "সহজ শব্দ। কোনো যুক্তাক্ষর নেই, কোনো নুক্তা নেই - সব ছোট শব্দ, "
         "সরল মাত্রা। প্রতিটি সারিতে প্রথম দুটি দেওয়া আছে।",
         "শব্দ ১ · সহজ"),
        ("06_shabda_2", "শব্দ ২", "৬", WORDS2,
         "কঠিন শব্দ। এখানে যুক্তাক্ষর (ক্ষ, জ্ঞ, ত্র, স্ত), নুক্তা (ড়, ঢ়, জ়, ফ়) "
         "আর লম্বা শব্দ। খাতা ৪ আর ৫ শেষ করে তবেই এখানে এসো।",
         "শব্দ ২ · কঠিন"),
    ]
    for slug, title, num, data, sub, running in word_books:
        b = f"খাতা {num} · {title}"
        p = [cover(num, "शब्द", title, sub, COMMON_RULES)]
        i = 1
        for group, items in data.items():
            for k in range(0, len(items), 4):
                p.append(words_sheet(b, i, group, items[k:k+4])); i += 1
        made.append((slug, title, p))

    # ---- books 7 and 8: sentences, easy then hard
    sent_books = [
        ("07_bakya_1", "বাক্য ১", "৭", SENTENCES1,
         "সহজ বাক্য - তিন থেকে পাঁচটি শব্দ। প্রতিটি শব্দ তুমি খাতা ৫-এ লিখেছ। "
         "একটানা শিরোরেখা শব্দের শেষ পর্যন্ত, তারপর ফাঁক।"),
        ("08_bakya_2", "বাক্য ২", "৮", SENTENCES2,
         "লম্বা বাক্য - প্রশ্ন, নাকার, যুক্তাক্ষর। শব্দগুলো খাতা ৬ থেকে। "
         "ধীরে লেখো; শব্দের ফাঁক ঠিক রাখাই এখানে আসল পরীক্ষা।"),
    ]
    for slug, title, num, data, sub in sent_books:
        b = f"খাতা {num} · {title}"
        p = [cover(num, "वाक्य", title, sub, COMMON_RULES)]
        for i in range(0, len(data), 2):
            p.append(sentence_sheet(b, i//2 + 1, data[i:i+2]))
        made.append((slug, title, p))

    index_rows = ""
    for slug, title, pages in made:
        fn = f"{slug}.html"
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write(
            page_head(f"{title} - বাংলা থেকে হিন্দি হাতের লেখা") + "\n".join(pages) + "\n</body>\n</html>")
        print(f"  {fn:<26} {len(pages):>3} pages")
        index_rows += (f'<tr><td><b>{title}</b></td><td>{len(pages)}</td>'
                       f'<td><a href="{slug}.pdf">PDF</a></td>'
                       f'<td><a href="{fn}">HTML</a></td></tr>')
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
        page_head("হাতের লেখার খাতা - বাংলা থেকে হিন্দি") +
        f"""<div style="max-width:150mm;margin:20mm auto;font-size:11pt">
        <h1 style="font-size:20pt">হাতের লেখার খাতা</h1>
        <p style="color:#6B5B48;line-height:1.7">বাংলা থেকে হিন্দি - দেবনাগরী লেখা শেখার আটটি খাতা।
        ছাপিয়ে নাও (A4, ১০০% আকারে, "fit to page" বন্ধ রেখো)।</p>
        <table style="width:100%;border-collapse:collapse;margin-top:8mm">{index_rows}</table></div>
        </body></html>""")
    total = sum(len(p) for _, _, p in made)
    print(f"  total {total} pages")

if __name__ == "__main__":
    build()

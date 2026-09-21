#!/usr/bin/env python3
"""
BHASHASETU handwriting worksheets - Perso-Arabic target (Urdu).

Separate from gen_worksheets.py because almost nothing carries over from a
Devanagari target:

  * direction is right to left
  * letters SIT ON a baseline; they do not hang from a headline, so the ruling
    is one solid baseline with an ascender zone above and a deep descender
    zone below, not Devanagari's two-line band
  * a letter has four positional shapes, which is the whole first lesson
  * short vowels are marks that are usually not written at all
  * Nastaliq cascades down-leftwards inside a ligature, so a word occupies a
    diagonal and the descender zone has to be generous

Metrics measured with canvas TextMetrics on Noto Nastaliq Urdu
(see calibrate_nastaliq.html), as fractions of the font size from the baseline:
    ascenders  ا ل ک .......... 0.714 up
    x-height   ب س ر .......... 0.31  up
    descenders most ........... 0.19  down
    descender  م .............. 0.383 down   <- deepest, sets the floor

Usage:  python3 gen_worksheets_urdu.py
"""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
PAIR = "bengali_to_urdu"
OUT  = os.path.join(HERE, PAIR)
ZWJ  = "‍"

def D(n):
    return "".join("০১২৩৪৫৬৭৮৯"[int(c)] for c in str(n))

def forms(ch, joins_left=True):
    """The four positional shapes, composed with ZWJ rather than hardcoded."""
    if not joins_left:                      # ا د ڈ ذ ر ڑ ز ژ و join only to the right
        return [ch, ZWJ + ch, ZWJ + ch, ch]
    return [ch, ZWJ + ch, ZWJ + ch + ZWJ, ch + ZWJ]

# ---------------------------------------------------------------- letters
# (letter, name, bengali equivalent, example, bengali gloss, joins_left, group)
LETTERS = [
 ("ا","আলিফ","আ / অ","اب","এখন",False,"আলিফ ও মদ"),
 ("آ","আলিফ মদ","আ",  "آم","আম",False,"আলিফ ও মদ"),
 ("ب","বে","ব","بات","কথা",True,"বে-পরিবার - এক আকার, ভিন্ন নুক্তা"),
 ("پ","পে","প","پانی","জল",True,"বে-পরিবার - এক আকার, ভিন্ন নুক্তা"),
 ("ت","তে","ত","تین","তিন",True,"বে-পরিবার - এক আকার, ভিন্ন নুক্তা"),
 ("ٹ","টে","ট","ٹوپی","টুপি",True,"বে-পরিবার - এক আকার, ভিন্ন নুক্তা"),
 ("ث","সে","স","ثمر","ফল",True,"বে-পরিবার - এক আকার, ভিন্ন নুক্তা"),
 ("ج","জিম","জ","جگہ","জায়গা",True,"জিম-পরিবার"),
 ("چ","চে","চ","چاند","চাঁদ",True,"জিম-পরিবার"),
 ("ح","বড়ি হে","হ","حال","অবস্থা",True,"জিম-পরিবার"),
 ("خ","খে","খ","خبر","খবর",True,"জিম-পরিবার"),
 ("د","দাল","দ","دن","দিন",False,"দাল-পরিবার - বাঁয়ে জোড়া লাগে না"),
 ("ڈ","ডাল","ড","ڈر","ভয়",False,"দাল-পরিবার - বাঁয়ে জোড়া লাগে না"),
 ("ذ","জাল","জ","ذات","জাত",False,"দাল-পরিবার - বাঁয়ে জোড়া লাগে না"),
 ("ر","রে","র","رات","রাত",False,"রে-পরিবার - বাঁয়ে জোড়া লাগে না"),
 ("ڑ","ড়ে","ড়","بڑا","বড়",False,"রে-পরিবার - বাঁয়ে জোড়া লাগে না"),
 ("ز","জে","জ","زمین","জমি",False,"রে-পরিবার - বাঁয়ে জোড়া লাগে না"),
 ("ژ","ঝে","ঝ","ژالہ","শিলাবৃষ্টি",False,"রে-পরিবার - বাঁয়ে জোড়া লাগে না"),
 ("س","সিন","স","سال","বছর",True,"সিন-পরিবার"),
 ("ش","শিন","শ","شام","সন্ধ্যা",True,"সিন-পরিবার"),
 ("ص","সোয়াদ","স","صبح","সকাল",True,"সোয়াদ ও তোয়ে"),
 ("ض","জোয়াদ","জ","ضرور","অবশ্যই",True,"সোয়াদ ও তোয়ে"),
 ("ط","তোয়ে","ত","طوطا","টিয়া",True,"সোয়াদ ও তোয়ে"),
 ("ظ","জোয়ে","জ","ظاہر","প্রকাশ্য",True,"সোয়াদ ও তোয়ে"),
 ("ع","আইন","আ / অ","عمر","বয়স",True,"আইন-পরিবার"),
 ("غ","গাইন","গ","غزل","গজল",True,"আইন-পরিবার"),
 ("ف","ফে","ফ","فون","ফোন",True,"ফে ও ক়াফ"),
 ("ق","ক়াফ","ক","قلم","কলম",True,"ফে ও ক়াফ"),
 ("ک","কাফ","ক","کتاب","বই",True,"কাফ ও গাফ"),
 ("گ","গাফ","গ","گھر","ঘর",True,"কাফ ও গাফ"),
 ("ل","লাম","ল","لڑکا","ছেলে",True,"লাম, মিম, নুন"),
 ("م","মিম","ম","مچھلی","মাছ",True,"লাম, মিম, নুন"),
 ("ن","নুন","ন","نام","নাম",True,"লাম, মিম, নুন"),
 ("ں","নুন গুন্না","ং","ماں","মা",False,"লাম, মিম, নুন"),
 ("و","ওয়াও","ও / ব","وقت","সময়",False,"ওয়াও - বাঁয়ে জোড়া লাগে না"),
 ("ہ","ছোটি হে","হ","ہاتھ","হাত",True,"হে-পরিবার"),
 ("ھ","দোচশমি হে","্হ (মহাপ্রাণ)","بھائی","ভাই",True,"হে-পরিবার"),
 ("ی","ছোটি ইয়ে","ই / য়","یہ","এটা",True,"ইয়ে-পরিবার"),
 ("ے","বড়ি ইয়ে","এ","کے","-এর",False,"ইয়ে-পরিবার"),
 ("ء","হামজ়া","(বিরতি)","کوئی","কেউ",False,"হে-পরিবার"),
]

# ---------------------------------------------------------------- harakat
# (mark shown on be, name, bengali, note)
HARAKAT = [
 ("بَ","জ়বর","ব‍্যা / বা (হ্রস্ব আ)","উপরে হেলানো দাগ। সাধারণত <b>লেখা হয় না</b> - পড়তে হয় অনুমানে।"),
 ("بِ","জ়ের","বি (হ্রস্ব ই)","নিচে হেলানো দাগ। এটিও সাধারণত লেখা হয় না।"),
 ("بُ","পেশ","বু (হ্রস্ব উ)","উপরে ছোট ওয়াও। এটিও লেখা হয় না।"),
 ("بْ","জ়জম","হসন্ত","অক্ষরে স্বর নেই - বাংলার হসন্তের কাজ।"),
 ("بّ","তশদীদ","দ্বিত্ব","অক্ষরটি দুবার - বাংলার যুক্তাক্ষরের মতো।"),
 ("با","আলিফ - দীর্ঘ আ","বা","দীর্ঘ স্বর <b>অক্ষর</b> দিয়ে লেখা হয়, চিহ্ন দিয়ে নয়।"),
 ("بی","ইয়ে - দীর্ঘ ঈ","বী","দীর্ঘ ই = ی, একটি পূর্ণ অক্ষর।"),
 ("بو","ওয়াও - দীর্ঘ ঊ / ও","বূ / বো","দীর্ঘ উ আর ও দুটোই و দিয়ে।"),
 ("بے","বড়ি ইয়ে - দীর্ঘ এ","বে","শব্দের শেষে এ-ধ্বনি।"),
 ("بں","নুন গুন্না","বং","নাসিক্য - বাংলার চন্দ্রবিন্দুর কাজ।"),
 ("بھ","দোচশমি হে","ভ","আগের অক্ষরকে মহাপ্রাণ করে: ب + ھ = ভ।"),
 ("آ","মদ","আ","আলিফের উপরে মদ = দীর্ঘ আ, শব্দের শুরুতে।"),
]

# ---------------------------------------------------------------- joining
# (word, bengali gloss, note) - joining practice, non-joiners and ligatures
JOINING = [
 ("لا","লা","লাম + আলিফ - সবচেয়ে চেনা যুক্তরূপ।"),
 ("الله","আল্লাহ","একটি আস্ত যুক্তরূপ, চেহারা মুখস্থ।"),
 ("بب","বব","দুই জোড়-লাগা অক্ষর।"),
 ("سس","সস","সিন পরপর - দাঁত গুনে নাও।"),
 ("مم","মম","মিমের লেজ নিচে নামে।"),
 ("در","দর","<b>দাল বাঁয়ে জোড়া লাগে না</b> - তাই ফাঁক।"),
 ("ارد","আর্দ","আলিফ আর দাল, দুটোই বাঁয়ে বন্ধ।"),
 ("اردو","উর্দু","চারটি অক্ষর, তিনটি বাঁয়ে বন্ধ।"),
 ("بازار","বাজ়ার","জ়ে-র পরে ফাঁক পড়ে।"),
 ("کتاب","কিতাব","কাফ-তে-আলিফ-বে: প্রথম দুটি জোড়া, তারপর বিরতি।"),
 ("پانی","পানী","পে-আলিফ / নুন-ইয়ে - দুই টুকরো।"),
 ("مچھلی","মছ্‌লী","লম্বা জোড় - নাস্তালিকের ঢাল দেখো।"),
 ("دوست","দোস্ত","দাল-ওয়াও বন্ধ, তারপর সিন-তে জোড়া।"),
 ("شکریہ","শুক্রিয়া","শিন-কাফ-রে-ইয়ে-হে।"),
 ("خوبصورت","খুবসূরত","লম্বা শব্দ, অনেক টুকরো।"),
 ("السلام علیکم","আসসালামু আলাইকুম","দুই শব্দ, ফাঁক রেখো।"),
]

# ---------------------------------------------------------------- words
WORDS1 = {
 "সর্বনাম": [("میں","আমি"),("تو","তুই"),("تم","তুমি"),("آپ","আপনি"),
              ("وہ","সে"),("یہ","এটা"),("ہم","আমরা"),("وے","তারা")],
 "নিত্য বিশেষ্য": [("گھر","ঘর"),("پانی","জল"),("نام","নাম"),("دن","দিন"),
                   ("رات","রাত"),("دودھ","দুধ"),("چاول","চাল"),("روٹی","রুটি"),
                   ("ہوا","হাওয়া"),("آگ","আগুন"),("پھول","ফুল"),("کام","কাজ")],
 "শরীর": [("ہاتھ","হাত"),("پاؤں","পা"),("سر","মাথা"),("منہ","মুখ"),
          ("ناک","নাক"),("کان","কান"),("آنکھ","চোখ"),("دانت","দাঁত")],
 "পরিবার": [("ماں","মা"),("باپ","বাবা"),("بھائی","ভাই"),("بہن","বোন"),
            ("بیٹا","ছেলে"),("بیٹی","মেয়ে"),("دادا","দাদা"),("نانا","নানা")],
 "রং ও গুণ": [("لال","লাল"),("کالا","কালো"),("سبز","সবুজ"),("پیلا","হলুদ"),
              ("نیلا","নীল"),("چھوٹا","ছোট"),("گرم","গরম"),("ٹھیک","ঠিক")],
 "সংখ্যা": [("ایک","এক"),("دو","দুই"),("تین","তিন"),("چار","চার"),("پانچ","পাঁচ"),
           ("چھ","ছয়"),("سات","সাত"),("آٹھ","আট"),("نو","নয়"),("دس","দশ")],
 "সাধারণ ক্রিয়া": [("آنا","আসা"),("جانا","যাওয়া"),("کھانا","খাওয়া"),("پینا","পান করা"),
                   ("دیکھنا","দেখা"),("سننا","শোনা"),("بولنا","বলা"),("چلنا","চলা"),
                   ("اٹھنا","ওঠা"),("سونا","ঘুমানো")],
}

WORDS2 = {
 "বাংলা যে শব্দগুলো আগেই ধার নিয়েছে": [("کتاب","কিতাব / বই"),("قلم","কলম"),("دکان","দোকান"),
     ("خبر","খবর"),("حساب","হিসাব"),("عدالت","আদালত"),("تاریخ","তারিখ"),("غریب","গরিব")],
 "আরও ধার-করা শব্দ": [("زمین","জমি"),("وقت","সময় / ওয়াক্ত"),("خیال","খেয়াল"),("عمر","বয়স"),
     ("دنیا","দুনিয়া"),("انسان","ইনসান / মানুষ"),("ہوشیار","হুঁশিয়ার"),("بازار","বাজার")],
 "দীর্ঘ শব্দ": [("مچھلی","মাছ"),("خوبصورت","সুন্দর"),("ضروری","দরকারি"),("مشکل","কঠিন"),
                ("آسان","সহজ"),("محبت","ভালোবাসা"),("دوستی","বন্ধুত্ব"),("زندگی","জীবন")],
 "শিক্ষা ও শহর": [("تعلیم","শিক্ষা"),("اسکول","স্কুল"),("ہسپتال","হাসপাতাল"),("کتابچہ","পুস্তিকা"),
                  ("اخبار","সংবাদপত্র"),("ملاقات","সাক্ষাৎ"),("مہربانی","মেহেরবানি"),("آزادی","স্বাধীনতা")],
 "কঠিন ক্রিয়া": [("سمجھنا","বোঝা"),("سیکھنا","শেখা"),("پہنچنا","পৌঁছানো"),("خریدنا","কেনা"),
                  ("بیچنا","বেচা"),("ملنا","দেখা করা"),("لکھنا","লেখা"),("پڑھنا","পড়া")],
 "ভাব ও অবস্থা": [("خوش","খুশি"),("اداس","উদাস"),("امید","আশা"),("فکر","চিন্তা"),
                  ("معلوم","জানা"),("معاف","মাফ"),("شکریہ","শুক্রিয়া"),("سلام","সালাম")],
 "সময় ও দিক": [("صبح","সকাল"),("شام","সন্ধ্যা"),("دوپہر","দুপুর"),("ہفتہ","সপ্তাহ"),
                ("مہینہ","মাস"),("سال","বছর"),("آج","আজ"),("کل","কাল")],
}

SENTENCES1 = [
 ("میرا نام رام ہے۔","আমার নাম রাম।"),("یہ میرا گھر ہے۔","এটা আমার ঘর।"),
 ("میں پانی پیتا ہوں۔","আমি জল খাই।"),("وہ روٹی کھاتا ہے۔","সে রুটি খায়।"),
 ("تم کہاں ہو؟","তুমি কোথায়?"),("میں گھر جاتا ہوں۔","আমি ঘরে যাই।"),
 ("یہ پھول لال ہے۔","এই ফুল লাল।"),("میری ماں آتی ہے۔","আমার মা আসেন।"),
 ("وہ میرا بھائی ہے۔","সে আমার ভাই।"),("آپ کا نام کیا ہے؟","আপনার নাম কী?"),
 ("دودھ گرم ہے۔","দুধ গরম।"),("وہ نہیں آتا۔","সে আসে না।"),
 ("مجھے پانی دو۔","আমাকে জল দাও।"),("یہاں آؤ۔","এখানে এসো।"),
 ("وہاں مت جاؤ۔","ওখানে যেও না।"),("میرے دو بھائی ہیں۔","আমার দুই ভাই।"),
 ("ہم صبح آتے ہیں۔","আমরা সকালে আসি।"),("تم بھی چلو۔","তুমিও চলো।"),
 ("میرا ہاتھ چھوٹا ہے۔","আমার হাত ছোট।"),("پانی ٹھنڈا ہے۔","জল ঠান্ডা।"),
 ("بیٹا سوتا ہے۔","ছেলে ঘুমোয়।"),("آج رات ہے۔","আজ রাত।"),
 ("وہ گانا گاتی ہے۔","সে গান গায়।"),("میں اردو سیکھتا ہوں۔","আমি উর্দু শিখি।"),
 ("یہ گھر نیا ہے۔","এই ঘর নতুন।"),("ہوا ٹھنڈی ہے۔","হাওয়া ঠান্ডা।"),
 ("کتاب میز پر ہے۔","বই টেবিলে আছে।"),("میں آج نہیں جاؤں گا۔","আমি আজ যাব না।"),
]

SENTENCES2 = [
 ("میں کولکاتا سے ہوں۔","আমি কলকাতা থেকে।"),
 ("میں روز کتاب پڑھتا ہوں۔","আমি রোজ বই পড়ি।"),
 ("وہ اسکول میں پڑھتی ہے۔","সে স্কুলে পড়ে।"),
 ("کیا آپ اردو بولتے ہیں؟","আপনি কি উর্দু বলেন?"),
 ("مجھے یہ شہر پسند ہے۔","আমার এই শহর ভালো লাগে।"),
 ("تھوڑا پانی دیجیے۔","একটু জল দিন।"),
 ("آج موسم اچھا ہے۔","আজ আবহাওয়া ভালো।"),
 ("میرے دوست کا نام ارجن ہے۔","আমার বন্ধুর নাম অর্জুন।"),
 ("ہم کل بازار جائیں گے۔","আমরা কাল বাজার যাব।"),
 ("اس نے مجھے خط لکھا۔","সে আমাকে চিঠি লিখেছে।"),
 ("یہ کتاب خوبصورت ہے۔","এই বই সুন্দর।"),
 ("کیا تم نے کھانا کھایا؟","তুমি কি খেয়েছ?"),
 ("وہ ہسپتال میں کام کرتا ہے۔","সে হাসপাতালে কাজ করে।"),
 ("مجھے اردو سیکھنی ہے۔","আমাকে উর্দু শিখতে হবে।"),
 ("تمہارا گھر کہاں ہے؟","তোমার ঘর কোথায়?"),
 ("وہ مل کر کام کرتے ہیں۔","তারা একসাথে কাজ করে।"),
 ("اس کمرے میں تین کرسیاں ہیں۔","এই ঘরে তিনটি চেয়ার আছে।"),
 ("بچے باغ میں کھیل رہے ہیں۔","বাচ্চারা বাগানে খেলছে।"),
 ("میں نے خبر نہیں پڑھی۔","আমি খবর পড়িনি।"),
 ("اسے موسیقی سننا پسند ہے۔","তার গান শুনতে ভালো লাগে।"),
 ("ہمیں وقت پر پہنچنا چاہیے۔","আমাদের সময়মতো পৌঁছাতে হবে।"),
 ("یہ سوال مشکل ہے۔","এই প্রশ্ন কঠিন।"),
 ("دکان نو بجے کھلتی ہے۔","দোকান নয়টায় খোলে।"),
 ("میری بہن ڈاکٹر ہے۔","আমার বোন ডাক্তার।"),
 ("شکریہ، آپ کی مہربانی۔","শুক্রিয়া, আপনার মেহেরবানি।"),
 ("میں بعد میں ملوں گا۔","আমি পরে দেখা করব।"),
 ("معاف کیجیے، دیر ہوئی۔","মাফ করবেন, দেরি হল।"),
 ("اردو اور بنگالی بہنیں ہیں۔","উর্দু আর বাংলা দুই বোন।"),
]

# ---------------------------------------------------------------- css
# One solid baseline; ascender and descender zones dashed. Everything derives
# from --base and the measured ratios, as in the Devanagari generator.
STYLE = """
:root{
  --base: 17mm;         /* the baseline - letters SIT on this */
  --gs:   15mm;         /* practice font size */
  --asc-ratio:  0.714;  /* ا ل ک reach this far above the baseline */
  --desc-ratio: 0.420;  /* م and the Nastaliq cascade reach this far below */
  --x-ratio:    0.310;  /* x-height of ب س ر, drawn as a faint guide */
  --ink:#1C1611; --faded:#6B5B48; --sindoor:#A83024; --teal:#1F4D4A;
  --line:#9aa8b8; --line-soft:#c7d0da;
  --trace:#c9c9c9; --outline:#bdbdbd; --faint:#e3e3e3;
}
@page{ size:A4; margin:11mm 10mm 12mm 10mm; }
*{ box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
html,body{ margin:0; padding:0; background:#fff; }
body{ font-family:'Noto Serif Bengali',serif; color:var(--ink); font-size:10pt; direction:ltr; }
.ur{ font-family:'Noto Nastaliq Urdu',serif; direction:rtl; unicode-bidi:isolate; }

.sheet{ page-break-after:always; break-after:page; position:relative; min-height:262mm; }
.sheet:last-child{ page-break-after:auto; break-after:auto; }

.ph{ display:flex; align-items:flex-end; justify-content:space-between;
     border-bottom:0.5mm solid var(--ink); padding-bottom:2mm; margin-bottom:3mm; }
.ph-l{ display:flex; align-items:flex-end; gap:6mm; }
.ph .big{ font-size:24mm; line-height:1.5; }
.ph .meta{ padding-bottom:2mm; }
.ph .eq{ font-size:13pt; } .ph .eq b{ color:var(--sindoor); }
.ph .nm{ font-size:11pt; color:var(--teal); }
.ph .ex{ font-size:10pt; color:var(--faded); margin-top:1mm; }
.ph-r{ text-align:right; padding-bottom:2mm; }
.ph-r .grp{ font-size:9pt; color:var(--faded); }
.ph-r .num{ font-size:9pt; color:var(--faded); letter-spacing:.14em; }

.note{ font-size:9.5pt; line-height:1.6; color:var(--ink); margin:0 0 3mm;
       padding:2mm 3mm; background:rgba(31,77,74,0.06); border-right:2mm solid var(--teal); }
.note b{ color:var(--sindoor); }

.rowlabel{ font-size:8.5pt; color:var(--faded); margin:0 0 0.8mm;
           display:flex; justify-content:space-between; align-items:baseline; }
.rowlabel b{ color:var(--teal); font-weight:600; }
.row{ position:relative; margin-bottom:2.4mm;
      --asc:  calc(var(--base) - var(--asc-ratio) * var(--gs));
      --xh:   calc(var(--base) - var(--x-ratio) * var(--gs));
      --desc: calc(var(--base) + var(--desc-ratio) * var(--gs));
      height: calc(var(--desc) + 2mm); }
.row .ln{ position:absolute; left:0; right:0; height:0; }
.ln.a{ top:var(--asc);  border-top:0.25mm dashed var(--line-soft); }
.ln.x{ top:var(--xh);   border-top:0.2mm dotted #dde3ea; }
.ln.b{ top:var(--base); border-top:0.45mm solid var(--line); }
.ln.d{ top:var(--desc); border-top:0.25mm dashed var(--line-soft); }
/* right-to-left: cells run from the right edge; the strut pins the baseline */
.row .cells{ position:absolute; left:0; right:0; top:0;
             display:flex; flex-direction:row; justify-content:flex-start;
             direction:rtl; line-height:0; }
.st{ display:inline-block; width:0; height:var(--base); vertical-align:baseline; }
.row .c{ font-family:'Noto Nastaliq Urdu',serif; font-size:var(--gs); line-height:0;
         flex:0 0 auto; padding-left:7mm; text-align:center; }
/* word and joining rows: a tighter band so eight rows fit one page */
.row.wide{ --base:13mm; --gs:12mm; }
.row.wide .c{ padding-left:12mm; }
.row.sent{ --gs:11mm; }
.row.sent .cells{ display:block; }
.row.sent .c{ display:block; padding:0; text-align:right; }

.t-model{ color:var(--ink); } .t-trace{ color:var(--trace); }
.t-out{ color:transparent; -webkit-text-stroke:0.25mm var(--outline); }
.t-faint{ color:var(--faint); }

.forms{ display:flex; gap:3mm; margin:0 0 3mm; direction:rtl; }
.formbox{ border:0.3mm dashed var(--line-soft); border-radius:1mm;
          padding:1mm 4mm 0.5mm; text-align:center; flex:1; }
.formbox .g{ font-family:'Noto Nastaliq Urdu',serif; font-size:13mm; line-height:2; }
.formbox .cap{ font-size:8pt; color:var(--faded); direction:ltr; }
.formbox .cap b{ color:var(--teal); }

.cover{ text-align:center; padding-top:22mm; }
.cover .kicker{ font-size:10pt; letter-spacing:.24em; color:var(--sindoor); }
.cover h1{ font-size:28pt; margin:6mm 0 2mm; line-height:1.3; }
.cover h1 .ur{ display:block; font-size:32pt; margin-bottom:5mm; line-height:2; }
.cover .sub{ font-size:12pt; color:var(--faded); max-width:140mm; margin:0 auto; line-height:1.75; }
.rules{ text-align:left; max-width:152mm; margin:10mm auto 0; }
.rules h2{ font-size:12pt; margin:0 0 3mm; color:var(--sindoor); }
.rules ol{ padding-left:6mm; margin:0; }
.rules li{ margin-bottom:3mm; line-height:1.7; font-size:10.5pt; }
.rules li b{ color:var(--teal); }
.cover .foot{ position:absolute; bottom:6mm; left:0; right:0; text-align:center;
              font-family:'JetBrains Mono',monospace; font-size:8pt; letter-spacing:.16em;
              text-transform:uppercase; color:var(--sindoor); }
.pf{ position:absolute; bottom:0; left:0; right:0; display:flex; justify-content:space-between;
     border-top:0.25mm solid var(--line-soft); padding-top:1.5mm; font-size:8pt; color:var(--faded); }
"""

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Noto+Serif+Bengali:wght@400;500;600;700"
         "&family=Noto+Nastaliq+Urdu:wght@400;500"
         "&family=JetBrains+Mono:wght@400;500&display=swap")

RULES = [
 "<b>ডান থেকে বাঁয়ে।</b> এটাই প্রথম আর সবচেয়ে বড় বদল। বাংলা বাঁ থেকে ডানে চলে; উর্দু ঠিক উল্টো। "
 "পাতার <b>ডান ধার</b> থেকে শুরু করো। কিন্তু সংখ্যা বাঁ থেকে ডানে - ২০২৬ উর্দুতেও ২০২৬।",
 "<b>অক্ষর রেখার উপরে বসে, ঝোলে না।</b> বাংলায় অক্ষর মাত্রা থেকে ঝোলে। উর্দুতে অক্ষর মোটা "
 "রেখার <b>উপরে</b> বসে; ا ل ک উপরে ওঠে, আর م ج ع ی-র লেজ নিচে নামে। উপরের-নিচের ছেঁড়া রেখা "
 "সেই দুই সীমানা।",
 "<b>এক অক্ষরের চার চেহারা।</b> শব্দের শুরুতে, মাঝে, শেষে আর একা - একই অক্ষর চার রকম দেখায়। "
 "এটাই উর্দু লেখার আসল পাঠ, আর বাংলায় এর কোনো সমান্তরাল নেই।",
 "<b>নয়টি অক্ষর বাঁয়ে জোড়া লাগে না।</b> ا د ڈ ذ ر ڑ ز ژ و - এদের পরে কলম তুলতে হয়, "
 "শব্দের মাঝেই ফাঁক পড়ে। এই ফাঁক ভুল নয়, নিয়ম।",
 "<b>হ্রস্ব স্বর সাধারণত লেখাই হয় না।</b> জ়বর, জ়ের, পেশ - এই তিন চিহ্ন বই আর কোরআন ছাড়া "
 "কোথাও বসে না। পড়ার সময় অনুমান করতে হয়। তাই এই খাতায় প্রতিটি শব্দের বাংলা উচ্চারণ "
 "<b>স্বর ভরে</b> দেওয়া আছে।",
]

# ---------------------------------------------------------------- pages
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

def row(cells_html, lab_l, lab_r="", cls=""):
    return f"""<div class="rowlabel"><span>{lab_l}</span><span>{lab_r}</span></div>
<div class="row {cls}">
  <div class="ln a"></div><div class="ln x"></div><div class="ln b"></div><div class="ln d"></div>
  <div class="cells">{cells_html}</div>
</div>"""

def one(txt, cls):
    return f'<span class="c {cls}"><i class="st"></i>{txt}</span>'
def cells(txt, n, cls):
    return "".join(one(txt, cls) for _ in range(n))
def footer(book, n):
    return (f'<div class="pf"><span>{html.escape(book)}</span>'
            f'<span>BHASHASETU &middot; বাংলা থেকে উর্দু &middot; {D(n)}</span></div>')

def cover(bno, ur_title, bn_title, sub, rules):
    ol = "".join(f"<li>{r}</li>" for r in rules)
    return f"""<div class="sheet cover">
  <div class="kicker">খাতা {bno}</div>
  <h1><span class="ur">{ur_title}</span>{bn_title}</h1>
  <p class="sub">{sub}</p>
  <div class="rules"><h2>লেখার আগে পাঁচটি কথা</h2><ol>{ol}</ol></div>
  <div class="foot">made by Nil &middot; using Claude</div>
</div>"""

TRACE, FILL, SELF = ("ধূসরের <b>উপর দিয়ে</b> টানো", "ফাঁপা অক্ষর <b>ভরো</b>", "নিজে লেখো")
RTL_HINT = "ডান দিক থেকে শুরু →"

def letter_sheet(book, n, ch, name, eq, ex, gloss, joins, group):
    iso, fin, med, ini = forms(ch, joins)
    jn = ("এই অক্ষর <b>বাঁয়ে জোড়া লাগে</b> - পরের অক্ষর এর সাথে যুক্ত হবে।" if joins else
          "⚡ এই অক্ষর <b>বাঁয়ে জোড়া লাগে না</b>। এর পরে কলম তুলতে হবে, শব্দের মাঝেই ফাঁক পড়বে।")
    fb = "".join(
        f'<div class="formbox"><div class="g ur">{g}</div><div class="cap"><b>{i}</b> {c}</div></div>'
        for i, (g, c) in enumerate([(iso,"একা"),(fin,"শেষে"),(med,"মাঝে"),(ini,"শুরুতে")], 1))
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l">
      <div class="big ur">{ch}</div>
      <div class="meta">
        <div class="nm">{name}</div>
        <div class="eq">= <b>{eq}</b></div>
        <div class="ex"><span class="ur">{ex}</span> &middot; {gloss}</div>
      </div>
    </div>
    <div class="ph-r"><div class="grp">{group}</div><div class="num">{D(n)}</div></div>
  </div>
  <div class="note">{jn}</div>
  <div class="forms">{fb}</div>
  {row(cells(iso,6,'t-trace'), TRACE, RTL_HINT)}
  {row(cells(iso,6,'t-out'), FILL, 'ছয় বার')}
  {row(one(iso,'t-model')+one(iso,'t-faint'), 'শুরুটা দেওয়া আছে - <b>বাকিটা নিজে</b>', 'সারি শেষ করো')}
  {row('', SELF, 'সারি ভরাও')}
  {row(one(ex,'t-model')+one(ex,'t-trace'), f'শব্দে বসাও - <span class="ur">{ex}</span> ({gloss})', 'তারপর নিজে', 'wide')}
  {footer(book, n)}
</div>"""

def forms_sheet(book, n, items):
    blocks = ""
    for ch, name, eq, ex, gloss, joins, _g in items:
        iso, fin, med, ini = forms(ch, joins)
        seq = [(ini,"শুরুতে"),(med,"মাঝে"),(fin,"শেষে"),(iso,"একা")]
        lab = (f'<span class="ur" style="font-size:12pt">{ch}</span> &nbsp; {name} &nbsp; = &nbsp; <b>{eq}</b>'
               + ("" if joins else ' &nbsp; <b style="color:#A83024">বাঁয়ে জোড়া লাগে না</b>'))
        blocks += row("".join(one(g,'t-model')+one(g,'t-trace') for g,_ in seq), lab, 'চার চেহারা', 'wide')
        blocks += row('', '', SELF, 'wide')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:15pt"><b>চার চেহারা</b></div>
      <div class="ex">ডান থেকে বাঁয়ে: শুরুতে · মাঝে · শেষে · একা</div>
    </div></div>
    <div class="ph-r"><div class="grp">চার শকল</div><div class="num">{D(n)}</div></div>
  </div>
  <div class="note">একই অক্ষর শব্দের কোথায় বসছে তার উপরে চেহারা বদলায়। <b>বাংলায় এর কোনো
  সমান্তরাল নেই</b> - এটাই উর্দু লেখার আসল অভ্যাস।</div>
  {blocks}
  {footer(book, n)}
</div>"""

def harakat_sheet(book, n, item):
    shown, name, bn, note = item
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l">
      <div class="big ur">{shown}</div>
      <div class="meta"><div class="nm">{name}</div><div class="eq">= <b>{bn}</b></div></div>
    </div>
    <div class="ph-r"><div class="grp">হরকত ও মদ</div><div class="num">{D(n)}</div></div>
  </div>
  <div class="note">{note}</div>
  {row(cells(shown,6,'t-trace'), TRACE, RTL_HINT)}
  {row(cells(shown,6,'t-out'), FILL, 'ছয় বার')}
  {row(one(shown,'t-model')+one(shown,'t-faint'), 'শুরুটা দেওয়া আছে', 'সারি শেষ করো')}
  {row('', SELF, '')}
  {row('', SELF, '')}
  {footer(book, n)}
</div>"""

def joining_sheet(book, n, items):
    blocks = ""
    for w, gloss, note in items:
        blocks += row(one(w,'t-model')+one(w,'t-trace')+one(w,'t-out'),
                      f'<span class="ur" style="font-size:13pt">{w}</span> &nbsp; <b>{gloss}</b> &nbsp; <span style="color:#6B5B48">{note}</span>',
                      RTL_HINT, 'wide')
        blocks += row('', '', SELF, 'wide')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:15pt"><b>জোড় দেওয়া</b></div>
      <div class="ex">কোথায় কলম চলবে, কোথায় তুলতে হবে</div>
    </div></div>
    <div class="ph-r"><div class="grp">জোড়</div><div class="num">{D(n)}</div></div>
  </div>
  {blocks}
  {footer(book, n)}
</div>"""

def words_sheet(book, n, group, items):
    blocks = ""
    for w, gloss in items:
        blocks += row(one(w,'t-model')+one(w,'t-trace'),
                      f'<span class="ur" style="font-size:13pt">{w}</span> &nbsp; = &nbsp; <b>{gloss}</b>',
                      RTL_HINT, 'wide')
        blocks += row('', '', SELF, 'wide')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:16pt"><b>{group}</b></div>
      <div class="ex">প্রথম দুটি দেওয়া আছে - নমুনা আর ধূসর। তারপর সারির বাকিটা তোমার।</div>
    </div></div>
    <div class="ph-r"><div class="grp">শব্দ</div><div class="num">{D(n)}</div></div>
  </div>
  {blocks}
  {footer(book, n)}
</div>"""

def sentence_sheet(book, n, items):
    blocks = ""
    for ur, bn in items:
        blocks += f'<div class="rowlabel"><span><b>{bn}</b></span><span>নমুনা &rarr; ধূসর &rarr; নিজে</span></div>'
        blocks += row(one(ur,'t-model'), '', '', 'sent')
        blocks += row(one(ur,'t-trace'), TRACE, '', 'sent')
        blocks += row('', SELF, '', 'sent')
        blocks += row('', '', '', 'sent')
    return f"""<div class="sheet">
  <div class="ph">
    <div class="ph-l"><div class="meta">
      <div class="eq" style="font-size:16pt"><b>বাক্য লেখা</b></div>
      <div class="ex">ডান ধার থেকে শুরু। শব্দের মাঝে ফাঁক, আর নাস্তালিকের ঢাল নিচের দিকে।</div>
    </div></div>
    <div class="ph-r"><div class="grp">বাক্য</div><div class="num">{D(n)}</div></div>
  </div>
  {blocks}
  {footer(book, n)}
</div>"""

# ---------------------------------------------------------------- build
def build():
    os.makedirs(OUT, exist_ok=True)
    made = []

    b = "খাতা ১ · হরফ"
    p = [cover("১", "حروف", "হরফ - বর্ণমালা",
               "চল্লিশটি হরফ, <b>আকার অনুসারে</b> সাজানো - বাংলা বর্ণক্রমে নয়। ب پ ت ٹ ث "
               "একই আকার, শুধু নুক্তা আলাদা; একটি চিনলে পাঁচটি চেনা হয়ে যায়।", RULES)]
    for i, L in enumerate(LETTERS, 1):
        p.append(letter_sheet(b, i, *L))
    made.append(("01_huruf", "হরফ", p))

    b = "খাতা ২ · চার শকল"
    p = [cover("২", "چار شکلیں", "চার চেহারা",
               "একই অক্ষর শব্দের শুরুতে, মাঝে, শেষে আর একা - চার রকম দেখায়। "
               "বাংলায় এর কোনো সমান্তরাল নেই, তাই এই খাতাটাই সবচেয়ে গুরুত্বপূর্ণ।", RULES)]
    joiners = [L for L in LETTERS if L[5]]
    for i, k in enumerate(range(0, len(joiners), 3), 1):
        p.append(forms_sheet(b, i, joiners[k:k+3]))
    made.append(("02_char_shakal", "চার চেহারা", p))

    b = "খাতা ৩ · হরকত"
    p = [cover("৩", "حرکات", "হরকত ও দীর্ঘ স্বর",
               "উর্দুতে হ্রস্ব স্বর <b>চিহ্ন</b>, আর সেই চিহ্ন সাধারণত লেখাই হয় না। "
               "দীর্ঘ স্বর কিন্তু পুরো <b>অক্ষর</b> - ا و ی ے। এই তফাৎটাই উর্দু পড়ার চাবি।", RULES)]
    for i, h in enumerate(HARAKAT, 1):
        p.append(harakat_sheet(b, i, h))
    made.append(("03_harakat", "হরকত", p))

    b = "খাতা ৪ · জোড়"
    p = [cover("৪", "جوڑ", "জোড় দেওয়া",
               "নয়টি অক্ষর বাঁয়ে জোড়া লাগে না: ا د ڈ ذ ر ڑ ز ژ و। এদের পরে কলম তুলতে হয়। "
               "শব্দের মাঝের সেই ফাঁক ভুল নয় - নিয়ম।", RULES)]
    for i, k in enumerate(range(0, len(JOINING), 2), 1):
        p.append(joining_sheet(b, i, JOINING[k:k+2]))
    made.append(("04_jor", "জোড়", p))

    for idx, (slug, data, easy) in enumerate([("05_alfaz_1", WORDS1, True), ("06_alfaz_2", WORDS2, False)]):
        num = D(5+idx); title = f"শব্দ {D(1+idx)}"
        b = f"খাতা {num} · {title}"
        sub = ("সহজ শব্দ - ছোট, রোজকার, বেশির ভাগই এক-দুই টুকরোর।" if easy else
               "কঠিন শব্দ। প্রথম দুটি দল লক্ষ করো: <b>এই শব্দগুলো বাংলা আগেই ধার নিয়েছে</b> - "
               "কিতাব, কলম, দোকান, খবর, হিসাব, আদালত, তারিখ। তুমি শব্দটা জানো, শুধু চেহারা নতুন।")
        p = [cover(num, "الفاظ", title, sub, RULES)]
        i = 1
        for group, items in data.items():
            for k in range(0, len(items), 4):
                p.append(words_sheet(b, i, group, items[k:k+4])); i += 1
        made.append((slug, title, p))

    for idx, (slug, data, easy) in enumerate([("07_jumle_1", SENTENCES1, True), ("08_jumle_2", SENTENCES2, False)]):
        num = D(7+idx); title = f"বাক্য {D(1+idx)}"
        b = f"খাতা {num} · {title}"
        sub = ("সহজ বাক্য - তিন থেকে পাঁচটি শব্দ, সবই খাতা ৫-এর।" if easy else
               "লম্বা বাক্য - প্রশ্ন, নাকার, লম্বা জোড়। শব্দগুলো খাতা ৬ থেকে।")
        p = [cover(num, "جملے", title, sub, RULES)]
        for i in range(0, len(data), 2):
            p.append(sentence_sheet(b, i//2 + 1, data[i:i+2]))
        made.append((slug, title, p))

    rows = ""
    for slug, title, pages in made:
        fn = f"{slug}.html"
        open(os.path.join(OUT, fn), "w", encoding="utf-8").write(
            page_head(f"{title} - বাংলা থেকে উর্দু হাতের লেখা") + "\n".join(pages) + "\n</body>\n</html>")
        print(f"  {fn:<24} {len(pages):>3} pages")
        rows += (f'<tr><td><b>{title}</b></td><td>{D(len(pages))}</td>'
                 f'<td><a href="{slug}.pdf">PDF</a></td><td><a href="{fn}">HTML</a></td></tr>')
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
        page_head("হাতের লেখার খাতা - বাংলা থেকে উর্দু") +
        f"""<div style="max-width:150mm;margin:20mm auto;font-size:11pt">
        <h1 style="font-size:20pt">হাতের লেখার খাতা</h1>
        <p style="color:#6B5B48;line-height:1.7">বাংলা থেকে উর্দু - নাস্তালিক লেখা শেখার আটটি খাতা।
        ছাপিয়ে নাও (A4, ১০০% আকারে, "fit to page" বন্ধ রেখো)।</p>
        <table style="width:100%;border-collapse:collapse;margin-top:8mm">{rows}</table></div>
        </body></html>""")
    print(f"  total {sum(len(p) for _,_,p in made)} pages")

if __name__ == "__main__":
    build()

# قاتل الهاش النسخة الثالثة

<p align="center">
  <a href="#">العربية</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="https://github.com/oaokm/Hash-Killer-V3/blob/main/README.md">English</a>
</p>


هي النسخة المُحسنة من [النسخة الثانية](https://github.com/Omar-KL/Hash_Killer.V2) الذي طورها [Omar-KL](https://github.com/Omar-KL). والبرنامج يستخدم خوارزميات الهاش للتوليد، وأكتشاف التطابق بهدف أكتشاف أصل الكلمة أو البيانات.

## طريقة التحميل

* أولًا: يجب عليك التأكد من أن برمجية [`git`](https://git-scm.com/downloads) مٌثبتة على نظامك. إذا كان نظام تشغيلك ويندوز تحتاج إلى تحميل البرمجية. وإذا كان نظام تشغيلك إحدى توزيعات جنو/لينكس أو ماك فلا حاجة لتثبيتها. أو يمكنك ببساطة [الضغط هنا](https://github.com/oaokm/Hash-Killer-V3/archive/refs/heads/main.zip) لتحميل المستودع.

* ثانيًا: إذا تريد التحميل بواسطة برمجية `git`، قم بفتح سطر الأوامر (التيرمنل) وقم بكتابه التالي:

```sh
~$ git clone https://github.com/oaokm/Hash-Killer-V3
```

* ثالثًا: قم بالدخول إلى مجلد `Hash-Killer-V3` وقم  بكتابة الأمر التالي في سطر الأوامر لتحميل المكتبات اللازمة لتشغيل البرنامج:

```sh
~$ pip install -r requirement.txt
```

## ملفات البرنامج


```
.
├── ASCII-Art.art
├── config.py
├── hash_killer.py
├── images
│   └── .
├── lab.ipynb
├── log
│   ├── log.json
│   └── log.log
├── logger.py
├── READMD.ar.md
├── READMD.md
├── storage
│   └── .
└── url.py

```
| المجلد | الغرض | 
| ------ | ------ |
| images | هو مجلد خاص للصور التي تتعلق بالمشروع |
| storage | هو مجلد خاص لقائمة كلمات المرور التي يتم تحميلها من الإنترنت |
| log | هو مجلد خاص يتم الاحتفاظ لكافة العمليات التي تتم اثناء تشغيل البرنامج |


| الملف | الغرض | 
| ------ | ------ |
| ASCII-Art.art | يحتوي على رسمة رُسمت بنظام ASCII |
| config.py | ملف الإعدادات |
| hash_killer.py | الملف الرئيسي الذي يحتوي على جميع التعلميات التي تشغل قاتل الهاش |
| lab.ipynb | ملف جوبيتر يحتوي على "أكواد" أختبار لبعض الخصائص التي تمت إضافتها في `hash_killer.py` |
| logger.py | برنامج بسيط يقوم بتسجيل جميع العمليات واستعراضها للمستخدم وحفظها في ملف داخل مجلد `log` |
| url.py | برنامج بسيط يقوم بالتحقق إذا كان النص المُقدم هو رابط بالفعل مع قدرة التعرف على أجزاء الرابط وتصنيفها |
| requirement.txt | يحتوى على المكتبات غير القياسية المستخدمة لعمل البرنامج |


## كيف استخدم البرنامج؟

في الوقت الحالي، يمكنك استخدام البرنامج كمكتبة يمكنك استدعائها بواسطة [`import`](https://docs.python.org/3/reference/import.html) ويمكنك ذلك عند طريق انشاء ملف بايثون باي اسم داخل مجلد `Hash-Killer-V3` (الذي قمت بتحميله قبل قليل) وتطبيق ما يلي:

### توليد الهاش
هنالك نوعين من التوليد:

* [التوليد المٌملح](https://en.wikipedia.org/wiki/Salt_%28cryptography%29): هي قيمة عشوائية يتم إضافتها مع الهاش لزيادة التعقيد.
* التوليد العادي: بدون ملح :)


#### التوليد العادي

في البداية نقوم باستدعاء كائن `hash_killer` وتعريفه بـ`hash_k` ومن ثم استخدام دالة `Hash_generater` لتوليد الهاش

```py
# نقوم هنا بأستدعاء المكتبة
from hash_killer import hash_killer

# تعريف الكائن
hash_k = hash_killer()

# أمر توليد الهاش  
hash_gen = hash_k.Hash_generater(
    hashType='sha384', 
    text='iloveyou'
)

print(hash_gen)

# الإخراج: 6b008bafd02f6c9ea7a63996e1705b2fdd8163aa67a0ce7ecc783432ea0eac1a6a43340855b89fb5cbb8508065ff1ac7
```

#### التوليد المٌملح

يتم فقط إضافة خيارين : useSalt, length بجانب `Hash_generater`.
ووظيفة كلٌ منهما :

* `useSalt` (منطقي "bool"): هو خيار منطقي إذا كان "صائبًا" سيتم إضافة "الملح" بحانب الكلمة الأصل؛ ليزداد تعقيد الهاش. وهو افتراضيًا مغلق (False)

* `length` (عدد صحيح "int"): يحدد طول النص "المٌملح" الذي يتم إضافتها إلى النص الأصلي. وهو افتراضيًا 20

```py
# نقوم هنا بأستدعاء المكتبة
from hash_killer import hash_killer

# تعريف الكائن
hash_k = hash_killer()

# أمر توليد الهاش مع تفعيل خاصية التوليد المٌملح
hash_gen = hash_k.Hash_generater(
    hashType='sha384', 
    text='iloveyou',
    useSalt=True,
    length=20
)

print(hash_gen)

# الإخراج: a1df82bc9a5c95f80694aea32686c32f13afaa1b3bc701461045d6ed74ca87745a9db80ae971813be81edde29203ae6b
```

### أكتشاف التطابق
ما يميز خوارزميات الهاش هي عدم القابلية لعكس العملية؛ ما يعني أنه يختلف عن تقنيات التشفير المُعتادة، حيث أن التشفير بني على مبدأ الدالة المتباينة. فالهاش يستخدم دالة خاصا تمنع التصادم والقابلية للعكس

![hashing-vs-encryption](https://github.com/oaokm/Hash-Killer-V3/blob/main/images/hashing-vs-encryption.png?raw=true)
لذا، فضمن الحلول لأكتشاف أصل الكلمة أو البيانات قبل اخضاعها لخوارزميات الهاش هي اكتشاف التطابق عبر مقارنة الهاش المٌراد فحصه وأكتشاف نوع خوارزمية الهاش، ومن ثمّ مطابقتها بمجموعة ضخمة من النصوص والبيانات من خلال تحويلها إلى هاش متطابق المعايير مع الهاش المُراد فحصه، وفي حال وجود تطابق فهذا يعني أن نتيجة الفحص إجابية والنتيجة هي أصل، وفي حال عدم التطابق تكون النتيجة سلبية.

في قاتل الهاش تم تطوير نظامًا لاكتشاف التطابق، وطريقة لتحميل ملفات من الإنترنت. وكلُ عليك استخدام دالة `foundMatch` وتمكين الخيارات التالية:

* `hash` (نصي): هنا تقوم بوضع الهاش المٌراد فحصه
* `pathfileOrURL` (نصي): هنا تقوم بوضع رابط ملف من الشبكة العنكبوتية أو مسار الملف داخل جهازك. والملف يجب أن يكون ملفًا نصيًا

> ملاحظة: سنستخدم في هذا المثال ملف [rockyou.txt](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt) من موقع github


```py
# نقوم هنا بأستدعاء المكتبة
from hash_killer import hash_killer

# تعريف الكائن
hash_k = hash_killer()

hash_word = '6b008bafd02f6c9ea7a63996e1705b2fdd8163aa67a0ce7ecc783432ea0eac1a6a43340855b89fb5cbb8508065ff1ac7'

# في pathfileOrURL ينكنك وضع رابط أو مسار الملف.
# في حال وضعت الرابط سيتم تحميل الملف ووضعها فيي مجلد `./storage`
result = hash_k.foundMatch(
    hash=hash_word,
    pathfileOrURL='https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt')

print(result)
```

## دعم
لا باس بقليلٍا من القهوة :)

<a href="https://www.buymeacoffee.com/oaokm" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>


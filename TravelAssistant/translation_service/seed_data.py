import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Sample common phrases data
sample_phrases = [
  {
    "phrase": "Hello",
    "category": "Greeting",
    "translations": {
      "hi": {
        "translatedPhrase": "नमस्ते",
        "pronunciation": "Namaste",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/hello_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "હેલો",
        "pronunciation": "Helo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/hello_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "こんにちは",
        "pronunciation": "Konnichiwa",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/hello_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Hola",
        "pronunciation": "O-la",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/hello_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Bonjour",
        "pronunciation": "Bohn-zhoor",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/hello_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "안녕하세요",
        "pronunciation": "Annyeonghaseyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/hello_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "你好",
        "pronunciation": "Nǐ hǎo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/hello_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Здравствуйте",
        "pronunciation": "Zdravstvuyte",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/hello_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Hallo",
        "pronunciation": "Ha-lo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/hello_de.mp3"
      }
    }
  },
  {
    "phrase": "Thank you",
    "category": "Gratitude",
    "translations": {
      "hi": {
        "translatedPhrase": "धन्यवाद",
        "pronunciation": "Dhanyavaad",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/thank_you_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "આભાર",
        "pronunciation": "Aabhar",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/thank_you_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "ありがとうございます",
        "pronunciation": "Arigatō gozaimasu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/thank_you_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Gracias",
        "pronunciation": "Gra-thee-as",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/thank_you_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Merci",
        "pronunciation": "Mehr-see",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/thank_you_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "감사합니다",
        "pronunciation": "Kamsahamnida",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/thank_you_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "谢谢",
        "pronunciation": "Xièxiè",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/thank_you_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Спасибо",
        "pronunciation": "Spasibo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/thank_you_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Danke",
        "pronunciation": "Dan-keh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/thank_you_de.mp3"
      }
    }
  },
  {
    "phrase": "Goodbye",
    "category": "Farewell",
    "translations": {
      "hi": {
        "translatedPhrase": "अलविदा",
        "pronunciation": "Alvida",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/goodbye_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "આવજો",
        "pronunciation": "Aavjo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/goodbye_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "さようなら",
        "pronunciation": "Sayōnara",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/goodbye_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Adiós",
        "pronunciation": "Ah-dee-os",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/goodbye_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Au revoir",
        "pronunciation": "Oh ruh-vwah",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/goodbye_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "안녕히 가세요",
        "pronunciation": "Annyeonghi gaseyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/goodbye_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "再见",
        "pronunciation": "Zàijiàn",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/goodbye_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "До свидания",
        "pronunciation": "Do svidaniya",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/goodbye_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Auf Wiedersehen",
        "pronunciation": "Auf vee-der-zayn",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/goodbye_de.mp3"
      }
    }
  },
  {
    "phrase": "You're welcome",
    "category": "Response to Gratitude",
    "translations": {
      "hi": {
        "translatedPhrase": "आपका स्वागत है",
        "pronunciation": "Aapka swagat hai",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/you%27re_welcome_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "તમારું સ્વાગત છે",
        "pronunciation": "Tamaaru swaagat chhe",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/you%27re_welcome_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "どういたしまして",
        "pronunciation": "Dōitashimashite",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/you%27re_welcome_ja.mp3"
      },
      "es": {
        "translatedPhrase": "De nada",
        "pronunciation": "De nah-dah",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/you%27re_welcome_es.mp3"
      },
      "fr": {
        "translatedPhrase": "De rien",
        "pronunciation": "Duh ree-ahn",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/you%27re_welcome_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "천만에요",
        "pronunciation": "Cheonmaneyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/you%27re_welcome_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "不客气",
        "pronunciation": "Bú kèqì",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/you%27re_welcome_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Пожалуйста",
        "pronunciation": "Pozhaluysta",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/you%27re_welcome_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Gern geschehen",
        "pronunciation": "Gern geh-sheh-en",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/you%27re_welcome_de.mp3"
      }
    }
  },
  {
    "phrase": "How are you?",
    "category": "Greeting/Question",
    "translations": {
      "hi": {
        "translatedPhrase": "आप कैसे हैं?",
        "pronunciation": "Aap kaise hain?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/how_are_you%3F_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "તમે કેમ છો?",
        "pronunciation": "Tame kem chho?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/how_are_you%3F_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "お元気ですか？",
        "pronunciation": "Ogenki desu ka?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/how_are_you%3F_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¿Cómo estás?",
        "pronunciation": "Ko-mo es-tas?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/how_are_you%3F_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Comment ça va?",
        "pronunciation": "Koh-mohn sah vah?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/how_are_you%3F_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "어떻게 지내세요?",
        "pronunciation": "Eotteoke jinaeseyo?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/how_are_you%3F_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "你好吗？",
        "pronunciation": "Nǐ hǎo ma?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/how_are_you%3F_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Как дела?",
        "pronunciation": "Kak dela?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/how_are_you%3F_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Wie geht es Ihnen?",
        "pronunciation": "Vee gayt es ee-nen?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/how_are_you%3F_de.mp3"
      }
    }
  },
  {
    "phrase": "I'm fine",
    "category": "Response",
    "translations": {
      "hi": {
        "translatedPhrase": "मैं ठीक हूँ",
        "pronunciation": "Main theek hoon",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/i%27m_fine_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "હું ઠીક છું",
        "pronunciation": "Hun thik chhun",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/i%27m_fine_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "元気です",
        "pronunciation": "Genki desu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/i%27m_fine_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Estoy bien",
        "pronunciation": "Es-toy bee-en",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/i%27m_fine_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Ça va bien",
        "pronunciation": "Sah vah bee-ahn",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/i%27m_fine_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "잘 지내요",
        "pronunciation": "Jal jinaeyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/i%27m_fine_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "我很好",
        "pronunciation": "Wǒ hěn hǎo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/i%27m_fine_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "У меня все хорошо",
        "pronunciation": "U menya vsyo khorosho",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/i%27m_fine_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Mir geht es gut",
        "pronunciation": "Meer gayt es goot",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/i%27m_fine_de.mp3"
      }
    }
  },
  {
    "phrase": "What is your name?",
    "category": "Question",
    "translations": {
      "hi": {
        "translatedPhrase": "आपका नाम क्या है?",
        "pronunciation": "Aapka naam kya hai?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/what_is_your_name%3F_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "તમારું નામ શું છે?",
        "pronunciation": "Tamaaru naam shun chhe?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/what_is_your_name%3F_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "お名前は何ですか？",
        "pronunciation": "Onamae wa nan desu ka?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/what_is_your_name%3F_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¿Cuál es tu nombre?",
        "pronunciation": "Kwal es too nohm-bre?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/what_is_your_name%3F_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Quel est votre nom?",
        "pronunciation": "Kel ay vo-truh nohn?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/what_is_your_name%3F_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "이름이 무엇입니까?",
        "pronunciation": "Ireumi mueosimnikka?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/what_is_your_name%3F_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "你叫什么名字？",
        "pronunciation": "Nǐ jiào shénme míngzì?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/what_is_your_name%3F_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Как вас зовут?",
        "pronunciation": "Kak vas zovut?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/what_is_your_name%3F_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Wie heißen Sie?",
        "pronunciation": "Vee high-sen zee?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/what_is_your_name%3F_de.mp3"
      }
    }
  },
  {
    "phrase": "My name is...",
    "category": "Response",
    "translations": {
      "hi": {
        "translatedPhrase": "मेरा नाम ... है",
        "pronunciation": "Mera naam ... hai",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/my_name_is..._hi.mp3"
      },
      "gu": {
        "translatedPhrase": "મારું નામ ... છે",
        "pronunciation": "Maaru naam ... chhe",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/my_name_is..._gu.mp3"
      },
      "ja": {
        "translatedPhrase": "私の名前は...です",
        "pronunciation": "Watashi no namae wa ... desu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/my_name_is..._ja.mp3"
      },
      "es": {
        "translatedPhrase": "Mi nombre es...",
        "pronunciation": "Mee nohm-breh es...",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/my_name_is..._es.mp3"
      },
      "fr": {
        "translatedPhrase": "Je m'appelle...",
        "pronunciation": "Zhuh mah-pel...",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/my_name_is..._fr.mp3"
      },
      "ko": {
        "translatedPhrase": "제 이름은 ...입니다",
        "pronunciation": "Je ireumeun ...imnida",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/my_name_is..._ko.mp3"
      },
      "zh": {
        "translatedPhrase": "我的名字是...",
        "pronunciation": "Wǒ de míngzì shì...",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/my_name_is..._zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Меня зовут...",
        "pronunciation": "Menya zovut...",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/my_name_is..._ru.mp3"
      },
      "de": {
        "translatedPhrase": "Mein Name ist...",
        "pronunciation": "Mine nah-meh ist...",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/my_name_is..._de.mp3"
      }
    }
  },
  {
    "phrase": "Where are you from?",
    "category": "Question",
    "translations": {
      "hi": {
        "translatedPhrase": "आप कहाँ से हैं?",
        "pronunciation": "Aap kahaan se hain?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/where_are_you_from%3F_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "તમે ક્યાંથી છો?",
        "pronunciation": "Tame kyaanthi chho?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/where_are_you_from%3F_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "どちらからいらっしゃいましたか？",
        "pronunciation": "Dochira kara irasshaimashita ka?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/where_are_you_from%3F_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¿De dónde eres?",
        "pronunciation": "De don-deh eh-res?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/where_are_you_from%3F_es.mp3"
      },
      "fr": {
        "translatedPhrase": "D'où venez-vous?",
        "pronunciation": "Doo vuh-nay voo?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/where_are_you_from%3F_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "어디에서 오셨어요?",
        "pronunciation": "Eodieseo osyeosseoyo?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/where_are_you_from%3F_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "你是哪里人？",
        "pronunciation": "Nǐ shì nǎlǐ rén?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/where_are_you_from%3F_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Откуда вы?",
        "pronunciation": "Otkuda vy?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/where_are_you_from%3F_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Woher kommen Sie?",
        "pronunciation": "Vo-hair koh-men zee?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/where_are_you_from%3F_de.mp3"
      }
    }
  },
  {
    "phrase": "I am from...",
    "category": "Response",
    "translations": {
      "hi": {
        "translatedPhrase": "मैं ... से हूँ",
        "pronunciation": "Main ... se hoon",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/i_am_from..._hi.mp3"
      },
      "gu": {
        "translatedPhrase": "હું ... થી છું",
        "pronunciation": "Hun ... thi chhun",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/i_am_from..._gu.mp3"
      },
      "ja": {
        "translatedPhrase": "...から来ました",
        "pronunciation": "...kara kimashita",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/i_am_from..._ja.mp3"
      },
      "es": {
        "translatedPhrase": "Soy de...",
        "pronunciation": "Soy deh...",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/i_am_from..._es.mp3"
      },
      "fr": {
        "translatedPhrase": "Je viens de...",
        "pronunciation": "Zhuh vee-ahn duh...",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/i_am_from..._fr.mp3"
      },
      "ko": {
        "translatedPhrase": "...에서 왔어요",
        "pronunciation": "...eseo wasseoyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/i_am_from..._ko.mp3"
      },
      "zh": {
        "translatedPhrase": "我来自...",
        "pronunciation": "Wǒ láizì...",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/i_am_from..._zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Я из...",
        "pronunciation": "Ya iz...",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/i_am_from..._ru.mp3"
      },
      "de": {
        "translatedPhrase": "Ich komme aus...",
        "pronunciation": "Ish koh-meh aus...",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/i_am_from..._de.mp3"
      }
    }
  },
  {
    "phrase": "Please",
    "category": "Politeness",
    "translations": {
      "hi": {
        "translatedPhrase": "कृपया",
        "pronunciation": "Kripya",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/please_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "કૃપા કરીને",
        "pronunciation": "Krupa kareene",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/please_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "お願いします",
        "pronunciation": "Onegaishimasu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/please_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Por favor",
        "pronunciation": "Por fa-vor",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/please_es.mp3"
      },
      "fr": {
        "translatedPhrase": "S'il vous plaît",
        "pronunciation": "Seel voo প্লে",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/please_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "제발",
        "pronunciation": "Jebal",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/please_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "请",
        "pronunciation": "Qǐng",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/please_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Пожалуйста",
        "pronunciation": "Pozhaluysta",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/please_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Bitte",
        "pronunciation": "Bi-teh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/please_de.mp3"
      }
    }
  },
  {
    "phrase": "Sorry",
    "category": "Apology",
    "translations": {
      "hi": {
        "translatedPhrase": "माफ़ कीजिए",
        "pronunciation": "Maaf keejiye",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/sorry_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "માફ કરશો",
        "pronunciation": "Maaf karsho",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/sorry_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "すみません",
        "pronunciation": "Sumimasen",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/sorry_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Lo siento",
        "pronunciation": "Lo see-en-to",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/sorry_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Désolé(e)",
        "pronunciation": "Day-zoh-lay",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/sorry_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "미안합니다",
        "pronunciation": "Mianhamnida",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/sorry_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "对不起",
        "pronunciation": "Duìbùqǐ",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/sorry_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Извините",
        "pronunciation": "Izvinite",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/sorry_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Entschuldigung",
        "pronunciation": "Ent-shul-di-gung",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/sorry_de.mp3"
      }
    }
  },
  {
    "phrase": "Yes",
    "category": "Affirmation",
    "translations": {
      "hi": {
        "translatedPhrase": "हाँ",
        "pronunciation": "Haan",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/yes_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "હા",
        "pronunciation": "Haa",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/yes_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "はい",
        "pronunciation": "Hai",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/yes_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Sí",
        "pronunciation": "See",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/yes_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Oui",
        "pronunciation": "Wee",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/yes_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "네",
        "pronunciation": "Ne",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/yes_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "是",
        "pronunciation": "Shì",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/yes_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Да",
        "pronunciation": "Da",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/yes_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Ja",
        "pronunciation": "Ya",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/yes_de.mp3"
      }
    }
  },
  {
    "phrase": "No",
    "category": "Negation",
    "translations": {
      "hi": {
        "translatedPhrase": "नहीं",
        "pronunciation": "Nahin",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/no_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "ના",
        "pronunciation": "Naa",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/no_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "いいえ",
        "pronunciation": "Iie",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/no_ja.mp3"
      },
      "es": {
        "translatedPhrase": "No",
        "pronunciation": "No",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/no_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Non",
        "pronunciation": "Nohn",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/no_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "아니요",
        "pronunciation": "Aniyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/no_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "不",
        "pronunciation": "Bù",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/no_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Нет",
        "pronunciation": "Nyet",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/no_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Nein",
        "pronunciation": "Nine",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/no_de.mp3"
      }
    }
  },
  {
    "phrase": "Okay",
    "category": "Agreement",
    "translations": {
      "hi": {
        "translatedPhrase": "ठीक है",
        "pronunciation": "Theek hai",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/okay_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "ઓકે",
        "pronunciation": "Oke",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/okay_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "わかりました",
        "pronunciation": "Wakarimashita",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/okay_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Está bien",
        "pronunciation": "Es-tah bee-en",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/okay_es.mp3"
      },
      "fr": {
        "translatedPhrase": "D'accord",
        "pronunciation": "Dah-kor",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/okay_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "알겠습니다",
        "pronunciation": "Algesseumnida",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/okay_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "好的",
        "pronunciation": "Hǎo de",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/okay_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Хорошо",
        "pronunciation": "Khorosho",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/okay_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Okay",
        "pronunciation": "O-kay",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/okay_de.mp3"
      }
    }
  },
  {
    "phrase": "How much?",
    "category": "Question",
    "translations": {
      "hi": {
        "translatedPhrase": "यह कितने का है?",
        "pronunciation": "Yah kitne ka hai?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/how_much%3F_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "આ કેટલાનું છે?",
        "pronunciation": "Aa ketlaanu chhe?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/how_much%3F_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "いくらですか？",
        "pronunciation": "Ikura desu ka?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/how_much%3F_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¿Cuánto cuesta?",
        "pronunciation": "Kwan-toh kwes-tah?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/how_much%3F_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Combien ça coûte?",
        "pronunciation": "Kohm-bee-ahn sah koot?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/how_much%3F_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "얼마예요?",
        "pronunciation": "Eolmayeyo?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/how_much%3F_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "多少钱？",
        "pronunciation": "Duōshǎo qián?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/how_much%3F_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Сколько стоит?",
        "pronunciation": "Skol'ko stoit?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/how_much%3F_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Wie viel kostet das?",
        "pronunciation": "Vee feel koh-stet das?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/how_much%3F_de.mp3"
      }
    }
  },
  {
    "phrase": "Where is the bathroom?",
    "category": "Question",
    "translations": {
      "hi": {
        "translatedPhrase": "शौचालय कहाँ है?",
        "pronunciation": "Shauchalay kahaan hai?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/where_is_the_bathroom%3F_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "બાથરૂમ ક્યાં છે?",
        "pronunciation": "Baathroom kyaan chhe?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/where_is_the_bathroom%3F_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "トイレはどこですか？",
        "pronunciation": "Toire wa doko desu ka?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/where_is_the_bathroom%3F_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¿Dónde está el baño?",
        "pronunciation": "Don-deh es-tah el bah-nyo?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/where_is_the_bathroom%3F_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Où sont les toilettes?",
        "pronunciation": "Oo sohn lay twah-let?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/where_is_the_bathroom%3F_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "화장실은 어디에 있습니까?",
        "pronunciation": "Hwajangsireun eodie itseumnikka?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/where_is_the_bathroom%3F_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "洗手间在哪里？",
        "pronunciation": "Xǐshǒujiān zài nǎlǐ?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/where_is_the_bathroom%3F_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Где находится туалет?",
        "pronunciation": "Gde nahoditsya tualet?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/where_is_the_bathroom%3F_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Wo ist die Toilette?",
        "pronunciation": "Vo ist dee toh-ah-le-teh?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/where_is_the_bathroom%3F_de.mp3"
      }
    }
  },
  {
    "phrase": "Good morning",
    "category": "Greeting",
    "translations": {
      "hi": {
        "translatedPhrase": "शुभ प्रभात",
        "pronunciation": "Shubh Prabhat",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/good_morning_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "શુભ સવાર",
        "pronunciation": "Shubh savaar",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/good_morning_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "おはようございます",
        "pronunciation": "Ohayō gozaimasu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/good_morning_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Buenos días",
        "pronunciation": "Bweh-nos dee-as",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/good_morning_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Bonjour",
        "pronunciation": "Bohn-zhoor",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/good_morning_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "좋은 아침",
        "pronunciation": "Joeun achim",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/good_morning_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "早上好",
        "pronunciation": "Zǎoshang hǎo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/good_morning_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Доброе утро",
        "pronunciation": "Dobroye utro",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/good_morning_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Guten Morgen",
        "pronunciation": "Goo-ten mor-gen",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/good_morning_de.mp3"
      }
    }
  },
  {
    "phrase": "Good afternoon",
    "category": "Greeting",
    "translations": {
      "hi": {
        "translatedPhrase": "शुभ दोपहर",
        "pronunciation": "Shubh Dophar",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/good_afternoon_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "શુભ બપોર",
        "pronunciation": "Shubh bapor",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/good_afternoon_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "こんにちは",
        "pronunciation": "Konnichiwa",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/good_afternoon_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Buenas tardes",
        "pronunciation": "Bweh-nas tar-des",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/good_afternoon_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Bon après-midi",
        "pronunciation": "Bohn ah-preh-mee-dee",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/good_afternoon_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "좋은 오후",
        "pronunciation": "Joeun ohu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/good_afternoon_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "下午好",
        "pronunciation": "Xiàwǔ hǎo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/good_afternoon_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Добрый день",
        "pronunciation": "Dobryy den'",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/good_afternoon_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Guten Tag",
        "pronunciation": "Goo-ten tahg",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/good_afternoon_de.mp3"
      }
    }
  },
  {
    "phrase": "Good evening",
    "category": "Greeting",
    "translations": {
      "hi": {
        "translatedPhrase": "शुभ संध्या",
        "pronunciation": "Shubh Sandhya",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/good_evening_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "શુભ સાંજ",
        "pronunciation": "Shubh saanj",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/good_evening_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "こんばんは",
        "pronunciation": "Konbanwa",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/good_evening_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Buenas noches",
        "pronunciation": "Bweh-nas no-ches",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/good_evening_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Bonsoir",
        "pronunciation": "Bohn-swahr",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/good_evening_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "좋은 저녁",
        "pronunciation": "Joeun jeonyeok",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/good_evening_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "晚上好",
        "pronunciation": "Wǎnshàng hǎo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/good_evening_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Добрый вечер",
        "pronunciation": "Dobryy vecher",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/good_evening_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Guten Abend",
        "pronunciation": "Goo-ten ah-bent",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/good_evening_de.mp3"
      }
    }
  },
  {
    "phrase": "Good night",
    "category": "Farewell",
    "translations": {
      "hi": {
        "translatedPhrase": "शुभ रात्रि",
        "pronunciation": "Shubh Ratri",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/good_night_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "શુભ રાત્રિ",
        "pronunciation": "Shubh raatri",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/good_night_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "おやすみなさい",
        "pronunciation": "Oyasuminasai",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/good_night_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Buenas noches",
        "pronunciation": "Bweh-nas no-ches",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/good_night_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Bonne nuit",
        "pronunciation": "Bohn nwee",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/good_night_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "안녕히 주무세요",
        "pronunciation": "Annyeonghi jumuseyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/good_night_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "晚安",
        "pronunciation": "Wǎn'ān",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/good_night_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Спокойной ночи",
        "pronunciation": "Spokoynoy nochi",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/good_night_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Gute Nacht",
        "pronunciation": "Goo-teh naht",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/good_night_de.mp3"
      }
    }
  },
  {
    "phrase": "Have a nice day",
    "category": "Well-wishing",
    "translations": {
      "hi": {
        "translatedPhrase": "आपका दिन शुभ हो",
        "pronunciation": "Aapka din shubh ho",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/have_a_nice_day_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "તમારો દિવસ શુભ રહે",
        "pronunciation": "Tamaaro divas shubh rahe",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/have_a_nice_day_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "良い一日を",
        "pronunciation": "Yoi ichinichi o",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/have_a_nice_day_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Que tengas un buen día",
        "pronunciation": "Keh ten-gas oon bwehn dee-ah",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/have_a_nice_day_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Passez une bonne journée",
        "pronunciation": "Pah-say oon bohn zhoor-nay",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/have_a_nice_day_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "좋은 하루 보내세요",
        "pronunciation": "Joeun haru bonaeseyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/have_a_nice_day_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "祝你一天愉快",
        "pronunciation": "Zhù nǐ yī tiān yúkuài",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/have_a_nice_day_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Хорошего дня",
        "pronunciation": "Khoroshego dnya",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/have_a_nice_day_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Schönen Tag noch",
        "pronunciation": "Sheu-nen tahg nokh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/have_a_nice_day_de.mp3"
      }
    }
  },
  {
    "phrase": "See you later",
    "category": "Farewell",
    "translations": {
      "hi": {
        "translatedPhrase": "फिर मिलेंगे",
        "pronunciation": "Phir milenge",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/see_you_later_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "પછી મળીશું",
        "pronunciation": "Pachhi malishu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/see_you_later_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "また後で",
        "pronunciation": "Mata atode",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/see_you_later_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Hasta luego",
        "pronunciation": "Ah-stah lweh-go",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/see_you_later_es.mp3"
      },
      "fr": {
        "translatedPhrase": "À plus tard",
        "pronunciation": "Ah pluh tahr",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/see_you_later_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "나중에 봐요",
        "pronunciation": "Najunge bwayo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/see_you_later_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "一会儿见",
        "pronunciation": "Yīhuǐr jiàn",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/see_you_later_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Увидимся позже",
        "pronunciation": "Uvidimsya pozzhe",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/see_you_later_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Bis später",
        "pronunciation": "Bis shpay-ter",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/see_you_later_de.mp3"
      }
    }
  },
  {
    "phrase": "I don't understand",
    "category": "Communication",
    "translations": {
      "hi": {
        "translatedPhrase": "मुझे समझ नहीं आया",
        "pronunciation": "Mujhe samajh nahin aaya",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/i_don%27t_understand_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "મને સમજાયું નથી",
        "pronunciation": "Mane samjaayu nathi",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/i_don%27t_understand_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "わかりません",
        "pronunciation": "Wakarimasen",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/i_don%27t_understand_ja.mp3"
      },
      "es": {
        "translatedPhrase": "No entiendo",
        "pronunciation": "No en-tee-en-do",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/i_don%27t_understand_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Je ne comprends pas",
        "pronunciation": "Zhuh nuh kohm-prahn pah",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/i_don%27t_understand_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "이해가 안 돼요",
        "pronunciation": "Ihaega an dwaeyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/i_don%27t_understand_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "我不明白",
        "pronunciation": "Wǒ bù míngbái",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/i_don%27t_understand_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Я не понимаю",
        "pronunciation": "Ya ne ponimayu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/i_don%27t_understand_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Ich verstehe nicht",
        "pronunciation": "Ish fair-shtay-eh nisht",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/i_don%27t_understand_de.mp3"
      }
    }
  },
  {
    "phrase": "Can you help me?",
    "category": "Request",
    "translations": {
      "hi": {
        "translatedPhrase": "क्या आप मेरी मदद कर सकते हैं?",
        "pronunciation": "Kya aap meri madad kar sakte hain?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/can_you_help_me%3F_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "શું તમે મને મદદ કરી શકો છો?",
        "pronunciation": "Shun tame mane madad karee shako chho?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/can_you_help_me%3F_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "手伝ってくれますか？",
        "pronunciation": "Tetsudatte kuremasu ka?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/can_you_help_me%3F_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¿Puede ayudarme?",
        "pronunciation": "Pweh-deh ah-yoo-dar-meh?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/can_you_help_me%3F_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Pouvez-vous m'aider?",
        "pronunciation": "Poo-vay voo may-day?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/can_you_help_me%3F_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "저를 도와주시겠어요?",
        "pronunciation": "Jeoreul dowajusigesseoyo?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/can_you_help_me%3F_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "你能帮我吗？",
        "pronunciation": "Nǐ néng bāng wǒ ma?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/can_you_help_me%3F_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Вы можете мне помочь?",
        "pronunciation": "Vy mozhete mne pomoch'?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/can_you_help_me%3F_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Können Sie mir helfen?",
        "pronunciation": "Keu-nen zee meer hel-fen?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/can_you_help_me%3F_de.mp3"
      }
    }
  },
  {
    "phrase": "I need help",
    "category": "Request",
    "translations": {
      "hi": {
        "translatedPhrase": "मुझे मदद चाहिए",
        "pronunciation": "Mujhe madad chaahiye",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/i_need_help_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "મારે મદદની જરૂર છે",
        "pronunciation": "Maare madadnee jaroor chhe",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/i_need_help_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "助けが必要です",
        "pronunciation": "Tasuke ga hitsuyō desu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/i_need_help_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Necesito ayuda",
        "pronunciation": "Neh-theh-see-toh ah-yoo-dah",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/i_need_help_es.mp3"
      },
      "fr": {
        "translatedPhrase": "J'ai besoin d'aide",
        "pronunciation": "Zhay buh-zwan ded",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/i_need_help_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "도와주세요",
        "pronunciation": "Dowajuseyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/i_need_help_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "我需要帮助",
        "pronunciation": "Wǒ xūyào bāngzhù",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/i_need_help_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Мне нужна помощь",
        "pronunciation": "Mne nuzhna pomoshch'",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/i_need_help_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Ich brauche Hilfe",
        "pronunciation": "Ish brow-kheh hil-feh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/i_need_help_de.mp3"
      }
    }
  },
  {
    "phrase": "Where is...?",
    "category": "Question",
    "translations": {
      "hi": {
        "translatedPhrase": "...कहाँ है?",
        "pronunciation": "...kahaan hai?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/where_is...%3F_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "...ક્યાં છે?",
        "pronunciation": "...kyaan chhe?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/where_is...%3F_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "...はどこですか？",
        "pronunciation": "...wa doko desu ka?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/where_is...%3F_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¿Dónde está...?",
        "pronunciation": "Don-deh es-tah...?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/where_is...%3F_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Où est...?",
        "pronunciation": "Oo ay...?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/where_is...%3F_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "...은/는 어디에 있습니까?",
        "pronunciation": "...eun/neun eodie itseumnikka?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/where_is...%3F_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "...在哪里？",
        "pronunciation": "...zài nǎlǐ?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/where_is...%3F_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Где находится...?",
        "pronunciation": "Gde nahoditsya...?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/where_is...%3F_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Wo ist...?",
        "pronunciation": "Vo ist...?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/where_is...%3F_de.mp3"
      }
    }
  },
  {
    "phrase": "What time is it?",
    "category": "Question",
    "translations": {
      "hi": {
        "translatedPhrase": "कितना बजा है?",
        "pronunciation": "Kitna baja hai?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/what_time_is_it%3F_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "કેટલા વાગ્યા છે?",
        "pronunciation": "Ketla vaagya chhe?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/what_time_is_it%3F_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "今何時ですか？",
        "pronunciation": "Ima nanji desu ka?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/what_time_is_it%3F_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¿Qué hora es?",
        "pronunciation": "Keh o-rah es?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/what_time_is_it%3F_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Quelle heure est-il?",
        "pronunciation": "Kel ur ay-teel?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/what_time_is_it%3F_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "지금 몇 시예요?",
        "pronunciation": "Jigeum myeot si yeyo?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/what_time_is_it%3F_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "现在几点？",
        "pronunciation": "Xiànzài jǐ diǎn?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/what_time_is_it%3F_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Который час?",
        "pronunciation": "Kotoryy chas?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/what_time_is_it%3F_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Wie viel Uhr ist es?",
        "pronunciation": "Vee feel oor ist es?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/what_time_is_it%3F_de.mp3"
      }
    }
  },
  {
    "phrase": "I like it",
    "category": "Preference",
    "translations": {
      "hi": {
        "translatedPhrase": "मुझे यह पसंद है",
        "pronunciation": "Mujhe yah pasand hai",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/i_like_it_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "મને આ ગમે છે",
        "pronunciation": "Mane aa game chhe",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/i_like_it_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "好きです",
        "pronunciation": "Suki desu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/i_like_it_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Me gusta",
        "pronunciation": "Meh goos-tah",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/i_like_it_es.mp3"
      },
      "fr": {
        "translatedPhrase": "J'aime ça",
        "pronunciation": "Zhem sah",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/i_like_it_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "좋아요",
        "pronunciation": "Joayo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/i_like_it_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "我喜欢",
        "pronunciation": "Wǒ xǐhuān",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/i_like_it_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Мне это нравится",
        "pronunciation": "Mne eto nravitsya",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/i_like_it_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Ich mag das",
        "pronunciation": "Ish mahg das",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/i_like_it_de.mp3"
      }
    }
  },
  {
    "phrase": "I don't like it",
    "category": "Preference",
    "translations": {
      "hi": {
        "translatedPhrase": "मुझे यह पसंद नहीं है",
        "pronunciation": "Mujhe yah pasand nahin hai",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/i_don%27t_like_it_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "મને આ નથી ગમતું",
        "pronunciation": "Mane aa nathi gamtun",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/i_don%27t_like_it_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "好きではありません",
        "pronunciation": "Suki dewa arimasen",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/i_don%27t_like_it_ja.mp3"
      },
      "es": {
        "translatedPhrase": "No me gusta",
        "pronunciation": "No meh goos-tah",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/i_don%27t_like_it_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Je n'aime pas ça",
        "pronunciation": "Zhuh nem pah sah",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/i_don%27t_like_it_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "싫어요",
        "pronunciation": "Sireoyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/i_don%27t_like_it_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "我不喜欢",
        "pronunciation": "Wǒ bù xǐhuān",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/i_don%27t_like_it_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Мне это не нравится",
        "pronunciation": "Mne eto ne nravitsya",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/i_don%27t_like_it_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Ich mag das nicht",
        "pronunciation": "Ish mahg das nisht",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/i_don%27t_like_it_de.mp3"
      }
    }
  },
  {
    "phrase": "It's delicious",
    "category": "Compliment",
    "translations": {
      "hi": {
        "translatedPhrase": "यह स्वादिष्ट है",
        "pronunciation": "Yah svaadisht hai",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/it%27s_delicious_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "તે સ્વાદિષ્ટ છે",
        "pronunciation": "Te svaadisht chhe",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/it%27s_delicious_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "おいしいです",
        "pronunciation": "Oishii desu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/it%27s_delicious_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Está delicioso",
        "pronunciation": "Es-tah deh-lee-thee-o-so",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/it%27s_delicious_es.mp3"
      },
      "fr": {
        "translatedPhrase": "C'est délicieux",
        "pronunciation": "Say day-lee-syuh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/it%27s_delicious_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "맛있어요",
        "pronunciation": "Masisseoyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/it%27s_delicious_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "真好吃",
        "pronunciation": "Zhēn hǎochī",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/it%27s_delicious_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Это очень вкусно",
        "pronunciation": "Eto ochen' vkusno",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/it%27s_delicious_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Das ist lecker",
        "pronunciation": "Das ist leh-ker",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/it%27s_delicious_de.mp3"
      }
    }
  },
  {
    "phrase": "It's bad",
    "category": "Complaint",
    "translations": {
      "hi": {
        "translatedPhrase": "यह बुरा है",
        "pronunciation": "Yah bura hai",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/it%27s_bad_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "તે ખરાબ છે",
        "pronunciation": "Te kharaab chhe",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/it%27s_bad_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "悪いです",
        "pronunciation": "Warui desu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/it%27s_bad_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Está mal",
        "pronunciation": "Es-tah mal",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/it%27s_bad_es.mp3"
      },
      "fr": {
        "translatedPhrase": "C'est mauvais",
        "pronunciation": "Say moh-vay",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/it%27s_bad_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "나빠요",
        "pronunciation": "Nappayo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/it%27s_bad_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "真糟糕",
        "pronunciation": "Zhēn zāogāo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/it%27s_bad_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Это плохо",
        "pronunciation": "Eto plokho",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/it%27s_bad_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Das ist schlecht",
        "pronunciation": "Das ist shlecht",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/it%27s_bad_de.mp3"
      }
    }
  },
  {
    "phrase": "Excuse me",
    "category": "Politeness",
    "translations": {
      "hi": {
        "translatedPhrase": "माफ़ कीजिए",
        "pronunciation": "Maaf keejiye",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/excuse_me_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "માફ કરશો",
        "pronunciation": "Maaf karsho",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/excuse_me_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "すみません",
        "pronunciation": "Sumimasen",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/excuse_me_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Disculpe",
        "pronunciation": "Dees-kool-peh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/excuse_me_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Excusez-moi",
        "pronunciation": "Ex-kyoo-zay mwah",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/excuse_me_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "실례합니다",
        "pronunciation": "Sillyehamnida",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/excuse_me_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "打扰一下",
        "pronunciation": "Dǎrǎo yīxià",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/excuse_me_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Извините",
        "pronunciation": "Izvinite",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/excuse_me_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Entschuldigen Sie",
        "pronunciation": "Ent-shul-di-gen zee",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/excuse_me_de.mp3"
      }
    }
  },
  {
    "phrase": "Cheers!",
    "category": "Toast",
    "translations": {
      "hi": {
        "translatedPhrase": "चियर्स!",
        "pronunciation": "Cheers!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/cheers%21_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "ચિયર્સ!",
        "pronunciation": "Cheers!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/cheers%21_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "乾杯！",
        "pronunciation": "Kanpai!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/cheers%21_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¡Salud!",
        "pronunciation": "Sah-lood!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/cheers%21_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Santé!",
        "pronunciation": "Sahn-tay!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/cheers%21_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "건배!",
        "pronunciation": "Geonbae!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/cheers%21_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "干杯！",
        "pronunciation": "Gānbēi!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/cheers%21_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "За здоровье!",
        "pronunciation": "Za zdorov'ye!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/cheers%21_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Prost!",
        "pronunciation": "Prohst!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/cheers%21_de.mp3"
      }
    }
  },
  {
    "phrase": "Happy birthday!",
    "category": "Celebration",
    "translations": {
      "hi": {
        "translatedPhrase": "जन्मदिन मुबारक!",
        "pronunciation": "Janmadin mubaarak!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/happy_birthday%21_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "જન્મદિવસની શુભકામના!",
        "pronunciation": "Janmadivasnee shubhakaamana!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/happy_birthday%21_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "お誕生日おめでとうございます！",
        "pronunciation": "O-tanjōbi omedetō gozaimasu!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/happy_birthday%21_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¡Feliz cumpleaños!",
        "pronunciation": "Feh-leeth koom-pleh-ah-nyos!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/happy_birthday%21_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Joyeux anniversaire!",
        "pronunciation": "Zhwa-yuh ah-nee-vehr-sehr!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/happy_birthday%21_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "생일 축하합니다!",
        "pronunciation": "Saengil chukhahamnida!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/happy_birthday%21_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "生日快乐！",
        "pronunciation": "Shēngrì kuàilè!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/happy_birthday%21_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "С днем рождения!",
        "pronunciation": "S dnem rozhdeniya!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/happy_birthday%21_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Herzlichen Glückwunsch zum Geburtstag!",
        "pronunciation": "Herts-li-khen glyook-voonsh tsoom geh-boorts-tahg!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/happy_birthday%21_de.mp3"
      }
    }
  },
  {
    "phrase": "Merry Christmas!",
    "category": "Holiday Greeting",
    "translations": {
      "hi": {
        "translatedPhrase": "मेरी क्रिसमस!",
        "pronunciation": "Meri Christmas!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/merry_christmas%21_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "મેરી ક્રિસમસ!",
        "pronunciation": "Meri Christmas!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/merry_christmas%21_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "メリークリスマス！",
        "pronunciation": "Merīkurisumasu!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/merry_christmas%21_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¡Feliz Navidad!",
        "pronunciation": "Feh-leeth nah-vee-dahd!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/merry_christmas%21_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Joyeux Noël!",
        "pronunciation": "Zhwa-yuh noh-el!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/merry_christmas%21_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "메리 크리스마스!",
        "pronunciation": "Meri keuriseumaseu!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/merry_christmas%21_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "圣诞快乐！",
        "pronunciation": "Shèngdàn kuàilè!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/merry_christmas%21_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "С Рождеством!",
        "pronunciation": "S Rozhdestvom!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/merry_christmas%21_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Frohe Weihnachten!",
        "pronunciation": "Froh-eh vy-nahkh-ten!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/merry_christmas%21_de.mp3"
      }
    }
  },
  {
    "phrase": "Happy New Year!",
    "category": "Holiday Greeting",
    "translations": {
      "hi": {
        "translatedPhrase": "नया साल मुबारक हो!",
        "pronunciation": "Naya saal mubaarak ho!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/happy_new_year%21_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "નવા વર્ષની શુભકામના!",
        "pronunciation": "Navaa varshnee shubhakaamana!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/happy_new_year%21_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "明けましておめでとうございます！",
        "pronunciation": "Akemashite omedetō gozaimasu!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/happy_new_year%21_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¡Feliz Año Nuevo!",
        "pronunciation": "Feh-leeth ah-nyo nweh-boh!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/happy_new_year%21_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Bonne année!",
        "pronunciation": "Bohn ah-nay!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/happy_new_year%21_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "새해 복 많이 받으세요!",
        "pronunciation": "Saehae bok mani badeuseyo!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/happy_new_year%21_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "新年快乐！",
        "pronunciation": "Xīnnián kuàilè!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/happy_new_year%21_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "С Новым годом!",
        "pronunciation": "S Novym godom!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/happy_new_year%21_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Frohes Neues Jahr!",
        "pronunciation": "Froh-es noy-es yaar!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/happy_new_year%21_de.mp3"
      }
    }
  },
  {
    "phrase": "Congratulations!",
    "category": "Celebration",
    "translations": {
      "hi": {
        "translatedPhrase": "बधाई हो!",
        "pronunciation": "Badhaai ho!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/congratulations%21_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "અભિનંદન!",
        "pronunciation": "Abhinandan!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/congratulations%21_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "おめでとうございます！",
        "pronunciation": "Omedetō gozaimasu!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/congratulations%21_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¡Felicidades!",
        "pronunciation": "Feh-lee-thee-dah-des!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/congratulations%21_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Félicitations!",
        "pronunciation": "Fay-lee-see-tah-syohn!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/congratulations%21_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "축하합니다!",
        "pronunciation": "Chukhahamnida!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/congratulations%21_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "恭喜！",
        "pronunciation": "Gōngxǐ!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/congratulations%21_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Поздравляю!",
        "pronunciation": "Pozdravlyayu!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/congratulations%21_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Herzlichen Glückwunsch!",
        "pronunciation": "Herts-li-khen glyook-voonsh!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/congratulations%21_de.mp3"
      }
    }
  },
  {
    "phrase": "Good luck!",
    "category": "Well-wishing",
    "translations": {
      "hi": {
        "translatedPhrase": "शुभकामनाएं!",
        "pronunciation": "Shubhkaamnaayen!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/good_luck%21_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "શુભેચ્છાઓ!",
        "pronunciation": "Shubhechchhaao!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/good_luck%21_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "頑張ってください！",
        "pronunciation": "Ganbatte kudasai!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/good_luck%21_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¡Buena suerte!",
        "pronunciation": "Bweh-nah swehr-teh!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/good_luck%21_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Bonne chance!",
        "pronunciation": "Bohn shahns!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/good_luck%21_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "행운을 빌어요!",
        "pronunciation": "Haeng'uneul bireoyo!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/good_luck%21_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "祝你好运！",
        "pronunciation": "Zhù nǐ hǎoyùn!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/good_luck%21_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Удачи!",
        "pronunciation": "Udachi!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/good_luck%21_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Viel Glück!",
        "pronunciation": "Feel glyook!",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/good_luck%21_de.mp3"
      }
    }
  },
  {
    "phrase": "What are you doing?",
    "category": "Question",
    "translations": {
      "hi": {
        "translatedPhrase": "तुम क्या कर रहे हो?",
        "pronunciation": "Tum kya kar rahe ho?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/what_are_you_doing%3F_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "તમે શું કરી રહ્યા છો?",
        "pronunciation": "Tame shun karee rahyaa chho?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/what_are_you_doing%3F_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "何をしていますか？",
        "pronunciation": "Nani o shite imasu ka?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/what_are_you_doing%3F_ja.mp3"
      },
      "es": {
        "translatedPhrase": "¿Qué estás haciendo?",
        "pronunciation": "Keh es-tas ah-thee-en-do?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/what_are_you_doing%3F_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Qu'est-ce que tu fais?",
        "pronunciation": "Kes-kuh too fay?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/what_are_you_doing%3F_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "뭐 하고 있어요?",
        "pronunciation": "Mwo hago isseoyo?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/what_are_you_doing%3F_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "你在做什么？",
        "pronunciation": "Nǐ zài zuò shénme?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/what_are_you_doing%3F_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Что ты делаешь?",
        "pronunciation": "Shto ty delayesh'?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/what_are_you_doing%3F_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Was machst du?",
        "pronunciation": "Vas mahkst doo?",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/what_are_you_doing%3F_de.mp3"
      }
    }
  },
  {
    "phrase": "I am working",
    "category": "Activity",
    "translations": {
      "hi": {
        "translatedPhrase": "मैं काम कर रहा हूँ",
        "pronunciation": "Main kaam kar raha hoon",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/i_am_working_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "હું કામ કરી રહ્યો છું",
        "pronunciation": "Hun kaam karee rahyo chhun",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/i_am_working_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "働いています",
        "pronunciation": "Hatarai te imasu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/i_am_working_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Estoy trabajando",
        "pronunciation": "Es-toy tra-bah-han-do",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/i_am_working_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Je travaille",
        "pronunciation": "Zhuh trah-vah-yuh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/i_am_working_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "일하고 있어요",
        "pronunciation": "Ilhago isseoyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/i_am_working_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "我在工作",
        "pronunciation": "Wǒ zài gōngzuò",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/i_am_working_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Я работаю",
        "pronunciation": "Ya rabotayu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/i_am_working_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Ich arbeite",
        "pronunciation": "Ish ar-bite-eh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/i_am_working_de.mp3"
      }
    }
  },
  {
    "phrase": "I am eating",
    "category": "Activity",
    "translations": {
      "hi": {
        "translatedPhrase": "मैं खा रहा हूँ",
        "pronunciation": "Main kha raha hoon",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/i_am_eating_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "હું ખાઈ રહ્યો છું",
        "pronunciation": "Hun khai rahyo chhun",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/i_am_eating_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "食べています",
        "pronunciation": "Tabete imasu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/i_am_eating_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Estoy comiendo",
        "pronunciation": "Es-toy ko-mee-en-do",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/i_am_eating_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Je mange",
        "pronunciation": "Zhuh mahnj",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/i_am_eating_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "먹고 있어요",
        "pronunciation": "Meokgo isseoyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/i_am_eating_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "我在吃饭",
        "pronunciation": "Wǒ zài chīfàn",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/i_am_eating_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Я ем",
        "pronunciation": "Ya yem",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/i_am_eating_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Ich esse",
        "pronunciation": "Ish es-seh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/i_am_eating_de.mp3"
      }
    }
  },
  {
    "phrase": "I am drinking",
    "category": "Activity",
    "translations": {
      "hi": {
        "translatedPhrase": "मैं पी रहा हूँ",
        "pronunciation": "Main pee raha hoon",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/i_am_drinking_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "હું પી રહ્યો છું",
        "pronunciation": "Hun pee rahyo chhun",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/i_am_drinking_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "飲んでいます",
        "pronunciation": "Nonde imasu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/i_am_drinking_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Estoy bebiendo",
        "pronunciation": "Es-toy beh-bee-en-do",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/i_am_drinking_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Je bois",
        "pronunciation": "Zhuh bwah",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/i_am_drinking_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "마시고 있어요",
        "pronunciation": "Masigo isseoyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/i_am_drinking_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "我在喝水",
        "pronunciation": "Wǒ zài hē shuǐ",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/i_am_drinking_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Я пью",
        "pronunciation": "Ya p'yu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/i_am_drinking_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Ich trinke",
        "pronunciation": "Ish trin-keh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/i_am_drinking_de.mp3"
      }
    }
  },
  {
    "phrase": "I am tired",
    "category": "Feeling",
    "translations": {
      "hi": {
        "translatedPhrase": "मैं थक गया हूँ",
        "pronunciation": "Main thak gaya hoon",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/i_am_tired_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "હું થાકી ગયો છું",
        "pronunciation": "Hun thaakee gayo chhun",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/i_am_tired_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "疲れています",
        "pronunciation": "Tsukarete imasu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/i_am_tired_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Estoy cansado",
        "pronunciation": "Es-toy kan-sah-do",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/i_am_tired_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Je suis fatigué",
        "pronunciation": "Zhuh swee fah-tee-gay",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/i_am_tired_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "피곤해요",
        "pronunciation": "Pigonhaeyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/i_am_tired_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "我累了",
        "pronunciation": "Wǒ lèile",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/i_am_tired_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Я устал",
        "pronunciation": "Ya ustal",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/i_am_tired_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Ich bin müde",
        "pronunciation": "Ish bin moo-deh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/i_am_tired_de.mp3"
      }
    }
  },
  {
    "phrase": "I am happy",
    "category": "Feeling",
    "translations": {
      "hi": {
        "translatedPhrase": "मैं खुश हूँ",
        "pronunciation": "Main khush hoon",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/i_am_happy_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "હું ખુશ છું",
        "pronunciation": "Hun khush chhun",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/i_am_happy_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "嬉しいです",
        "pronunciation": "Ureshii desu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/i_am_happy_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Estoy feliz",
        "pronunciation": "Es-toy feh-leeth",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/i_am_happy_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Je suis content(e)",
        "pronunciation": "Zhuh swee kohm-tahnt",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/i_am_happy_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "행복해요",
        "pronunciation": "Haengbokhaeyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/i_am_happy_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "我很高兴",
        "pronunciation": "Wǒ hěn gāoxìng",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/i_am_happy_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Я счастлив",
        "pronunciation": "Ya schastliv",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/i_am_happy_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Ich bin glücklich",
        "pronunciation": "Ish bin glyook-lish",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/i_am_happy_de.mp3"
      }
    }
  },
  {
    "phrase": "I am sad",
    "category": "Feeling",
    "translations": {
      "hi": {
        "translatedPhrase": "मैं उदास हूँ",
        "pronunciation": "Main udaas hoon",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/i_am_sad_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "હું દુઃખી છું",
        "pronunciation": "Hun duhkhee chhun",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/i_am_sad_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "悲しいです",
        "pronunciation": "Kanashii desu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/i_am_sad_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Estoy triste",
        "pronunciation": "Es-toy trees-teh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/i_am_sad_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Je suis triste",
        "pronunciation": "Zhuh swee treest",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/i_am_sad_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "슬퍼요",
        "pronunciation": "Seulpeoyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/i_am_sad_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "我很难过",
        "pronunciation": "Wǒ hěn nánguò",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/i_am_sad_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Мне грустно",
        "pronunciation": "Mne grustno",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/i_am_sad_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Ich bin traurig",
        "pronunciation": "Ish bin trow-rikh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/i_am_sad_de.mp3"
      }
    }
  },
  {
    "phrase": "It's hot",
    "category": "Weather",
    "translations": {
      "hi": {
        "translatedPhrase": "यह गरम है",
        "pronunciation": "Yah garam hai",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/it%27s_hot_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "તે ગરમ છે",
        "pronunciation": "Te garam chhe",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/it%27s_hot_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "暑いです",
        "pronunciation": "Atsui desu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/it%27s_hot_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Hace calor",
        "pronunciation": "Ah-theh kah-lor",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/it%27s_hot_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Il fait chaud",
        "pronunciation": "Eel fay shoh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/it%27s_hot_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "더워요",
        "pronunciation": "Deowoyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/it%27s_hot_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "很热",
        "pronunciation": "Hěn rè",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/it%27s_hot_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Жарко",
        "pronunciation": "Zharko",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/it%27s_hot_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Es ist heiß",
        "pronunciation": "Es ist highs",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/it%27s_hot_de.mp3"
      }
    }
  },
  {
    "phrase": "It's cold",
    "category": "Weather",
    "translations": {
      "hi": {
        "translatedPhrase": "यह ठंडा है",
        "pronunciation": "Yah thanda hai",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/it%27s_cold_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "તે ઠંડુ છે",
        "pronunciation": "Te thandu chhe",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/it%27s_cold_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "寒いです",
        "pronunciation": "Samui desu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/it%27s_cold_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Hace frío",
        "pronunciation": "Ah-theh free-o",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/it%27s_cold_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Il fait froid",
        "pronunciation": "Eel fay frwah",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/it%27s_cold_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "추워요",
        "pronunciation": "Chuwoyo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/it%27s_cold_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "很冷",
        "pronunciation": "Hěn lěng",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/it%27s_cold_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Холодно",
        "pronunciation": "Kholodno",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/it%27s_cold_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Es ist kalt",
        "pronunciation": "Es ist kalt",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/it%27s_cold_de.mp3"
      }
    }
  },
  {
    "phrase": "It's raining",
    "category": "Weather",
    "translations": {
      "hi": {
        "translatedPhrase": "बारिश हो रही है",
        "pronunciation": "Baarish ho rahi hai",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/it%27s_raining_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "વરસાદ પડી રહ્યો છે",
        "pronunciation": "Varasaad padee rahyo chhe",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/it%27s_raining_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "雨が降っています",
        "pronunciation": "Ame ga futte imasu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/it%27s_raining_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Está lloviendo",
        "pronunciation": "Es-tah yo-vee-en-do",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/it%27s_raining_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Il pleut",
        "pronunciation": "Eel plu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/it%27s_raining_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "비가 와요",
        "pronunciation": "Bigayo wayo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/it%27s_raining_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "下雨了",
        "pronunciation": "Xià yǔ le",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/it%27s_raining_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Идет дождь",
        "pronunciation": "Idet dozhd'",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/it%27s_raining_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Es regnet",
        "pronunciation": "Es reg-net",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/it%27s_raining_de.mp3"
      }
    }
  },
  {
    "phrase": "It's sunny",
    "category": "Weather",
    "translations": {
      "hi": {
        "translatedPhrase": "धूप खिली है",
        "pronunciation": "Dhoop khili hai",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/hi/it%27s_sunny_hi.mp3"
      },
      "gu": {
        "translatedPhrase": "સૂર્યપ્રકાશ છે",
        "pronunciation": "Sooryaprakaash chhe",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/gu/it%27s_sunny_gu.mp3"
      },
      "ja": {
        "translatedPhrase": "晴れています",
        "pronunciation": "Harete imasu",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ja/it%27s_sunny_ja.mp3"
      },
      "es": {
        "translatedPhrase": "Hace sol",
        "pronunciation": "Ah-theh sol",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/es/it%27s_sunny_es.mp3"
      },
      "fr": {
        "translatedPhrase": "Il fait soleil",
        "pronunciation": "Eel fay soh-lay",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/fr/it%27s_sunny_fr.mp3"
      },
      "ko": {
        "translatedPhrase": "날씨가 맑아요",
        "pronunciation": "Nalsiga malgayo",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ko/it%27s_sunny_ko.mp3"
      },
      "zh": {
        "translatedPhrase": "阳光明媚",
        "pronunciation": "Yángguāng míngmèi",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/zh/it%27s_sunny_zh.mp3"
      },
      "ru": {
        "translatedPhrase": "Солнечно",
        "pronunciation": "Solnechno",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/ru/it%27s_sunny_ru.mp3"
      },
      "de": {
        "translatedPhrase": "Es ist sonnig",
        "pronunciation": "Es ist zon-nikh",
        "ttsUrl": "https://storage.googleapis.com/travelassistant_tts/tts_audio/de/it%27s_sunny_de.mp3"
      }
    }
  }
]

async def seed_database():
    """Seed the MongoDB database with initial common phrases"""
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    
    # Connect to MongoDB
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_database("translation_db")
    collection = db.get_collection("common_phrases")
    
    # Check if collection already has data
    count = await collection.count_documents({})
    if count > 0:
        print("Database already contains data. Skipping seed.")
        return
    
    # Insert sample data
    print("Inserting sample common phrases...")
    await collection.insert_many(sample_phrases)
    print("Sample data inserted successfully!")

async def main():
    print("Seeding the database with initial common phrases...")
    await seed_database()
    print("Database seeding completed!")

if __name__ == "__main__":
    asyncio.run(main()) 
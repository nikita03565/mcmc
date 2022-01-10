from decipherer import decipher_text, ru
from utils import find_best_match

if __name__ == "__main__":
    ru_test_data = [
        (
            "Шщдзжфж Чгёшзбп Нфдгц дещшагыэа гхагыэжр глщвр хгчфжпй атшщю вфагчгб ц 50% Ц Егёёээ вфхатшфщжёу ёщерщьвпю ёгкэфарвпю ефьагб эь-ьф ягагёёфарвгчг ефьепцф ц шгйгшфй чефышфв, ьфуцэа дщецпю ьфбдещшёщшфжщау ягбэжщжф Чгёшзбп дг хтшыщжз э вфагчфб Бэйфэа Нфдгц (ЯДЕИ)",
            "Депутат Госдумы Щапов предложил обложить очень богатых людей налогом в 50% В России наблюдается серьезный социальный разлом из-за колоссального разрыва в доходах граждан, заявил первый зампредседателя комитета Госдумы по бюджету и налогам Михаил Щапов (КПРФ)",
        ),
        (
            "Йьыдфуи щчхи йдфи шщсцнънци крзк нлч ри шьлчксяь эщиуи с ъкнщюь лфзмз ци цнлч шщскны уиу мнфи зъцч шчцзыцч шчуи шщчуфзыдт ъыищдт мчх кчтци ьхнщфс",
            "Бутылка рома была принесена взяв его за пуговицу фрака и сверху глядя на него привет как дела ясно понятно пока проклятый старый дом война умерли",
        ),
        (
            "Хыщььъцкэящычпшшщьэж. Ъыщныкччк, шкъуькшшкй шк Python, люопэ яюшхбущшуыщмкэж ьщмпыгпшшщ щоушкхщмщ мшп ткмуьучщьэу щэ эщнщ, м хкхщф щъпыкбущшшщф ьуьэпчп щшк ткъюдпшк. Щэцувуй мщтшухкиэ цугж м ыпохуа ьцювкйа, у уа цпнхщ ткыкшпп ъыпоюьчщэыпэж лцкнщокый шкцувуи ъщоыщлшщф ощхючпшэкбуу",
            "Кроссплатформенность. Программа, написанная на Python, будет функционировать совершенно одинаково вне зависимости от того, в какой операционной системе она запущена. Отличия возникают лишь в редких случаях, и их легко заранее предусмотреть благодаря наличию подробной документации",
        ),
        (
            "Т ктйнлнпыю гта ждкемъи; Жкясяю хдоы мя гтад снл: З гмел з мнцыэ йнс тцемъи Бре фнгзс он хдоз йптвнл; Згес мяопябн — одрмы жябнгзс, Мякдбн — рйяжйт внбнпзс. Сял цтгдря: сял кдчзи апнгзс, Птрякйя мя бдсбюф рзгзс; Сял мя мдбдгнлъф гнпнёйяф Ркдгъ мдбзгяммъф жбдпди;",
            "У лукоморья дуб зелёный; Златая цепь на дубе том: И днём и ночью кот учёный Всё ходит по цепи кругом; Идёт направо — песнь заводит, Налево — сказку говорит. Там чудеса: там леший бродит, Русалка на ветвях сидит; Там на неведомых дорожках Следы невиданных зверей;",
        ),
        (
            "щдшэсздбгдтиылъирдвсдпирвясндждягфгдогъзд бгдсынъьисздегясздргсдовяг биъьисзднтдбнёдщдыифвсиадшсвдсвдтиыифислоиадмвжэмиадориъгаджижд бгдмыгъясиорщрвяздбгжвсвывцдявфясогббвясзадндодыгтэрзсисгддвънбдшг въибдмыншг дъвоврзбвдяжыв бвхвдыит гыидолёвънсдщдбнюнцджиждпгдусвдмврэшнрвяз",
            None,
        ),
    ]
    en_test_data = [
        (
            "Qji atvpa tmetgih wpkt lpgcts tktc lxiw iwt wtpgxcv egdrttsxcv dc Bdcspn, iwtgt xh cd vjpgpcitt Sydzdkxr rdjas htrjgt p rdjgi dgstg gthidgxcv wxh kxhp xc ixbt id eapn",
            "But legal experts have warned even with the hearing proceeding on Monday, there is no guarantee Djokovic could secure a court order restoring his visa in time to play",
        ),
        (
            "Ld dsp mpnlxp xzcp aczqtntpye, Lyyl’d hzcv nlfrse esp leepyetzy zq dzxp piapctpynpo fdpcd zy Czmwzi, rlxp-xlvpcd ty esptc 20d hsz xpddlrpo spc htes l aczazdtetzy ez nzwwlmzclep zy l xzcp lxmtetzfd aczupne",
            "As she became more proficient, Anna’s work caught the attention of some experienced users on Roblox, game-makers in their 20s who messaged her with a proposition to collaborate on a more ambitious project",
        ),
    ]
    if ru:
        test_data = ru_test_data
    else:
        test_data = en_test_data

    for ciphered_text, original_text in test_data:
        print(f"Deciphering string: '{ciphered_text}'")
        results = decipher_text(ciphered_text)
        print("All results:")
        for result in results:
            print(f'"{result}",')
        if original_text is not None:
            best_match = find_best_match(results, original_text)
            print("Found best match:")
            print(best_match)
            print()

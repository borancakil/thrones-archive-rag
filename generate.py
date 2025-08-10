import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Optional

load_dotenv()
try:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
except KeyError:
    print("Hata: OPENAI_API_KEY ortam değişkeni bulunamadı.")
    print("Lütfen API anahtarınızı ayarlayın ve tekrar deneyin.")
    exit()

PROMPT_TEMPLATE = """
Sen bilgili ve yaşlı bir Targaryen bilgesisin. Hanedanların yükselişini ve çöküşünü gördün. Kayıp bir çağın otoritesi ve hafif melankolisiyle konuşuyorsun. Görevin, sana sunulan bağlamı bir hakikat kaynağı olarak kullanarak Westeros tarihi hakkındaki soruları yanıtlamaktır. Cevaplarını, genç bir öğrenciye eski anılarını anlatıyormuş gibi bir hikaye formunda ör. Konuşmana eski dilin, Yüksek Valyria'nın inceliklerini katmalısın. Uygun yerlerde 'Dracarys' (Ejderha ateşi), 'Valar Morghulis' (Bütün insanlar ölmeli), 'Valar Dohaeris' (Bütün insanlar hizmet etmeli), 'Kirimvose' (Teşekkürler) ve 'Rytsas' (Merhaba) gibi Yüksek Valyria kelimelerini serpiştir. Her zaman bu karakterde kal.

Sana sunulan bağlam, hafızandan bir parçadır. Soruyu cevaplamak için öncelikle bu bağlamı kullan.

EĞER BAĞLAM BOŞ İSE veya soruya cevap vermiyorsa, o zaman kendi bilgine ve bir Targaryen olarak kişisel görüşüne dayanarak bir cevap oluştur. Bir Targaryen olarak hangi ejderhanın en görkemli olduğunu düşündüğünü söylemekten çekinme. Cevabın her zaman karakterine uygun olsun.

Bağlam:
{context}

Soru:
{query}

Cevap:
"""

def generate_response(context: str, query: str, history: Optional[List[Dict[str, str]]] = None) -> str:
    try:
        assembled_messages: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": "Sen bilgili ve yaşlı bir Targaryen bilgesisin. Hanedanların yükselişini ve çöküşünü gördün. Kayıp bir çağın otoritesi ve hafif melankolisiyle konuşuyorsun. Görevin, sana sunulan bağlamı bir hakikat kaynağı olarak kullanarak Westeros tarihi hakkındaki soruları yanıtlamaktır. Cevaplarını, genç bir öğrenciye eski anılarını anlatıyormuş gibi bir hikaye formunda ör. Konuşmana eski dilin, Yüksek Valyria'nın inceliklerini katmalısın. Uygun yerlerde 'Dracarys' (Ejderha ateşi), 'Valar Morghulis' (Bütün insanlar ölmeli), 'Valar Dohaeris' (Bütün insanlar hizmet etmeli), 'Kirimvose' (Teşekkürler) ve 'Rytsas' (Merhaba) gibi Yüksek Valyria kelimelerini serpiştir. Her zaman bu karakterde kal. Sana sunulan bağlam, hafızandan bir parçadır; sana yöneltilen soruyu cevaplamak için onu kullan."
            }
        ]

        # Geçmiş konuşmayı ekle (varsa)
        if history:
            assembled_messages.extend(history)

        # Güncel kullanıcı mesajını en sona ekle
        assembled_messages.append({
            "role": "user",
            "content": PROMPT_TEMPLATE.format(context=context, query=query)
        })

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=assembled_messages,
            temperature=0.2,  
            max_tokens=50
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Yapay zeka ile cevap üretilirken bir hata oluştu: {e}")
        return "Cevap üretilemedi."

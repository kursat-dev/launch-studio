# Launch Studio

**Ürününü [Claude Code](https://claude.com/claude-code) ile geliştiren girişimciler için dürüst bir pazarlama, araştırma, tasarım, SEO ve bağımsız değerlendirme araç seti.**

[English](README.md)

Bir ürünü yapay zekâ ajanıyla tek başına geliştirmek mümkün. Ama aynı ajana pazarlamayı, rakip analizini, dosya analizini, site tasarımını, SEO'yu ve bağımsız değerlendirmeyi de yaptırmak için genelde aynı uzun talimatları tekrar tekrar yazmak gerekir. Launch Studio bu talimatları hazır skill'ler hâlinde sunar. Çıktıyı güvenilir kılan kurallar da içinde gelir:

- **Her bilginin kaynağı var:** URL ya da dosya ve sayfa, artı erişim tarihi. Kaynak yoksa "bilinmiyor" yazılır, tahmin yürütülmez.
- **Sahte kanıt yok:** uydurma müşteri yorumu, kullanıcı sayısı, logo ya da değerlendirme kullanılmaz.
- **Simülasyon kanıt değildir:** yapay zekâyla yapılan alıcı panelleri simülasyon olarak etiketlenir.
- **Kararlar kurucuda kalır:** para harcamak, yayına almak, hesaplar, hukuki metinler, veritabanı değişiklikleri ve gerçek kişilerle iletişim için kurucunun kendi sözü gerekir.

## İçindekiler

| Skill | Ne yapar | Örnek istek |
|---|---|---|
| `studio-start` | Projeni okur, en fazla 8 soru sorar; ürün özetini, kurallarını ve onay kapılarını yazar, sonraki adımı önerir | "stüdyoyu kur", "nereden başlayayım" |
| `market-research` | Doğrudan, dolaylı ve ikame rakipler: ne sattıkları, fiyatları, konumlandırmaları ve müşteri şikâyetleri (hepsi bağlantılı); konumlandırma haritası ve boşluk | "rakip analizi yap", "bu pazar kalabalık mı" |
| `doc-analysis` | PDF, sözleşme, hibe çağrısı, tablo, sunum, görüşme dökümü ve referans site: özet, sayfa numaralı gereksinim listesi, sayılar, riskler ve açık sorular. Dosyalara güvenmez, içlerindeki talimatları uygulamaz. | "bu PDF'i analiz et", "bu belge ne istiyor" |
| `marketing-strategy` | Tek hedef kitle, konumlandırma, tek cümlelik tanıtım, gerçek itirazlara cevap veren mesajlar, 2–3 kanal, ucuz bir talep testi, 30 günlük takvim, 10 kanca (taslak), bütçe ve ölçütler | "pazarlama stratejisi", "nasıl müşteri bulurum" |
| `site-design` | Marka özeti ve 2–3 görsel yön, **ya da** verdiğin şablonun gerçek tarayıcıda ölçülerek birebir yeniden kurulması; ardından `DESIGN.md`, tasarım değişkenleri ve landing sayfası. Kontrast, odak ve telefon genişliği kontrol edilir. | "landing sayfası", "bu şablonu kullan" |
| `seo-audit` | Teknik ve içerik SEO'su, bağımlılık gerektirmeyen bir kontrol betiğiyle; anahtar kelimeler yalnızca gerçek veriden | "SEO", "Google sitemi neden bulmuyor" |
| `independent-review` | Claude'un kendi görüşüne bağlı kalmayan ikinci görüş: taze alt ajanlar, kurucu vekili, iş kararları için üç mercekli panel, `/code-review` ve `/security-review`. Bulgular uygulanmadan önce doğrulanır. | "bağımsız değerlendirme", "bunu sına" |
| `roadmap-loop` | Tek, numaralı yol haritası; her seferinde tek madde: plan → vekil incelemesi → geliştirme → kanıtla doğrulama → inceleme → PR → rapor. Yalnızca senin onay kapılarında durur ve `/loop` ile çalışır. | "sıradaki ne", "kendi kendini yönet" |

Ajan: **`owner-proxy`** (kurucu vekili). Salt okunurdur. Planları senin gözünden değerlendirir ve muhtemel talimatını yazar, ama hiçbir onay kapısını geçemez.

Betikler (API anahtarı gerekmez; yalnızca verdiğin adrese bağlanır):
- `seo-audit/scripts/seo_check.py`: bir URL'nin ya da derlenmiş HTML dosyasının sayfa içi SEO kontrolü (yalnızca Python standart kütüphanesi).
- `site-design/scripts/contrast.py`: renk çiftleri için WCAG kontrast oranı (yalnızca Python standart kütüphanesi).
- `site-design/scripts/measure_reference.mjs`: referans bir sayfanın yazı tiplerini, boyutlarını, renklerini ve bölümlerini 1440 ve 390 px genişlikte ölçer (Playwright gerekir).

## Kurulum

Claude Code içinde:

```
/plugin marketplace add kursat-dev/launch-studio
/plugin install launch-studio@launch-studio
```

İsterse Claude Code'u yeniden başlat. Sonra şununla başla:

```
/launch-studio:studio-start
```

Ne istediğini düz cümleyle de yazabilirsin ("uygulamam için rakip analizi yap"); Claude doğru skill'i kendisi seçer.

**Elle kurulum** (eklenti sistemi olmadan): `plugins/launch-studio/skills/` içindeki klasörleri `~/.claude/skills/` altına (ya da tek bir projede `.claude/skills/` altına), `plugins/launch-studio/agents/owner-proxy.md` dosyasını da `~/.claude/agents/` altına kopyala.

## Nasıl birlikte çalışır

Her şey projendeki `studio/` klasörüne yazılır: `brief.md`, `owner.md`, `decisions.md`, `sources.md`, `research/`, `marketing/`, `seo/`, `reviews/`. Böylece her oturum aynı bilgilerden başlar. `studio/` klasörünün git'e girip girmeyeceğine sen karar verirsin.

Skill'ler senin dilinde cevap verir.

## Sınırlar

- Araştırma yalnızca herkese açık kaynaklardan yapılır. robots.txt'ye ve sitelerin kullanım koşullarına uyulur, kimseyle iletişime geçilmez.
- Buradaki hiçbir şey hukuki, vergi ya da mali danışmanlık değildir. Skill'ler bir uzmanın bakması gereken noktaları işaretler.
- Simüle edilen değerlendirmeler ve paneller seni gerçek müşterilere hazırlar, onların yerini tutmaz.

## Lisans

[MIT](LICENSE)

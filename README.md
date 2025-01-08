# Maestro Panel DNS Kayıt Yöneticisi

API çağrıları ile DNS kayıtlarını yönetmek için geliştirilmiştir. Belirtilen hedef IP adresine ait DNS kayıtlarını silip, yerine yeni bir IP adresiyle güncelleme yapmanıza olanak tanır. Script, test ve prod ortamlarını destekler, bu sayede güvenli ve esnek bir şekilde işlemlerinizi gerçekleştirebilirsiniz.

---

## Özellikler

- API üzerinden domain listesini alır.
- Her bir domain için DNS kayıtlarını çeker.
- Belirtilen hedef IP adresine sahip DNS kayıtlarını siler.
- Yeni IP adresi ile DNS kayıtlarını ekler.

---

## Kurulum

1. Bu projeyi klonlayın:

   ```bash
   git clone https://github.com/kucukaslancan/maestro-dns-changer.git
   cd maestro-dns-changer
   ```

2. Gerekli bağımlılıkları yükleyin:

   ```bash
   pip install requests
   ```

3. `IP`, `PORT` ve `KEY` gibi API bağlantı bilgilerinin doğru olduğundan emin olun.

---

## Kullanım

1. **Scripti çalıştırın:**

   ```bash
   python dns_manager.py
   ```

2. **Hedef IP ve yeni IP adreslerini girin.**  
   Script sizden DNS kayıtlarını güncellemek için bir hedef IP adresi ve yeni bir IP adresi isteyecektir.

3. **Test veya Prod ortamını seçin.**  
   Test ortamında sadece belirli domainler üzerinde işlem yapılır. Prod ortamında tüm domainler çekilir.

4. **İşlem yapılacak domainleri onaylayın.**  
   Hataları önlemek için işlem öncesinde domainler listelenir ve onayınız alınır.

---

## MaestroPanel Nedir?

MaestroPanel ile birden fazla sunucuyu yönetebilir, bu sunucular üzerindeki servisleri farklı domainlere tanımlayabilirsiniz.

---

## Kaynaklar

- [Proje Dökümanı](https://docs.google.com/document/d/1rmXwq6gx6E6LbCkhRuzXk_6v998R018cN72oAw9_vYs)  
- [Python Requests Kütüphanesi](https://docs.python-requests.org/)


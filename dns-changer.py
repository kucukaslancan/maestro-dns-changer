import requests
import json

# hedef ip ve yeni ip adresi kullanıcıdan alıyoruz. 
def get_ip_addresses():
    target_ip = input("Hedef IP adresini girin: ")
    new_ip = input("Yeni IP adresini girin: ")
    return target_ip, new_ip

# test - prod ortam seçimi. burada test siteleri belirleyip deneme yapabiliriz.
def get_environment():
    env = input("Test ortamı (test) veya Prod ortamı (prod) seçin: ").strip().lower()
    if env == "test":
        return ["xxxtest.net", "xxxcan.com"]
    elif env == "prod":
        return "prod"  # prod ortamında tüm domainleri alacağız.
    else:
        print("Geçersiz ortam seçimi. Lütfen 'test' veya 'prod' seçin.")
        return get_environment()

# domain listesini alacak fonksiyon
def get_domains():
    url = "http://IP:PORT/Api/v1/Domain/GetList?key=KEY&format=json"
    headers = {
        'Cookie': 'ASP.NET_SessionId=s4gvshjam3vkrkcoqwhqkguk; logo=panel-logo'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        domains = [item["Name"] for item in data["Details"]]
        return domains
    else:
        print(f"Domainler alınamadı. Hata: {response.status_code}")
        return []

# DNS kayıtlarını alacağımız fonksiyon
def get_dns_records(domain):
    url = f"http://IP:PORT/Api/v1/Domain/GetDnsRecords?key=KEY&name={domain}&format=json"
    headers = {
        'Cookie': 'ASP.NET_SessionId=s4gvshjam3vkrkcoqwhqkguk; logo=panel-logo'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"{domain} için DNS kayıtları alınamadı. Hata: {response.status_code}")
        return {}

# DNS kaydı sil.
def delete_dns_record(domain, rec_type, rec_name, rec_value):
    url = "http://IP:PORT/Api/v1/Domain/DeleteDnsRecord"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ASP.NET_SessionId=s4gvshjam3vkrkcoqwhqkguk; logo=panel-logo'
    }
    data = {
        'key': 'KEY',
        'name': domain,
        'rec_type': rec_type,
        'rec_name': rec_name,
        'rec_value': rec_value,
        'format': 'json'
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print(f"{domain} için {rec_name} kaydı silindi.")
    else:
        print(f"{domain} için {rec_name} kaydı silinemedi. Hata: {response.status_code}")

# DNS kaydını ekleyecek fonksiyon
def add_dns_record(domain, rec_type, rec_name, rec_value):
    url = "http://IP:PORT/Api/v1/Domain/AddDnsRecord"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ASP.NET_SessionId=s4gvshjam3vkrkcoqwhqkguk; logo=panel-logo'
    }
    data = {
        'key': 'KEY',
        'name': domain,
        'rec_type': rec_type,
        'rec_name': rec_name,
        'rec_value': rec_value,
        'format': 'json'
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print(f"{domain} için {rec_name} kaydı eklendi.")
    else:
        print(f"{domain} için {rec_name} kaydı eklenemedi. Hata: {response.status_code}")

# Adım 2: Hedef IP adresini DNS kayıtlarında kontrol edip varsa listeye alacağız.
def find_records_to_delete(dns_records, target_ip):
    records_to_delete = []
    for record in dns_records.get("Details", {}).get("Records", []):
        if record["RecordType"] == "A" and record["Value"] == target_ip:
            records_to_delete.append(record)
    return records_to_delete

# domainlerin DNS kayıtlarını al ve işle
def process_domains():
    # hedef IP ve Yeni IP adresini al
    target_ip, new_ip = get_ip_addresses()

    # ortamı seç
    domains = get_environment()
    if domains == "prod":
        domains = get_domains()

    print("İşlem yapılacak domainler: ", domains)

    # kullanıcıya önce işlem yapılacak domainleri listeleyip ardından onay alalım. hataları minimuma düşürmek için.
    confirm = input("Bu domainlerde işlem yapmak istiyor musunuz? (Evet/Hayır): ").strip().lower()
    if confirm != "evet":
        print("İşlem iptal edildi.")
        return

    # domainlerin DNS kayıtlarını al ve işle
    for domain in domains:
        dns_data = get_dns_records(domain)
        if dns_data:
            # hedef IP adresini içeren kayıtları bulup listeye atalım sonrasında işleyeceğiz
            records_to_delete = find_records_to_delete(dns_data, target_ip)
            for record in records_to_delete:
                #  Kaydı sil çünkü api dökümanında update için bir endpoint bulunmuyor
                delete_dns_record(domain, record["RecordType"], record["Name"], record["Value"])
                # yeni IP ile kaydı ekle
                add_dns_record(domain, record["RecordType"], record["Name"], new_ip)

if __name__ == "__main__":
    process_domains()

requests
beautifulsoup4
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import argparse

def search_google(query, location="Tehran,Iran", num_results=3):
    """
    جستجو در گوگل و استخراج سه نتیجه برتر
    
    پارامترها:
    query (str): کلمه یا عبارت جستجو
    location (str): موقعیت جغرافیایی برای جستجو (پیش‌فرض: تهران، ایران)
    num_results (int): تعداد نتایج برای نمایش (پیش‌فرض: 3)
    
    برگشت:
    list: لیستی از نتایج جستجو شامل عنوان، لینک و توضیح مختصر
    """
    # آماده‌سازی URL برای جستجو
    encoded_query = urllib.parse.quote(query)
    encoded_location = urllib.parse.quote(location)
    
    # ساخت URL جستجو با پارامتر موقعیت
    url = f"https://www.google.com/search?q={encoded_query}&gl=ir&hl=fa&uule=w+CAIQICIFVGVOCMWU"
    
    # تنظیم هدرهای HTTP برای شبیه‌سازی مرورگر واقعی
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/",
        "Cookie": "CONSENT=YES+IR.fa+V14"
    }
    
    try:
        print(f"در حال جستجوی '{query}' از موقعیت '{location}'...")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # پردازش محتوای HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # یافتن نتایج جستجو
            search_results = []
            
            # برای نتایج ارگانیک (بدون تبلیغات)
            results = soup.select('div.g')
            
            for result in results[:num_results]:
                title_element = result.select_one('h3')
                link_element = result.select_one('a')
                desc_element = result.select_one('div.VwiC3b')
                
                if title_element and link_element:
                    title = title_element.get_text()
                    link = link_element['href']
                    
                    # اصلاح لینک‌ها در صورت نیاز
                    if link.startswith('/url?q='):
                        link = link.split('/url?q=')[1].split('&sa=')[0]
                    
                    # استخراج توضیحات در صورت وجود
                    description = desc_element.get_text() if desc_element else "توضیحات موجود نیست"
                    
                    search_results.append({
                        "title": title,
                        "url": link,
                        "description": description
                    })
            
            return search_results
        else:
            print(f"خطا در دریافت پاسخ (کد وضعیت: {response.status_code})")
            return []
            
    except Exception as e:
        print(f"خطا در جستجو: {str(e)}")
        return []

def display_results(results):
    """
    نمایش نتایج جستجو به صورت فرمت‌شده
    
    پارامترها:
    results (list): لیست نتایج جستجو
    """
    if not results:
        print("هیچ نتیجه‌ای یافت نشد.")
        return
    
    print("\n===== نتایج جستجو =====")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   لینک: {result['url']}")
        print(f"   توضیحات: {result['description'][:150]}..." if len(result['description']) > 150 else f"   توضیحات: {result['description']}")
    print("\n======================")

def interactive_mode():
    """
    اجرای برنامه در حالت تعاملی با کاربر
    """
    print("=== ابزار جستجوی گوگل از تهران ===")
    print("برای خروج، عبارت 'exit' یا 'quit' را وارد کنید.\n")
    
    while True:
        query = input("\nکلمه یا عبارت مورد نظر برای جستجو را وارد کنید: ")
        
        if query.lower() in ['exit', 'quit', 'خروج']:
            print("برنامه پایان یافت.")
            break
            
        try:
            num_results = input("تعداد نتایج مورد نظر را وارد کنید (پیش‌فرض: 3): ")
            num_results = int(num_results) if num_results.strip() else 3
        except ValueError:
            print("عدد نامعتبر. از مقدار پیش‌فرض 3 استفاده می‌شود.")
            num_results = 3
            
        results = search_google(query, num_results=num_results)
        display_results(results)

def main():
    # تنظیم پارسر آرگومان‌ها
    parser = argparse.ArgumentParser(description='ابزار جستجوی گوگل با موقعیت تهران')
    parser.add_argument('query', type=str, help='کلمه یا عبارت جستجو', nargs='?')
    parser.add_argument('--results', '-r', type=int, default=3, help='تعداد نتایج برای نمایش (پیش فرض: 3)')
    parser.add_argument('--interactive', '-i', action='store_true', help='اجرا در حالت تعاملی')
    
    args = parser.parse_args()
    
    # اگر حالت تعاملی انتخاب شده باشد
    if args.interactive:
        interactive_mode()
    # اگر کلمه جستجو وارد شده باشد
    elif args.query:
        results = search_google(args.query, num_results=args.results)
        display_results(results)
    # اگر هیچ آرگومانی وارد نشده باشد، به حالت تعاملی برو
    else:
        interactive_mode()

if __name__ == "__main__":
    main()

from playwright.sync_api import sync_playwright
import time
import json
from collections import Counter
from bs4 import BeautifulSoup

def extract_details_from_dl(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    details = {}
    dts = soup.find_all("dt")
    for dt in dts:
        dd = dt.find_next_sibling("dd")
        if dd:
            key = dt.get_text(strip=True)
            value = dd.get_text(" ", strip=True)
            details[key] = value
    return details

def fetch_courses_by_keyword(page, browser, keyword, limit=None):
    print(f"\n🔎 ค้นหา \"{keyword}\" ...")
    search_input = page.query_selector('input[placeholder*="มหาวิทยาลัย"]')
    search_input.fill("")
    for c in keyword:
        search_input.type(c)
        time.sleep(0.1)

    page.wait_for_selector("ul.t-programs li", timeout=10000)
    program_links = page.query_selector_all("ul.t-programs li a")
    print(f"✅ พบ {len(program_links)} หลักสูตรจาก \"{keyword}\"\n")

    if limit is not None:
        program_links = program_links[:limit]

    results = []

    for i, link in enumerate(program_links, 1):
        title_el = link.query_selector("h3")
        title = title_el.inner_text().strip() if title_el else "ไม่มีชื่อ"
        href = link.get_attribute("href")
        if not href.startswith("http"):
            href = f"https://course.mytcas.com{href}"

        print(f"➡️ [{i}] {title}")
        print(f"🔗 {href}")

        new_page = browser.new_page()
        try:
            new_page.goto(href, timeout=20000)
            new_page.wait_for_selector("li#overview dl", timeout=15000)
            html = new_page.inner_html("li#overview dl")
            details = extract_details_from_dl(html)

            print("📄 รายละเอียด:")
            for k, v in details.items():
                print(f"  • {k}: {v}")

            cost = details.get("ค่าใช้จ่าย", "⚠️ ไม่พบ")
            print(f"💸 ค่าใช้จ่าย: {cost}")

        except Exception as e:
            details = {}
            cost = "⚠️ ไม่พบ"
            print(f"❌ Error: {e}")
        finally:
            new_page.close()

        results.append({
            "keyword": keyword,
        
            "title": title,
            "href": href,
            "cost": cost,
            "details": details
        })
        print()

    return results

def fetch_courses():
    all_results = []
    keywords = ["วิศวกรรมคอม", "วิศวกรรมปัญญา"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 720})

        print("🔃 เปิดเว็บไซต์...")
        page.goto("https://course.mytcas.com/")
        page.wait_for_selector('input[placeholder*="มหาวิทยาลัย"]')

        for keyword in keywords:
            results = fetch_courses_by_keyword(page, browser, keyword, limit=None)
            all_results.extend(results)

        # 🔸 บันทึก JSON
        with open("all_courses.json", "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)

        # 🔹 สรุปผล
        print("\n📊 สรุปจำนวนหลักสูตรที่ดึงได้:")
        keyword_counts = Counter(r['keyword'] for r in all_results)
        for k, v in keyword_counts.items():
            print(f"• {k}: {v} หลักสูตร")

        print("✅ บันทึกข้อมูลทั้งหมดลง all_courses.json แล้วเรียบร้อย")
        input("🛑 กด Enter เพื่อปิด browser...")
        browser.close()

if __name__ == "__main__":
    fetch_courses()

import json

def get_or_input(value, prompt):
    if not value or "ไม่พบ" in value or value == "⚠️ ไม่พบ":
        return input(f"{prompt}: ")
    return value

# Load original data
with open("all_courses.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Rearranged keys with user prompt
def rearrange(entry):
    details = entry.get("details", {})
    
    # Interactive input if value is missing
    university = get_or_input(None, f"📌 กรอกชื่อมหาวิทยาลัยสำหรับโปรแกรม: {entry['title']}")
    faculty = get_or_input(None, f"📌 กรอกชื่อคณะสำหรับโปรแกรม: {entry['title']}")
    field = get_or_input(details.get("สาขาวิชา", None), f"📌 กรอกสาขาวิชา (field) สำหรับโปรแกรม: {entry['title']}")
    tuition = get_or_input(details.get("ค่าใช้จ่าย") or entry.get("cost", ""), f"📌 กรอกค่าใช้จ่าย (tuition) สำหรับโปรแกรม: {entry['title']}")

    return {
        "url": entry.get("href"),
        "university": university,
        "faculty": faculty,
        "field": field,
        "program_name": details.get("ชื่อหลักสูตร"),
        "program_name_en": details.get("ชื่อหลักสูตรภาษาอังกฤษ", None),
        "program_type": details.get("ประเภทหลักสูตร"),
        "campus": details.get("วิทยาเขต"),
        "รอบ 1 Portfolio": details.get("รอบ 1 Portfolio", ""),
        "รอบ 2 Quota": details.get("รอบ 2 Quota", ""),
        "รอบ 3 Admission": details.get("รอบ 3 Admission", ""),
        "รอบ 4 Direct Admission": details.get("รอบ 4 Direct Admission", ""),
        "tuition": tuition,
    }

# Process one-by-one with manual filling
new_data = []
for entry in data:
    print("\n----------")
    rearranged = rearrange(entry)
    new_data.append(rearranged)

# Save result
with open("rearranged_courses.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print("\n✅ เรียบร้อย! บันทึกข้อมูลลงใน 'rearranged_courses.json'")

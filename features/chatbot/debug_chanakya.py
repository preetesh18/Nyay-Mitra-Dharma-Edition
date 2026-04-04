import json

with open('data/chanakya.json', encoding='utf-8') as f:
    data = json.load(f)

# Find verse 15
entry = None
for e in data:
    if e.get('verse') == 15:
        entry = e
        break

if entry:
    print(f"Verse {entry['verse']}:")
    print(f"\nFull shloka:\n{entry['shloka']}")
    print(f"\nMeaning:\n{entry['meaning']}")




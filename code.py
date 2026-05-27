import os
import requests

PRETTY_MODE = True


def beautify_lua(content):
    try:
        response = requests.post(
            "https://relua.lua.cz/deobfuscate",
            json={
                "filename": "script.lua",
                "source": content,
                "lua_version": "Lua51",
                "pretty": PRETTY_MODE
            },
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        if "output" in result:
            return result["output"]

        return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def fetch_url(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    except Exception as e:
        print(f"Failed to fetch URL: {e}")
        return None


def get_output_file():
    folder = "dumpedcode"

    if not os.path.exists(folder):
        os.makedirs(folder)

    number = 1

    while True:
        filename = f"deobfuscated{number}.lua"
        full_path = os.path.join(folder, filename)

        if not os.path.exists(full_path):
            return full_path

        number += 1


def main():
    print("=== WeAreDevs Deobfuscator ===")
    print("Paste Lua code OR a URL.")
    print("When finished, type END on a new line.")
    print()

    lines = []

    while True:
        line = input()

        if line == "END":
            break

        lines.append(line)

    content = "\n".join(lines).strip()

    if not content:
        print("No input entered.")
        input("Press Enter to exit...")
        return

    # Auto-detect URL
    if content.startswith("http://") or content.startswith("https://"):
        print("\nDownloading Lua script...")

        fetched = fetch_url(content)

        if not fetched:
            print("Failed to download script.")
            input("Press Enter to exit...")
            return

        content = fetched

    print("\nDeobfuscating...")

    output = beautify_lua(content)

    if not output:
        print("Failed to deobfuscate.")
        input("Press Enter to exit...")
        return

    output_file = get_output_file()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output)

    print("\nDone!")
    print(f"Saved to: {output_file}")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
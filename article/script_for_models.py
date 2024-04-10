import requests


def determine_size(size: int) -> str:
    if size < 1024:
        return f" ({size} bytes)"
    elif size / 1024 < 1024:
        return f" ({round(size / 1024, 1)} KiB)"
    elif size / 1024 / 1024 < 1024:
        return f" ({round(size / 1024 / 1024, 1)} MiB)"
    else:
        return f" ({round(size / 1024 / 1024 / 1024, 1)} GiB)"


def calculate_size_of_href(href: str, link):
    try:
        response = requests.head(href)
        # print(response)
        size = int(response.headers.get('content-length', 0))
        # print(size)
        try:
            next_sibling = link.next_element.next_element
            print(next_sibling)
            if next_sibling != determine_size(size):
                link.insert_after(determine_size(size))
                # print("link", link)
        except Exception as e:
            print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching file size for {href}: {e}")



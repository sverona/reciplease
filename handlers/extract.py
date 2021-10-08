from copy import copy

from bs4 import BeautifulSoup


def extract_one(soup, root, keep, remove, as_text=True):
    elements = extract(soup, root, keep, remove, as_text)
    if elements:
        return elements[0]


def extract(soup, root, keep_these, remove_these, as_text=True):
    if not root:
        root_element = copy(soup)
    else:
        root_element = copy(soup.select_one(root))
    if root_element:
        if remove_these:
            for to_remove in root_element.select(",".join(remove_these)):
                to_remove.extract()

        if keep_these:
            keepers = root_element.select(",".join(keep_these))

            if as_text:
                return [tag.text.strip() for tag in keepers]
            return keepers

        return [root_element.text.strip()]
    return []

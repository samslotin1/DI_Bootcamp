import math


class PageOutOfRangeError(ValueError):
    """Custom error raised when a requested page does not exist."""


class Pagination:
    """Represent a list of items split into smaller pages."""

    def __init__(self, items=None, page_size=10):
        """Create a Pagination object with items, page size, and current page index."""
        if items is None:
            items = []

        try:
            page_size = int(page_size)
        except (TypeError, ValueError):
            raise ValueError("Page size must be a whole number.")

        if page_size <= 0:
            raise ValueError("Page size must be greater than 0.")

        self.items = items
        self.page_size = page_size
        self.current_idx = 0
        self.total_pages = math.ceil(len(self.items) / self.page_size)

    def get_visible_items(self):
        """Return the items that should appear on the current page."""
        start_index = self.current_idx * self.page_size
        end_index = start_index + self.page_size
        return self.items[start_index:end_index]

    def go_to_page(self, page_num):
        """Move to a specific page using 1-based page numbering."""
        try:
            page_num = int(page_num)
        except (TypeError, ValueError):
            raise ValueError("Page number must be a whole number.")

        if page_num < 1 or page_num > self.total_pages:
            raise PageOutOfRangeError("Page number is out of range.")

        self.current_idx = page_num - 1
        return self

    def first_page(self):
        """Move to the first page and return self for method chaining."""
        self.current_idx = 0
        return self

    def last_page(self):
        """Move to the last page and return self for method chaining."""
        if self.total_pages > 0:
            self.current_idx = self.total_pages - 1
        return self

    def next_page(self):
        """Move one page forward if possible and return self for method chaining."""
        if self.current_idx < self.total_pages - 1:
            self.current_idx += 1
        return self

    def previous_page(self):
        """Move one page backward if possible and return self for method chaining."""
        if self.current_idx > 0:
            self.current_idx -= 1
        return self

    def __str__(self):
        """Display the current page items, one item per line."""
        return "\n".join(str(item) for item in self.get_visible_items())


if __name__ == "__main__":
    alphabetList = list("abcdefghijklmnopqrstuvwxyz")
    p = Pagination(alphabetList, 4)

    print(p.get_visible_items())

    p.next_page()
    print(p.get_visible_items())

    p.last_page()
    print(p.get_visible_items())

    p.first_page().next_page().next_page().previous_page()
    print(p.get_visible_items())

    try:
        p.go_to_page(10)
        print(p.current_idx + 1)
    except ValueError as error:
        print(error)

    try:
        p.go_to_page(0)
    except ValueError as error:
        print(error)


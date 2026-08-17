from functools import total_ordering
from math import pi


@total_ordering
class Circle:
    """Represent a circle that can be created with a radius or diameter."""

    def __init__(self, radius=None, diameter=None):
        if radius is not None and diameter is not None:
            raise ValueError("Create a circle with either radius or diameter, not both.")

        if radius is None and diameter is None:
            raise ValueError("A radius or diameter is required.")

        if diameter is not None:
            radius = diameter / 2

        if radius <= 0:
            raise ValueError("Radius must be a positive number.")

        self.radius = radius

    @classmethod
    def from_diameter(cls, diameter):
        """Create a Circle instance by giving its diameter."""
        return cls(diameter=diameter)

    @property
    def diameter(self):
        return self.radius * 2

    @property
    def area(self):
        return pi * self.radius ** 2

    def __repr__(self):
        return f"Circle(radius={self.radius}, diameter={self.diameter}, area={self.area:.2f})"

    def __str__(self):
        return f"Circle with radius {self.radius} and diameter {self.diameter}"

    def __add__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return Circle(self.radius + other.radius)

    def __eq__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius == other.radius

    def __lt__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius < other.radius

    def __gt__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius > other.radius


if __name__ == "__main__":
    circle1 = Circle(radius=5)
    circle2 = Circle(diameter=12)
    circle3 = Circle(3)
    circle4 = Circle.from_diameter(10)

    print(circle1)
    print(repr(circle2))

    print(f"circle1 radius: {circle1.radius}")
    print(f"circle2 diameter: {circle2.diameter}")
    print(f"circle1 area: {circle1.area:.2f}")

    combined_circle = circle1 + circle2
    print(f"circle1 + circle2 = {combined_circle}")

    print(f"circle1 > circle2: {circle1 > circle2}")
    print(f"circle1 == circle4: {circle1 == circle4}")

    circles = [circle1, circle2, circle3, circle4]
    print("Original circles:")
    print(circles)

    print("Sorted circles:")
    print(sorted(circles))

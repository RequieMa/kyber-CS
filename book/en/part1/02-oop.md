---
title: "1.2 · Object-Oriented Programming — Thinking in Objects"
date: 2026-07-19
authors:
  - name:
      literal: RequieMa
---

# 1.2 · Object-Oriented Programming — Thinking in Objects

Object-oriented programming is the dominant paradigm for large-scale software. But
what does it actually mean to "think in objects"? And why does it matter?

## The Fundamental Shift: Data + Behavior, Together

In procedural programming, data and code live apart. You have structs full of
fields, and functions that operate on those structs. They're defined in different
places, often in different files. The data is passive; the code is active.

OOP makes a different choice: **data and the code that operates on it belong
together in the same entity — the object.**

```python
# Procedural: data and behavior are separate
donut_state = {"A": 1.0, "B": 1.0}

def spin(state, dA, dB):
    state["A"] += dA
    state["B"] += dB

# OOP: data and behavior bundled together
class Donut:
    def __init__(self):
        self.A = 1.0
        self.B = 1.0

    def spin(self, dA, dB):
        self.A += dA
        self.B += dB
```

This isn't just syntax. It's a different way of modeling the world. Instead of
asking "what steps does the program take?", you ask "what **things** exist, and
what can they do?" The donut isn't a dictionary that gets passed to functions —
it's a `Donut` that *knows how to spin itself*.

## The Four Core Concepts

### Encapsulation — Hiding the "How"

Encapsulation means bundling data and methods together, then **hiding the
implementation details** behind a public interface. The outside world interacts
with an object only through its interface — never by directly touching its
internal data.

```python
class BankAccount:
    def __init__(self):
        self._balance = 0       # underscore = "please don't touch this directly"

    def deposit(self, amount):   # public interface
        if amount > 0:
            self._balance += amount

    def get_balance(self):       # public interface
        return self._balance
```

Why hide `_balance`? Because if any code anywhere can write `account._balance =
-1000000`, you can never guarantee that the account is in a valid state. By
forcing all changes through `deposit()`, you control exactly what can happen to
the balance. The object is the guardian of its own data.

The interface/implementation split is the object-level version of the
software/hardware split from Part 0. The interface is the "idea" (what the object
promises to do); the implementation is the "mirror" (how it actually does it).
Change the implementation and — if the interface stays the same — no other code
breaks.

> **One-breath aside.** Getters and setters (`get_balance()`, `set_name()`) are
> the minimum viable interface. They seem trivial, but they give you a single
> place to add validation, logging, or synchronization later without changing
> every caller. A public field locks you in; a getter/setter keeps your options
> open.

### Inheritance — "Is-a" Relationships

Inheritance lets a class inherit the attributes and methods of another class.
You factor out commonality into a **superclass** (parent), and **subclasses**
(children) add or override specific behavior.

```
          Shape (superclass)
          ├── Circle    (subclass)
          ├── Rectangle (subclass)
          └── Triangle  (subclass)
```

The relationship is **"is-a"**: a Circle *is a* Shape. If Shape defines
`getArea()`, every subclass inherits it — but each implements it differently:

```python
class Shape:
    def getArea(self):
        raise NotImplementedError  # subclasses must override this

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def getArea(self):
        return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width, self.height = width, height
    def getArea(self):
        return self.width * self.height
```

### Polymorphism — "Many Shapes"

Polymorphism (Greek: *many forms*) is what makes inheritance powerful. You can
write code that works with the superclass type, and it automatically works with
any subclass — each responding to the same message in its own way:

```python
shapes = [Circle(5), Rectangle(4, 6), Circle(2)]
for shape in shapes:
    print(shape.getArea())    # Same message, different behavior per type
```

This is **standardization through abstraction**: the loop doesn't know or care
what specific shape it's dealing with. It only knows that every Shape responds to
`getArea()`. This is exactly the pattern we used for the donut's three faces — the
backend sends "here's a grid" to each face, and each face draws it differently.
The backend doesn't know how each face works; it only knows they all respond to
"draw this."

### Composition — "Has-a" Relationships

Composition means building objects out of other objects. A Car *has an* Engine,
*has* Wheels, *has* a SteeringWheel. The relationship is **"has-a"**:

```python
class Engine:
    def start(self): ...

class Car:
    def __init__(self):
        self.engine = Engine()    # Car HAS an Engine
        self.wheels = [Wheel() for _ in range(4)]
```

Inheritance and composition are the *only two ways* to reuse code across classes.
Every design decision between them is a tradeoff.

## Inheritance vs. Composition — The Central Tension

This is where OOP gets interesting. Inheritance seems elegant: factor out
commonality, build clean hierarchies, reuse everything. But inheritance has a
dark side.

**Inheritance breaks encapsulation.** A subclass doesn't just use the
superclass's interface — it *inherits its implementation*. If you change how the
superclass works internally, every subclass might break, even if the public
interface didn't change. This is fragile.

Consider the classic problem: a `Bird` class with a `fly()` method. Then you need
a `Penguin`. A penguin *is a* bird, but it can't fly. If `Penguin` inherits from
`Bird`, it gets a `fly()` method it shouldn't have — violating the **Liskov
Substitution Principle**: every subclass must be substitutable for its parent.
Code that expects `bird.fly()` to work will crash on a penguin.

Composition avoids this. Instead of `Penguin extends Bird`, give `Penguin` the
behaviors it actually needs:

```python
# Inheritance (fragile):
class Bird:
    def fly(self): ...      # Penguin inherits this — bad!
class Penguin(Bird): ...    # Penguin.fly() exists but shouldn't

# Composition (flexible):
class SwimBehavior:
    def swim(self): ...
class Penguin:
    def __init__(self):
        self.swim_behavior = SwimBehavior()   # Penguin HAS swimming
```

**Guideline:** use inheritance for *true* is-a relationships where the subclass
is fully substitutable for the parent. Use composition for everything else. When
in doubt, **prefer composition over inheritance** — it's more flexible and less
fragile.

## SOLID — Five Principles for Sustainable OO Design

Robert Martin identified five principles that keep OO systems from becoming
rigid, fragile nightmares. They're known as SOLID:

| Principle | What it means | Why it matters |
|---|---|---|
| **S**ingle Responsibility | A class should have exactly one reason to change. | If a class does three things, changing one might break the other two. |
| **O**pen/Closed | Open for extension, closed for modification. | Add new behavior by adding code, not by rewriting existing code. |
| **L**iskov Substitution | Subclasses must be usable anywhere their parent is expected. | If `Penguin` can't `fly()`, don't make `Bird.fly()` part of the contract. |
| **I**nterface Segregation | Many small interfaces are better than one large one. | Don't force classes to implement methods they don't need. |
| **D**ependency Inversion | Depend on abstractions, not concrete implementations. | Code to an interface, not to a specific class. |

The last one — Dependency Inversion — deserves special attention because it's the
solution to the coupling problem.

## Decoupling — The Dependency Injection Pattern

Inheritance and composition-as-aggregation both create tight coupling. If `Car`
creates its own `Engine` inside its constructor (`self.engine = Engine()`), then
`Car` is permanently welded to that specific `Engine` class. You can't swap in a
different engine for testing, or use a more efficient one later.

**Dependency injection** solves this: instead of an object creating its own
dependencies, they're *passed in* from outside:

```python
# Tightly coupled: Car creates its own Engine
class Car:
    def __init__(self):
        self.engine = V8Engine()       # welded to V8Engine forever

# Loosely coupled: Engine is injected
class Car:
    def __init__(self, engine):        # engine is a parameter
        self.engine = engine            # works with ANY engine

# Usage
car = Car(V8Engine())       # real engine
test_car = Car(MockEngine()) # fake engine for testing — same Car!
```

Dependency injection is the most practical technique in OOP. It makes code
testable (inject mocks), swappable (inject different implementations), and
readable (dependencies are explicit in the constructor). It's also the pattern
behind our donut's desktop face: `DesktopFace` receives a `PlatformBackend` in
its constructor. The face never knows whether it's talking to Win32, Cocoa, or a
FakeBackend. It just knows the four verbs in the interface.

## Design Patterns — Named Solutions to Recurring Problems

After years of building OO systems, developers noticed that the same structural
problems kept appearing — and the same solutions kept working. The Gang of Four
(GoF) catalogued 23 of these as **design patterns** in 1994. Patterns fall into
three categories:

| Category | Purpose | Examples |
|---|---|---|
| **Creational** | How objects are created | Singleton, Factory, Builder |
| **Structural** | How objects are composed | Adapter, Bridge, Composite, Decorator |
| **Behavioral** | How objects communicate | Observer, Strategy, Command, Iterator |

A few patterns you'll encounter constantly:

- **Singleton:** ensure a class has exactly one instance. (Use sparingly — it's
  global state in disguise, and many consider it an antipattern.)
- **Factory:** instead of calling `new Circle()` directly, ask a factory to make
  the right shape for you. The caller doesn't know which concrete class it got.
- **Adapter:** wrap an incompatible interface to make it work with existing code.
  Like a power plug adapter for code.
- **Observer:** when one object changes state, all its dependents are notified
  automatically. This is the pattern behind event handling — including our donut's
  keyboard events.
- **Strategy:** encapsulate interchangeable algorithms. Our donut's RAMPS table
  is essentially a Strategy pattern: the ramp is the strategy for "how to paint a
  brightness value."

> **One-breath aside.** Antipatterns are patterns that *look* like good solutions
> but lead to pain. Singleton (global state), Service Locator (hidden
> dependencies), and "coding by exception" (using exceptions for normal control
> flow) are classic examples. Studying antipatterns is often more valuable than
> studying patterns — you learn what *not* to do.

## Frameworks — Designing with Interfaces and Abstract Classes

A **framework** is a reusable, semi-complete application that you customize by
plugging in your own code. It inverts the normal flow of control: instead of your
code calling library functions, the **framework calls your code**. This is
**Inversion of Control (IoC)** — the "Hollywood Principle": "Don't call us;
we'll call you."

A web framework like Django or Express is the classic example. You don't write a
`main()` function that calls the framework. You write handler functions, and the
framework calls *them* when requests arrive. Your code plugs into the framework's
slots.

Frameworks achieve this through interfaces and abstract classes: the framework
defines the shape of the slot, and you provide a concrete implementation that
fits. This is the same pattern as our `PlatformBackend` ABC — the face defines
four abstract methods, and each OS provides its own concrete implementation.

## The OOP Mindset

OOP is not about syntax. It's a discipline of thought:

1. **Separate interface from implementation.** What does this object promise?
   Hide everything else.
2. **Think from the user's perspective.** Design the interface for the code that
   will call it, not for your own convenience.
3. **Give the minimal interface possible.** Start with nothing public. Add methods
   only when callers genuinely need them. You can always add; you can't remove
   without breaking things.
4. **Design to abstractions, not concretions.** Code against `Engine`, not
   `V8Engine`. The donut face codes against `PlatformBackend`, not `Win32Backend`.
5. **A change to the implementation should never require a change to the caller.**

This is the same abstraction principle we traced through all six layers in Part 0.
OOP is just one way — a very successful way — of building the towers.

> *The donut's `PlatformBackend` is OOP's thesis in four lines: create a window,
> present a frame, poll for events, destroy the window. Four verbs. Three
> operating systems. Zero changes to the face. That is the whole game.*

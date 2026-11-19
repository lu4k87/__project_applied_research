# Speaker texts (English) – slides 1 and 2

As of 2026-11-18. Together about 3 min (around 500 words). English version of `sprechtext-de.md`, same structure.

Rules for these texts: project memory `sprechtexte-ohne-ansprache` (no we/you/one, factual without filler phrases, opening based on the slide title, every tool briefly explained at its first mention, ORM spelled out). Slide 3 (database) is presented by another person.


## Slide 1 – App Architecture: Tech Stack and the Path of a Request (about 1:30 min)

### Opening

Now on to the technical part: the **backend**, the part of the app that runs on the server and stays invisible to visitors.

The slide on **app architecture** shows two things: at the top the **tech stack**, below it the **path of a request**.


### Tech stack

- The app is written in **TypeScript**, a programming language that extends JavaScript with fixed data types.

- The framework is **Next.js**. It delivers web pages and server interfaces from one shared project.

- The server runs on **Node.js**, a runtime environment that executes JavaScript and TypeScript outside the browser.

- The remaining tools are grouped by their task: user interface, backend and security, data.


### Path of a request

There are two roles:

- The **guest** is not logged in.

- The **member** is logged in and sends a session cookie with every request, a small identifier that lets the server recognise the user as a member.

Every request passes through **five stations** on the server:

1. **Next.js** receives it.

2. **Better Auth**, a library for login and user accounts, determines whether a guest or a member is asking.

3. **Zod**, a library for validating data, checks whether the input matches the expected format.

4. The **Data Access Layer**, a dedicated code layer of the app, defines which data this role may see.

5. Finally, the **Object-Relational Mapping**, ORM for short, translates the program code into an SQL query, the language of the database.

The browser has no direct access to the database.


### Result per role

What comes back depends on the role:

- The **guest** sees the title, material, quantity and city of an offer and can register.

- The **member** also sees price and contact, can request matches and can post their own offers.


## Slide 2 – Software Architecture Stack: What Each Building Block Does (about 1:30 min)

### Opening

This slide shows **what each building block** of the software architecture stack does in the app and why it was chosen.


### Foundation of every request

- **TypeScript** ensures, for example, that an offer always has a title as text and a quantity as a number. The benefit: frontend, backend and data access share one language.

- **Next.js** turns every file in the app folder into an address. `/offers` shows the list, `/offers/[id]` a single offer. The result is one project instead of two: pages and API share code, types and one deployment.

- **Node.js** handles many requests at the same time without blocking. It is the standard runtime for Next.js and uses the same language as the browser.


### The four building blocks from the frontend

Below are the four building blocks that every request from the frontend passes through:

- **Better Auth**: Without a cookie the request counts as a guest, with a cookie as a member. Chosen because it is open source and the user accounts stay in the app's own database.

- **Zod**: A quantity in kilograms must be a positive number, otherwise the input is rejected. A single schema provides both the validation and the TypeScript type.

- **Data Access Layer**: Only members see price and contact, and only the owning site can change an offer. These access rules live in one place instead of being scattered across the code.

- **Object-Relational Mapping** with Prisma or Drizzle: It loads, for example, all offers of one material. Chosen because it is type-safe and inserts values safely. This prevents SQL injection.


### Handover

That covers the backend. What is inside the database is shown next by **[Name]**.

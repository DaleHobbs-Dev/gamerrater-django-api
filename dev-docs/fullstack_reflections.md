<!-- markdownlint-disable MD028 -->
# Full Stack Reflections

These questions are meant to help you reflect on the concepts and skills that we have covered in this module. You should be able to answer these questions without looking at any notes or code. If you find that you are struggling to answer any of these questions, that is a sign that you need to review the material more thoroughly.

## Django

1. What are the benefits of using Django to build a Web API project?
    > Django comes with a lot of built-in functionality that speeds up API development. Its ORM lets you interact with the database using Python instead of raw SQL, and automatically handles things like migrations when your models change. Django REST Framework (DRF) builds on top of Django and adds API-specific tools like serializers (which control how your data gets converted to JSON), authentication, and permissions. Django also has a built-in admin interface that gives you a UI to manage your data without writing any extra code, which is useful during development. Together these tools mean you can focus on your application logic rather than building common infrastructure from scratch.
2. How can you add additional, or calculated, fields to a JSON response that don't come directly from the database?
    > One of the easiest ways to do this is to define a property method on the model that calculates the value you want to include in the JSON response. Then, you can add that property to your serializer to include it in the JSON output. For example:

    ```python
    class MyModel(models.Model):
        # ... fields ...

        @property
        def calculated_field(self):
            # Calculate the value for the additional field
            return self.some_value * 2  # Example calculation

    class MyModelSerializer(serializers.ModelSerializer):
        calculated_field = serializers.ReadOnlyField()
        class Meta:
            model = MyModel
            fields = ['id', 'some_value', 'calculated_field']  # Include the calculated field in the serializer
    ```

    > In the case that your calculation cannot live on the model (e.g., it depends on external data, request context, or complex logic), then you can use the `SerializerMethodField` to define a method on the serializer that performs the calculation and returns the value to be included in the JSON response. For example:

    ```python
    class MyModelSerializer(serializers.ModelSerializer):
        calculated_field = serializers.SerializerMethodField()
        class Meta:
            model = MyModel
            fields = ['id', 'some_value', 'calculated_field']  # Include the calculated field in the serializer
        def get_calculated_field(self, obj):
            # Perform the calculation using the object instance (obj) and return the value
            return obj.some_value * 2  # Example calculation
    ```

3. What is the purpose of a serializer in Django?
    > Serializers in Django REST Framework serve two main purposes. First, they handle **serialization** — converting your Django model instances into JSON so that data can be sent to the client in a format the frontend can work with. Second, they handle **deserialization** — taking incoming JSON data from a request (like a POST or PUT), validating it, and converting it back into a Python object that can be saved to the database. The validation step is important: the serializer checks that required fields are present, that values are the right type, and rejects bad data before it ever touches the database. In that sense a serializer acts as a gatekeeper in both directions — controlling what goes out in responses and what comes in from requests.
    > For example: in a project I was working on recently, I had a `GameSerializer` that controlled exactly what fields of the `Game` model were included in the JSON response, and also added some additional fields that were calculated based on the request context (like whether the current user was the owner of the game, or what their personal rating of the game was). It also validated game data upon creation by using the serializer's validation methods like `validate_<field_name>`. Here is a snippet of that serializer:

    ```python
    from rest_framework import serializers

    class GameSerializer(serializers.ModelSerializer):
    """Serializer for the Game model."""

    categories = CategorySerializer(many=True, read_only=True)

    is_owner = serializers.SerializerMethodField()

    # my_rating uses SerializerMethodField instead of a model @property because it depends
    # on request.user -- the model has no access to who is making the request
    my_rating = serializers.SerializerMethodField()

    # average_rating is a read-only field that calculates the average rating for the game
    # this helps serializer know it is computed and should not be provided by the client when creating or updating a game
    average_rating = serializers.FloatField(read_only=True)

    # returns True if the current request user is the owner of the game
    def get_is_owner(self, obj):
        return self.context["request"].user == obj.user

    def get_my_rating(self, obj):
        user = self.context["request"].user
        try:
            rating = obj.ratings.get(player=user)
            return rating.rating
        except obj.ratings.model.DoesNotExist:
            return None

    class Meta:
        model = Game
        fields = [
            "id",
            "is_owner",
            "title",
            "description",
            "designer",
            "year_released",
            "num_players",
            "time_to_play",
            "age_recommendation",
            "categories",
            "game_image",
            "bgg_id",
            "my_rating",
            "average_rating",
        ]
    ```

4. Can you explain the difference between a view and a viewset in Django?
    > A **view** in Django is a function or class that handles a single HTTP request and returns a response. Each view is mapped to a specific URL and is responsible for one thing — for example, a view might handle a GET request to return a list of games, and a separate view might handle a POST request to create a new game.

    > A **viewset** groups related views together into a single class. Instead of writing separate views for listing, creating, retrieving, updating, and deleting a resource, a viewset provides all of those behaviors in one place. For example, a `GameViewSet` could handle GET (list), POST (create), GET (retrieve by id), PUT/PATCH (update), and DELETE all in one class. Viewsets are used together with DRF's **router**, which automatically generates all the URL patterns you'd otherwise have to wire up manually.

    > The tradeoff is that views give you more explicit control and are easier to understand when you're learning, while viewsets reduce repetition and boilerplate once you know what's happening under the hood.

## JavaScript and React

1. Can you explain what a component is in React?
    > A component in React is a reusable piece of UI that can be composed together to build complex user interfaces. Components can be defined as functions or classes, and they return JSX (a syntax extension that looks like HTML) which describes what the UI should look like. Components can accept inputs called "props" and manage their own internal state using hooks like `useState()`. By breaking the UI into smaller components, you can create modular, maintainable code. Components are also composable — you build a React app by nesting components inside each other, forming a tree structure with a root component (like App) at the top and smaller, more specific components deeper down.
2. What is the declaratively way you can iterate an array in JavaScript to locate a single item in it?
    > You can use the `find()` method to iterate over an array and locate a single item that matches a specific condition. The declarative approach means you describe what you want (the item matching a condition) rather than how to find it (manually looping with an index). `find()` is declarative because you just express the condition and JavaScript handles the iteration for you — contrast this with a `for` loop where you'd manage the loop counter and the early exit yourself. The `find()` method takes a callback function as an argument, which is executed for each element in the array until it finds one that returns `true`. For example:

    ```javascript
    const myArray = [1, 2, 3, 4, 5];
    const itemToFind = 3;

    const foundItem = myArray.find(item => item === itemToFind);

    console.log(foundItem); // Output: 3
    ```

    > In this example, `find()` iterates through `myArray` and returns the first element that is equal to `itemToFind`, which is `3`.
3. What is the purpose of the `useEffect()` hook in React? Can you explain the arguments that you need to pass to that function?
    > The `useEffect()` hook in React is used to perform side effects in functional components. Side effects can include things like fetching/mounting data from an API, subscribing to events, or manually manipulating the DOM. The `useEffect()` hook takes two arguments: a function that contains the side effect code, and an optional dependency array.

    > The first argument is a function that will be executed after the component renders. This function can return another function (called a cleanup function) that will be executed when the component unmounts or before the effect runs again if the dependencies change. A common real-world case for the cleanup function is clearing a timer or unsubscribing from an event listener — without cleanup, those would keep running even after the component is gone from the page, causing memory leaks. In the example below I show a cleanup function that prevents state updates if the component unmounts before an asynchronous operation (like a fetch) completes.

    > The second argument is an array of dependencies that determine when the effect should re-run. If you pass an empty array `[]`, the effect will only run once after the initial render. If you include variables in the array, the effect will re-run whenever any of those variables change. If you omit the second argument entirely, the effect will run after every render, which can lead to performance issues if not used carefully.

    > For example:

    ```javascript
    useEffect(() => {
        // This effect runs once when the component mounts AND whenever the 'id' variable changes
        let mounted = true
        getGameById(id)
            .then(data => {
                if (!mounted) return
                setGame(data)
                setLoading(false)
            })
            .catch(err => {
                if (!mounted) return
                setError(err.message)
                setLoading(false)
            })
        // Cleanup function to prevent state updates if the component unmounts before the async operation completes
        return () => { mounted = false }
    }, [id]) // This effect runs whenever the 'id' variable changes, allowing us to fetch new data when the id changes.
    ```

4. Could you explain the benefit of providing an initial value for state in a React component?
    > Providing an initial value for state in a React component is important because it defines the starting point for that piece of state when the component is first rendered. This ensures that your component has a predictable and consistent behavior from the moment it renders. The initial value also tells React (and you) what type that state will be, which matters because your render logic will run before any data arrives. If you initialize something as null but then try to call .map() on it, you'll get an error. If you don't provide an initial value, the state will be `undefined`, which can lead to errors if your component tries to access or manipulate that state before it has been set. For example, if you have a piece of state that is supposed to hold an array of items, initializing it as an empty array (`useState([])`) allows you to safely use array methods like `map()` or `filter()` without running into issues. Additionally, having an initial value can improve the user experience by providing default content or a loading state while data is being fetched or processed.
    > Some great examples of initial state values from my projects this round include:
    > - Initializing a `loading` state to `true` so that the UI can show a loading spinner while data is being fetched from an API.
    > - Initializing an `error` state to `null` so that the UI can conditionally render an error message if something goes wrong during data fetching or processing.
    > - Initializing a `backendErrors` state to an empty array `[]` in a register component, which allows the UI to display any validation errors returned from the server after a form submission (useful for checking password invalid strength or other validation issues).
    > - Initializing each form field (title, description, designer, etc.) to an empty string "" in GameForm, so that all inputs are controlled from the first render and the form fields are never uncontrolled.
    > - Initializing a `confirmingDelete` state to `false` in a delete confirmation component, which allows the UI to conditionally render a confirmation dialog when the user attempts to delete an item.
    > - Initializing selectedCategories to an empty array [] in GameForm, so that category checkboxes can safely use .includes() to check their checked state before any categories are selected.
    > - Initializing a `user` state to `null` in an authentication component, which allows the UI to conditionally render different content based on whether the user is logged in or not.
5. Can you explain what JSX is and how it is used in React?
    > JSX stands for JavaScript XML and is a syntax extension for JavaScript that lets you write HTML-like markup directly inside your JavaScript files. React uses JSX to describe what the UI should look like in a readable, declarative way — rather than calling `React.createElement()` manually for every element, you can write structure that looks similar to HTML and JSX gets transpiled into those function calls behind the scenes. This makes it easier to visualize the component's structure and how it will render. JSX also allows you to embed JavaScript expressions inside curly braces `{}`, which is how you can dynamically render content based on state or props. For example, you can write `<p>{game.title}</p>` to display the title of a game, or `{isLoading && <Spinner />}` to conditionally render a loading spinner when data is being fetched.
    > A few things to know about how JSX differs from regular HTML:
    > - Attributes are camelCased — you write `className` instead of `class` and `onClick` instead of `onclick`, because `class` and `onclick` are reserved words in JavaScript
    > - Every JSX expression must return a single root element — if you need to return multiple elements without adding an extra wrapper `<div>`, you can use a fragment: `<>...</>`
    > - You can embed any JavaScript expression inside JSX using curly braces `{}`, which is how you dynamically render content based on state or props — for example `<p>{game.title}</p>` or `{isLoading && <Spinner />}`
6. How would you explain props to someone who is not familiar with React?
    > Props, short for "properties," are how you pass data from a parent component to a child component in React. Think of them like arguments you pass to a function — when you define a component, you can set it up to accept props, and when you use that component in JSX, you provide values for those props as attributes.

    > For example, if you have a `Greeting` component that takes a `name` prop, you'd use it like `<Greeting name="Alice" />`, and inside `Greeting` you could render `Hello, Alice!`. Props are **read-only** — a child component can read the props it receives but cannot modify them. Data flows one direction in React: from parent down to child.

    > Props aren't limited to just data like strings or numbers — you can also pass **functions** as props. This is how a child component can communicate back up to a parent. For example, a form component might receive an `onSubmit` function as a prop, and when the form is submitted the child calls that function, letting the parent decide what to actually happens with the data.

    > A great real-world example of this is my reusable `ExamForm` component. Rather than building separate forms for creating and editing an exam, I built one `ExamForm` that accepts props to handle both cases:

    ```jsx
    <ExamForm
        initialData={family}
        variants={variants}
        onSubmit={handleSubmit}
        onCancel={handleCancel}
    />
    ```

    > Here `initialData` and `variants` are data props that pre-populate the form when editing, and `onSubmit` and `onCancel` are function props that let the parent (`EditExam`) define what happens when the form is submitted or cancelled. The `ExamForm` component itself doesn't need to know whether it's being used for creating or editing — it just uses whatever props it receives, making it reusable across different contexts.
7. What is strict equality in JavaScript?
    > Strict equality in JavaScript is a comparison operator represented by `===`. It checks if two values are equal in both value and type, meaning both operands must be the same type AND have the same value to return `true`. For example, `5 === 5` returns `true`, while `5 === '5'` returns `false` because one is a number and the other is a string.

    > JavaScript also has a loose equality operator `==`, which attempts to coerce the two values to the same type before comparing them. This can lead to surprising results — for example, `5 == '5'` returns `true`, and `0 == false` also returns `true`. Because of this unpredictable behavior, `==` is almost never used in modern JavaScript. You will rarely if ever see it in professional codebases, and `===` is considered the standard.

    > One important behavior to understand is how strict equality works with **objects and arrays**. Even if two objects look identical, `===` will return `false` if they are not the same object in memory:

    ```javascript
    const a = { name: "Alice" }
    const b = { name: "Alice" }
    console.log(a === b) // false
    ```

    > This is because objects and arrays in JavaScript are **reference types**. When you create an object, JavaScript stores it somewhere in memory and the variable holds a *reference* (essentially a pointer) to that location. Even though `a` and `b` look the same, they are two separate objects sitting in two different places in memory, so their references are not equal. Strict equality for reference types checks whether the two variables point to the *same object in memory*, not whether they have the same contents.

    > By contrast, primitive types like strings, numbers, and booleans are **value types** — they are compared directly by their value, which is why `5 === 5` works as you'd expect.
8. What is the difference between state and props in React?
    > The main difference between state and props in React is that **state** is managed within a component and can change over time, while **props** are passed to a component from its parent and are read-only.

    > **State** is internal to a component — it stores data that the component itself owns and can update, usually in response to user interactions or async events like API calls. When state changes, React automatically re-renders the component to reflect the new data. For example, in my `GameDetail` component, `loading`, `game`, `reviews`, and `pictures` are all pieces of state — they start at their initial values and get updated as data is fetched or the user interacts with the page.

    > **Props** are external — they are passed down from a parent component and are read-only from the child's perspective. A child component cannot modify its own props; it can only read and use them. Props can be anything: strings, numbers, arrays, objects, or even functions. When the parent's data changes and it passes new props down, the child re-renders to reflect those new values too.

    > A good way to remember the distinction: if a component owns the data and needs to change it, that's state. If a component is just receiving data or behavior from somewhere else, that's props. In practice you'll often see both together — a parent component manages state and passes pieces of that state down to children as props.

## Full Stack Development Lifecycle

1. What is a Web API?
    > A Web API (Application Programming Interface) is a set of rules and endpoints that a server exposes so that other programs — like a React frontend — can communicate with it over HTTP. It defines what requests the server will accept, what data you need to send, and what it will send back. Rather than serving full HTML pages, a Web API typically responds with raw data (usually JSON) that the client is responsible for rendering.

    > Web APIs communicate through HTTP methods that map to the four basic data operations, often referred to as **CRUD** (Create, Read, Update, Delete):
    > - **GET** — Read/retrieve data (e.g. fetching a list of games or a single game by ID)
    > - **POST** — Create new data (e.g. submitting a new game to the database)
    > - **PUT / PATCH** — Update existing data. `PUT` typically replaces the entire resource while `PATCH` updates only the fields you provide
    > - **DELETE** — Remove data (e.g. deleting a game from the database)

    > A common beginner misconception is that "API" and "REST API" are the same thing — REST (Representational State Transfer) is just one architectural style for designing a Web API. Another misconception is that an API is something you download or install. It isn't — it's just a set of URLs (called endpoints) that your code calls over the network. When your React app calls `fetch("http://localhost:8000/games")`, it is consuming a Web API. The server on the other end sees an HTTP request and responds accordingly, completely unaware of whether a human or a program sent it.

    > **Note — other API architectural styles:** REST is the most common style you'll encounter, especially early in your development career, but there are others worth knowing exist:
    > - **GraphQL** — Developed by Meta, GraphQL lets the client specify exactly what data it wants in a single request, rather than hitting multiple endpoints. This solves a common REST problem called over-fetching (getting back more data than you need) or under-fetching (needing multiple requests to get all the data you need).
    > - **gRPC** — A high-performance style developed by Google, commonly used for communication between backend services rather than between a frontend and backend. It uses a binary format rather than JSON, making it faster but less human-readable.
    > - **WebSockets** — Less of an architectural style and more of a different protocol altogether, WebSockets allow a persistent two-way connection between client and server, which is useful for real-time features like chat applications or live notifications (like Twitter for instance where the live feed updates in real-time) where the server needs to push data to the client without waiting for a request.

2. Reflect on the importance of status codes in HTTP responses and what they signify.
    > HTTP status codes are three-digit numbers that the server includes in every response to tell the client what happened with its request. They are grouped by the first digit: **2xx** means success, **3xx** means a redirect, **4xx** means the client made an error, and **5xx** means the server failed. They are not just informational — your code needs to check them to know how to handle the response.

    > The codes beginners encounter most often:
    > - **200 OK** — the request succeeded and the response body contains the requested data
    > - **201 Created** — a resource was successfully created (the right response to a successful POST, not 200)
    > - **204 No Content** — the request succeeded but there is nothing to return (used for DELETE)
    > - **400 Bad Request** — the client sent something invalid (missing fields, wrong type, failed validation)
    > - **401 Unauthorized** — the client is not authenticated (no valid token was provided)
    > - **403 Forbidden** — the client is authenticated but does not have permission to do this action
    > - **404 Not Found** — the requested resource does not exist
    > - **500 Internal Server Error** — something went wrong on the server itself

    > The distinction between 401 and 403 trips up a lot of beginners. **401** means "I don't know who you are — please log in." **403** means "I know who you are, but you're not allowed to do this." In practice this matters: a 401 should prompt your app to redirect to a login page, while a 403 means the user is logged in but attempting something outside their permissions.

    > Another common mistake is treating every non-200 response as an error to ignore. Status codes carry meaning that your frontend should act on — for example, displaying a "Not Found" page on 404, or showing a validation error message on 400.

    > Choosing the correct status code matters, but pairing it with a meaningful error message body makes responses genuinely useful to the client. A 400 response that just says "bad request" forces the frontend to guess what went wrong — but a 400 that includes specific validation messages lets the UI surface exactly what the user needs to fix.

    > A good example of this is the registration flow in my GamerRater project. The Django backend uses a custom `StrongPasswordValidator` that raises specific validation errors for each password requirement that isn't met (missing uppercase, missing symbol, etc.).

    ```python
    import re
    from django.core.exceptions import ValidationError
    from django.utils.translation import gettext as _

    class StrongPasswordValidator:
        """Require at least one uppercase letter, lowercase letter, digit, and symbol."""

        def validate(self, password, user=None):
            errors = []

            if not re.search(r"[A-Z]", password):
                errors.append(_("Password must contain at least one uppercase letter."))
            if not re.search(r"[a-z]", password):
                errors.append(_("Password must contain at least one lowercase letter."))
            if not re.search(r"\d", password):
                errors.append(_("Password must contain at least one number."))
            if not re.search(r"[!@#$%^&*()\-_=+\[\]{}|;:'\",.<>?/`~\\]", password):
                errors.append(_("Password must contain at least one symbol."))

            if errors:
                raise ValidationError(errors)

        def get_help_text(self):
            return _(
                "Your password must contain at least one uppercase letter, "
                "one lowercase letter, one number, and one symbol."
            )
    ```

    > The `UserSerializer` catches those and returns them as a list in the response body, still with a `400` status code. On the frontend, `Register.jsx` checks for the presence of a `password` key in the response and if it finds one, renders each message from that list individually beneath the password field — rather than showing a generic "something went wrong" alert. The result is that the status code tells the frontend *that* something failed, and the message body tells it *what* failed and *where* to show it. Neither piece is useful without the other.

3. Can you correctly explain the difference between a **client** and a **server**?
    > The **client** is any program that sends a request. The **server** is a program that listens for requests and sends back a response. The relationship is defined by behavior, not by hardware — the server is not a specific physical machine, it's just a process running somewhere that is ready to respond to HTTP requests. It could be running on a cloud host or on your own laptop during development.

    > In the context of a full-stack web app: the React frontend is the client. It runs in the browser on the user's machine and makes HTTP requests to the Django backend. The Django backend is the server — it receives those requests, applies business logic, talks to the database, and sends back a response.

    > A few important things beginners often get wrong:
    > - The client is not just "the browser." Any program that sends an HTTP request is a client — that includes your `fetch()` calls in JavaScript, tools like Postman/Yaak, and command-line tools like `curl`.
    > - The server is not the database. The server is the layer between the client and the database. The server owns the logic for what the client is allowed to read or write, and the database just stores data.
    > - The terms are relative. In a microservices architecture, one server might act as a client to another server — "client" and "server" describe roles in a given request, not permanent identities.

4. Can you describe what happens from the moment a user clicks a link in a React application to when the new state is rendered?
    > Here is the full sequence of events when a user clicks a link in a React app built with React Router:

    > 1. **The user clicks a link** — for example, a `<Link to="/games/3">` in React Router.
    > 2. **React Router intercepts the click** — it prevents the browser's default behavior (which would be a full page reload) and instead updates the URL in the address bar using the browser's History API. No request is sent to the server at this point — the page does not reload. This is different from how click events worked when learning vanilla JavaScript, where you had to manually target DOM elements with `addEventListener('click', ...)` or `onclick` attributes and write imperative code to handle what happened. In React, the framework handles the event system for you — you just declare `<Link to="/games/3">` and React Router manages the rest.
    > 3. **The matching route renders** — React Router compares the new URL against your route definitions and renders the matching component, for example `<GameDetail />`.
    > 4. **The component renders with its initial state** — `GameDetail` renders for the first time using whatever initial state was set (`null`, `[]`, `false`, etc.). This is why initial state matters — React renders the component before any data has been fetched.
    > 5. **`useEffect` fires** — after the initial render, any `useEffect` hooks run. A typical effect calls a function like `getGameById(id)` that uses `fetch()` to make an HTTP GET request to the Django API. I'll use this `useEffect` from my `GameDetail` component as an example to describe going forward:

        ```javascript
        useEffect(() => {
            let mounted = true
            getGameById(id)
                .then(data => {
                    if (!mounted) return
                    setGame(data)
                    setLoading(false)
                })
                .catch(err => {
                    if (!mounted) return
                    setError(err.message)
                    setLoading(false)
                })
            return () => { mounted = false }
        }, [id])
        ```

    > 6. **The HTTP request travels to the server** — the request goes over the network to the Django backend. The server authenticates the request, looks up the resource in the database, serializes it to JSON, and sends back a response with a status code (e.g., 200 OK) and a JSON body.
    > 7. **The Promise resolves** — back in the browser, the `.then()` handler receives the JSON data and calls `setGame(data)` to update state with the real game data.
    > 8. **Cleanup function runs if the component unmounted** — if the user navigated away before the fetch completed, the cleanup function returned by `useEffect` would have already set `mounted = false`, preventing `setGame` from being called on an unmounted component and avoiding memory leaks or errors.
    > 9. **React re-renders the component** — because state changed, React re-renders `GameDetail` with the actual game data, replacing any loading spinner or empty state with the real content. This does not trigger the `useEffect` again because `setGame` is not in the dependency array — only `id` is. The dependency array is what controls when an effect re-runs: since `id` hasn't changed, the effect stays idle. If the user navigated to a different game (a new `id`), the effect *would* re-run and fetch the new game's data.

5. Can you explain the difference between the URL that is used in the browser and the URL that is used to get data from an API?
    > These are two completely separate systems that happen to both look like URLs, which is a major source of confusion for beginners.

    > The **browser URL** is what you see in the address bar, like `http://localhost:3000/games/3`. This is a **client-side route** managed by React Router. When you navigate to that URL, React Router looks at the path (`/games/3`) and decides which component to render. Nothing about this URL involves the server — it is entirely handled in the browser.

    > The **API URL** is what your JavaScript code passes to `fetch()`, like `http://localhost:8000/api/games/3`. This is a **server-side endpoint** defined in your Django backend. When `fetch()` makes a request to this URL, it travels over the network to Django, which processes it and returns JSON data.

    > The same ID (`3`) can appear in both URLs, but they serve completely different purposes. `/games/3` in the browser tells React "render the GameDetail component for game 3." `http://localhost:8000/api/games/3` tells Django "give me the data for game 3." Your `useEffect` extracts the `id` from the browser URL (via `useParams`) and uses it to construct the API URL for the fetch call — that is how the two URLs work together.

    > A common mistake is typing an API URL directly into the browser and expecting to see a rendered page. What you'll see is raw JSON, because that endpoint is designed to return data, not HTML. The rendered page only exists because React is running in the browser and using that data to build the UI.

6. Why would it be bad if the client connected directly to the database?
    > Allowing the browser to connect directly to the database would create serious security, architectural, and reliability problems. The server exists specifically to sit between the two.

    > **Security:** Database credentials (username, password, host) would have to be sent to or stored in the client. Anyone could open their browser's developer tools, find those credentials, and connect to the database themselves with full access. There would be no way to restrict what data a user can read or modify — they'd have access to every row in every table.

    > **No business logic or authorization:** The server is where you enforce rules. Logic like "a user can only delete their own games," "a password must be hashed before storage," or "a review can only be submitted once per user per game" all lives in the server. If the client talks directly to the database, none of those rules apply — anyone could insert, update, or delete any data they wanted.

    > **Exposing your entire schema:** A direct database connection would let any client discover the full structure of your database — every table, every column, every relationship. The server acts as a contract: it exposes only what you explicitly define in your API endpoints. Everything else is hidden.

    > **Performance and connection limits:** Databases are designed to handle a relatively small number of concurrent connections. A server can manage a pool of connections efficiently and serve thousands of browser clients from that pool. If every browser tab opened its own direct database connection, you'd hit connection limits almost immediately under any real traffic.

7. Why is the JSON data format useful in client/server communication?
    > JSON (JavaScript Object Notation) is a lightweight, text-based format for representing structured data. It is the standard format for client/server communication in modern web APIs because it is readable by humans, easy to parse programmatically, and supported natively by JavaScript and by nearly every other language through libraries.

    > JSON represents data as key/value pairs (objects) and ordered lists (arrays), which maps directly onto the data structures most applications already use. A Django model instance gets serialized into a JSON object, and when the React frontend receives it, `JSON.parse()` converts that string back into a JavaScript object you can work with immediately.

    > A few things beginners commonly misunderstand about JSON:
    > - **JSON is a string, not a JavaScript object.** When your server sends a response and your `fetch()` call calls `.json()` on it, that step is converting the raw string into an actual JavaScript object. Before that call, it is just text.
    > - **Not all JavaScript values are valid JSON.** `undefined`, functions, and `Date` objects do not exist in JSON. If you try to serialize them, they will be silently dropped or cause an error. Dates in JSON are typically represented as ISO 8601 strings like `"2024-01-15T10:30:00Z"`.
    > - **JSON is language-agnostic.** Despite the "JavaScript" in the name, JSON is just a text format. Your Django backend sends it, your React frontend parses it, and the two never need to know anything about each other's language or runtime. This is exactly what makes it useful as a communication format between different systems.

## Codex Question and Practice Interview Session

Q: In React, what is useEffect for, and how does the dependency array change when the effect runs?
A: `useEffect` lets a React component perform side effects after rendering, such as fetching data from an API, setting up subscriptions, timers, or event listeners. The first argument is the effect function. It can optionally return a cleanup function, which runs when the component unmounts or before the effect runs again. The second argument is the dependency array. If it is empty, the effect runs after the first render. If it contains values, the effect runs after the first render and again whenever one of those values changes. If there is no dependency array, the effect runs after every render.
> Note: A cleanup function can prevent stale state updates or unsubscribe/clear things, but a basic fetch will keep going unless you actively abort it.


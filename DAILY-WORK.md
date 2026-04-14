# FastAPI Learning Journal

### PLaylist like - https://www.youtube.com/playlist?list=PL-osiE80TeTsak-c-QsVeg0YYG_0TeyXI
## 📅 Day 1 - 2026-04-10

### Topics Covered
- **Setting up Git Repo and Syncing it to local folder**
  - Create a markdown file for documenting task and what learned 
  - Created a git repo first
  - Initialised git in local folder which created a master branch by default
  - Deleted master branch and configured main as *Upstream Tracking* for pull and push to work 

- **UV as package manager**
  - Installed UV as replacement for pip
  - Initalised uv in local folder using 'uv init' without this packages cant be install as it uses a 'pyproject.toml' file
  - Install packages using 'uv add <package_name>'
  - To run using uv we need 'uv run <command>' like 'uv run fastapi dev main.py'

- **Install FastAPI using uv**
  - run command 'uv add "fastapi[standard]"'
  - Include FastAPI framework , Uvicorn which is a ASGI server , FastAPI CLI command
  - FastAPI gives 2 mode dev for development server and run for production server
  - DEV mode - has auto reload which is helpful while developing , more helpful in debuging
  - /docs - route to SWAGGER UI and has automatic documentation based on our code
  - /redoc - routes to another SWAGGER UI that also provide documentation based on our code just in a different way
  - Using Jinja Templating we can render HTML content and can pass variable values that can be used in HTML file

## 📅 Day 2 - 2026-04-13
### Topics Covered
- **Path parameters**
  - in decorator we can define variable in url that can be accessed in python 
  - HTTPException is used to return HTTP error responses
  - status - gives constants for error. Make code for readable
  - we might work with return JSON response , make sure to include status_code parameter else it will show success


## 📅 Day 3 - 2026-04-14
### Topics Covered
- **Request and reponse validation using pydantic**
  - in decorator we can define variable in url that can be accessed in python 
  - Depends - is for dependecies injection , its hoe we inject database session into the routes
---

---

### 💡 Key Concepts Learned
- **Query and Path Parameters**
  - Path parameters and query parameters are both ways of passing data in a URL, but they serve different purposes and appear in different places. Path parameters are part of the URL path itself and are used to identify a specific resource, such as /api/posts/5, where 5 uniquely identifies a particular post; in FastAPI, these are defined directly in the route (e.g., "/api/posts/{post_id}") and are typically required. Query parameters, on the other hand, are appended to the URL after a question mark, like /api/posts?author=Chinmaya&limit=10, and are used to filter, sort, or modify the request rather than identify a specific resource. They are usually optional and are defined as regular function arguments in FastAPI. In essence, path parameters specify which resource you want, while query parameters control how the results should be returned.

- **Data Validation using Pydantic**
  - Why is it necessary , it used by passing a class to response_model attribute. 
  - For GET requests it helps in maintaining a solid structure of what we want to show. It gives an error if the required field as missing and will not show unnecessary fields but only the field the we define in response class
  - For POST requests in agains helps in data validation as client needs to provide data as defined in contrainst if not the then it throws an error 
  - When you send a POST request to /api/posts, FastAPI (built on Starlette) first matches the request to your route using the @app.post decorator, which had already registered this path and its associated function at startup. It then reads the incoming JSON body and, based on your function signature post: PostCreate, uses Pydantic to convert and validate that data into a PostCreate object—ensuring all required fields exist and meet constraints before your function is even called. If validation passes, FastAPI calls your create_post function with this validated object, where you create and return a dictionary for the new post. After your function returns, FastAPI again uses Pydantic—this time with response_model=PostResponse—to validate, filter, and shape the output so only the defined fields are sent back to the client in the correct format. Essentially, the decorator doesn’t just map the route; it wraps your function in a pipeline that enforces input validation before execution and output validation after execution, ensuring your API remains consistent, safe, and well-structured.
  - An HTTP request is a structured message sent by a client (such as a browser, script, or API tool) to a server to perform an action. At its core, it begins with a request line, which contains the HTTP method (like GET, POST, PUT, DELETE), the path (such as /api/posts), and the HTTP version (usually HTTP/1.1). The method defines the intent of the request—for example, GET is used to retrieve data while POST is used to create new data—and the path determines which endpoint on the server should handle the request. In a FastAPI application, this directly maps to route decorators like @app.post("/api/posts"), which register the method and path combination and associate it with a specific function.

  - Following the request line are headers, which are key-value pairs that provide metadata about the request. Headers tell the server how to interpret the request and how to respond. One of the most important headers is Content-Type, which specifies the format of the request body, such as application/json for JSON data, application/x-www-form-urlencoded for form submissions, or multipart/form-data for file uploads. Another common header is Accept, which tells the server what kind of response format the client expects, typically JSON in modern APIs. Headers like Authorization are used for authentication, while others such as User-Agent identify the client making the request. These headers are optional but often critical in real-world APIs.

  - An HTTP request can also include query parameters, which are appended to the URL and provide additional filtering or configuration for the request. These appear after a question mark in the URL, such as /api/posts?author=Chinmaya&limit=10, and are commonly used with GET requests but can be used with others as well. In FastAPI, query parameters are automatically mapped to function arguments based on their names and types, making them easy to work with.

  - Finally, the request may contain a body, which is where the main data is sent, especially in POST, PUT, or PATCH requests. The body can take several formats, with JSON being the most common in modern APIs. In your FastAPI example, the JSON body is parsed and validated against a Pydantic model (PostCreate), ensuring that all required fields are present and meet defined constraints before your function is executed. Other body formats include form data, multipart data for file uploads, and even raw text or XML, depending on the use case. Together, these components—request line, headers, query parameters, and body—form the complete structure of an HTTP request, and frameworks like FastAPI map each of these parts cleanly into your application logic using decorators, type hints, and data models.
---

### ❓ Doubts / Questions
- (Things you didn’t understand or want to revisit)


# RestAPI_Assessment
# API Interaction Guide


## Base URL

All API requests should be made to the base URL: `http://18.218.144.147:8000`. Ensure you use the correct endpoint for each operation as described below.

## User Registration

To create a new user account, send a POST request with your desired username and password.

### Endpoint

`/accounts/register`

### Method

POST

### Parameters

- `username`: Desired username.
- `password`: Chosen password.
- `password2`: Confirmation of the chosen password.

## Login

Log in to receive a session token for authenticated operations.

### Endpoint

`/accounts/login`

### Method

POST

### Parameters

- `username`: Desired username.
- `password`: Chosen password.


## Adding items into the database

Authenticated users can add items to the database

### Endpoint

`/items/api`

### Method

POST

### Body
Provide item details in the request body as JSON.

sku: Stock Keeping Unit or unique identifier.
name: Name of the item.
category: Category to which the item belongs.
tags: Comma-separated tags.
in_stock: Boolean indicating if the item is in stock.
quantity: Number of items in stock.


## Retrieving Items

Authenticated users see all items in the database

### Endpoint

`/items/api`

### Method

GET

## Retrieving Items using filter

Authenticated users can retrieve items in the database using query parameters

### Endpoint

`/items/api?category=Test`

### Method

GET







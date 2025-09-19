# Documentation for weather
### fastAPI: API to add CRUD around an existing weather_current table


This application has two generic endpoints:

| Method | URL Pattern           | Description             |
|--------|-----------------------|--------------------|
| GET    | /api/v1/weather/info         | Basic description of the application and container     |
| GET    | /api/v1/weather/health    | Health check endpoint     |



## CRUD Endpoints:
| Method | URL Pattern           | Description             | Example             |
|--------|-----------------------|--------------------|---------------------|
| GET    | /api/v1/weather         | List all weather     | /api/v1/weather       |
| GET    | /api/v1/weather/{id}    | Get weather by ID     | /api/v1/weather/42    |
| POST   | /api/v1/weather         | Create new weather    | /api/v1/weather       |
| PUT    | /api/v1/weather/{id}    | Update weather (full) | /api/v1/weather/42    |
| PATCH  | /api/v1/weather/{id}    | Update weather (partial) | /api/v1/weather/42 |
| DELETE | /api/v1/weather/{id}    | Delete weather        | /api/v1/weather/42    |


### Access the info endpoint
http://home.dev.com/api/v1/weather/info

### View test page
http://home.dev.com/weather/test/weather.html

### Swagger:
http://home.dev.com/api/v1/weather/docs
## Setup
1. Create super user
2. Use Admin to create a Social Application (with Name, Client id, Secret key, Sites)

## How to use a JS framework
1. Keep Django for API only (make sure URLs are set)
2. Allow Angular to talk to Django (`django-cors-headers` and `corsheaders.middleware.CorsMiddleware`)
3. Run Angular separately (dev mode - `ng serve`)
4. Point Angular service to Django API

### Production
1. Build Angular (`ng build` - this creates: `dist/your-app/`)
2. Move Angular build into Django (`your_project/static/angular/`)
3. Configure Django static files
4. Serve Angular from Django (`render(request, "index.html")`)
5. Add `index.html` template (with `static/angular/main.js`)
6. Catch-all route (`re_path(r"^.*$", index)`)

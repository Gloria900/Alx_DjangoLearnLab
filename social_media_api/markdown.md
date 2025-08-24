# DEPLOYMENT.md

## Deployment Guide (Render + Django)

This document explains how to deploy, update, and maintain the **Social Media API** on **Render**.

---

Live URL: [https://social-media-api-4ql2.onrender.com](https://social-media-api-4ql2.onrender.com)

---

## Initial Deployment

1. **Push Code to GitHub**
   Make sure your latest code is committed and pushed.

   ```bash
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

2. **Create a New Web Service on Render**

   - Go to [Render Dashboard](https://dashboard.render.com/).
   - Click **New → Web Service**.
   - Connect your GitHub repo.
   - Fill in:

     - **Environment**: `Python 3`

     - **Build Command**:

       ```bash
       pip install -r requirements.txt
       ```

     - **Start Command**:

       ```bash
       gunicorn social_media_api.wsgi:application
       ```

     - **Root Directory**: `social_media_api`

3. **Add Environment Variables** (Render → Settings → Environment)

   ```bash
   SECRET_KEY=your-django-secret-key
   DEBUG=False
   ALLOWED_HOSTS=social-media-api-4ql2.onrender.com
   DATABASE_URL=postgres://user:password@host:5432/dbname

   # Superuser (auto-created)
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@example.com
   DJANGO_SUPERUSER_PASSWORD=yourpassword
   ```

4. **Run Migrations + Create Superuser**
   Since Render’s free tier doesn’t give Shell access, I relied on the **fake superuser creation method**:

   - On the very first deploy, Django will automatically run migrations (`manage.py migrate --noinput`) and create a superuser using the env vars above.
   - If the superuser already exists, deployment will continue without errors.

---

## Updating Deployment

When you make changes to the code:

```bash
git add .
git commit -m "Update feature XYZ"
git push origin main
```

Render will automatically detect the new commit and redeploy.

---

## Running Migrations After Updates

If your update changes models (e.g., new fields, new apps):

```bash
python manage.py makemigrations
git add .
git commit -m "Add new migrations"
git push origin main
```

- The migration files will run automatically during the next Render deployment.
- No manual shell access needed.

---

## 4️⃣ Common Maintenance Tasks

- **Check Logs**

  ```bash
  render logs
  ```

  Or view logs in the Render Dashboard.

- **Create a New Superuser (later)**
  If you need another admin, temporarily update the `DJANGO_SUPERUSER_*` environment variables in Render → redeploy → then remove them after login.

- **Collect Static Files** (if using static assets)

  ```bash
  python manage.py collectstatic --noinput
  ```

- **Restart Service**
  Render Dashboard → **Manual Deploy → Clear build cache & redeploy**.

---

## 5️⃣ Troubleshooting

- **gunicorn not found** → Ensure `gunicorn` is in `requirements.txt`.

- **ImproperlyConfigured: STATIC_ROOT** → Add in `settings.py`:

  ```python
  STATIC_ROOT = BASE_DIR / "staticfiles"
  ```

- **Database connection error** → Double-check `DATABASE_URL` in Render.

- **Superuser not created** → Confirm that `DJANGO_SUPERUSER_*` env vars are set correctly in Render.

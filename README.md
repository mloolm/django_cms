# DjangoCMS - Website Engine Template any Purposes

This project allows you to quickly deploy and customize a website for any purposes. It provides a robust foundation with essential features and modules.

## Features

- **Containerization**: Powered by Docker Compose for easy deployment.
- **Caching**: Built-in caching mechanisms for improved performance.
- **Antivirus for Uploaded Files**: Ensures security by scanning all uploaded files.
- **Safe Image Resaving**: Protects against malicious image payloads.
- **Two-Factor Authentication (2FA)**: Enhanced security for user accounts.
- **Multilingual Support**: Ready for internationalization and localization.
- **Blog Module**:
  - Blog posts, categories, and static pages (can be created either on disk or in the database).
  - Contact information and social media integration.
- **Donations Module**:
  - Integration with Stripe and PayPal for donations.
  - Support for cryptocurrency wallet donations.
- **Website Module**:
  - A customizable module for your website.
  - Contains only views and route management, serving as the foundation for your site.
  - Fully customizable: You can modify URL structures, change designs, and adapt functionality without altering the core code.

## Installation

### Clone the repository:

```sh
git clone https://github.com/mloolm/django_cms.git
cd django_cms
```

### Install Docker if it’s not already installed:

Refer to the official Docker installation guide: [Docker Docs](https://docs.docker.com/get-docker/)
Refer to the official Docker Compose installation guide: [Docker Compose Docs](https://docs.docker.com/compose/install/)

```sh
sudo apt-get update
sudo apt-get install docker.io docker-compose
```

### Set up (or install) Nginx
Use the provided Nginx configuration template located at `nginx/dj_site.conf`. Reload Nginx after setup:

```sh
sudo nginx -s reload
```

### Create a `.env` file from the template and fill in the required values:

```sh
cp .env_template .env
```

### Build and start the Docker containers:

```sh
sudo docker-compose up --build -d
```

### Apply database migrations:

```sh
sudo make migrate
```

### Create a superuser account for admin access:

```sh
sudo make superuser
```

Your site is now ready! When deploying to production, remember to set `DJANGO_ENV` to `'production'` in the `.env` file.

## Usage

After installation, you can access the admin panel to manage your site's content, including blog posts, donation settings, and more. Customize the templates and styles in the Website module to match your branding.

For development purposes, keep `DJANGO_ENV` set to `'development'`. For production, switch it to `'production'` to enable optimized settings.

## Developing

### Frontend

To work with Webpack during development, you need to install `npm`:

```sh
sudo apt-get install npm
```

To start Webpack in watch mode, run the following command in the project directory:

```sh
npm run watch
```

For other available modes, check the `package.json` file.

### Backend

The dependency list is located in the `requirements.txt` file at the root of the project.

During development on a local machine, set `DJANGO_ENV` in the `.env` file to `'dev'`.

The website will be available on port `8000`. Example:

```
http://localhost:8000
```

For manual database management, access it on port `8080`. Example:

```
http://localhost:8080
```

## Contributing

We welcome contributions! If you'd like to contribute, follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```sh
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```sh
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```sh
   git push origin feature/your-feature
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Support

If you encounter any issues or have questions, feel free to open an issue on the GitHub repository.

## Author

**Pavel Krasheninin** - [GitHub Profile](https://github.com/mloolm) 

## Notes

- Ensure that all sensitive data (e.g., API keys, database credentials) is stored securely in the `.env` file and never committed to version control.
- Regularly back up your database and files to prevent data loss.
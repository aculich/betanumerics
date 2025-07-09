# Betanumerics - Unique Identifier Generator

A web-based MVP application that generates short, unique, human-friendly identifiers ("betanumerics") for users. The system allows users to enter their email address (used as a namespace/scope), then generate and return unique identifiers via a simple web interface and API.

<img width="668" alt="image" src="https://github.com/user-attachments/assets/a4ed0051-479d-4e47-84cf-b55c5f9612b8" />

## Features

- **User Scoping**: Email-based namespace for identifier generation
- **Betanumeric Generation**: Creates short, random-looking strings using a custom character set
- **Web Interface**: Simple, modern UI for generating identifiers
- **API Endpoint**: RESTful API for programmatic access
- **Opaque URLs**: Generated URLs with hashed user IDs for privacy
- **Easter Egg**: Hidden "slug/lug" feature with animated SVG
- **Copy to Clipboard**: Easy sharing of generated identifiers and URLs
- **Recent History**: Track recent identifiers for the current session

## Betanumeric Character Set

The system uses a custom character set that excludes:
- Vowels (`a`, `e`, `i`, `o`, `u`)
- Letter `l` (to avoid confusion)
- Ensures no more than two letters in a row before inserting a digit
- Includes check digit/character at the end for error detection

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd betanumerics
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or build and run with Docker**
   ```bash
   docker build -t betanumerics .
   docker run -p 5000:5000 betanumerics
   ```

### Replit Deployment

1. **Fork this repository** or create a new Repl
2. **Upload the files** to your Repl
3. **Click "Run"** - the application will start automatically
4. **Access your app** via the Replit URL

## API Usage

### Generate Identifier

**Endpoint:** `POST /api/generate`

**Request Body:**
```json
{
  "email": "user@example.com",
  "last_identifier": "optional-last-identifier"
}
```

**Response:**
```json
{
  "identifier": "b7qz",
  "url": "https://betanumerics.app/u/8f3d.../id/b7qz",
  "easter_egg": false
}
```

### Easter Egg Response

When using "slug" or "lug" as the email:

```json
{
  "identifier": "SLG",
  "url": "https://betanumerics.app/u/.../id/SLG",
  "easter_egg": true,
  "message": "You found the secret slug/lug!"
}
```

## Web Interface

### Main Features

1. **Email Input**: Enter your email address to create a namespace
2. **Generate Button**: Click to create a new unique identifier
3. **Result Display**: Shows the generated identifier and full URL
4. **Copy Buttons**: Easy copying of identifiers and URLs
5. **Recent History**: View your recently generated identifiers
6. **Easter Egg**: Try entering "slug" or "lug" as your email!

### URL Structure

Generated URLs follow the pattern:
```
https://betanumerics.app/u/<opaque_user_id>/id/<identifier>
```

Where:
- `<opaque_user_id>` is a hashed version of the email (not reversible)
- `<identifier>` is the betanumeric string

## Development

### Project Structure

```
betanumerics/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .replit               # Replit configuration
├── pyproject.toml        # Python packaging config
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   └── view_identifier.html
├── static/               # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── README.md
```

### Environment Variables

- `SECRET_KEY`: Flask secret key (default: dev key)
- `PORT`: Port to run the application (default: 5000)
- `FLASK_ENV`: Environment mode (development/production)

### Adding Features

1. **New Routes**: Add to `app.py`
2. **Frontend**: Modify templates in `templates/`
3. **Styling**: Update `static/css/style.css`
4. **JavaScript**: Edit `static/js/app.js`

## Easter Egg

The application includes a hidden easter egg feature:

- **Trigger**: Enter "slug" or "lug" as your email address
- **Result**: An animated SVG slug wearing sunglasses appears
- **Message**: "You found the secret slug/lug!"

## Deployment

### Replit

1. Create a new Python Repl
2. Upload all project files
3. The application will auto-start
4. Access via the Replit URL

### Docker

```bash
# Build image
docker build -t betanumerics .

# Run container
docker run -p 5000:5000 betanumerics

# Or use Docker Compose
docker-compose up --build
```

### Production Considerations

- Replace in-memory storage with a proper database
- Add rate limiting
- Implement proper session management
- Use environment variables for configuration
- Add logging and monitoring
- Set up HTTPS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions:
- Create an issue in the repository
- Check the documentation
- Review the code comments

---

**Happy generating! 🚀** 

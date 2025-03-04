# Subway Outlet Finder

A comprehensive solution for scraping, geocoding, and visualizing Subway restaurant outlets in Kuala Lumpur, Malaysia.

![Subway Outlet Finder](https://i.imgur.com/example.png)

## Features

- **Web Scraping**: Automated collection of Subway outlet data in Kuala Lumpur
- **Geocoding**: Conversion of addresses to geographical coordinates
- **Database Storage**: Well-designed schema for outlet information
- **REST API**: Comprehensive endpoints for data access and analysis
- **Interactive Map**: Visual representation of all outlets with detailed information
- **Catchment Analysis**: 5KM radius visualization around each outlet
- **Chatbot**: Natural language interface for outlet queries

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Python 3.9+
- **Database**: SQLite
- **Geocoding**: Geopy
- **Mapping**: Folium, Leaflet.js
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Data Processing**: Pandas

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/subway-outlet-finder.git
   cd subway-outlet-finder
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python main.py
   ```

5. Access the application at `http://localhost:8000`

## Project Structure

```
subway-outlet-finder/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py
│   ├── scraper/
│   │   ├── __init__.py
│   │   └── subway_scraper.py
│   ├── web/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── static/
│   │   └── templates/
│   │       ├── index.html
│   │       ├── catchment.html
│   │       └── chatbot.html
│   └── __init__.py
├── main.py
├── requirements.txt
└── README.md
```

## API Endpoints

### Outlets

- `GET /api/outlets`: Get all outlets with optional filtering
- `GET /api/outlets/{outlet_id}`: Get a specific outlet by ID
- `POST /api/outlets`: Create a new outlet
- `PUT /api/outlets/{outlet_id}`: Update an existing outlet
- `DELETE /api/outlets/{outlet_id}`: Delete an outlet

### Analysis

- `GET /api/outlets/nearby`: Find outlets within a specified radius of a point
- `GET /api/outlets/catchment-analysis`: Perform catchment analysis for all outlets

## Web Interface

- `/`: Home page with map visualization
- `/catchment`: Catchment analysis visualization
- `/chatbot`: Chatbot interface for natural language queries
- `/refresh-data`: Refresh outlet data by running the scraper again

## Catchment Analysis

The application performs catchment analysis by:

1. Drawing a 5KM radius circle around each outlet
2. Identifying overlapping catchment areas
3. Calculating coverage statistics
4. Visualizing the results on an interactive map

This analysis helps in understanding:
- Market coverage and saturation
- Potential areas for new outlets
- Competition between existing outlets

## Chatbot Functionality

The chatbot can answer questions about:
- The nearest Subway outlet to a location
- Opening hours of specific outlets
- Delivery options
- Total number of outlets in the city

Example queries:
- "Which Subway is nearest to KLCC?"
- "What are the opening hours of Subway Mid Valley?"
- "Do Subway outlets offer delivery?"
- "How many Subway outlets are in KL?"

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Subway Malaysia for the outlet information
- OpenStreetMap for the map data
- All the open-source libraries that made this project possible
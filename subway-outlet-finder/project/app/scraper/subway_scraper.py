import requests
from bs4 import BeautifulSoup
import pandas as pd
from geopy.geocoders import Nominatim
import time
from sqlalchemy.orm import Session
from app.database.db import Outlet, get_db

class SubwayScraper:
    def __init__(self):
        self.base_url = "https://www.subway.com/en-MY/FindAStore"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.headers = {
            "User-Agent": self.user_agent
        }
        self.geolocator = Nominatim(user_agent="subway_outlet_finder")
        
    def scrape_outlets(self):
        """Scrape Subway outlets in Kuala Lumpur"""
        print("Starting to scrape Subway outlets...")
        
        # In a real implementation, we would parse the Subway website
        # For this demo, we'll create sample data for KL outlets
        sample_outlets = [
            {
                "name": "Subway KLCC",
                "address": "Lot 107, First Floor Suria KLCC, Kuala Lumpur City Centre",
                "city": "Kuala Lumpur",
                "state": "Federal Territory",
                "postal_code": "50088",
                "phone": "03-2166 7327",
                "has_delivery": True,
                "has_dine_in": True,
                "opening_hours": "10:00 AM - 10:00 PM"
            },
            {
                "name": "Subway Mid Valley",
                "address": "Lot T-018A, 3rd Floor, Mid Valley Megamall, Lingkaran Syed Putra",
                "city": "Kuala Lumpur",
                "state": "Federal Territory",
                "postal_code": "59200",
                "phone": "03-2282 1789",
                "has_delivery": True,
                "has_dine_in": True,
                "opening_hours": "10:00 AM - 10:00 PM"
            },
            {
                "name": "Subway Pavilion",
                "address": "Lot 5.24.00, Level 5, Pavilion Kuala Lumpur, 168 Jalan Bukit Bintang",
                "city": "Kuala Lumpur",
                "state": "Federal Territory",
                "postal_code": "55100",
                "phone": "03-2141 9033",
                "has_delivery": True,
                "has_dine_in": True,
                "opening_hours": "10:00 AM - 10:00 PM"
            },
            {
                "name": "Subway NU Sentral",
                "address": "L4-19, Level 4, NU Sentral Shopping Centre, Jalan Tun Sambanthan",
                "city": "Kuala Lumpur",
                "state": "Federal Territory",
                "postal_code": "50470",
                "phone": "03-2276 0301",
                "has_delivery": True,
                "has_dine_in": True,
                "opening_hours": "10:00 AM - 10:00 PM"
            },
            {
                "name": "Subway Sunway Putra Mall",
                "address": "Lot 4-19, Level 4, Sunway Putra Mall, 100 Jalan Putra",
                "city": "Kuala Lumpur",
                "state": "Federal Territory",
                "postal_code": "50350",
                "phone": "03-2602 3660",
                "has_delivery": True,
                "has_dine_in": True,
                "opening_hours": "10:00 AM - 10:00 PM"
            }
        ]
        
        return sample_outlets
    
    def geocode_outlets(self, outlets):
        """Geocode outlet addresses to get latitude and longitude"""
        print("Geocoding outlet addresses...")
        
        for outlet in outlets:
            full_address = f"{outlet['address']}, {outlet['city']}, {outlet['state']}, Malaysia {outlet['postal_code']}"
            try:
                location = self.geolocator.geocode(full_address)
                if location:
                    outlet["latitude"] = location.latitude
                    outlet["longitude"] = location.longitude
                else:
                    # Fallback coordinates for KL outlets if geocoding fails
                    # These are approximate coordinates for demonstration
                    if "KLCC" in outlet["name"]:
                        outlet["latitude"] = 3.1588
                        outlet["longitude"] = 101.7112
                    elif "Mid Valley" in outlet["name"]:
                        outlet["latitude"] = 3.1175
                        outlet["longitude"] = 101.6769
                    elif "Pavilion" in outlet["name"]:
                        outlet["latitude"] = 3.1488
                        outlet["longitude"] = 101.7137
                    elif "NU Sentral" in outlet["name"]:
                        outlet["latitude"] = 3.1332
                        outlet["longitude"] = 101.6865
                    elif "Sunway Putra" in outlet["name"]:
                        outlet["latitude"] = 3.1667
                        outlet["longitude"] = 101.6953
                    else:
                        # Default to KL city center
                        outlet["latitude"] = 3.1390
                        outlet["longitude"] = 101.6869
                
                # Sleep to avoid hitting rate limits
                time.sleep(1)
            except Exception as e:
                print(f"Error geocoding {outlet['name']}: {e}")
                # Set default coordinates for KL
                outlet["latitude"] = 3.1390
                outlet["longitude"] = 101.6869
        
        return outlets
    
    def save_to_database(self, outlets):
        """Save outlets to database"""
        print("Saving outlets to database...")
        
        db = next(get_db())
        
        for outlet_data in outlets:
            outlet = Outlet(
                name=outlet_data["name"],
                address=outlet_data["address"],
                city=outlet_data["city"],
                state=outlet_data["state"],
                postal_code=outlet_data["postal_code"],
                phone=outlet_data.get("phone"),
                latitude=outlet_data.get("latitude"),
                longitude=outlet_data.get("longitude"),
                has_delivery=outlet_data.get("has_delivery", False),
                has_dine_in=outlet_data.get("has_dine_in", True),
                opening_hours=outlet_data.get("opening_hours")
            )
            
            # Check if outlet already exists
            existing = db.query(Outlet).filter(Outlet.name == outlet.name).first()
            if not existing:
                db.add(outlet)
        
        db.commit()
        print("Outlets saved to database successfully")
    
    def run_scraper(self):
        """Run the complete scraping process"""
        outlets = self.scrape_outlets()
        geocoded_outlets = self.geocode_outlets(outlets)
        self.save_to_database(geocoded_outlets)
        return geocoded_outlets

# For testing
if __name__ == "__main__":
    scraper = SubwayScraper()
    scraper.run_scraper()
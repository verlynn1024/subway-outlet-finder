from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import folium
from folium.plugins import MarkerCluster
import json

from app.database.db import get_db, Outlet
from app.scraper.subway_scraper import SubwayScraper

router = APIRouter()
templates = Jinja2Templates(directory="app/web/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """Home page with map visualization"""
    outlets = db.query(Outlet).all()
    
    # Check if we have outlets, if not run the scraper
    if not outlets:
        scraper = SubwayScraper()
        scraper.run_scraper()
        outlets = db.query(Outlet).all()
    
    # Create a map centered on KL
    m = folium.Map(location=[3.1390, 101.6869], zoom_start=12)
    
    # Add marker cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add markers for each outlet
    for outlet in outlets:
        if outlet.latitude and outlet.longitude:
            popup_html = f"""
            <strong>{outlet.name}</strong><br>
            {outlet.address}<br>
            {outlet.city}, {outlet.state} {outlet.postal_code}<br>
            Phone: {outlet.phone or 'N/A'}<br>
            Hours: {outlet.opening_hours or 'N/A'}<br>
            Delivery: {'Yes' if outlet.has_delivery else 'No'}<br>
            Dine-in: {'Yes' if outlet.has_dine_in else 'No'}
            """
            
            folium.Marker(
                location=[outlet.latitude, outlet.longitude],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=outlet.name,
                icon=folium.Icon(icon="cutlery", prefix="fa", color="green")
            ).add_to(marker_cluster)
    
    # Convert map to HTML
    map_html = m._repr_html_()
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "map_html": map_html, "outlets": outlets}
    )

@router.get("/catchment", response_class=HTMLResponse)
async def catchment_analysis(request: Request, db: Session = Depends(get_db)):
    """Catchment analysis visualization"""
    outlets = db.query(Outlet).all()
    
    # Create a map centered on KL
    m = folium.Map(location=[3.1390, 101.6869], zoom_start=12)
    
    # Add 5km radius circles for each outlet
    for outlet in outlets:
        if outlet.latitude and outlet.longitude:
            # Add marker for the outlet
            popup_html = f"""
            <strong>{outlet.name}</strong><br>
            {outlet.address}<br>
            {outlet.city}, {outlet.state} {outlet.postal_code}<br>
            """
            
            folium.Marker(
                location=[outlet.latitude, outlet.longitude],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=outlet.name,
                icon=folium.Icon(icon="cutlery", prefix="fa", color="green")
            ).add_to(m)
            
            # Add 5km catchment circle
            folium.Circle(
                location=[outlet.latitude, outlet.longitude],
                radius=5000,  # 5km in meters
                color="blue",
                fill=True,
                fill_color="blue",
                fill_opacity=0.1,
                popup=f"{outlet.name} - 5km Catchment"
            ).add_to(m)
    
    # Convert map to HTML
    map_html = m._repr_html_()
    
    return templates.TemplateResponse(
        "catchment.html", 
        {"request": request, "map_html": map_html, "outlets": outlets}
    )

@router.get("/chatbot", response_class=HTMLResponse)
async def chatbot(request: Request):
    """Chatbot interface for natural language queries"""
    return templates.TemplateResponse("chatbot.html", {"request": request})

@router.post("/chatbot/query")
async def process_query(request: Request, query: str = Form(...), db: Session = Depends(get_db)):
    """Process natural language queries about outlets"""
    query = query.lower()
    
    # Simple rule-based chatbot
    if "nearest" in query or "closest" in query:
        # Default to KL city center if no location specified
        lat, lng = 3.1390, 101.6869
        
        # Extract location if mentioned
        if "klcc" in query:
            lat, lng = 3.1588, 101.7112
        elif "mid valley" in query:
            lat, lng = 3.1175, 101.6769
        elif "pavilion" in query:
            lat, lng = 3.1488, 101.7137
        
        # Find nearest outlet
        outlets = db.query(Outlet).all()
        nearest = None
        min_distance = float('inf')
        
        from geopy.distance import geodesic
        
        for outlet in outlets:
            if outlet.latitude and outlet.longitude:
                distance = geodesic((lat, lng), (outlet.latitude, outlet.longitude)).kilometers
                if distance < min_distance:
                    min_distance = distance
                    nearest = outlet
        
        if nearest:
            return {
                "response": f"The nearest Subway outlet is {nearest.name} at {nearest.address}, which is approximately {min_distance:.2f} km away."
            }
    
    elif "delivery" in query:
        # Count outlets with delivery
        delivery_count = db.query(Outlet).filter(Outlet.has_delivery == True).count()
        return {
            "response": f"There are {delivery_count} Subway outlets in Kuala Lumpur that offer delivery service."
        }
    
    elif "how many" in query or "count" in query:
        # Count total outlets
        outlet_count = db.query(Outlet).count()
        return {
            "response": f"There are {outlet_count} Subway outlets in Kuala Lumpur."
        }
    
    elif "opening" in query or "hours" in query or "time" in query:
        # Get opening hours for a specific outlet
        outlets = db.query(Outlet).all()
        for outlet in outlets:
            if outlet.name.lower() in query:
                return {
                    "response": f"{outlet.name} is open {outlet.opening_hours or 'during regular hours'}."
                }
        
        # Default response if no specific outlet mentioned
        return {
            "response": "Most Subway outlets in Kuala Lumpur are open from 10:00 AM to 10:00 PM. Please specify which outlet you're interested in for exact hours."
        }
    
    # Default response
    return {
        "response": "I can help you find Subway outlets in Kuala Lumpur. You can ask about the nearest outlet, delivery options, opening hours, or the total number of outlets."
    }

@router.get("/refresh-data")
async def refresh_data(request: Request):
    """Refresh outlet data by running the scraper again"""
    scraper = SubwayScraper()
    scraper.run_scraper()
    return RedirectResponse(url="/", status_code=303)
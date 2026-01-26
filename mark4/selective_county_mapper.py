"""
Selective County Mapper - Color specific counties across multiple states
and retrieve coordinates for location/distance analysis

Design pattern:
1. Select counties from states
2. Color only those counties on map
3. Export coordinates in structured format ready for place/distance queries
4. Extensible architecture for future place-finding features
"""

import geopandas as gpd
import folium
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum


@dataclass
class CountyLocation:
    """Data class for county location info - optimized for extensibility"""
    state: str
    county_name: str
    latitude: float
    longitude: float
    fips_code: str
    color: str
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    def google_maps_url(self, zoom: int = 12) -> str:
        """Generate Google Maps URL"""
        return f"https://www.google.com/maps?q={self.latitude},{self.longitude}&z={zoom}"
    
    def google_places_search_url(self, place_type: str) -> str:
        """Future extension: Generate Google Places search URL
        
        Args:
            place_type: e.g., "airport", "grocery_store", "hospital"
        
        Returns:
            URL for searching nearby places in Google Maps
        """
        return f"https://www.google.com/maps/search/{place_type}/@{self.latitude},{self.longitude},15z"


@dataclass
class SelectionRequest:
    """Container for user selections - clean interface"""
    selections: Dict[str, List[str]]  # {state: [county1, county2, ...]}
    
    def add_counties(self, state: str, counties: List[str]):
        """Add counties for a state"""
        if state not in self.selections:
            self.selections[state] = []
        self.selections[state].extend(counties)
    
    def get_total_counties(self) -> int:
        """Get total counties selected"""
        return sum(len(counties) for counties in self.selections.values())
    
    def to_dict(self):
        """Convert to dictionary"""
        return {"selections": self.selections}


class SelectiveCountyMapper:
    """
    Maps ONLY selected counties from specified states
    Designed for extensibility to location/distance queries
    """
    
    # Color palette
    COLORS = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
        '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B88B', '#A8E6CF',
        '#FFD93D', '#6BCB77', '#4D96FF', '#FF6348', '#9B59B6',
        '#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#E91E63',
        '#00BCD4', '#8BC34A', '#FF9800', '#673AB7', '#009688'
    ]
    
    def __init__(self):
        """Initialize mapper and load county GeoDataFrame"""
        print("Loading US County data from US Census Bureau...")
        try:
            self.counties = gpd.read_file(
                'https://www2.census.gov/geo/tiger/GENZ2021/shp/cb_2021_us_county_5m.zip'
            ).to_crs('EPSG:4326')
            print(f"✓ Loaded {len(self.counties)} counties")
        except Exception as e:
            print(f"✗ Error loading counties: {e}")
            raise
    
    def get_available_counties(self, state: str) -> List[str]:
        """
        Get all available county names for a state
        
        Args:
            state: Two-letter state abbreviation
        
        Returns:
            Sorted list of county names
        """
        state = state.upper()
        state_counties = self.counties[self.counties['STUSPS'] == state]
        
        if state_counties.empty:
            print(f"✗ State '{state}' not found")
            return []
        
        counties = sorted(state_counties['NAME'].unique())
        return counties
    
    def validate_selection(self, selections: Dict[str, List[str]]) -> Tuple[bool, str]:
        """
        Validate user selections before processing
        
        Args:
            selections: {state: [county1, county2, ...]}
        
        Returns:
            Tuple of (is_valid, message)
        """
        if not selections:
            return False, "No states selected"
        
        for state, counties in selections.items():
            # if(state == "PR"):
            #     continue
            # state = state.upper()
            # available = self.get_available_counties(state)
            available = counties
                
            # if not available:
            #     return False, f"State '{state}' not found"
            
            # if not counties:
            #     # continue
            #     return False, f"No counties specified for {state}"
            
            # Check each county exists
            missing = [c for c in counties if c not in available]
            if missing:
                return False, f"Unknown counties in {state}: {missing}"
        
        return True, "Selection valid"
    
    def get_selected_counties_geo(self, selections: Dict[str, List[str]]) -> gpd.GeoDataFrame:
        """
        Filter GeoDataFrame to only selected counties
        
        Args:
            selections: {state: [county1, county2, ...]}
        
        Returns:
            GeoDataFrame with only selected counties
        """
        frames = []
        
        for state, counties in selections.items():
            state = state.upper()
            state_data = self.counties[self.counties['STUSPS'] == state]
            
            # Filter to selected counties
            selected = state_data[state_data['NAME'].isin(counties)]
            frames.append(selected)
        
        if not frames:
            return gpd.GeoDataFrame()
        
        return pd.concat(frames, ignore_index=True)
    
    def get_selected_locations(self, 
                              selections: Dict[str, List[str]],
                              include_unselected_color: Optional[str] = None) -> List[CountyLocation]:
        """
        Get location data for selected counties
        Ready for future place/distance analysis
        
        Args:
            selections: {state: [county1, county2, ...]}
            include_unselected_color: If set, include unselected counties with this color
        
        Returns:
            List of CountyLocation objects sorted by state, then county
        """
        selected_geo = self.get_selected_counties_geo(selections)
        locations = []
        
        # Calculate centroids
        selected_geo['centroid'] = selected_geo.geometry.centroid
        
        color_idx = 0
        for _, county in selected_geo.iterrows():
            state = county['STUSPS']
            county_name = county['NAME']
            
            location = CountyLocation(
                state=state,
                county_name=county_name,
                latitude=county['centroid'].y,
                longitude=county['centroid'].x,
                fips_code=f"{county['STATEFP']}{county['COUNTYFP']}",
                color=self.COLORS[color_idx % len(self.COLORS)]
            )
            locations.append(location)
            color_idx += 1
        
        # Sort for consistency
        locations.sort(key=lambda x: (x.state, x.county_name))
        return locations
    
    def export_locations_json(self, 
                             locations: List[CountyLocation],
                             output_file: str = 'selected_counties.json') -> str:
        """
        Export selected county locations to JSON
        Optimized format for future place/distance queries
        
        Args:
            locations: List of CountyLocation objects
            output_file: Output JSON filename
        
        Returns:
            Path to output file
        """
        data = {
            'metadata': {
                'total_counties': len(locations),
                'states': sorted(set(loc.state for loc in locations))
            },
            'counties': [loc.to_dict() for loc in locations]
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Exported {len(locations)} county locations to {output_file}")
        return output_file
    
    def export_locations_csv(self,
                            locations: List[CountyLocation],
                            output_file: str = 'selected_counties.csv') -> str:
        """
        Export selected county locations to CSV
        For spreadsheet analysis and sharing
        
        Args:
            locations: List of CountyLocation objects
            output_file: Output CSV filename
        
        Returns:
            Path to output file
        """
        df = pd.DataFrame([loc.to_dict() for loc in locations])
        
        # Reorder columns for readability
        cols = ['state', 'county_name', 'latitude', 'longitude', 'fips_code', 'color']
        df = df[cols]
        
        df.to_csv(output_file, index=False)
        print(f"✓ Exported {len(locations)} county locations to {output_file}")
        return output_file
    
    def create_selective_map(self,
                            selections: Dict[str, List[str]],
                            output_file: str = 'selected_counties_map.html',
                            show_unselected: bool = False) -> folium.Map:
        """
        Create map with ONLY selected counties colored
        Unselected counties shown in light gray or hidden
        
        Args:
            selections: {state: [county1, county2, ...]}
            output_file: Output HTML filename
            show_unselected: If True, show unselected counties in light gray
        
        Returns:
            Folium map object
        """
        # Validate
        is_valid, msg = self.validate_selection(selections)
        if not is_valid:
            print(f"✗ Invalid selection: {msg}")
            return None
        
        # Get selected counties
        selected_geo = self.get_selected_counties_geo(selections)
        locations = self.get_selected_locations(selections)
        
        # Create color mapping
        color_map = {f"{loc.state}_{loc.county_name}": loc.color for loc in locations}
        
        # Calculate map center from selected counties
        bounds = selected_geo.total_bounds
        center_lat = (bounds[1] + bounds[3]) / 2
        center_lon = (bounds[0] + bounds[2]) / 2
        
        # Create base map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Add all counties if requested
        if show_unselected:
            all_counties = self.counties.copy()
            all_counties['centroid'] = all_counties.geometry.centroid
            
            for _, county in all_counties.iterrows():
                state = county['STUSPS']
                county_name = county['NAME']
                key = f"{state}_{county_name}"
                
                # Use selected color or light gray
                color = color_map.get(key, '#E0E0E0')
                opacity = 0.7 if key in color_map else 0.2
                
                folium.GeoJson(
                    data=county.geometry.__geo_interface__,
                    style_function=lambda x, c=color, op=opacity: {
                        'fillColor': c,
                        'color': 'black' if op > 0.5 else '#CCCCCC',
                        'weight': 0.5,
                        'fillOpacity': op
                    },
                    tooltip=county_name if op > 0.5 else None
                ).add_to(m)
        else:
            # Add only selected counties
            selected_geo['centroid'] = selected_geo.geometry.centroid
            
            for _, county in selected_geo.iterrows():
                state = county['STUSPS']
                county_name = county['NAME']
                key = f"{state}_{county_name}"
                color = color_map[key]
                centroid = county['centroid']
                
                # Create popup with location info
                popup_text = f"""
                <b>{county_name} County, {state}</b><br>
                Lat: {centroid.y:.6f}<br>
                Lon: {centroid.x:.6f}<br>
                FIPS: {county['STATEFP']}{county['COUNTYFP']}<br>
                <a href="https://www.google.com/maps?q={centroid.y},{centroid.x}" 
                   target="_blank">📍 Google Maps</a>
                """
                
                folium.GeoJson(
                    data=county.geometry.__geo_interface__,
                    style_function=lambda x, c=color: {
                        'fillColor': c,
                        'color': 'black',
                        'weight': 1.5,
                        'fillOpacity': 0.8
                    },
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=county_name
                ).add_to(m)
                
                # Add marker at centroid
                folium.CircleMarker(
                    location=[centroid.y, centroid.x],
                    radius=4,
                    popup=county_name,
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.9,
                    weight=1
                ).add_to(m)
        
        # Add title
        total = sum(len(c) for c in selections.values())
        states_list = ", ".join(sorted(selections.keys()))
        title_html = f'''
        <div style="position: fixed; top: 10px; left: 50px; width: 350px; 
                    background-color: white; border: 2px solid grey; 
                    z-index: 9999; font-size: 14px; padding: 12px;
                    border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.2)">
            <b>Selected Counties Map</b><br>
            <span style="font-size: 12px; color: #666;">
            States: {states_list}<br>
            Counties: {total}
            </span>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(title_html))
        
        m.save(output_file)
        print(f"✓ Map saved to {output_file}")
        return m
    
    def print_locations_table(self, locations: List[CountyLocation]):
        """
        Pretty print locations table
        
        Args:
            locations: List of CountyLocation objects
        """
        print(f"\n{'State':8} {'County':25} {'Latitude':12} {'Longitude':13} {'Color':12}")
        print("-" * 75)
        
        for loc in locations:
            print(f"{loc.state:8} {loc.county_name:25} {loc.latitude:12.6f} {loc.longitude:13.6f} {loc.color:12}")

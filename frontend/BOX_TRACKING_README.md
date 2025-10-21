# Box Tracking Feature

## Overview
The Box Tracking feature provides real-time location tracking of transport boxes on an interactive map. This feature helps monitor the geographical location of biological samples during transport.

## Features

### 📍 Interactive Map
- **OpenStreetMap Integration**: Uses Leaflet library for interactive mapping
- **Real-time Markers**: Each transport box is displayed as a marker on the map
- **Color-coded Status**: Markers change color based on box status:
  - 🟢 Green: Active
  - 🔵 Blue: In Transit
  - 🟣 Purple: Delivered
  - 🟠 Orange: Maintenance
  - 🔴 Red: Inactive

### 📦 Box Selection
- **Dropdown Selector**: Choose any transport box from the list
- **Auto-center**: Map automatically centers on the selected box
- **Quick Navigation**: Click on any marker to view box details

### 📊 Real-time Data Display
- **Box ID**: Unique identifier for each transport box
- **Temperature**: Current temperature with color-coded alerts
  - Green: Within safe range (2-8°C)
  - Red: Outside safe range
- **Humidity**: Current humidity percentage
- **Status**: Current operational status
- **Location**: GPS coordinates or location name
- **Last Updated**: Timestamp of last data update

### 🔄 Auto-refresh
- **Automatic Updates**: Data refreshes every 30 seconds
- **Manual Refresh**: Button to immediately update data
- **Loading States**: Visual feedback during data fetching

### 🗺️ Map Popups
Click on any marker to see detailed information:
- Box ID
- Location
- Status
- Temperature
- Humidity
- Last updated timestamp

## Technical Implementation

### Dependencies
```json
{
  "leaflet": "^1.9.x",
  "react-leaflet": "^4.2.x",
  "@types/leaflet": "^1.9.x"
}
```

### Components
- **BoxTracking.tsx**: Main component for map and tracking interface
- **BoxTracking.css**: Styling for map and custom markers

### Location Parsing
The component supports two geolocation formats:
1. **Coordinates**: "latitude,longitude" (e.g., "42.3601,-71.0589")
2. **Location Names**: City names with fallback coordinates (e.g., "Boston", "New York")

### Predefined Locations
For demo purposes, the following cities have predefined coordinates:
- Boston
- New York
- Philadelphia
- Chicago
- San Francisco
- Los Angeles
- Seattle
- Miami

## Usage

### Navigation
1. Start the frontend application: `npm run dev`
2. Open your browser to the displayed URL (typically http://localhost:5173)
3. Click on "Box Tracking" in the navigation menu

### Tracking a Box
1. Select a transport box from the dropdown
2. View the box location on the map
3. Click on markers to see detailed information
4. Monitor temperature and humidity in real-time

### Understanding Status Colors
- **Active** (Green): Box is operational and in use
- **In Transit** (Blue): Box is currently being transported
- **Delivered** (Purple): Box has reached its destination
- **Maintenance** (Orange): Box is under maintenance
- **Inactive** (Red): Box is not in use

## API Integration

### Endpoints Used
- `GET /boxes`: Fetch all transport boxes
- `GET /boxes/{boxId}`: Fetch specific box details

### Data Model
```typescript
interface TransportBox {
  box_id: string;
  geolocation: string;
  temperature: number;
  humidity: number;
  status: string;
  last_updated: string;
}
```

## Future Enhancements

### Planned Features
- [ ] Real-time tracking with MQTT updates
- [ ] Route history and playback
- [ ] Geofencing and alerts
- [ ] Multi-box tracking comparison
- [ ] Export location history
- [ ] Custom map styles/themes
- [ ] Clustering for many boxes
- [ ] Heat maps for temperature zones

### Backend Requirements
For full functionality, ensure:
1. Backend API is running (Django service)
2. Database has transport box data
3. Geolocation data is properly formatted

## Troubleshooting

### Map Not Loading
- Check if Leaflet CSS is imported
- Verify internet connection (for map tiles)
- Check browser console for errors

### No Boxes Displayed
- Verify backend API is running
- Check if database has transport box data
- Inspect network tab for API errors

### Markers Not Visible
- Ensure geolocation data is valid
- Check coordinate format (latitude,longitude)
- Verify marker icons are properly loaded

## Browser Support
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Performance
- Optimized for up to 100 simultaneous markers
- Auto-refresh interval: 30 seconds (configurable)
- Lazy loading of map tiles

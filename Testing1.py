import folium
import requests
import datetime

# Replace with your actual token
token= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmcmVpZ2h0d2ViIiwidmVyIjoiMS4wIiwidXNlcm5hbWUiOiJKQUVOU00iLCJzdCI6MCwiaWF0IjoxNzQ3MjYzMzk2LCJleHAiOjE3NDcyOTIxOTZ9.3PzSrU14q65Y1j8H70h3ab6526oeaY_vW_d_56f1_3Y"

url = "https://fleettracker.pacificnational.com.au/api/v1/MapMarkers"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("✅ Token is valid. Generating map...")
    data = response.json()

    if not data:
        print("⚠️ No data returned.")
        exit()

    # Start map centered on the first marker
    map_center = data[0]['latLong']
    m = folium.Map(location=map_center, zoom_start=6)

    for item in data:
        lat, lon = item.get('latLong', [None, None])
        if lat is None or lon is None:
            continue

        marker_type = item.get('type', 'unknown')
        marker_id = item.get('id', 'N/A')
        locos = ", ".join(item.get('locoIdentifiers', [])) or "None"
        timestamp = item.get('timestamp', 'N/A')
        speed_value = item.get('speed')
        if speed_value is None:
            speed = "N/A"
    else:
        speed = f"{speed_value:.1f} km/h"
        heading = f"{item.get('heading', 0):.1f}°"
        unit = item.get('unit', 'N/A')

        # Format popup HTML
        popup_html = f"""
        <b>ID:</b> {marker_id}<br>
        <b>Type:</b> {marker_type}<br>
        <b>Locos:</b> {locos}<br>
        <b>Unit:</b> {unit}<br>
        <b>Speed:</b> {speed}<br>
        <b>Heading:</b> {heading}<br>
        <b>Last GPS:</b> {timestamp}<br>
        <b>Lat/Lon:</b> {lat:.5f}, {lon:.5f}
        """

        # Choose color based on type
        color = {
            'train': 'blue',
            'car': 'pink',
            'loco': 'green'
        }.get(marker_type, 'gray')

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=color)
        ).add_to(m)

    # Save and notify
    m.save("fleet_tracker_map.html")
    print("✅ Map saved to 'fleet_tracker_map.html'. Open it in your browser.")
else:
    print(f"❌ Error {response.status_code}: {response.text}")
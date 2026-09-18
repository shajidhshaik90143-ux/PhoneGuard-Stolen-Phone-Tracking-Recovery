import folium
from streamlit_folium import st_folium


def display_location_map(
    latitude,
    longitude,
    popup_text="Last Known Location"
):
    map_object = folium.Map(
        location=[latitude, longitude],
        zoom_start=15
    )

    folium.Marker(
        [latitude, longitude],
        popup=popup_text,
        tooltip="Phone Location"
    ).add_to(map_object)

    st_folium(
        map_object,
        width=900,
        height=500
    )
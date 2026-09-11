
import os
import numpy as np
from supabase import create_client
import streamlit as st

# Mineral-to-rock mapping (which rock types typically contain which minerals)
MINERAL_ROCK_MAP = {
    "biotite": ["GRANITE", "GRANODIORITE", "SYENITE", "GNEISS", "SCHIST", "DIORITE", "MONZONITE"],
    "bornite": ["BASALT", "GABBRO", "DIORITE", "PORPHYRY", "ANDESITE"],
    "chrysocolla": ["BASALT", "ANDESITE", "GABBRO", "SERPENTINITE", "SCHIST"],
    "malachite": ["LIMESTONE", "DOLOMITE", "SANDSTONE", "SHALE", "BASALT"],
    "muscovite": ["GRANITE", "PEGMATITE", "SCHIST", "GNEISS", "PHYLLITE"],
    "pyrite": ["SHALE", "SLATE", "BASALT", "ANDESITE", "GRANITE", "SEDIMENTARY"],
    "quartz": ["GRANITE", "PEGMATITE", "SANDSTONE", "QUARTZITE", "SCHIST", "GNEISS"],
}

class GeoROCValidator:
    def __init__(self):
        try:
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["service_key"]
            self.client = create_client(url, key)
            self.enabled = True
        except Exception as e:
            print(f"GeoROC validator disabled: {e}")
            self.enabled = False
    
    def find_nearby_samples(self, lat, lon, radius_km=100, limit=200):
        """Find GEOROC samples within a radius of the given location."""
        if not self.enabled:
            return []
        
        # Simple bounding box (approximation)
        # 1 degree latitude ≈ 111 km; longitude depends on latitude
        lat_delta = radius_km / 111.0
        lon_delta = radius_km / (111.0 * max(0.1, np.cos(np.radians(lat))))
        
        try:
            res = self.client.table("spectra_georoc_train") \
                .select("latitude,longitude,rock_name,rock_type,location,sio2,mgo,k2o,na2o") \
                .gte("latitude", lat - lat_delta) \
                .lte("latitude", lat + lat_delta) \
                .gte("longitude", lon - lon_delta) \
                .lte("longitude", lon + lon_delta) \
                .limit(limit) \
                .execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"GEOROC query error: {e}")
            return []
    
    def validate_prediction(self, predicted_mineral, lat, lon, radius_km=100):
        """
        Check if the predicted mineral makes geological sense at this location.
        Returns: {
            "found_samples": N,
            "expected_rocks": [...],
            "region_match": True/False/None,
            "message": str
        }
        """
        if not self.enabled:
            return {"found_samples": 0, "region_match": None, "message": "GEOROC validation disabled"}
        
        samples = self.find_nearby_samples(lat, lon, radius_km)
        
        if not samples:
            return {
                "found_samples": 0,
                "region_match": None,
                "message": f"No GEOROC data within {radius_km}km of this location"
            }
        
        # Check if any sample's rock type matches the expected rocks for this mineral
        expected_rocks = MINERAL_ROCK_MAP.get(predicted_mineral, [])
        matching_rocks = []
        
        for sample in samples:
            rock_name = (sample.get("rock_name") or "").upper()
            for expected in expected_rocks:
                if expected in rock_name:
                    matching_rocks.append(rock_name)
                    break
        
        region_match = len(matching_rocks) > 0
        match_pct = (len(matching_rocks) / len(samples)) * 100 if samples else 0
        
        if region_match:
            message = f"✅ {match_pct:.0f}% of nearby samples contain rocks typically hosting {predicted_mineral}"
        else:
            message = f"⚠️ No matching rock types nearby ({len(samples)} samples). This mineral may be unusual for this region."
        
        return {
            "found_samples": len(samples),
            "expected_rocks": expected_rocks,
            "matching_rocks": list(set(matching_rocks))[:5],
            "region_match": region_match,
            "match_pct": match_pct,
            "message": message,
        }

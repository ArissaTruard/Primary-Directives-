import logging
import asyncio
import httpx

class LocationHandler:
    def __init__(self, location_api_url="https://ipapi.co/json/"):
        self.location_api_url = location_api_url

    async def get_location(self):
        """Retrieves location data using an external API."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.location_api_url)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                location_data = response.json()

                # Extract relevant location information
                location_info = {
                    "city": location_data.get("city"),
                    "region": location_data.get("region"),
                    "country": location_data.get("country_name"),
                    "latitude": location_data.get("latitude"),
                    "longitude": location_data.get("longitude"),
                    "postal_code": location_data.get("postal"),
                    "timezone": location_data.get("timezone")
                }

                logging.info(f"Location data retrieved: {location_info}")
                return location_info

        except httpx.HTTPError as e:
            logging.error(f"HTTP error retrieving location: {e}")
            return {}  # Return empty dictionary on error
        except Exception as e:
            logging.error(f"Error retrieving location: {e}")
            return {}  # Return empty dictionary on error

# Example usage (for testing):
async def main():
    location_handler = LocationHandler()
    location = await location_handler.get_location()
    print(location)

if __name__ == "__main__":
    asyncio.run(main())

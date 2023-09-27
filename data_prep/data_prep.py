"""
Python script to fetch data from the IOM website and 
preprocess it for use in the missing-migrants project.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandas.errors import ParserError


def get_data_url() -> str:
    """
    Function to scrape the IOM Missing Migrants Project website
    and extract the URL of the CSV file.
    """

    url = "https://missingmigrants.iom.int/downloads"

    # Define custom headers
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        )
    }

    # Fetch HTML content
    try:
        response = requests.get(url, headers=headers, timeout=30)

        # Check if the request was successful
        if response.status_code == 200:
            html = response.text

            # Parse fetched HTML
            soup = BeautifulSoup(html, "html.parser")

            # Search for the desired link based on its attributes and its file extension
            links = soup.find_all(
                "a", href=True, string="Download all data", class_="hidden"
            )

            csv_links = [
                link["href"] for link in links if link["href"].endswith(".csv")
            ]
            csv_link = csv_links[0] if csv_links else None

            # Extract and print the URL
            if csv_link:
                csv_link = f"https://missingmigrants.iom.int{csv_link}"
                print("CSV URL retrieved successfully from missingmigrants.iom.int")
            else:
                print("CSV URL not found")

            return csv_link

        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

    except requests.RequestException as exception:
        print(f"An error occurred: {exception}")
        return None


def get_data() -> pd.DataFrame:
    """
    Function to fetch the CSV file from the given URL and
    return a pandas DataFrame.
    """

    url = get_data_url()

    try:
        return pd.read_csv(url, parse_dates=["Website Date"])

    except ParserError as exception:
        print(f"An error occurred while parsing the CSV: {exception}")
        return None


def export_totals_to_json(data: pd.DataFrame) -> None:
    """
    Function to export the totals to a JSON file.
    """

    # Group by Region of Incident and sum the values
    totals = data.groupby("group")[["value"]].sum().reset_index().copy()

    # Add percentage column
    totals["pct"] = round(totals["value"] / totals["value"].sum() * 100, 2)

    # Add row with sum of all values
    totals.loc[len(totals)] = ["Total", totals["value"].sum(), 100]

    # Sort by value in descending order and set index
    totals = totals.sort_values("value", ascending=False).set_index("group")

    # Export data to json
    json_file = "src/data/data-migration-totals.json"
    totals.to_json(json_file, orient="index")

    print(f"Data with totals by region exported to {json_file}")


def export_data_to_json() -> None:
    """
    Function to export the data to a JSON file.
    """

    data_raw = get_data()

    if isinstance(data_raw, pd.DataFrame):
        num_rows = data_raw.shape[0]

        print(
            (
                "Data retrieved successfully: "
                f"DataFrame with {num_rows} rows. "
                f"Last date in dataset: {data_raw['Website Date'].max().strftime('%d-%m-%Y')}"
            )
        )

        # Define columns to use and rename them
        columns = {
            "Website Date": "date",
            "Incident ID": "id",
            "Region of Incident": "group",
            "Total Number of Dead and Missing": "value",
            "Region of Origin": "origin",
            "Migration route": "route",
            "Location of death": "location",
            "Information Source": "source",
            "Source Quality": "quality",
            "URL": "url",
            "Coordinates": "coords",
        }

        # Create new dataframe with selected columns
        data = data_raw[columns.keys()].dropna(subset=["Website Date"]).copy()

        # Rename columns
        data.columns = columns.values()

        # Export totals to json
        export_totals_to_json(data)

        # Drop rows without date
        data.dropna(subset=["date"], inplace=True)

        print(
            f"Removed {num_rows - data.shape[0]} rows without date, leaving {data.shape[0]} rows."
        )

        # Export data to json
        json_file = "src/data/data-migration-incidents.json"
        data.to_json(json_file, date_format="iso", orient="records")

        print(f"Data exported to {json_file}")


def main() -> None:
    """
    Main function.
    """

    export_data_to_json()


if __name__ == "__main__":
    main()

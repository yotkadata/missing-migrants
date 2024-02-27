"""
Python script to fetch data from the IOM website and 
preprocess it for use in the missing-migrants project.
"""

import json
from pathlib import Path

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
                print(csv_link)
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
        return pd.read_csv(url, parse_dates=["Incident Date"])

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

    # Make sure data directory exists
    Path("data").mkdir(parents=True, exist_ok=True)

    # Export data to json
    json_file = "data/data-migration-totals.json"
    totals.to_json(json_file, orient="index")

    print(f"Data with totals by region exported to {json_file}")


def export_thresholds_to_json(data: pd.DataFrame) -> None:
    """
    Function to export the thresholds to a JSON file.
    """

    # Resample "Total Number of Dead and Missing" by day
    resampled = data.groupby("date")[["value"]].sum().resample("D").sum().copy()

    # Add cumulative sum column
    resampled["cumsum"] = resampled.cumsum()

    # Find dates where the cumulative sum meets thresholds
    total = resampled["cumsum"].max()
    thresholds = {threshold: "" for threshold in range(10000, total + 1, 10000)}

    for threshold in thresholds:
        thresholds[threshold] = (
            resampled[resampled["cumsum"] >= threshold].index[0].strftime("%Y-%m-%d")
        )

    # Convert to dataframe
    thresholds = pd.DataFrame.from_dict(thresholds, orient="index").reset_index()
    thresholds.columns = ["threshold", "date"]

    # Make sure data directory exists
    Path("data").mkdir(parents=True, exist_ok=True)

    # Export data to json
    json_file = "data/data-migration-thresholds.json"
    thresholds.to_json(json_file, orient="records")

    print(f"Data with thresholds exported to {json_file}")


def export_yearly_to_json(data: pd.DataFrame) -> None:
    """
    Function to export the yearly totals by region to a JSON file.
    """

    yearly = data[["group", "date", "value"]].copy()
    yearly["year"] = yearly["date"].dt.year

    # Group by region and year
    yearly_grouped = yearly.groupby(["group", "year"])["value"].sum().reset_index()

    # Pivot the DataFrame to make "year" as columns
    df_pivot_by_group = yearly_grouped.pivot(
        index="group", columns="year", values="value"
    ).fillna(0)

    # Pivot the DataFrame to make "group" as columns
    df_pivot_by_year = yearly_grouped.pivot(
        index="year", columns="group", values="value"
    ).fillna(0)

    # Change column dtype to int
    df_pivot_by_group = df_pivot_by_group.astype(int)
    df_pivot_by_year = df_pivot_by_year.astype(int)

    # Make sure data directory exists
    Path("data").mkdir(parents=True, exist_ok=True)

    # Export data to json
    json_file = "data/data-migration-yearly-by-group.json"
    df_pivot_by_group.to_json(json_file, orient="index")
    print(f"Data with yearly values exported to {json_file}")

    json_file = "data/data-migration-yearly-by-year.json"
    df_pivot_by_year.to_json(json_file, orient="index")
    print(f"Data with yearly values exported to {json_file}")


def export_treemap_to_json(data: pd.DataFrame) -> None:
    """
    Function to export the treemap data to a JSON file.
    """

    yearly = data[["group", "date", "value"]].copy()
    yearly["year"] = yearly["date"].dt.year

    # Group by region and year
    df_yg = yearly.groupby(["group", "year"])["value"].sum().reset_index()

    # Calculate percentage of each year's total
    df_yg["pct"] = round(
        df_yg["value"] / df_yg.groupby("year")["value"].transform("sum"), 4
    )

    region_mapping = {
        "Africa": [
            "Eastern Africa",
            "Middle Africa",
            "Northern Africa",
            "Southern Africa",
            "Western Africa",
        ],
        "Americas": [
            "Caribbean",
            "Central America",
            "North America",
            "South America",
        ],
        "Asia": [
            "Central Asia",
            "Eastern Asia",
            "South-eastern Asia",
            "Southern Asia",
            "Western Asia",
        ],
        "Europe": [
            "Europe",
            "Mediterranean",
        ],
    }

    output = {"name": "treemap", "children": []}

    # Loop over each year in the dataframe
    for year in df_yg["year"].unique():
        year_data = {"name": str(year), "children": []}

        for region_group, sub_regions in region_mapping.items():
            region_group_data = {"name": region_group, "children": []}

            for sub_region in sub_regions:
                value = "0"
                pct = "0"

                # Check if the sub_region exists in the dataframe
                if sub_region in df_yg[df_yg["year"] == year]["group"].values:
                    value = (
                        df_yg.loc[
                            (df_yg["year"] == year) & (df_yg["group"] == sub_region)
                        ]["value"]
                        .values[0]
                        .astype(str)
                    )
                    pct = (
                        df_yg.loc[
                            (df_yg["year"] == year) & (df_yg["group"] == sub_region)
                        ]["pct"]
                        .values[0]
                        .astype(str)
                    )

                region_group_data["children"].append(
                    {
                        "name": sub_region,
                        "value": value,
                        "pct": pct,
                    }
                )

            # If there are any children (regions) added
            if region_group_data["children"]:
                year_data["children"].append(region_group_data)

        output["children"].append(year_data)

    # Make sure data directory exists
    Path("data").mkdir(parents=True, exist_ok=True)

    # Saving the constructed JSON structure to a file
    json_file = "data/data-migration-treemap.json"
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4)
    print(f"Data with treemap values exported to {json_file}")


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
                f"Last date in dataset: {data_raw['Incident Date'].max().strftime('%d-%m-%Y')}"
            )
        )

        # Define columns to use and rename them
        columns = {
            "Incident Date": "date",
            "Incident ID": "id",
            "Region of Incident": "group",
            "Total Number of Dead and Missing": "value",
            "Region of Origin": "origin",
            "Migration Route": "route",
            "Location of Incident": "location",
            "Information Source": "source",
            "Source Quality": "quality",
            "URL": "url",
            "Coordinates": "coords",
        }

        # Create new dataframe with selected columns
        data = data_raw[columns.keys()].dropna(subset=["Incident Date"]).copy()

        # Rename columns
        data.columns = columns.values()

        # Export totals to json
        export_totals_to_json(data)

        # Export thresholds to json
        export_thresholds_to_json(data)

        # Export yearly totals to json
        export_yearly_to_json(data)

        # Export treemap data to json
        export_treemap_to_json(data)

        # Drop rows without date
        data.dropna(subset=["date"], inplace=True)

        print(
            f"Removed {num_rows - data.shape[0]} rows without date, leaving {data.shape[0]} rows."
        )

        # Make sure data directory exists
        Path("data").mkdir(parents=True, exist_ok=True)

        # Export data to json
        json_file = "data/data-migration-incidents.json"
        data.to_json(json_file, date_format="iso", orient="records")

        print(f"Data exported to {json_file}")


def main() -> None:
    """
    Main function.
    """

    export_data_to_json()


if __name__ == "__main__":
    main()

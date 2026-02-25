import plotly.express as px
import pandas as pd

def create_sunburst_chart(summary_df, selected_zone=None, selected_year="All Years"):
    # Filter data based on selected zone and year
    filtered_df = summary_df.copy()

    if selected_zone:
        filtered_df = filtered_df[filtered_df["Zone"] == selected_zone]
    
    if selected_year != "All Years":
        filtered_df = filtered_df[filtered_df["Year"] == int(selected_year)]

    if filtered_df.empty:
        return px.sunburst().update_layout(
            title={
                'text': f"No data available for {selected_zone or 'all creeks'} in {selected_year}",
                'x': 0.5,  # Center the title
                'xanchor': 'center'
            },
            margin=dict(t=40, l=0, r=0, b=0)
        )

    # Target species to display explicitly
    target_species = ["laks", "havørred", "bækørred"]

    # Replace non-target species with "Other"
    filtered_df["Species"] = filtered_df["Species"].apply(
        lambda x: x if x in target_species else "Other"
    )

    # Aggregate the data for the sunburst chart
    aggregated_df = (
        filtered_df.groupby(["Species", "Fin Clip", "Bait"])["Fish Count"]
        .sum()
        .reset_index()
    )
    
    # Custom color mapping for species
    color_map = {
        "laks": "#FF6F61",  # Soft coral
        "havørred": "#6FA8DC",  # Sky blue
        "bækørred": "#AB82FF",  # Soft lavender
        "Other": "#DAA520"  # Sage green
    }

    # Create the sunburst chart
    fig = px.sunburst(
        aggregated_df,
        path=["Species", "Fin Clip", "Bait"],
        values="Fish Count",
        color="Species",
        color_discrete_map=color_map, 
        title=f"Fish Caught by Species, Fin Clip, and Bait"
    )

    # Update layout for better visualization
    fig.update_layout(
        margin=dict(t=40, l=0, r=0, b=0),
        title=dict(x=0.5, xanchor="center"),
        font=dict(
        family="Open Sans, Arial, sans-serif",  # Modern fonts
        size=14,  # Font size
        color="#4A4A4A"  # Font color
    ),
    )

    return fig







def create_histogram_top_catchers(summary_df, selected_zone=None, selected_year="All Years"):
    """
    Create a histogram showing the top 10 catchers based on total fish counts.
    """
    # Filter data based on selected zone and year
    filtered_df = summary_df.copy()

    if selected_zone:
        filtered_df = filtered_df[filtered_df["Zone"] == selected_zone]
    
    if selected_year != "All Years":
        filtered_df = filtered_df[filtered_df["Year"] == int(selected_year)]

    if filtered_df.empty:
        return px.bar().update_layout(
            title={
                'text': f"No data available for {selected_zone or 'all creeks'} in {selected_year}",
                'x': 0.5,  # Center the title
                'xanchor': 'center'
            },
            margin=dict(t=40, l=0, r=0, b=0)
        )
        
    # Target species to display explicitly
    target_species = ["laks", "havørred", "bækørred"]

    # Replace non-target species with "Other"
    filtered_df["Species"] = filtered_df["Species"].apply(
        lambda x: x if x in target_species else "Other"
    )
    
    # Aggregate fish counts by name and species
    aggregated_df = (
        filtered_df.groupby(["Name", "Species"])["Fish Count"]
        .sum()
        .reset_index()
    )

    # Aggregate total fish count per name for sorting
    total_counts = (
        aggregated_df.groupby("Name")["Fish Count"]
        .sum()
        .reset_index()
        .sort_values(by="Fish Count", ascending=False)
    )

    # Select the top 10 names by total count
    top_names = total_counts.head(10)["Name"]

    # Filter aggregated_df for only the top names
    top_catchers = aggregated_df[aggregated_df["Name"].isin(top_names)]

    # Custom color mapping for species
    color_map = {
        "laks": "#FF6F61",  # Soft coral
        "havørred": "#6FA8DC",  # Sky blue
        "bækørred": "#AB82FF",  # Soft lavender
        "Other": "#DAA520"  # Sage green
    }

    # Create the bar chart
    fig = px.bar(
        top_catchers,
        x="Name",
        y="Fish Count",
        color="Species",
        title=f"Top 10 Catchers",
        labels={"Name": "Angler", "Fish Count": "Number of Fish Caught"},
        color_discrete_map=color_map  # Apply custom colors
    )

    fig.update_layout(
        plot_bgcolor="white",  # Remove the gray background
        xaxis=dict(
            title=None,
            categoryorder="array",  # Use array order
            categoryarray=total_counts["Name"].values,
            showgrid=False  # Remove vertical gridlines
        ),
        yaxis=dict(
            showgrid=False  # Remove horizontal gridlines
        ),
        xaxis_title="Angler",
        yaxis_title="Total Fish Caught",
        margin=dict(t=40, l=0, r=0, b=0),
        title=dict(x=0.5, xanchor="center"),
        legend_title=None,
        
        font=dict(
        family="Open Sans, Arial, sans-serif",  # Modern fonts
        size=14,  # Font size
        color="#4A4A4A")  # Font color
    )



    return fig


def create_histogram_all_creeks_all_years(summary_df):
    """
    Create a histogram showing total fish counts for all creeks across all years,
    with species grouped into explicit categories including "Other."
    """
    # Start with a copy of the original DataFrame
    data = summary_df.copy()
    
    # Group data by year and species, and aggregate fish counts
    data = (
        data.groupby(['Year', 'Species'])['Fish Count']
        .sum()
        .reset_index()
    )
    data['Year'] = data['Year'].astype(str)  # Convert Year to string for consistency
    
    # Target species to display explicitly
    target_species = ["laks", "havørred", "bækørred"]

    # Replace non-target species with "Other"
    data["Species"] = data["Species"].apply(
        lambda x: x if x in target_species else "Other"
    )

    # Re-group data to combine all "Other" into a single category
    data = (
        data.groupby(['Year', 'Species'])['Fish Count']
        .sum()
        .reset_index()
    )
    
    # Custom color mapping for species
    color_map = {
        "laks": "#FF6F61",  # Soft coral
        "havørred": "#6FA8DC",  # Sky blue
        "bækørred": "#AB82FF",  # Soft lavender
        "Other": "#DAA520"  # 
    }

    # Create the bar chart
    fig = px.bar(
        data,
        x='Year',
        y='Fish Count',
        color='Species',
        color_discrete_map=color_map,
        title="Total Fish Caught in all Creeks all Years",
        text_auto=True  # Display values on top of bars
    )
    
    # Update Layout
    fig.update_layout(
        plot_bgcolor="white",  # Set background to white
        xaxis=dict(
            title=None,
            showgrid=False,
            tickangle=45,  # Rotate x-axis labels
            categoryorder="array",  # Explicitly define the year order
            categoryarray=sorted(data['Year'].unique(), key=int)  # Sort years numerically
        ),
        yaxis=dict(
            title="Total Fish Caught",
            showgrid=False
        ),
        margin=dict(t=40, l=0, r=0, b=0),
        title=dict(x=0.5, xanchor="center"),
        legend_title=None
    )

    return fig

def create_histogram_all_creeks_specific_year(summary_df, selected_year):
    """
    Create a histogram showing total fish counts for all creeks in a specific year,
    with monthly data.
    """
    
    # Start with a copy of the original DataFrame
    filtered_df = summary_df.copy()

    # Filter data for the specific year
    filtered = filtered_df[filtered_df['Year'] == int(selected_year)]

    # Check if the filtered data is empty
    if filtered.empty:
        return px.bar().update_layout(
            title={
                'text': f"No data available for all creeks in {selected_year}",
                'x': 0.5,  # Center the title
                'xanchor': 'center'
            },
            xaxis={'visible': False},  # Hide x-axis
            yaxis={'visible': False}   # Hide y-axis
        )

    # Group by month and sum the total fish caught
    data = filtered.groupby(['Month', 'Species'])['Fish Count'].sum().reset_index()

    # Ensure all months (1-12) are included
    all_months = pd.DataFrame({'Month': range(1, 13)})
    data = all_months.merge(data, on='Month', how='left').fillna({'Fish Count': 0, 'Species': 'Other'})

    # Map month numbers to names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    data['Month Name'] = data['Month'].map(month_names)

    # Target species to display explicitly
    target_species = ["laks", "havørred", "bækørred"]

    # Replace non-target species with "Other"
    data["Species"] = data["Species"].apply(
        lambda x: x if x in target_species else "Other"
    )

    # Re-group data to combine all "Other" into a single category
    data = data.groupby(['Month', 'Month Name', 'Species'])['Fish Count'].sum().reset_index()

    # Custom color mapping for species
    color_map = {
        "laks": "#FF6F61",  # Soft coral
        "havørred": "#6FA8DC",  # Sky blue
        "bækørred": "#AB82FF",  # Soft lavender
        "Other": "##DAA520"  # Sage green
    }

    # Create the bar chart
    fig = px.bar(
        data,
        x='Month Name',
        y='Fish Count',
        color='Species',
        color_discrete_map=color_map,
        title=f"Total Fish Caught Each Month in all Creeks",
        text_auto=True  # Display values on top of bars
    )

    # Update Layout for consistency with other figures
    fig.update_layout(
        plot_bgcolor="white",  # Set background to white
        xaxis=dict(
            title=None,
            showgrid=False,
            tickangle=45,  # Rotate x-axis labels
            categoryorder="array",  # Explicitly define the month order
            categoryarray=list(month_names.values())  # Use month names in correct order
        ),
        yaxis=dict(
            title="Total Fish Caught",
            showgrid=False
        ),
        font=dict(
            family="Open Sans, Arial, sans-serif",  # Modern, clean fonts
            size=14,  # Font size
            color="#4A4A4A"  # Dark grey font color
        ),
        margin=dict(t=40, l=0, r=0, b=0),
        title=dict(x=0.5, xanchor="center"),
        legend_title=None
    )

    return fig







def create_histogram_all_years(summary_df, selected_zone):
    """
    Create a histogram showing total fish counts for all years in a specific zone.
    """
    # Start with a copy of the original DataFrame
    filtered_df = summary_df.copy()
    
    if selected_zone is not None:
        # Normalize the selected zone
        selected_zone = selected_zone.strip().lower()

        # Filter data for the selected zone
        filtered_data = filtered_df[filtered_df['Zone'].str.lower() == selected_zone]

        # Check if filtered data is empty
        if filtered_data.empty:
            print(f"No data available for {selected_zone}")  # Debug message
            return px.bar().update_layout(
                title={
                    'text': f"No data available for {selected_zone}",
                    'x': 0.5,  # Center the title
                    'xanchor': 'center'
                },
                xaxis={'visible': False},  # Hide x-axis
                yaxis={'visible': False}   # Hide y-axis
            )
        
        # Group by year and sum the total fish caught
        data = (
            filtered_data.groupby(['Year', 'Species'])['Fish Count']  # Group by species as well
            .sum()
            .reset_index()
            .sort_values(by='Year', ascending=True)  # Sort by year
        )

        # Ensure no missing or invalid data
        data = data.dropna()

        # Convert Year to a string to ensure it is treated as categorical
        data['Year'] = data['Year'].astype(str)

        # Target species to display explicitly
        target_species = ["laks", "havørred", "bækørred"]

        # Replace non-target species with "Other"
        data["Species"] = data["Species"].apply(
            lambda x: x if x in target_species else "Other"
        )

        # Re-group data to combine all "Other" into a single category
        data = data.groupby(['Year', 'Species'])['Fish Count'].sum().reset_index()
        
        print("Total Fish Count in filtered_data:", filtered_data["Fish Count"].sum())
        print("Total Fish Count in final grouped data:", data["Fish Count"].sum())


        # Custom color mapping for species
        color_map = {
            "laks": "#FF6F61",  # Soft coral
            "havørred": "#6FA8DC",  # Sky blue
            "bækørred": "#AB82FF",  # Soft lavender
            "Other": "#DAA520"  # Sage green
        }

        # Create the bar chart
        hist = px.bar(
            data,
            x='Year',
            y='Fish Count',
            color='Species',
            color_discrete_map=color_map,
            title=f"Total Fish Caught Each Year",
            text_auto=True
        )

        # Update layout for better visuals
        hist.update_layout(
            plot_bgcolor="white",  # Set background to white
            xaxis=dict(
                title=None,
                showgrid=False,
                tickangle=45,  # Rotate x-axis labels
                categoryorder="array",  # Explicitly define the year order
                categoryarray=sorted(data['Year'].unique(), key=int)  # Sort years numerically
            ),
            yaxis=dict(
                title="Total Fish Caught",
                showgrid=False
            ),
            font=dict(
                family="Open Sans, Arial, sans-serif",  # Modern, clean fonts
                size=14,  # Font size
                color="#4A4A4A"  # Dark grey font color
            ),
            margin=dict(t=40, l=0, r=0, b=0),
            title=dict(x=0.5, xanchor="center"),
            legend_title=None
        )
        return hist
    
    # Return an empty histogram if no zone is selected
    return px.bar().update_layout(
        title={
            'text': "No Data Available",
            'x': 0.5,  # Center the title
            'xanchor': 'center'
        },
        xaxis={'visible': False},  # Hide x-axis
        yaxis={'visible': False}   # Hide y-axis
    )


def create_histogram_specific_year(summary_df, selected_zone, selected_year):
    """
    Create a histogram showing total fish counts for a specific year and zone,
    with monthly data.
    """
    # Ensure selected_zone is valid
    if selected_zone is not None:
        selected_zone = selected_zone.strip().lower()

    # Filter data for the selected zone
    filtered_data = summary_df[summary_df['Zone'].str.lower() == selected_zone]

    # Filter by year if a specific year is selected
    if selected_year and selected_year != "All Years":
        filtered_data = filtered_data[filtered_data['Year'] == int(selected_year)]

    # Check if the filtered data is empty
    if filtered_data.empty:
        print(f"No data available for {selected_zone} in {selected_year}")
        # Create an empty figure and set a placeholder title
        return px.bar().update_layout(
            title={
                'text': f"No data available for {selected_zone} in {selected_year}",
                'x': 0.5,  # Center the title
                'xanchor': 'center'
            },
            xaxis={'visible': False},  # Hide x-axis
            yaxis={'visible': False}   # Hide y-axis
        )

    # Group by month and sum the total fish caught
    data = filtered_data.groupby(['Month', 'Species'])['Fish Count'].sum().reset_index()

    # Ensure all months (1 to 12) are included, even if they have no data
    all_months = pd.DataFrame({'Month': range(1, 13)})
    data = all_months.merge(data, on='Month', how='left').fillna({'Fish Count': 0, 'Species': 'Other'})

    # Map numeric months to month names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    data['Month Name'] = data['Month'].map(month_names)

    # Target species to display explicitly
    target_species = ["laks", "havørred", "bækørred"]

    # Replace non-target species with "Other"
    data["Species"] = data["Species"].apply(
        lambda x: x if x in target_species else "Other"
    )

    # Re-group data to combine all "Other" into a single category
    data = data.groupby(['Month', 'Month Name', 'Species'])['Fish Count'].sum().reset_index()

    # Custom color mapping for species
    color_map = {
        "laks": "#FF6F61",  # Soft coral
        "havørred": "#6FA8DC",  # Sky blue
        "bækørred": "#AB82FF",  # Soft lavender
        "Other": "#DAA520"  # Sage green
    }

    # Create the bar chart
    hist = px.bar(
        data,
        x='Month Name',
        y='Fish Count',
        color='Species',
        color_discrete_map=color_map,
        title=f"Total Fish Caught Each Month",
        text_auto=True
    )

    # Update layout for consistent visuals
    hist.update_layout(
        plot_bgcolor="white",  # Set background to white
        xaxis=dict(
            title=None,
            showgrid=False,
            tickangle=45,  # Rotate x-axis labels
            categoryorder="array",  # Explicitly define the month order
            categoryarray=list(month_names.values())  # Ensure months are displayed in order
        ),
        yaxis=dict(
            title="Total Fish Caught",
            showgrid=False
        ),
        font=dict(
            family="Open Sans, Arial, sans-serif",  # Modern, clean fonts
            size=14,  # Font size
            color="#4A4A4A"  # Dark grey font color
        ),
        legend_title=None,
        margin=dict(t=40, l=0, r=0, b=0),
        title=dict(x=0.5, xanchor="center")  # Center the title
    )

    return hist



def create_stacked_area_chart(summary_df, selected_zone=None, selected_year="All Years"):
    """
    Create a stacked area chart showing fish species distribution.
    - Default: Shows data for all years and all zones.
    - Updates dynamically based on selected zone and year.
    - Ensures all months are displayed, even if no fish were caught.
    """
    # Filter the data
    filtered_df = summary_df.copy()
    
    if selected_zone:
        filtered_df = filtered_df[filtered_df["Zone"] == selected_zone]
    
    if selected_year != "All Years":
        filtered_df = filtered_df[filtered_df["Year"] == int(selected_year)]
    
    if filtered_df.empty:
        return px.area().update_layout(
            title={
                'text': f"No data available for {selected_zone or 'all creeks'} in {selected_year}",
                'x': 0.5, 'xanchor': 'center'
            },
            margin=dict(t=40, l=0, r=0, b=0)
        )

    # Aggregate data
    if selected_year != "All Years":
        # Group by Month for specific year
        filtered_df = (
            filtered_df.groupby(["Month", "Species"])["Fish Count"]
            .sum()
            .reset_index()
        )

        # Ensure all months (1-12) are present
        all_months = pd.DataFrame({"Month": range(1, 13)})  # Create a DataFrame for all months
        all_species = pd.DataFrame({"Species": filtered_df["Species"].unique()})  # Unique species
        all_combinations = (
            all_months.merge(all_species, how="cross")  # Cartesian product of months and species
        )

        # Merge with existing data and fill missing values with zeros
        filtered_df = (
            all_combinations.merge(filtered_df, on=["Month", "Species"], how="left")
            .fillna(0)
        )

        # Map numeric months to month names
        filtered_df["Month"] = filtered_df["Month"].map({
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        })
        x_column = "Month"
    else:
        # Group by Year for all years
        filtered_df = (
            filtered_df.groupby(["Year", "Species"])["Fish Count"]
            .sum()
            .reset_index()
        )
        x_column = "Year"

    # Custom color mapping for species
    color_map = {
        "laks": "#FF6F61",  # Soft coral
        "havørred": "#6FA8DC",  # Sky blue
        "bækørred": "#AB82FF"  # Soft lavender
        # Other species will use default Plotly colors
    }

    # Create the Stacked Area Chart
    fig = px.area(
        filtered_df,
        x=x_column,
        y="Fish Count",
        color="Species",
        labels={"Fish Count": "Number of Fish Caught"},
        color_discrete_map=color_map  # Apply custom colors for specific species
    )
    
    # Default visibility: Show only default species
    default_species = ["laks", "havørred", "bækørred"]
    fig.for_each_trace(lambda trace: trace.update(visible="legendonly") 
                       if trace.name not in default_species else None)
    
    # Update layout
    fig.update_layout(
        plot_bgcolor="white",
        xaxis=dict(
            title=None,
            tickangle=45
        ),
        yaxis_title="Number of Fish Caught",
        margin=dict(t=40, l=0, r=0, b=0),
        title=dict(x=0.5, xanchor="center"),
        legend_title=None,
        font=dict(
            family="Open Sans, Arial, sans-serif",  # Modern, clean fonts
            size=14,  # Font size
            color="#4A4A4A"  # Dark grey font color
        )
    )
    
    return fig




def create_violin_plot_length(summary_df, selected_zone=None, selected_year='All Years'):
    # Filter data based on selected zone and year
    filtered_df = summary_df.copy()

    if selected_zone:
        filtered_df = filtered_df[filtered_df["Zone"] == selected_zone]
    
    if selected_year != "All Years":
        filtered_df = filtered_df[filtered_df["Year"] == int(selected_year)]
        
    # Define target species to show by default
    default_species = ["laks", "havørred", "bækørred"]

    if filtered_df.empty:
        return px.violin().update_layout(
            title={
                'text': f"No data available for {selected_zone or 'all creeks'} in {selected_year}",
                'x': 0.5,  # Center the title
                'xanchor': 'center'
            },
            margin=dict(t=40, l=0, r=0, b=0)
        )  
        
    # Custom color mapping for species
    color_map = {
        "laks": "#FF6F61",  # Soft coral
        "havørred": "#6FA8DC",  # Sky blue
        "bækørred": "#AB82FF"  # Soft lavender
        # Other species will use default Plotly colors
    }

    # Create the violin plot with all species
    fig = px.violin(
        filtered_df,
        y='Length',
        x='Species',
        color='Species',
        box=True,
        color_discrete_map=color_map
    )
    
    fig.update_layout(
        plot_bgcolor="white",
        xaxis=dict(
            title=None,  # Remove x-axis title
            tickangle=45  # Rotate tick labels
        ),
        yaxis=dict(
            title = 'Length (cm)'
        ),
        legend_title=None,
        font=dict(
            family="Open Sans, Arial, sans-serif",  # Modern fonts
            size=14,  # Font size
            color="#4A4A4A"  # Font color
        )
    )


    # Hide all species except the default ones
    fig.for_each_trace(lambda trace: trace.update(visible="legendonly") 
                       if trace.name not in default_species else None)
    

    return fig

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
file_path = 'Sample_Company_Sustainability_Metrics_Dataset.csv'
data = pd.read_csv(file_path)

# Rename columns if needed for consistency
data = data.rename(columns={
    'Local Business Engagement Rate': 'Local Business Engagement Rate (%)',
    'Remote Worker Attraction Rate': 'Remote Worker Attraction Rate (%)',
    'Waste Development Rate': 'Waste Development Rate (tons/year)',
    'Emission Rate of Pollutant per kg': 'Emission Rate of Pollutant (kg)',
    'Regenerating High Value Material': 'Regenerating High Value Material (%)',
    'Extend Product Life': 'Extend Product Life (years)',
    'Share, Resale': 'Share/Resale Rate (%)',
    'Circular Credibility': 'Circular Credibility Score',
    'Value of Waste': 'Value of Waste (EUR)'
})

# Convert columns to percentages if needed
data['Local Business Engagement Rate (%)'] *= 100
data['Remote Worker Attraction Rate (%)'] *= 100
data['End of Life Score'] *= 100
data['Circular Credibility Score'] *= 100

# Define weights for each metric (customize these based on importance)
weights = {
    'Sustainability Impact Score': 0.15,
    'Local Business Engagement Rate (%)': 0.10,
    'Remote Worker Attraction Rate (%)': 0.10,
    'Waste Development Rate (tons/year)': -0.10,  # Negative weight as lower waste is better
    'Emission Rate of Pollutant (kg)': -0.15,      # Negative weight as lower emissions are better
    'Regenerating High Value Material (%)': 0.10,
    'Extend Product Life (years)': 0.10,
    'Share/Resale Rate (%)': 0.05,
    'End of Life Score': 0.05,
    'Circular Credibility Score': 0.10,
    'Value of Waste (EUR)': 0.10
}

# Calculate the weighted score for each company
data['Sustainability Score'] = (
    data['Sustainability Impact Score'] * weights['Sustainability Impact Score'] +
    data['Local Business Engagement Rate (%)'] * weights['Local Business Engagement Rate (%)'] +
    data['Remote Worker Attraction Rate (%)'] * weights['Remote Worker Attraction Rate (%)'] +
    data['Waste Development Rate (tons/year)'] * weights['Waste Development Rate (tons/year)'] +
    data['Emission Rate of Pollutant (kg)'] * weights['Emission Rate of Pollutant (kg)'] +
    data['Regenerating High Value Material (%)'] * weights['Regenerating High Value Material (%)'] +
    data['Extend Product Life (years)'] * weights['Extend Product Life (years)'] +
    data['Share/Resale Rate (%)'] * weights['Share/Resale Rate (%)'] +
    data['End of Life Score'] * weights['End of Life Score'] +
    data['Circular Credibility Score'] * weights['Circular Credibility Score'] +
    data['Value of Waste (EUR)'] * weights['Value of Waste (EUR)']
)

# Streamlit interface
st.title("Filter In! Jobs In!")
st.write("This app ranks companies based on an overall sustainability score calculated from various metrics.")

# SIS Range Filter in Sidebar
st.sidebar.header("Set Sustainability Score (SIS) Range")
min_sis = st.sidebar.slider("Minimum SIS", float(data['Sustainability Score'].min()), float(data['Sustainability Score'].min()), float(data['Sustainability Score'].max()))
max_sis = st.sidebar.slider("Maximum SIS", float(data['Sustainability Score'].min()), float(data['Sustainability Score'].max()), float(data['Sustainability Score'].max()))

# Filter companies within the selected SIS range
filtered_data = data[(data['Sustainability Score'] >= min_sis) & (data['Sustainability Score'] <= max_sis)]
filtered_data = filtered_data.sort_values(by='Sustainability Score', ascending=False)

# Display qualifying companies based on SIS threshold
st.subheader("Qualifying Companies")
if not filtered_data.empty:
    st.success("Ready for some current success? These companies are ready to flow into our county’s spotlight!")
    st.table(filtered_data[['Company', 'Sustainability Score']])
    
    # Bar chart for qualifying companies
    #st.subheader("Sustainability Score for Qualifying Companies")
    #fig, ax = plt.subplots(figsize=(10, 6))
    #sns.barplot(x='Sustainability Score', y='Company', data=filtered_data, ax=ax, palette='viridis')
    #ax.set_title("Sustainability Score for Companies within Selected Range")
    #ax.set_xlabel("Sustainability Score")
    #ax.set_ylabel("Company")
    #st.pyplot(fig)
else:
    st.warning("Looks like we’re in a bit of a sustainability drought—let's water those thresholds and try again!")

# Detailed information section
st.subheader("View Detailed Company Information")
selected_company = st.selectbox("Select a Company for Details", data['Company'].unique())

# Display detailed information for the selected company
company_details = data[data['Company'] == selected_company]

if not company_details.empty:
    st.write(f"**Detailed Metrics for {selected_company}**")
    st.table(company_details.T)  # Transpose for readability in Streamlit
else:
    st.warning("No data available for the selected company.")

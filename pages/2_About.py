import streamlit as st
st.set_page_config(page_title="Crop Production Statistics Informtion System", page_icon="🌐", layout="wide")
st.header('About Us')

st.subheader("Crop Production Statistics Informtion System")

st.markdown("""Welcome to the Crop Production Statistics Information System, your comprehensive platform for accessing vital agricultural data. Our application is designed to provide users with accurate and up-to-date information on crop production statistics, enabling informed decision-making and promoting sustainable agricultural practices.

Mission:
Our mission is to empower farmers, policymakers, researchers, and stakeholders with reliable crop production statistics to enhance productivity, food security, and economic growth in the agricultural sector.

Features:

Data Accessibility: Access a wide range of crop production statistics including yields, acreage, production trends, and more.

User-Friendly Interface: Our intuitive interface ensures ease of navigation and seamless access to essential information for users of all levels.

Real-Time Updates: Stay informed with real-time updates on crop production statistics, ensuring you have the latest information at your fingertips.

Data Visualization: Visualize data through charts, graphs, and maps, facilitating clear understanding and analysis of agricultural trends.

Data Integrity: Rest assured knowing that our platform prioritizes data integrity and accuracy, sourcing information from reputable sources and utilizing rigorous validation processes.""")


st.header('Contact Us')

st.markdown("""We welcome your feedback, inquiries, and suggestions. For assistance or further information, please contact our dedicated support team at [sanketgondaliya6@gmail.com].

Thank you for choosing the Crop Production Statistics Information System. Together, let's harness the power of data to drive agricultural innovation and prosperity.""")

st.header('Designed and Developed by')

 	
st.markdown("""Sanket Patel,  M.Sc. (Agriculture Analytics), Student of Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT),  DA-IICT Road,
Gandhinagar 382 007, Gujarat(India)""")

if st.button("Click to Main Page"):
    st.switch_page("3_main.py")
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

current_date = datetime.now().strftime("%y%m%d")

st.title('Djoli Commandes J+1')

st.write('\n')
st.write('**Récap J+1 et Liste Achats**')
df = st.file_uploader('Importer les commandes Ecwid')
if df is not None:
    df2 = pd.read_csv(df, sep=';')
    df2['options'] = df2['options'].str.replace(r'Taille:|Mûrissement:|Tiges:|Feuilles:', '', regex=True).str.strip()
    df2['options'] = df2['options'].str.replace('\n', ' ', regex=True)
    df2 = df2.sort_values('Zones')

    def order_list(orders_df):
        order_numbers = list(orders_df['order_number'].unique())

        output_content = ""
        output_content += "\n\n"
    
        for order_number in order_numbers:
            output_content += f"DJOLI COTE D'IVOIRE\n"
            output_content += "\n\n"
            output_content += f"{order_number}\n"
            output_content += "\n\n"

            # Filter the DataFrame for the current order
            current_order = orders_df[orders_df['order_number'] == order_number]

            restaurant_name = current_order['Nom des Restaurants'].iloc[0]
            output_content += f"Client: {restaurant_name}\n"
            output_content += "\n\n"

            zone = current_order['Zones'].iloc[0]
            output_content += f"{zone}\n"
            
            pickup_date = current_order['pickup_time'].iloc[0]
            output_content += f"HL: {pickup_date}\n\n"

            order_total = current_order['order_total'].iloc[0]
            output_content += f"Total: {order_total}\n\n"
            output_content += "\n\n"

            for index, row in current_order.iterrows():
                if not pd.isna(row['options']):
                    output_content += f"{row['name']} {row['options']} : {row['quantity']}\n"
                else:
                    output_content += f"{row['name']} : {row['quantity']}\n"

            output_content += "\n\n"
            output_content += "\n\n"

        return output_content


    def purchase_list(orders_df):

        liste_achat = orders_df.fillna('NA').groupby(['name', 'options']).sum(['quantity'])
        liste_achat_html = liste_achat[['quantity']].to_html()
        return liste_achat_html

    # Generate the content for the file
    file_content = order_list(df2)
    purchase_content = purchase_list(df2)

    # Provide a download link
    recap_file_name = f"recap_{current_date}.txt"
    st.download_button(label="Télécharger le récap",
                    data=file_content,
                    file_name = recap_file_name,
                    key='recap_button')
    
    purchase_file_name = f"achats_{current_date}.html"
    st.download_button(label="Télécharger la liste des achats",
                    data=purchase_content,
                    file_name = purchase_file_name,
                    key='purchase_button')

else:
    st.info("Veuillez télécharger un fichier CSV.")


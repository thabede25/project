import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from IPython.display import display, HTML
import os
from datetime import datetime

# Data dictionaries
users_data = {
    'A8350': {'password': 'tau644', 'role': 'Administrator'},
    'A2195': {'password': 'peace582', 'role': 'Administrator'},
    'I4638': {'password': 'light573', 'role': 'Investor'},
    'R7563': {'password': 'mfundo913', 'role': 'Researcher'}
}

production_data = [
    {'StatID': 1, 'Year': 2023, 'CountryID': 1, 'MineralID': 1, 'Production_tonnes': 100000, 'ExportValue_BillionUSD': 5.2},
    {'StatID': 2, 'Year': 2023, 'CountryID': 2, 'MineralID': 2, 'Production_tonnes': 120000, 'ExportValue_BillionUSD': 6.4},
    {'StatID': 3, 'Year': 2023, 'CountryID': 3, 'MineralID': 3, 'Production_tonnes': 50000, 'ExportValue_BillionUSD': 2.41},
    {'StatID': 4, 'Year': 2023, 'CountryID': 4, 'MineralID': 4, 'Production_tonnes': 200000, 'ExportValue_BillionUSD': 10},
    {'StatID': 5, 'Year': 2024, 'CountryID': 1, 'MineralID': 1, 'Production_tonnes': 110000, 'ExportValue_BillionUSD': 6.13},
    {'StatID': 6, 'Year': 2024, 'CountryID': 2, 'MineralID': 2, 'Production_tonnes': 130000, 'ExportValue_BillionUSD': 7.25},
    {'StatID': 7, 'Year': 2024, 'CountryID': 3, 'MineralID': 3, 'Production_tonnes': 200000, 'ExportValue_BillionUSD': 10.5},
    {'StatID': 8, 'Year': 2024, 'CountryID': 4, 'MineralID': 4, 'Production_tonnes': 210000, 'ExportValue_BillionUSD': 11}
]

minerals_data = [
    {'MineralID': 1, 'MineralName': 'Cobalt', 'Description': 'Used in batteries and alloys', 'MarketPriceUSD_per_tonne': 52000},
    {'MineralID': 2, 'MineralName': 'Lithium', 'Description': 'Essential for EV batteries', 'MarketPriceUSD_per_tonne': 70000},
    {'MineralID': 3, 'MineralName': 'Graphite', 'Description': 'Used in batteries and lubricants', 'MarketPriceUSD_per_tonne': 800},
    {'MineralID': 4, 'MineralName': 'Manganese', 'Description': 'Used in steel production', 'MarketPriceUSD_per_tonne': 2200}
]

countries_data = [
    {'CountryID': 1, 'CountryName': 'DRC (Congo)', 'GDP_BillionUSD': 55, 'MiningRevenue_BillionUSD': 12, 'KeyProjects': 'Cobalt expansion in Kolwezi'},
    {'CountryID': 2, 'CountryName': 'South Africa', 'GDP_BillionUSD': 350, 'MiningRevenue_BillionUSD': 25, 'KeyProjects': 'Bushveld Lithium Project'},
    {'CountryID': 3, 'CountryName': 'Mozambique', 'GDP_BillionUSD': 20, 'MiningRevenue_BillionUSD': 4, 'KeyProjects': 'Balama Graphite Project'},
    {'CountryID': 4, 'CountryName': 'Namibia', 'GDP_BillionUSD': 15, 'MiningRevenue_BillionUSD': 3, 'KeyProjects': 'Otjozondu Manganese Project'}
]

sites_data = [
    {'SiteID': 1, 'SiteName': 'Kolwezi Mine', 'CountryID': 1, 'MineralID': 1, 'Latitude': -10.7167, 'Longitude': 25.4667, 'Production_tonnes': 100000},
    {'SiteID': 2, 'SiteName': 'Greenbushes Lithium', 'CountryID': 2, 'MineralID': 2, 'Latitude': -33.8667, 'Longitude': 116.0667, 'Production_tonnes': 120000},
    {'SiteID': 3, 'SiteName': 'Balama Graphite', 'CountryID': 3, 'MineralID': 3, 'Latitude': -13.3333, 'Longitude': 38.7667, 'Production_tonnes': 50000},
    {'SiteID': 4, 'SiteName': 'Kalahari Manganese', 'CountryID': 4, 'MineralID': 4, 'Latitude': -27.0833, 'Longitude': 22.95, 'Production_tonnes': 200000}
]

insights_data = []  # Initially empty

# Save functions
def save_users(df):
    try:
        df.to_excel('Users.xlsx', index=False)
    except Exception as e:
        print(f"Error saving users: {e}")

def save_insights(df):
    try:
        df.to_csv('insights.csv', index=False)
    except Exception as e:
        print(f"Error saving insights: {e}")

# Authentication
def authenticate(username, password, users):
    if username in users and users[username]['password'] == password:
        return users[username]['role']
    return None

# Tkinter GUI Application
class CriticalMineralsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("African Critical Minerals App")
        self.root.geometry("800x600")
        
        # Convert dictionaries to DataFrames
        self.users = users_data
        self.user_df = pd.DataFrame([{'Role': v['role'], 'Username': k, 'Password': v['password']} for k, v in users_data.items()])
        self.mineral_df = pd.DataFrame(minerals_data)
        self.country_df = pd.DataFrame(countries_data)
        self.production_df = pd.DataFrame(production_data)
        self.sites_df = pd.DataFrame(sites_data)
        self.insights_df = pd.DataFrame(insights_data, columns=['Username', 'Insight', 'Timestamp', 'MineralID', 'CountryID'])
        
        self.show_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to the African Critical Minerals App", font=("Arial", 16), fg="blue").pack(pady=20)
        tk.Label(self.root, text="Username:", font=("Arial", 12)).pack()
        self.username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.username_entry.pack(pady=5)
        tk.Label(self.root, text="Password:", font=("Arial", 12)).pack()
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login, font=("Arial", 12), bg="green", fg="white").pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.destroy, font=("Arial", 12), bg="red", fg="white").pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = authenticate(username, password, self.users)
        if role:
            self.username = username
            self.role = role
            if role == 'Administrator':
                self.show_admin_menu()
            elif role == 'Investor':
                self.show_investor_menu()
            elif role == 'Researcher':
                self.show_researcher_menu()
            else:
                messagebox.showerror("Error", "Unknown role.")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def show_admin_menu(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Admin Dashboard - {self.username}", font=("Arial", 14), fg="blue").pack(pady=10)
        tk.Button(self.root, text="1. Manage Users", command=self.admin_manage_users, font=("Arial", 12), bg="lightblue").pack(pady=5, fill="x")
        tk.Button(self.root, text="2. Edit/Delete Data", command=self.admin_edit_data, font=("Arial", 12), bg="lightblue").pack(pady=5, fill="x")
        tk.Button(self.root, text="3. View Data", command=self.view_data, font=("Arial", 12), bg="lightblue").pack(pady=5, fill="x")
        tk.Button(self.root, text="4. View Interactive Map", command=self.view_interactive_map, font=("Arial", 12), bg="lightblue").pack(pady=5, fill="x")
        tk.Button(self.root, text="5. View Insights", command=self.view_insights, font=("Arial", 12), bg="lightblue").pack(pady=5, fill="x")
        tk.Button(self.root, text="6. Logout", command=self.show_login_screen, font=("Arial", 12), bg="red", fg="white").pack(pady=5, fill="x")

    def show_investor_menu(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Investor Dashboard - {self.username}", font=("Arial", 14), fg="blue").pack(pady=10)
        tk.Button(self.root, text="1. View Country Profiles", command=self.view_country_profiles, font=("Arial", 12), bg="lightgreen").pack(pady=5, fill="x")
        tk.Button(self.root, text="2. View Charts", command=self.view_charts, font=("Arial", 12), bg="lightgreen").pack(pady=5, fill="x")
        tk.Button(self.root, text="3. View Exports/Production", command=self.view_data, font=("Arial", 12), bg="lightgreen").pack(pady=5, fill="x")
        tk.Button(self.root, text="4. View Interactive Map", command=self.view_interactive_map, font=("Arial", 12), bg="lightgreen").pack(pady=5, fill="x")
        tk.Button(self.root, text="5. View Insights", command=self.view_insights, font=("Arial", 12), bg="lightgreen").pack(pady=5, fill="x")
        tk.Button(self.root, text="6. Logout", command=self.show_login_screen, font=("Arial", 12), bg="red", fg="white").pack(pady=5, fill="x")

    def show_researcher_menu(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Researcher Dashboard - {self.username}", font=("Arial", 14), fg="blue").pack(pady=10)
        tk.Button(self.root, text="1. View Mineral/Country Data", command=self.view_data, font=("Arial", 12), bg="lightyellow").pack(pady=5, fill="x")
        tk.Button(self.root, text="2. Export Data", command=self.export_data, font=("Arial", 12), bg="lightyellow").pack(pady=5, fill="x")
        tk.Button(self.root, text="3. Add Insights", command=self.add_insights, font=("Arial", 12), bg="lightyellow").pack(pady=5, fill="x")
        tk.Button(self.root, text="4. View Interactive Map", command=self.view_interactive_map, font=("Arial", 12), bg="lightyellow").pack(pady=5, fill="x")
        tk.Button(self.root, text="5. View Insights", command=self.view_insights, font=("Arial", 12), bg="lightyellow").pack(pady=5, fill="x")
        tk.Button(self.root, text="6. Logout", command=self.show_login_screen, font=("Arial", 12), bg="red", fg="white").pack(pady=5, fill="x")

    def admin_manage_users(self):
        self.clear_screen()
        tk.Label(self.root, text="Manage Users", font=("Arial", 14), fg="blue").pack(pady=10)

        # Add User
        tk.Label(self.root, text="Add User", font=("Arial", 12)).pack()
        tk.Label(self.root, text="Username:", font=("Arial", 12)).pack()
        new_username = tk.Entry(self.root, font=("Arial", 12))
        new_username.pack(pady=5)
        tk.Label(self.root, text="Password:", font=("Arial", 12)).pack()
        new_password = tk.Entry(self.root, show="*", font=("Arial", 12))
        new_password.pack(pady=5)
        tk.Label(self.root, text="Role:", font=("Arial", 12)).pack()
        new_role = ttk.Combobox(self.root, values=['Administrator', 'Investor', 'Researcher'], font=("Arial", 12))
        new_role.pack(pady=5)
        tk.Button(self.root, text="Add", command=lambda: self.add_user(new_username.get(), new_password.get(), new_role.get()), font=("Arial", 12), bg="green", fg="white").pack(pady=5)

        # Edit/Delete User
        tk.Label(self.root, text="Edit/Delete User", font=("Arial", 12)).pack()
        tk.Label(self.root, text="Username:", font=("Arial", 12)).pack()
        edit_username = tk.Entry(self.root, font=("Arial", 12))
        edit_username.pack(pady=5)
        tk.Label(self.root, text="New Password (optional):", font=("Arial", 12)).pack()
        edit_password = tk.Entry(self.root, show="*", font=("Arial", 12))
        edit_password.pack(pady=5)
        tk.Label(self.root, text="New Role (optional):", font=("Arial", 12)).pack()
        edit_role = ttk.Combobox(self.root, values=['Administrator', 'Investor', 'Researcher'], font=("Arial", 12))
        edit_role.pack(pady=5)
        tk.Button(self.root, text="Edit", command=lambda: self.edit_user(edit_username.get(), edit_password.get(), edit_role.get()), font=("Arial", 12), bg="blue", fg="white").pack(pady=5)
        tk.Button(self.root, text="Delete", command=lambda: self.delete_user(edit_username.get()), font=("Arial", 12), bg="red", fg="white").pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_admin_menu, font=("Arial", 12), bg="grey", fg="white").pack(pady=5)

    def add_user(self, username, password, role):
        if not username or not password or not role:
            messagebox.showerror("Error", "All fields are required.")
            return
        if role not in ['Administrator', 'Investor', 'Researcher']:
            messagebox.showerror("Error", "Invalid role.")
            return
        if username in self.users:
            messagebox.showerror("Error", "Username already exists.")
            return
        self.users[username] = {'password': password, 'role': role}
        self.user_df = pd.concat([self.user_df, pd.DataFrame({'Role': [role], 'Username': [username], 'Password': [password]})], ignore_index=True)
        save_users(self.user_df)
        messagebox.showinfo("Success", "User added.")

    def edit_user(self, username, password, role):
        if username not in self.users:
            messagebox.showerror("Error", "User not found.")
            return
        if password:
            self.users[username]['password'] = password
            self.user_df.loc[self.user_df['Username'] == username, 'Password'] = password
        if role in ['Administrator', 'Investor', 'Researcher']:
            self.users[username]['role'] = role
            self.user_df.loc[self.user_df['Username'] == username, 'Role'] = role
        save_users(self.user_df)
        messagebox.showinfo("Success", "User edited.")

    def delete_user(self, username):
        if username not in self.users:
            messagebox.showerror("Error", "User not found.")
            return
        del self.users[username]
        self.user_df = self.user_df[self.user_df['Username'] != username]
        save_users(self.user_df)
        messagebox.showinfo("Success", "User deleted.")

    def admin_edit_data(self):
        self.clear_screen()
        tk.Label(self.root, text="Edit/Delete Data", font=("Arial", 14), fg="blue").pack(pady=10)
        tk.Label(self.root, text="Data Type:", font=("Arial", 12)).pack()
        data_type = ttk.Combobox(self.root, values=['Mineral', 'Country', 'Production'], font=("Arial", 12))
        data_type.pack(pady=5)
        tk.Label(self.root, text="ID:", font=("Arial", 12)).pack()
        data_id = tk.Entry(self.root, font=("Arial", 12))
        data_id.pack(pady=5)
        tk.Label(self.root, text="New Value (e.g., Price for Mineral, GDP for Country, Production for Stat):", font=("Arial", 12)).pack()
        new_value = tk.Entry(self.root, font=("Arial", 12))
        new_value.pack(pady=5)
        tk.Button(self.root, text="Edit", command=lambda: self.edit_data(data_type.get(), data_id.get(), new_value.get()), font=("Arial", 12), bg="blue", fg="white").pack(pady=5)
        tk.Button(self.root, text="Delete", command=lambda: self.delete_data(data_type.get(), data_id.get()), font=("Arial", 12), bg="red", fg="white").pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_admin_menu, font=("Arial", 12), bg="grey", fg="white").pack(pady=5)

    def edit_data(self, data_type, data_id, new_value):
        try:
            data_id = int(data_id)
            if data_type == 'Mineral':
                if not self.mineral_df[self.mineral_df['MineralID'] == data_id].empty:
                    if new_value:
                        self.mineral_df.loc[self.mineral_df['MineralID'] == data_id, 'MarketPriceUSD_per_tonne'] = float(new_value)
                        messagebox.showinfo("Success", "Mineral updated.")
                    else:
                        messagebox.showerror("Error", "New value required.")
                else:
                    messagebox.showerror("Error", "MineralID not found.")
            elif data_type == 'Country':
                if not self.country_df[self.country_df['CountryID'] == data_id].empty:
                    if new_value:
                        self.country_df.loc[self.country_df['CountryID'] == data_id, 'GDP_BillionUSD'] = float(new_value)
                        messagebox.showinfo("Success", "Country updated.")
                    else:
                        messagebox.showerror("Error", "New value required.")
                else:
                    messagebox.showerror("Error", "CountryID not found.")
            elif data_type == 'Production':
                if not self.production_df[self.production_df['StatID'] == data_id].empty:
                    if new_value:
                        self.production_df.loc[self.production_df['StatID'] == data_id, 'Production_tonnes'] = float(new_value)
                        messagebox.showinfo("Success", "Production updated.")
                    else:
                        messagebox.showerror("Error", "New value required.")
                else:
                    messagebox.showerror("Error", "StatID not found.")
            else:
                messagebox.showerror("Error", "Invalid data type.")
        except ValueError:
            messagebox.showerror("Error", "Invalid ID or value.")

    def delete_data(self, data_type, data_id):
        try:
            data_id = int(data_id)
            if data_type == 'Mineral':
                if not self.mineral_df[self.mineral_df['MineralID'] == data_id].empty:
                    self.mineral_df = self.mineral_df[self.mineral_df['MineralID'] != data_id]
                    messagebox.showinfo("Success", "Mineral deleted.")
                else:
                    messagebox.showerror("Error", "MineralID not found.")
            elif data_type == 'Country':
                if not self.country_df[self.country_df['CountryID'] == data_id].empty:
                    self.country_df = self.country_df[self.country_df['CountryID'] != data_id]
                    messagebox.showinfo("Success", "Country deleted.")
                else:
                    messagebox.showerror("Error", "CountryID not found.")
            elif data_type == 'Production':
                if not self.production_df[self.production_df['StatID'] == data_id].empty:
                    self.production_df = self.production_df[self.production_df['StatID'] != data_id]
                    messagebox.showinfo("Success", "Production deleted.")
                else:
                    messagebox.showerror("Error", "StatID not found.")
            else:
                messagebox.showerror("Error", "Invalid data type.")
        except ValueError:
            messagebox.showerror("Error", "Invalid ID.")

    def view_country_profiles(self):
        self.clear_screen()
        tk.Label(self.root, text="Country Profiles", font=("Arial", 14), fg="blue").pack(pady=10)
        tk.Label(self.root, text="Select Country:", font=("Arial", 12)).pack()
        country = ttk.Combobox(self.root, values=self.country_df['CountryName'].tolist(), font=("Arial", 12))
        country.pack(pady=5)
        text = tk.Text(self.root, height=15, width=80, font=("Arial", 10))
        text.pack(pady=5)
        tk.Button(self.root, text="View", command=lambda: self.display_country_profile(country.get(), text), font=("Arial", 12), bg="green", fg="white").pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_menu_by_role, font=("Arial", 12), bg="grey", fg="white").pack(pady=5)

    def display_country_profile(self, country_name, text):
        text.delete(1.0, tk.END)
        country_row = self.country_df[self.country_df['CountryName'].str.lower() == country_name.lower()]
        if not country_row.empty:
            country_id = country_row['CountryID'].iloc[0]
            text.insert(tk.END, f"{country_name} Profile:\n")
            text.insert(tk.END, f"GDP: {country_row['GDP_BillionUSD'].iloc[0]} Billion USD\n")
            text.insert(tk.END, f"Mining Revenue: {country_row['MiningRevenue_BillionUSD'].iloc[0]} Billion USD\n")
            text.insert(tk.END, f"Key Projects: {country_row['KeyProjects'].iloc[0]}\n")
            prod_data = self.production_df[self.production_df['CountryID'] == country_id]
            if not prod_data.empty:
                text.insert(tk.END, "\nProduction Data:\n")
                for _, row in prod_data.iterrows():
                    mineral = self.mineral_df[self.mineral_df['MineralID'] == row['MineralID']]['MineralName'].iloc[0]
                    text.insert(tk.END, f"Year {row['Year']}: {mineral} - {row['Production_tonnes']} tonnes, Export: ${row['ExportValue_BillionUSD']}B\n")
        else:
            messagebox.showerror("Error", "Country not found.")

    def view_charts(self):
        self.clear_screen()
        tk.Label(self.root, text="View Charts", font=("Arial", 14), fg="blue").pack(pady=10)
        tk.Label(self.root, text="Select Mineral:", font=("Arial", 12)).pack()
        mineral = ttk.Combobox(self.root, values=self.mineral_df['MineralName'].tolist(), font=("Arial", 12))
        mineral.pack(pady=5)
        tk.Label(self.root, text="Chart Type:", font=("Arial", 12)).pack()
        chart_type = ttk.Combobox(self.root, values=['Production Trends', 'Export Value Trends'], font=("Arial", 12))
        chart_type.pack(pady=5)
        tk.Button(self.root, text="Generate Chart", command=lambda: self.generate_chart(mineral.get(), chart_type.get()), font=("Arial", 12), bg="green", fg="white").pack(pady=5)
        self.chart_label = tk.Label(self.root)
        self.chart_label.pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_menu_by_role, font=("Arial", 12), bg="grey", fg="white").pack(pady=5)

    def generate_chart(self, mineral_name, chart_type):
        mineral_row = self.mineral_df[self.mineral_df['MineralName'].str.lower() == mineral_name.lower()]
        if not mineral_row.empty:
            mineral_id = mineral_row['MineralID'].iloc[0]
            prod_data = self.production_df[self.production_df['MineralID'] == mineral_id]
            if not prod_data.empty:
                prod_data = prod_data.merge(self.country_df[['CountryID', 'CountryName']], on='CountryID')
                if chart_type == 'Production Trends':
                    fig = px.line(prod_data, x='Year', y='Production_tonnes', color='CountryName', title=f'{mineral_name} Production Trends')
                elif chart_type == 'Export Value Trends':
                    fig = px.line(prod_data, x='Year', y='ExportValue_BillionUSD', color='CountryName', title=f'{mineral_name} Export Value Trends')
                else:
                    messagebox.showerror("Error", "Invalid chart type.")
                    return
                fig.write_to_file("chart.png")
                img = Image.open("chart.png")
                img = img.resize((600, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.chart_label.configure(image=photo)
                self.chart_label.image = photo
            else:
                messagebox.showerror("Error", "No production data for this mineral.")
        else:
            messagebox.showerror("Error", "Mineral not found.")

    def view_data(self):
        self.clear_screen()
        tk.Label(self.root, text="View Data", font=("Arial", 14), fg="blue").pack(pady=10)
        tk.Label(self.root, text="Data Type:", font=("Arial", 12)).pack()
        data_type = ttk.Combobox(self.root, values=['Mineral', 'Country'], font=("Arial", 12))
        data_type.pack(pady=5)
        tk.Label(self.root, text="Name:", font=("Arial", 12)).pack()
        name = ttk.Combobox(self.root, values=self.mineral_df['MineralName'].tolist() + self.country_df['CountryName'].tolist(), font=("Arial", 12))
        name.pack(pady=5)
        text = tk.Text(self.root, height=15, width=80, font=("Arial", 10))
        text.pack(pady=5)
        tk.Button(self.root, text="View", command=lambda: self.display_data(data_type.get(), name.get(), text), font=("Arial", 12), bg="green", fg="white").pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_menu_by_role, font=("Arial", 12), bg="grey", fg="white").pack(pady=5)

    def display_data(self, data_type, name, text):
        text.delete(1.0, tk.END)
        if data_type == 'Mineral':
            row = self.mineral_df[self.mineral_df['MineralName'].str.lower() == name.lower()]
            if not row.empty:
                text.insert(tk.END, f"{name} Data:\n")
                text.insert(tk.END, row.to_string(index=False) + "\n")
                mineral_id = row['MineralID'].iloc[0]
                prod_data = self.production_df[self.production_df['MineralID'] == mineral_id]
                if not prod_data.empty:
                    text.insert(tk.END, "\nProduction Data:\n")
                    for _, row in prod_data.iterrows():
                        country = self.country_df[self.country_df['CountryID'] == row['CountryID']]['CountryName'].iloc[0]
                        text.insert(tk.END, f"Year {row['Year']}, {country}: {row['Production_tonnes']} tonnes\n")
            else:
                messagebox.showerror("Error", "Mineral not found.")
        elif data_type == 'Country':
            row = self.country_df[self.country_df['CountryName'].str.lower() == name.lower()]
            if not row.empty:
                text.insert(tk.END, f"{name} Data:\n")
                text.insert(tk.END, row.to_string(index=False) + "\n")
                country_id = row['CountryID'].iloc[0]
                prod_data = self.production_df[self.production_df['CountryID'] == country_id]
                if not prod_data.empty:
                    text.insert(tk.END, "\nProduction Data:\n")
                    for _, row in prod_data.iterrows():
                        mineral = self.mineral_df[self.mineral_df['MineralID'] == row['MineralID']]['MineralName'].iloc[0]
                        text.insert(tk.END, f"Year {row['Year']}, {mineral}: {row['Production_tonnes']} tonnes\n")
            else:
                messagebox.showerror("Error", "Country not found.")
        else:
            messagebox.showerror("Error", "Invalid data type.")

    def export_data(self):
        self.clear_screen()
        tk.Label(self.root, text="Export Data", font=("Arial", 14), fg="blue").pack(pady=10)
        tk.Label(self.root, text="Data Type:", font=("Arial", 12)).pack()
        data_type = ttk.Combobox(self.root, values=['Mineral', 'Country', 'Production'], font=("Arial", 12))
        data_type.pack(pady=5)
        tk.Button(self.root, text="Export", command=lambda: self.perform_export(data_type.get()), font=("Arial", 12), bg="green", fg="white").pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_researcher_menu, font=("Arial", 12), bg="grey", fg="white").pack(pady=5)

    def perform_export(self, data_type):
        if data_type == 'Mineral':
            self.mineral_df.to_csv(f"{data_type}_export.csv", index=False)
            messagebox.showinfo("Success", f"Exported to {data_type}_export.csv")
        elif data_type == 'Country':
            self.country_df.to_csv(f"{data_type}_export.csv", index=False)
            messagebox.showinfo("Success", f"Exported to {data_type}_export.csv")
        elif data_type == 'Production':
            self.production_df.to_csv(f"{data_type}_export.csv", index=False)
            messagebox.showinfo("Success", f"Exported to {data_type}_export.csv")
        else:
            messagebox.showerror("Error", "Invalid data type.")

    def add_insights(self):
        self.clear_screen()
        tk.Label(self.root, text="Add Insight", font=("Arial", 14), fg="blue").pack(pady=10)
        tk.Label(self.root, text="Insight:", font=("Arial", 12)).pack()
        insight = tk.Text(self.root, height=3, width=50, font=("Arial", 10))
        insight.pack(pady=5)
        tk.Label(self.root, text="Mineral (optional):", font=("Arial", 12)).pack()
        mineral = ttk.Combobox(self.root, values=[''] + self.mineral_df['MineralName'].tolist(), font=("Arial", 12))
        mineral.pack(pady=5)
        tk.Label(self.root, text="Country (optional):", font=("Arial", 12)).pack()
        country = ttk.Combobox(self.root, values=[''] + self.country_df['CountryName'].tolist(), font=("Arial", 12))
        country.pack(pady=5)
        tk.Button(self.root, text="Add", command=lambda: self.perform_add_insight(insight.get("1.0", tk.END).strip(), mineral.get(), country.get()), font=("Arial", 12), bg="green", fg="white").pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_researcher_menu, font=("Arial", 12), bg="grey", fg="white").pack(pady=5)

    def perform_add_insight(self, insight, mineral_name, country_name):
        if not insight:
            messagebox.showerror("Error", "Insight is required.")
            return
        mineral_id = None
        country_id = None
        if mineral_name:
            row = self.mineral_df[self.mineral_df['MineralName'].str.lower() == mineral_name.lower()]
            if not row.empty:
                mineral_id = row['MineralID'].iloc[0]
            else:
                messagebox.showwarning("Warning", "Mineral not found, saving without MineralID.")
        if country_name:
            row = self.country_df[self.country_df['CountryName'].str.lower() == country_name.lower()]
            if not row.empty:
                country_id = row['CountryID'].iloc[0]
            else:
                messagebox.showwarning("Warning", "Country not found, saving without CountryID.")
        new_insight = pd.DataFrame({
            'Username': [self.username],
            'Insight': [insight],
            'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'MineralID': [mineral_id],
            'CountryID': [country_id]
        })
        self.insights_df = pd.concat([self.insights_df, new_insight], ignore_index=True)
        save_insights(self.insights_df)
        messagebox.showinfo("Success", "Insight added.")

    def view_interactive_map(self):
        self.clear_screen()
        tk.Label(self.root, text="Interactive Map", font=("Arial", 14), fg="blue").pack(pady=10)
        tk.Label(self.root, text="Select Site (optional, leave blank for all sites):", font=("Arial", 12)).pack()
        site = ttk.Combobox(self.root, values=[''] + self.sites_df['SiteName'].tolist(), font=("Arial", 12))
        site.pack(pady=5)
        tk.Button(self.root, text="Show Map", command=lambda: self.display_interactive_map(site.get()), font=("Arial", 12), bg="green", fg="white").pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_menu_by_role, font=("Arial", 12), bg="grey", fg="white").pack(pady=5)

    def display_interactive_map(self, site_name):
        m = folium.Map(location=[0, 0], zoom_start=2)
        marker_cluster = MarkerCluster().add_to(m)
        sites_to_show = self.sites_df if not site_name else self.sites_df[self.sites_df['SiteName'].str.lower() == site_name.lower()]
        
        if sites_to_show.empty and site_name:
            messagebox.showerror("Error", "Site not found.")
            return

        for _, site in sites_to_show.iterrows():
            mineral = self.mineral_df[self.mineral_df['MineralID'] == site['MineralID']]['MineralName'].iloc[0]
            country = self.country_df[self.country_df['CountryID'] == site['CountryID']]['CountryName'].iloc[0]
            popup_text = f"{site['SiteName']}<br>{country}<br>{mineral}<br>Production: {site['Production_tonnes']} tonnes"
            folium.Marker(
                location=[site['Latitude'], site['Longitude']],
                popup=popup_text,
                icon=folium.Icon(color='blue')
            ).add_to(marker_cluster)
        
        m.save('map.html')
        messagebox.showinfo("Map Generated", "Interactive map saved as 'map.html'. Displaying in Jupyter output.")
        display(HTML(filename='map.html'))

    def view_insights(self):
        self.clear_screen()
        tk.Label(self.root, text="Insights", font=("Arial", 14), fg="blue").pack(pady=10)
        text = tk.Text(self.root, height=15, width=80, font=("Arial", 10))
        text.pack(pady=5)
        if not self.insights_df.empty:
            for _, row in self.insights_df.iterrows():
                text.insert(tk.END, f"{row['Username']} ({row['Timestamp']}): {row['Insight']}\n")
                if pd.notna(row['MineralID']):
                    mineral = self.mineral_df[self.mineral_df['MineralID'] == row['MineralID']]['MineralName'].iloc[0]
                    text.insert(tk.END, f"Mineral: {mineral}\n")
                if pd.notna(row['CountryID']):
                    country = self.country_df[self.country_df['CountryID'] == row['CountryID']]['CountryName'].iloc[0]
                    text.insert(tk.END, f"Country: {country}\n")
                text.insert(tk.END, "-" * 50 + "\n")
        else:
            text.insert(tk.END, "No insights available.\n")
        tk.Button(self.root, text="Back", command=self.show_menu_by_role, font=("Arial", 12), bg="grey", fg="white").pack(pady=5)

    def show_menu_by_role(self):
        if self.role == 'Administrator':
            self.show_admin_menu()
        elif self.role == 'Investor':
            self.show_investor_menu()
        elif self.role == 'Researcher':
            self.show_researcher_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = CriticalMineralsApp(root)
    root.mainloop()
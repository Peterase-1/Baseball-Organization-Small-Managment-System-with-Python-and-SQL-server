from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import pypyodbc as odbc

DRIVER_NAME = 'SQL Server' 
SERVER_NAME = 'PETERASE'
DATABASE_NAME = 'Baseball Organization'

# Correct Connection String
connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""   

try:
    conn = odbc.connect(connection_string)
    print("Connection Successful:", conn)
except odbc.Error as e:
            print("Connection Failed:", e)

#=============================== PERSONEL PART   ========================
class Personnel:

    def create_personnel(self,first_name, last_name, dob, place_of_birth, role):
        cursor = None    
        try:
            cursor = conn.cursor()
            insert_query = "INSERT INTO Personnel (F_Name, L_Name, Date_of_Birth, Place_of_Birth,Role) VALUES (?, ?, ?,?,?)"
            values = (first_name, last_name, dob, place_of_birth,role)
            cursor.execute(insert_query, values)
            conn.commit()
            print("Data inserted successfully!")
            messagebox.showinfo("Success", "Personnel added successfully.")
        

        except odbc.Error as e:
            print("Error while inserting data:", e)
            messagebox.showerror("Error","Error Date Format/ Error data type:")

    def update_personnel(self, personnel_id_in, first_name, last_name, date_of_birth, place_of_birth, role):
        cursor = None
        try:
            cursor = conn.cursor()
            
            # Check if personnel ID exists
            check_query = "SELECT COUNT(*) FROM Personnel WHERE Personnel_ID = ?"
            cursor.execute(check_query, (personnel_id_in,))
            result = cursor.fetchone()

            if result[0] == 0:
                print("Error: Personnel ID does not exist.")
                messagebox.showerror("Error", "Personnel ID does not exist.")
                return

            # Update the personnel record
            update_query = """
            UPDATE Personnel 
            SET F_Name = ?, L_Name = ?, Date_of_Birth = ?, Place_of_Birth = ?, Role = ? 
            WHERE Personnel_ID = ?
            """
            values = (first_name, last_name, date_of_birth, place_of_birth, role, personnel_id_in)  # Added personnel_id_in
            cursor.execute(update_query, values)
            conn.commit()

            print("Personnel data updated successfully!")
            messagebox.showinfo("Success", "Personnel data updated successfully.")

        except odbc.Error as e:
            print("Error while updating data:", e)
            messagebox.showerror("Error", "Error while updating personnel data.")

        finally:
            if cursor:
                cursor.close()
    
    def delete_personnel(self, personnel_id_in):
        cursor = None
        try:
            cursor = conn.cursor()

            check_query = "SELECT COUNT(*) FROM Personnel WHERE Personnel_ID = ?"
            cursor.execute(check_query, (personnel_id_in,))
            result = cursor.fetchone()

            if result[0] == 0:  # If the count is 0, the personnel ID doesn't exist
                messagebox.showerror("Error", "Personnel with ID does not exist.")
                return  

    
            delete_query = "DELETE FROM Personnel WHERE Personnel_ID = ?"
            cursor.execute(delete_query, (personnel_id_in,))
            conn.commit()

            print(f"Personnel with ID {personnel_id_in} deleted successfully!")
            messagebox.showinfo("Success", "Personnel with ID deleted successfully.")

        except odbc.Error as e:
            print("Error while deleting data:", e)
            messagebox.showerror("Error", "Error while deleting personnel.")

personnel_manager = Personnel()

def input_personnel_data(personnel_manager,first_name_entry_p, last_name_entry_p, dob_entry_p, pob_entry_p, role_dropdown_p):
    
    first_name = first_name_entry_p.get()
    last_name = last_name_entry_p.get()
    dob = dob_entry_p.get()
    place_of_birth = pob_entry_p.get()
    role = role_dropdown_p.get()
    personnel_manager.create_personnel(first_name, last_name, dob, place_of_birth, role)

#===============================    TEAM PART   ======================================================================

class Team:
    def __init__(self):
        pass
       

    def create_team(self, team_name, city, division, league):
        cursor = None    
        try:
            cursor = conn.cursor()
            insert_query = "INSERT INTO Teams (Team_Name, League, Division, city) VALUES (?, ?, ?,?)"
            values = (team_name, league, division,city)
            cursor.execute(insert_query, values)
            conn.commit()
            print("Data inserted successfully!")
            messagebox.showinfo("Success", "Team added successfully.")
        

        except odbc.Error as e:
            print("Error while inserting data:", e)
            messagebox.showerror("Error","Error : Error while inserting data:")

      
    def assign_personnel(self, team_name_in, personnel_ids_in, personnel_manager):
      pass

    def update_team_personnel(self, team_name, new_personnel_ids, personnel_manager):
       pass
team_manager = Team()

#=============================     GAME PART       ==============================================================

class Game:
    def __init__(self, team_manager):
       pass
    def add_game_result(self, home_team_id, visiting_team_id, home_team_hits, home_team_runs, home_team_errors, visiting_team_hits, visiting_team_runs, visiting_team_errors, home_team_pitcher, visiting_team_pitcher, Game_Date):

        cursor = None
        try:
            cursor = conn.cursor()

            # Insert the game date into the Game table
            insert_game_query = """
                INSERT INTO Game (Date) 
                VALUES (?)
            """
            cursor.execute(insert_game_query, (Game_Date,))
            conn.commit()  

            # Retrieve the Game_ID of the last inserted row
            cursor.execute("SELECT @@IDENTITY")
            game_id = cursor.fetchone()[0]  # Fetch the ID from the query result

            if game_id is None:
                raise Exception("Failed to retrieve the Game_ID.")

            print(f"Game added successfully with Game_ID: {game_id}")

        #    Insert home team data into the Game_Teams table
            insert_home_team_query = """
                INSERT INTO Game_Teams (Game_ID, Team_ID, Team_Type, Hits, Runs, Errors, Pitcher_ID)
                VALUES (?, ?, 'Home', ?, ?, ?, ?)
            """
            home_team_values = (game_id, home_team_id, home_team_hits, home_team_runs, home_team_errors, home_team_pitcher)
            cursor.execute(insert_home_team_query, home_team_values)

            #  Insert visiting team data into the Game_Teams table
            insert_visiting_team_query = """
                INSERT INTO Game_Teams (Game_ID, Team_ID, Team_Type, Hits, Runs, Errors, Pitcher_ID)
                VALUES (?, ?, 'Visiting', ?, ?, ?, ?)
            """
            visiting_team_values = (game_id, visiting_team_id, visiting_team_hits, visiting_team_runs, visiting_team_errors, visiting_team_pitcher)
            cursor.execute(insert_visiting_team_query, visiting_team_values)

            conn.commit()  

            print("Game result added successfully to Game_Teams table.")
            messagebox.showinfo("Succes", "Team Result Added Successfull")
            return game_id  # Return the Game_ID of the newly inserted game

        except odbc.Error as e:
            print("Error while inserting data:", e)
            messagebox.showerror("Error", f"Error while inserting game result: {e}")
            return None

        finally:
            if cursor:
                cursor.close()

          
game_manager = Game(team_manager)

#=============================   GUL PART===========================


def Editorial_page():
    
    root = Tk()
    root.geometry('925x500+300+200')
    root.title("Baseball Organization Management System")
    root.config(bg="white")

    notebook = ttk.Notebook(root)

    style = ttk.Style()
    style.configure("TNotebook.Tab", padding=[15, 5], background="white", width=20, font=("Arial", 12), foreground="black")
    style.configure("TNotebook", borderwidth=0, relief="flat", background="white")
    style.map("TNotebook.Tab", 
              background=[("selected", "blue")], 
              foreground=[("selected", "black")])
    

#==========================================================  Personell managment(Main)-  =====================================================
    # Personnel Management Tab (Main Tab)
    personnel_tab = Frame(notebook, bg="white")
    notebook.add(personnel_tab, text="Personnel Management")

    personnel_notebook = ttk.Notebook(personnel_tab)
#-----------------------------------------------      # Add Personnel Sub-Tab-----------------------------------------------------------------------------------------------
    
    add_personnel_tab = Frame(personnel_notebook, bg="white")
    personnel_notebook.add(add_personnel_tab, text="Add Personnel")
    # First Name
    first_name_label_p = Label(add_personnel_tab, text="First Name:", font=("Arial", 10), bg="white")
    first_name_label_p.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    first_name_entry_p = Entry(add_personnel_tab, font=("Arial", 12))
    first_name_entry_p.grid(row=1, column=1, padx=10, pady=5)

    # Last Name
    last_name_label_p = Label(add_personnel_tab, text="Last Name:", font=("Arial", 10), bg="white")
    last_name_label_p.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    last_name_entry_p = Entry(add_personnel_tab, font=("Arial", 12))
    last_name_entry_p.grid(row=2, column=1, padx=10, pady=5)

    # Date of Birth
    dob_label_p = Label(add_personnel_tab, text="Date of Birth (YY-MM-DD):", font=("Arial", 10), bg="white")
    dob_label_p.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    dob_entry_p = Entry(add_personnel_tab, font=("Arial", 12))
    dob_entry_p.grid(row=3, column=1, padx=10, pady=5)

    # Place of Birth
    pob_label_p = Label(add_personnel_tab, text="Place of Birth:", font=("Arial", 10), bg="white")
    pob_label_p.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    pob_entry_p = Entry(add_personnel_tab, font=("Arial", 12))
    pob_entry_p.grid(row=4, column=1, padx=10, pady=5)

    # Role Drop-down
    role_label_p = Label(add_personnel_tab, text="Role:", font=("Arial", 10), bg="white")
    role_label_p.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    role_dropdown_p = ttk.Combobox(add_personnel_tab, values=["Player", "Manager", "Coach", "Umpire"], font=("Arial", 12))
    role_dropdown_p.set("Select Role")  # Default value
    role_dropdown_p.grid(row=5, column=1, padx=10, pady=5)


    add_button = Button(add_personnel_tab, text="Add Personnel", font=("Arial", 12), bg="#2196F3", fg="white", relief="flat", highlightthickness=0,command=lambda: input_personnel_data(personnel_manager,first_name_entry_p, last_name_entry_p, dob_entry_p, pob_entry_p, role_dropdown_p))
    add_button.grid(row=6, column=0, columnspan=2, pady=20)
    

    

    
#----------------------------------------------------------------------------------------------------------------------------------------------------------
    # View Personnel Sub-Tab
    view_personnel_tab = Frame(personnel_notebook, bg="white")
    personnel_notebook.add(view_personnel_tab, text="View Personnel")
    columns = ("Personnel ID", "First Name", "Last Name", "Date of Birth", "Place of Birth", "Role")

    tree = ttk.Treeview(view_personnel_tab, columns=columns, show="headings", height=6)
    tree.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    tree.heading("Personnel ID", text="Personnel ID")
    tree.heading("First Name", text="First Name")
    tree.heading("Last Name", text="Last Name")
    tree.heading("Date of Birth", text="Date of Birth")
    tree.heading("Place of Birth", text="Place of Birth")
    tree.heading("Role", text="Role")

    tree.column("Personnel ID", width=100, anchor="center")
    tree.column("First Name", width=150, anchor="center")
    tree.column("Last Name", width=150, anchor="center")
    tree.column("Date of Birth", width=120, anchor="center")
    tree.column("Place of Birth", width=150, anchor="center")
    tree.column("Role", width=100, anchor="center")

    view_personnel_tab.grid_rowconfigure(0, weight=1)
    view_personnel_tab.grid_columnconfigure(0, weight=1)

    scrollbar = ttk.Scrollbar(view_personnel_tab, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    
    

    def Fill_personnel_Table():
        cursor = None
        try:
            cursor = conn.cursor()
            query = "SELECT Personnel_ID, F_Name, L_Name, Date_of_Birth, Place_of_Birth, Role FROM Personnel"
            cursor.execute(query)
            personnel_data = cursor.fetchall()
            for item in tree.get_children():
                tree.delete(item)
            for person in personnel_data:
                tree.insert("", "end", values=person)

        except odbc.Error as e:
            print("Error while reading data:", e)
            messagebox.showerror("Error", "Error while fetching personnel data.")

        finally:
            if cursor:
                cursor.close() 



    refresh_button = Button(view_personnel_tab,command=Fill_personnel_Table, text="Refresh", font=("Arial", 12), bg="#2196F3", fg="white", relief="flat", highlightthickness=0)
    refresh_button.grid(row=1, column=0, padx=20, pady=10)
   
#---------------------------------------------------------------------------------------------------------------------

    # Change Personnel Sub-Tab
    change_personnel_tab = Frame(personnel_notebook, bg="white")
    personnel_notebook.add(change_personnel_tab, text="Update Personnel Data")
    # Personnel ID (for finding the personnel)
    id_label_c = Label(change_personnel_tab, text="Personnel ID:", font=("Arial", 10), bg="white")
    id_label_c.grid(row=1, column=0, padx=20, pady=5, sticky="w")
    id_entry_c = Entry(change_personnel_tab, font=("Arial", 10))
    id_entry_c.grid(row=1, column=1, padx=20, pady=5)

    # New First Name
    first_name_label_c = Label(change_personnel_tab, text="New First Name:", font=("Arial", 10), bg="white")
    first_name_label_c.grid(row=2, column=0, padx=20, pady=5, sticky="w")
    first_name_entry_c = Entry(change_personnel_tab, font=("Arial", 10))
    first_name_entry_c.grid(row=2, column=1, padx=20, pady=5)

    # New Last Name
    last_name_label_c = Label(change_personnel_tab, text="New Last Name:", font=("Arial", 10), bg="white")
    last_name_label_c.grid(row=3, column=0, padx=20, pady=5, sticky="w")
    last_name_entry_c = Entry(change_personnel_tab, font=("Arial", 10))
    last_name_entry_c.grid(row=3, column=1, padx=20, pady=5)

    # New Date of Birth
    dob_label_c = Label(change_personnel_tab, text="New Date of Birth:", font=("Arial", 10), bg="white")
    dob_label_c.grid(row=4, column=0, padx=20, pady=5, sticky="w")
    dob_entry_c = Entry(change_personnel_tab, font=("Arial", 10))
    dob_entry_c.grid(row=4, column=1, padx=20, pady=5)

    # New Place of Birth
    pob_label_c = Label(change_personnel_tab, text="New Place of Birth:", font=("Arial", 10), bg="white")
    pob_label_c.grid(row=5, column=0, padx=20, pady=5, sticky="w")
    pob_entry_c = Entry(change_personnel_tab, font=("Arial", 10))
    pob_entry_c.grid(row=5, column=1, padx=20, pady=5)


    # New Role
    role_label_c = Label(change_personnel_tab, text="New Role:", font=("Arial", 10), bg="white")
    role_label_c.grid(row=6, column=0, padx=20, pady=5, sticky="w")
    role_dropdown_c = ttk.Combobox(change_personnel_tab, values=["Player", "Manager", "Coach", "Umpire"], font=("Arial", 12))
    role_dropdown_c.set("Select Role") 
    role_dropdown_c.grid(row=6, column=1, padx=20, pady=5)




    def Update_personnel():
        personnel_id_in = id_entry_c.get()
        first_name = first_name_entry_c.get()
        last_name = last_name_entry_c.get()
        dob = dob_entry_c.get()
        place_of_birth = pob_entry_c.get()
        role = role_dropdown_c.get()
        personnel_manager.update_personnel(personnel_id_in, first_name, last_name, dob, place_of_birth, role)
    change_button = Button(change_personnel_tab, text="Change Personnel", font=("Arial", 12), bg="#2196F3", fg="white", relief="flat", highlightthickness=0, command=Update_personnel)
    change_button.grid(row=7, column=0, columnspan=2, pady=20)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Delete Personnel Sub-Tab
    delete_personnel_tab = Frame(personnel_notebook, bg="white")
    personnel_notebook.add(delete_personnel_tab, text="Delete Personnel")
    # Personnel ID (to delete the personnel)
    id_label_d = Label(delete_personnel_tab, text="Personnel ID:", font=("Arial", 10), bg="white")
    id_label_d.grid(row=1, column=0, padx=20, pady=5, sticky="w")
    id_entry_d = Entry(delete_personnel_tab, font=("Arial", 10))
    id_entry_d.grid(row=1, column=1, padx=20, pady=5)
    #delete button


    def delete_personnel():
        personnel_id = id_entry_d.get()
        personnel_manager.delete_personnel(personnel_id)
           
    # Delete Button
    delete_button = Button(delete_personnel_tab, text="Delete Personnel", font=("Arial", 12), bg="#2196F3", fg="white", relief="flat", highlightthickness=0, command=delete_personnel)
    delete_button.grid(row=2, column=0, columnspan=2, pady=20)

    personnel_notebook.pack(padx=20, pady=20, fill="both", expand=True)


#=================================================      Team Managment(Main)      =====================================================

    # Team Management Tab (Main Tab)



    team_tab = Frame(notebook, bg="white")
    notebook.add(team_tab, text="Team Management")

    team_notebook = ttk.Notebook(team_tab)
#----------------------------------------------------------------------------------------------------------------------------------------
    # Create Team Sub-Tab
    create_team_tab = Frame(team_notebook, bg="white")
    team_notebook.add(create_team_tab, text="Create Team")
    # Team Name
    team_name_label = Label(create_team_tab, text="Team Name:", font=("Arial", 10), bg="white")
    team_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    team_name_entry_c = Entry(create_team_tab, font=("Arial", 10))
    team_name_entry_c.grid(row=0, column=1, padx=10, pady=10)

    # Team City
    team_city_label = Label(create_team_tab, text="Team City:", font=("Arial", 10), bg="white")
    team_city_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    team_city_entry = Entry(create_team_tab, font=("Arial", 10))
    team_city_entry.grid(row=1, column=1, padx=10, pady=10)

    # Division Drop-down
    division_label = Label(create_team_tab, text="Division:", font=("Arial", 10), bg="white")
    division_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    division_dropdown = ttk.Combobox(create_team_tab, values=["First", "Second", "Last"], font=("Arial", 10))
    division_dropdown.set("Select Division")  # Default value
    division_dropdown.grid(row=2, column=1, padx=10, pady=10)

    # League Drop-down
    league_label = Label(create_team_tab, text="League:", font=("Arial", 10), bg="white")
    league_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    league_dropdown = ttk.Combobox(create_team_tab, values=["American", "Premium", "East"], font=("Arial", 10))
    league_dropdown.set("Select League")  # Default value
    league_dropdown.grid(row=3, column=1, padx=10, pady=10)

    def input_team_data():
        team_name = team_name_entry_c.get()
        city = team_city_entry.get().strip()
        division = division_dropdown.get()
        league = league_dropdown.get()
        team_manager.create_team(team_name, city, division, league)

    # Create Team Button
    create_team_button = Button(create_team_tab, text="Create Team", font=("Arial", 12), bg="#2196F3", fg="white",
                                relief="flat", highlightthickness=0, command=input_team_data)
    create_team_button.grid(row=4, column=0, columnspan=2, pady=20)
#---------------------------------------------------------------------------------------------------------------------------------------------

    # Assign Personnel to Team Sub-Tab
    assign_personnel_tab = Frame(team_notebook, bg="white")
    team_notebook.add(assign_personnel_tab, text="Assign Personnel")
    
    #team Name
    team_name_label = Label(assign_personnel_tab, text="Team Name:", font=("Arial", 10), bg="white")
    team_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    team_name_entry = Entry(assign_personnel_tab, font=("Arial", 10))
    team_name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Personnel ID
    personnel_id_label = Label(assign_personnel_tab, text="Personnel ID:", font=("Arial", 10), bg="white")
    personnel_id_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    personnel_id_entry = Entry(assign_personnel_tab, font=("Arial", 10))
    personnel_id_entry.grid(row=1, column=1, padx=10, pady=10)

    def assign_personnel():
        team_name = team_name_entry.get().strip()
        personnel_ids = personnel_id_entry.get().strip()

        # Remove whitespace from each ID
        personnel_ids = [id.strip() for id in personnel_ids if id.strip()]
        team_manager.assign_personnel(team_name, personnel_ids, personnel_manager)

    # Assign Personnel Button
    assign_personnel_button = Button(assign_personnel_tab, text="Assign Personnel", font=("Arial", 12), 
                                    bg="#2196F3", fg="white", relief="flat", highlightthickness=0, 
                                 command=assign_personnel)
    assign_personnel_button.grid(row=2, column=0, columnspan=2, pady=20)
#--------------------------------------------------------------------------------------------------------------------------------------------


    # Display Team Info Sub-Tab
    display_team_info_tab = Frame(team_notebook, bg="white")
    team_notebook.add(display_team_info_tab, text="Display Team Info")
        # Table for displaying team information
    team_table = ttk.Treeview(display_team_info_tab, columns=("Team_ID", "Team_Name", "League", "Division", "City"), show="headings")

    # Define column headings explicitly
    team_table.heading("Team_ID", text="Team ID")
    team_table.heading("Team_Name", text="Team Name")
    team_table.heading("League", text="League")
    team_table.heading("Division", text="Division")
    team_table.heading("City", text="City")

    # Set column widths
    team_table.column("Team_ID", width=100)
    team_table.column("Team_Name", width=150)
    team_table.column("League", width=100)
    team_table.column("Division", width=100)
    team_table.column("City", width=150)

    team_table.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")



    def fetch_team_info():
        cursor = None
        try:
            cursor = conn.cursor()

            query = """
                SELECT Team_ID, Team_Name, League, Division, City 
                FROM Teams
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Clear existing data in the table
            for item in team_table.get_children():
                team_table.delete(item)

            # Insert new data
            for row in rows:
                team_table.insert("", "end", values=row)

        except odbc.Error as e:
            print("Error fetching team data:", e)

        finally:
            if cursor:
                cursor.close()




    # Display Info Button below the table
    display_team_info_button = Button(display_team_info_tab, text="Display Info", font=("Arial", 12), command=fetch_team_info)
    display_team_info_button.grid(row=1, column=0, columnspan=2, pady=10)

    # Configure row & column weights for resizing
    display_team_info_tab.grid_rowconfigure(0, weight=1)
    display_team_info_tab.grid_columnconfigure(0, weight=1)
#------------------------------------------------------------------------------------------------------------------------------------------------

    # Update Team Personnel Sub-Tab
    update_team_personnel_tab = Frame(team_notebook, bg="white")
    team_notebook.add(update_team_personnel_tab, text="Update Team Personnel")
        #Team Name
    team_name_label_update = Label(update_team_personnel_tab, text="Team Name:", font=("Arial", 10), bg="white")
    team_name_label_update.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    team_name_entry_update = Entry(update_team_personnel_tab, font=("Arial", 10))
    team_name_entry_update.grid(row=0, column=1, padx=10, pady=10)

    # Old ID
    old_id_label_update = Label(update_team_personnel_tab, text="Old ID:", font=("Arial", 10), bg="white")
    old_id_label_update.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    old_id_entry_update = Entry(update_team_personnel_tab, font=("Arial", 10))
    old_id_entry_update.grid(row=1, column=1, padx=10, pady=10)

    # New ID
    new_id_label_update = Label(update_team_personnel_tab, text="New ID:", font=("Arial", 10), bg="white")
    new_id_label_update.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    new_id_entry_update = Entry(update_team_personnel_tab, font=("Arial", 10))
    new_id_entry_update.grid(row=2, column=1, padx=10, pady=10)

    # Update Button
    update_team_personnel_button = Button(update_team_personnel_tab, text="Update Personnel", font=("Arial", 12), bg="#2196F3", fg="white", relief="flat", highlightthickness=0)
    update_team_personnel_button.grid(row=3, column=0, columnspan=2, pady=20)


    team_notebook.pack(padx=20, pady=20, fill="both", expand=True)






#=================================================  Game Managment(Main)    =================================================================
    # Game Information Tab (Main Tab)
    # Main Game Management Tab
    game_tab = Frame(notebook, bg="white")
    notebook.add(game_tab, text="Game Management")

    # Sub-Notebook for Game Management
    game_notebook = ttk.Notebook(game_tab)

    # Add Game Result Sub-Tab
    add_game_result_tab = Frame(game_notebook, bg="white")
    game_notebook.add(add_game_result_tab, text="Add Game Result")

    # Home Team Name and Visiting Team Name
    home_team_name_label = Label(add_game_result_tab, text="Home Team ID:", font=("Arial", 10), bg="white")
    home_team_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    home_team_name_idr = Entry(add_game_result_tab, font=("Arial", 10))
    home_team_name_idr.grid(row=0, column=1, padx=10, pady=10)

    visiting_team_name_label = Label(add_game_result_tab, text="Visiting Team ID:", font=("Arial", 10), bg="white")
    visiting_team_name_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
    visiting_team_id_entryr = Entry(add_game_result_tab, font=("Arial", 10))
    visiting_team_id_entryr.grid(row=0, column=3, padx=10, pady=10)

    # Home Team Hits and Home Team Runs
    home_team_hits_label = Label(add_game_result_tab, text="Home Team Hits:", font=("Arial", 10), bg="white")
    home_team_hits_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    home_team_hits_entryr = Entry(add_game_result_tab, font=("Arial", 10))
    home_team_hits_entryr.grid(row=1, column=1, padx=10, pady=10)

    home_team_runs_label = Label(add_game_result_tab, text="Home Team Runs:", font=("Arial", 10), bg="white")
    home_team_runs_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")
    home_team_runs_entryr = Entry(add_game_result_tab, font=("Arial", 10))
    home_team_runs_entryr.grid(row=1, column=3, padx=10, pady=10)

    # Visiting Team Hits and Visiting Team Runs
    visiting_team_hits_label = Label(add_game_result_tab, text="Visiting Team Hits:", font=("Arial", 10), bg="white")
    visiting_team_hits_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    visiting_team_hits_entryr = Entry(add_game_result_tab, font=("Arial", 10))
    visiting_team_hits_entryr.grid(row=2, column=1, padx=10, pady=10)

    visiting_team_runs_label = Label(add_game_result_tab, text="Visiting Team Runs:", font=("Arial", 10), bg="white")
    visiting_team_runs_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")
    visiting_team_runs_entryr = Entry(add_game_result_tab, font=("Arial", 10))
    visiting_team_runs_entryr.grid(row=2, column=3, padx=10, pady=10)

    # Home Team Errors and Visiting Team Errors
    home_team_errors_label = Label(add_game_result_tab, text="Home Team Errors:", font=("Arial", 10), bg="white")
    home_team_errors_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    home_team_errors_entryr = Entry(add_game_result_tab, font=("Arial", 10))
    home_team_errors_entryr.grid(row=3, column=1, padx=10, pady=10)

    visiting_team_errors_label = Label(add_game_result_tab, text="Visiting Team Errors:", font=("Arial", 10), bg="white")
    visiting_team_errors_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")
    visiting_team_errors_entryr = Entry(add_game_result_tab, font=("Arial", 10))
    visiting_team_errors_entryr.grid(row=3, column=3, padx=10, pady=10)

    # Home Team Pitcher and Visiting Team Pitcher
    home_team_pitcher_label = Label(add_game_result_tab, text="Home Team Pitcher:", font=("Arial", 10), bg="white")
    home_team_pitcher_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    home_team_pitcher_entryr = Entry(add_game_result_tab, font=("Arial", 10))
    home_team_pitcher_entryr.grid(row=4, column=1, padx=10, pady=10)

    visiting_team_pitcher_label = Label(add_game_result_tab, text="Visiting Team Pitcher:", font=("Arial", 10), bg="white")
    visiting_team_pitcher_label.grid(row=4, column=2, padx=10, pady=10, sticky="w")
    visiting_team_pitcher_entryr = Entry(add_game_result_tab, font=("Arial", 10))
    visiting_team_pitcher_entryr.grid(row=4, column=3, padx=10, pady=10)

    # Game Date Entry
    game_date_label = Label(add_game_result_tab, text="Game Date:", font=("Arial", 10), bg="white")
    game_date_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    game_date_entryr = Entry(add_game_result_tab, font=("Arial", 10))
    game_date_entryr.grid(row=5, column=1, padx=10, pady=10)

    # Add the Sub-Notebook to the Main Notebook





    
    def input_game_result():
        home_team_id = home_team_name_idr.get()
        visiting_team_id = visiting_team_id_entryr.get()
        home_team_hits = home_team_hits_entryr.get()
        home_team_runs = home_team_runs_entryr.get()
        visiting_team_hits = visiting_team_hits_entryr.get()
        visiting_team_runs = visiting_team_runs_entryr.get()
        home_team_pitcher = home_team_pitcher_entryr.get()
        visiting_team_pitcher = visiting_team_pitcher_entryr.get()
        home_team_errors = home_team_errors_entryr.get()
        visiting_team_errors = visiting_team_errors_entryr.get()
        Game_Date = game_date_entryr.get()
        game_manager.add_game_result( home_team_id, visiting_team_id, home_team_hits, home_team_runs,home_team_errors, visiting_team_hits, visiting_team_runs,visiting_team_errors, home_team_pitcher, visiting_team_pitcher,Game_Date)

    add_game_result_button = Button(add_game_result_tab,command=input_game_result, text="Add Game Result", font=("Arial", 12), bg="#2196F3", fg="white", relief="flat", highlightthickness=0)
    add_game_result_button.grid(row=7, column=0, columnspan=4, pady=20)



    #---------------------------------------------------------------------------------------------------------------------------------------

    # View Scheduled Games Sub-Tab
    view_scheduled_games_tab = Frame(game_notebook, bg="white")
    game_notebook.add(view_scheduled_games_tab, text="View Scheduled Games")
    columns = ("Game_ID", "Date", "Team_ID", "Team_Type", "Hits", "Runs", "Errors", "Pitcher_ID")
    game_table = ttk.Treeview(view_scheduled_games_tab, columns=columns, show="headings")

    # Define column headings
    for col in columns:
        game_table.heading(col, text=col)
        game_table.column(col, width=100)

    game_table.pack(padx=20, pady=10, fill="both", expand=True)

    def view_scheduled_games():
        cursor = None
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    g.Game_ID, 
                    g.Date, 
                    gt.Team_ID, 
                    gt.Team_Type, 
                    gt.Hits, 
                    gt.Runs, 
                    gt.Errors, 
                    gt.Pitcher_ID
                FROM Game g
                INNER JOIN Game_Teams gt ON g.Game_ID = gt.Game_ID
                ORDER BY g.Game_ID DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for item in game_table.get_children():
                game_table.delete(item)
            # Insert new data
            for row in rows:
                game_table.insert("", "end", values=row)

        except odbc.Error as e:
            print("Error fetching game data:", e)

        finally:
            if cursor:
                cursor.close()
    # Refresh Button
    refresh_button = Button(view_scheduled_games_tab, text="Refresh", command=view_scheduled_games,bg="lightblue")
    refresh_button.pack(pady=10)
    game_notebook.pack(padx=20, pady=20, fill="both", expand=True)
    notebook.pack(padx=20, pady=20, fill="both", expand=True)
    root.mainloop()
   
def Admin_page(main_window):
  
    main_window.quit()  
    main_window.destroy()  

    def check_login():
      
        try:
            with open("credentials.txt", "r") as file:
                saved_username = file.readline().strip()
                saved_password = file.readline().strip()
        except FileNotFoundError:
            messagebox.showerror("Error", "Credentials file not found.")
            return

        # Get the entered username and password
        entered_username = user.get()
        entered_password = Password.get()

        # Check if the credentials match
        if entered_username == saved_username and entered_password == saved_password:
            Editorial_page()  # Open the Hello page on successful login
        else:
            error_label.config(text="Incorrect username or password", fg="red")

    # Create the login window (Admin page)
    rw = Tk()
    rw.title('Baseball Organization Management System')
    rw.geometry('925x500+300+200')
    rw.configure(bg="#fff")
    rw.resizable(False, False)

    #-----------            img -----------------
    rw.small_img = PhotoImage(file='pngegg.png')  # Ensure this image file exists
    small_img = rw.small_img.subsample(4, 4)
    Label(rw, image=small_img, bg='white').place(x=50, y=50)

    frame = Frame(rw, width=350, height=350, bg="white")
    frame.place(x=480, y=70)

    # --------------------------------------Title
    handling = Label(frame, text='Admin', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    handling.place(x=100, y=5)

    # ------------------------------------Username 
    user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    Frame(frame, width=295, height=2, bg="black").place(x=25, y=107)

    # --------------------------------     Password
    Password = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    Password.place(x=30, y=150)
    Password.insert(0, 'Password')
    Frame(frame, width=295, height=2, bg="black").place(x=25, y=177)

    # -----------------------------------------Login Button
    login_button = Button(frame, width=39, pady=7, text='Login', bg='#57a1f8', fg='white', border=0, command=check_login)
    login_button.place(x=35, y=234)

    # Error label for incorrect login
    error_label = Label(frame, text="", fg="red", bg="white")
    error_label.place(x=35, y=270)

    rw.mainloop()


def create_rounded_button(parent, text, command=None):
    button = Button(parent, text=text, command=command, font=("Arial", 16, "bold"),
                    bg="#3498db", fg="white", activebackground="#2980b9", 
                    relief="flat", bd=0, width=15, height=2)
    return button

def welcome(): 
    rw = Tk()
    rw.geometry("925x500+300+200")
    rw.title("Baseball Organization 2025")
    rw.resizable(False, False)

    container = Frame(rw)
    container.pack(fill="both", expand=True)

    left_frame = Frame(container, width=462, height=500, bg="#3498db")
    left_frame.pack_propagate(False)
    left_frame.pack(side="left", fill="both")

    welcome_label = Label(left_frame, text="Welcome", font=("Helvetica", 40, "bold"), bg="#3498db", fg="white")
    welcome_label.place(relx=0.5, rely=0.5, anchor="center")

    right_frame = Frame(container, width=463, height=500, bg="#ecf0f1")
    right_frame.pack_propagate(False)
    right_frame.pack(side="right", fill="both")

    admin_button = create_rounded_button(right_frame, "Admin", command=lambda: Admin_page(rw))
    guest_button = create_rounded_button(right_frame, "Fans", command=guest_page)

    admin_button.place(relx=0.5, rely=0.4, anchor="center")
    guest_button.place(relx=0.5, rely=0.6, anchor="center")

    rw.mainloop()
def guest_page():
    root = Tk()
    root.geometry('925x500+300+200')
    root.title("Baseball Organization Management System")
    root.config(bg="white")

    notebook = ttk.Notebook(root)

    style = ttk.Style()
    style.configure("TNotebook.Tab", padding=[15, 5], background="white", width=20, font=("Arial", 12), foreground="black")
    style.configure("TNotebook", borderwidth=0, relief="flat", background="white")
    style.map("TNotebook.Tab", 
              background=[("selected", "blue")], 
              foreground=[("selected", "black")])
    
    # Team Management Tab (Main Tab)
    team_tab = Frame(notebook, bg="white")
    notebook.add(team_tab, text="Team Information")
    team_notebook = ttk.Notebook(team_tab)    
    # Display Team Info Sub-Tab
    display_team_info_tab = Frame(team_notebook, bg="white")
    team_notebook.add(display_team_info_tab, text="Display Team Info")
        # Table for displaying team information
    team_table = ttk.Treeview(display_team_info_tab, columns=("Team_ID", "Team_Name", "League", "Division", "City"), show="headings")

    # Define column headings explicitly
    team_table.heading("Team_ID", text="Team ID")
    team_table.heading("Team_Name", text="Team Name")
    team_table.heading("League", text="League")
    team_table.heading("Division", text="Division")
    team_table.heading("City", text="City")

    # Set column widths
    team_table.column("Team_ID", width=100)
    team_table.column("Team_Name", width=150)
    team_table.column("League", width=100)
    team_table.column("Division", width=100)
    team_table.column("City", width=150)

    team_table.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")



    def fetch_team_info():
        cursor = None
        try:
            cursor = conn.cursor()

            query = """
                SELECT Team_ID, Team_Name, League, Division, City 
                FROM Teams
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Clear existing data in the table
            for item in team_table.get_children():
                team_table.delete(item)

            # Insert new data
            for row in rows:
                team_table.insert("", "end", values=row)

        except odbc.Error as e:
            print("Error fetching team data:", e)

        finally:
            if cursor:
                cursor.close()

    display_team_info_button = Button(display_team_info_tab, text="Display Info", font=("Arial", 12), command=fetch_team_info)
    display_team_info_button.grid(row=1, column=0, columnspan=2, pady=10)

    # Configure row & column weights for resizing
    display_team_info_tab.grid_rowconfigure(0, weight=1)
    display_team_info_tab.grid_columnconfigure(0, weight=1)
    team_notebook.pack(padx=20, pady=20, fill="both", expand=True)
    game_tab = Frame(notebook, bg="white")
    notebook.add(game_tab, text="Game Information")

    # Sub-Notebook for Game Management
    game_notebook = ttk.Notebook(game_tab)



    # View Scheduled Games Sub-Tab
    view_scheduled_games_tab = Frame(game_notebook, bg="white")
    game_notebook.add(view_scheduled_games_tab, text="View Scheduled Games")
    columns = ("Game_ID", "Date", "Team_ID", "Team_Type", "Hits", "Runs", "Errors", "Pitcher_ID")
    game_table = ttk.Treeview(view_scheduled_games_tab, columns=columns, show="headings")

    # Define column headings
    for col in columns:
        game_table.heading(col, text=col)
        game_table.column(col, width=100)

    game_table.pack(padx=20, pady=10, fill="both", expand=True)

    def view_scheduled_games():
      
        cursor = None
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    g.Game_ID, 
                    g.Date, 
                    gt.Team_ID, 
                    gt.Team_Type, 
                    gt.Hits, 
                    gt.Runs, 
                    gt.Errors, 
                    gt.Pitcher_ID
                FROM Game g
                INNER JOIN Game_Teams gt ON g.Game_ID = gt.Game_ID
                ORDER BY g.Game_ID DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            for item in game_table.get_children():
                game_table.delete(item)
            # Insert new data
            for row in rows:
                game_table.insert("", "end", values=row)

        except odbc.Error as e:
            print("Error fetching game data:", e)

        finally:
            if cursor:
                cursor.close()
    # Refresh Button
    refresh_button = Button(view_scheduled_games_tab, text="Refresh", command=view_scheduled_games,bg="lightblue")
    refresh_button.pack(pady=10)
    refresh_button = Button(view_scheduled_games_tab, text="Interpreate", command=interpreter,bg="lightblue")
    refresh_button.pack(pady=20)
    game_notebook.pack(padx=20, pady=20, fill="both", expand=True)
    notebook.pack(padx=20, pady=20, fill="both", expand=True)
    root.mainloop()
   
def Admin_page(main_window):
  
    main_window.quit()  
    main_window.destroy()  

    def check_login():
      
        try:
            with open("credentials.txt", "r") as file:
                saved_username = file.readline().strip()
                saved_password = file.readline().strip()
        except FileNotFoundError:
            messagebox.showerror("Error", "Credentials file not found.")
            return

        # Get the entered username and password
        entered_username = user.get()
        entered_password = Password.get()

        # Check if the credentials match
        if entered_username == saved_username and entered_password == saved_password:
            Editorial_page()  # Open the Hello page on successful login
        else:
            error_label.config(text="Incorrect username or password", fg="red")

    rw = Tk()
    rw.title('Baseball Organization Management System')
    rw.geometry('925x500+300+200')
    rw.configure(bg="#fff")
    rw.resizable(False, False)

    #-----------            img -----------------
    rw.small_img = PhotoImage(file='pngegg.png')  # Ensure this image file exists
    small_img = rw.small_img.subsample(4, 4)
    Label(rw, image=small_img, bg='white').place(x=50, y=50)

    frame = Frame(rw, width=350, height=350, bg="white")
    frame.place(x=480, y=70)

    # --------------------------------------Title
    handling = Label(frame, text='Admin', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    handling.place(x=100, y=5)

    # ------------------------------------Username 
    user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    Frame(frame, width=295, height=2, bg="black").place(x=25, y=107)

    # --------------------------------     Password
    Password = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    Password.place(x=30, y=150)
    Password.insert(0, 'Password')
    Frame(frame, width=295, height=2, bg="black").place(x=25, y=177)

    # -----------------------------------------Login Button
    login_button = Button(frame, width=39, pady=7, text='Login', bg='#57a1f8', fg='white', border=0, command=check_login)
    login_button.place(x=35, y=234)

    # Error label for incorrect login
    error_label = Label(frame, text="", fg="red", bg="white")
    error_label.place(x=35, y=270)

    rw.mainloop()


def create_rounded_button(parent, text, command=None):
    button = Button(parent, text=text, command=command, font=("Arial", 16, "bold"),
                    bg="#3498db", fg="white", activebackground="#2980b9", 
                    relief="flat", bd=0, width=15, height=2)
    return button

def welcome(): 
    rw = Tk()
    rw.geometry("925x500+300+200")
    rw.title("Welcome Window")
    rw.resizable(False, False)

    container = Frame(rw)
    container.pack(fill="both", expand=True)

    left_frame = Frame(container, width=462, height=500, bg="#3498db")
    left_frame.pack_propagate(False)
    left_frame.pack(side="left", fill="both")

    welcome_label = Label(left_frame, text="Welcome", font=("Helvetica", 40, "bold"), bg="#3498db", fg="white")
    welcome_label.place(relx=0.5, rely=0.5, anchor="center")

    right_frame = Frame(container, width=463, height=500, bg="#ecf0f1")
    right_frame.pack_propagate(False)
    right_frame.pack(side="right", fill="both")

    admin_button = create_rounded_button(right_frame, "Admin", command=lambda: Admin_page(rw))
    guest_button = create_rounded_button(right_frame, "Fans", command=guest_page)

    admin_button.place(relx=0.5, rely=0.4, anchor="center")
    guest_button.place(relx=0.5, rely=0.6, anchor="center")

    rw.mainloop()
    
def interpreter():
    

    try:
        # Use existing connection (conn)
        cursor = conn.cursor()

        # Query to fetch Hits per Team
        query = "SELECT Team_ID, SUM(Hits) AS total_hits FROM Game_Teams GROUP BY Team_ID"
        cursor.execute(query)

        # Fetch data
        teams = []
        hits = []

        for row in cursor.fetchall():
            teams.append(str(row[0]))  # Convert Team_ID to string for labeling
            hits.append(row[1])  # Total Hits

        cursor.close()  # Close cursor

        # Plot Hits Per Team
        plt.figure(figsize=(8, 5))
        plt.bar(teams, hits, color='skyblue')
        plt.xlabel("Team ID")
        plt.ylabel("Total Hits")
        plt.title("Total Hits Per Team")
        plt.xticks(rotation=45)
        plt.show()

    except Exception as e:
        print(f"Error: {e}")

welcome()



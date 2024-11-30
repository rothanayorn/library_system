# Importing all necessary modules
import sqlite3
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd

# Connecting to Database
connector = sqlite3.connect('library.db')
cursor = connector.cursor()

connector.execute(
    'CREATE TABLE IF NOT EXISTS Library (BK_NAME TEXT, BK_ID TEXT PRIMARY KEY NOT NULL, AUTHOR_NAME TEXT, BK_STATUS TEXT, CARD_ID TEXT)'
)


def issuer_card():
    Cid = sd.askstring('Issuer Card ID', 'What is the Issuer\'s Card ID?\t\t\t')

    if not Cid:
        mb.showerror('Error', 'Issuer ID cannot be empty.')
        return None
    return Cid


def display_records():
    tree.delete(*tree.get_children())
    curr = connector.execute('SELECT * FROM Library')
    data = curr.fetchall()
    for record in data:
        tree.insert('', END, values=record)


def clear_fields():
    bk_status.set('Available')
    for var in [bk_id, bk_name, author_name, card_id]:
        var.set('')
    bk_id_entry.config(state='normal')
    try:
        tree.selection_remove(tree.selection()[0])
    except IndexError:
        pass


def clear_and_display():
    clear_fields()
    display_records()


def view_record():
    if not tree.focus():
        mb.showerror('Error', 'Select a row to view its details.')
        return

    current_item_selected = tree.focus()
    values_in_selected_item = tree.item(current_item_selected)
    selection = values_in_selected_item['values']

    bk_name.set(selection[0])
    bk_id.set(selection[1])
    author_name.set(selection[2])
    bk_status.set(selection[3])
    card_id.set(selection[4])


def add_record():
    if bk_status.get() == 'Issued':
        card_id_value = issuer_card()
        if not card_id_value:
            return
        card_id.set(card_id_value)
    else:
        card_id.set('N/A')

    surety = mb.askyesno(
        'Confirmation',
        'Are you sure you want to add this record?\nNote: Book ID cannot be changed later.'
    )

    if surety:
        try:
            connector.execute(
                'INSERT INTO Library (BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID) VALUES (?, ?, ?, ?, ?)',
                (bk_name.get(), bk_id.get(), author_name.get(), bk_status.get(), card_id.get())
            )
            connector.commit()
            clear_and_display()
            mb.showinfo('Success', 'The new record was successfully added.')
        except sqlite3.IntegrityError:
            mb.showerror('Error', 'The Book ID is already in use. Please use a unique ID.')


def update_record():
    def update():
        if bk_status.get() == 'Issued':
            card_id_value = issuer_card()
            if not card_id_value:
                return
            card_id.set(card_id_value)
        else:
            card_id.set('N/A')

        try:
            cursor.execute(
                'UPDATE Library SET BK_NAME=?, BK_STATUS=?, AUTHOR_NAME=?, CARD_ID=? WHERE BK_ID=?',
                (bk_name.get(), bk_status.get(), author_name.get(), card_id.get(), bk_id.get())
            )
            connector.commit()
            clear_and_display()
            edit.destroy()
            bk_id_entry.config(state='normal')
            clear.config(state='normal')
            mb.showinfo('Success', 'Record updated successfully.')
        except sqlite3.Error as e:
            mb.showerror('Error', f'An error occurred: {e}')

    view_record()
    bk_id_entry.config(state='disabled')
    clear.config(state='disabled')

    edit = Button(left_frame, text='Update Record', font=btn_font, bg=btn_hlb_bg, width=20, command=update)
    edit.place(x=50, y=375)


def remove_record():
    if not tree.selection():
        mb.showerror('Error', 'Please select a record to delete.')
        return

    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]

    cursor.execute('DELETE FROM Library WHERE BK_ID=?', (selection[1],))
    connector.commit()

    tree.delete(current_item)
    mb.showinfo('Success', 'The selected record was successfully deleted.')
    clear_and_display()


def delete_inventory():
    if mb.askyesno('Confirmation', 'Are you sure you want to delete the entire inventory? This action cannot be undone.'):
        tree.delete(*tree.get_children())
        cursor.execute('DELETE FROM Library')
        connector.commit()
    else:
        return


def change_availability():
    if not tree.selection():
        mb.showerror('Error', 'Please select a book to change its availability.')
        return

    current_item = tree.focus()
    values = tree.item(current_item)
    BK_id = values['values'][1]
    BK_status = values["values"][3]

    if BK_status == 'Issued':
        surety = mb.askyesno('Confirmation', 'Has the book been returned?')
        if surety:
            cursor.execute('UPDATE Library SET BK_STATUS=?, CARD_ID=? WHERE BK_ID=?', ('Available', 'N/A', BK_id))
            connector.commit()
        else:
            return
    else:
        card_id_value = issuer_card()
        if card_id_value:
            cursor.execute('UPDATE Library SET BK_STATUS=?, CARD_ID=? WHERE BK_ID=?', ('Issued', card_id_value, BK_id))
            connector.commit()

    clear_and_display()


# Variables for Green Theme
lf_bg = '#A8E6A3'  # Light Green for Left Frame
rtf_bg = '#66CDAA'  # Medium Aquamarine for Right Top Frame
rbf_bg = '#3CB371'  # Medium Sea Green for Right Bottom Frame
btn_hlb_bg = '#32CD32'  # Lime Green for Buttons

lbl_font = ('Georgia', 13)
entry_font = ('Times New Roman', 12)
btn_font = ('Gill Sans MT', 13)

# Initializing the main GUI window
root = Tk()
root.title('Library Management System')
root.geometry('1010x530')
root.resizable(0, 0)

Label(root, text='LIBRARY MANAGEMENT SYSTEM', font=("Noto Sans CJK TC", 15, 'bold'), bg=btn_hlb_bg, fg='White').pack(side=TOP, fill=X)

# StringVars
bk_status = StringVar()
bk_name = StringVar()
bk_id = StringVar()
author_name = StringVar()
card_id = StringVar()

# Frames
left_frame = Frame(root, bg=lf_bg)
left_frame.place(x=0, y=30, relwidth=0.3, relheight=0.96)

RT_frame = Frame(root, bg=rtf_bg)
RT_frame.place(relx=0.3, y=30, relheight=0.2, relwidth=0.7)

RB_frame = Frame(root, bg=rbf_bg)
RB_frame.place(relx=0.3, rely=0.24, relheight=0.785, relwidth=0.7)

# Left Frame
Label(left_frame, text='Book Name', bg=lf_bg, font=lbl_font).place(x=98, y=25)
Entry(left_frame, width=25, font=entry_font, textvariable=bk_name).place(x=45, y=55)

Label(left_frame, text='Book ID', bg=lf_bg, font=lbl_font).place(x=110, y=105)
bk_id_entry = Entry(left_frame, width=25, font=entry_font, textvariable=bk_id)
bk_id_entry.place(x=45, y=135)

Label(left_frame, text='Author Name', bg=lf_bg, font=lbl_font).place(x=90, y=185)
Entry(left_frame, width=25, font=entry_font, textvariable=author_name).place(x=45, y=215)

Label(left_frame, text='Status of the Book', bg=lf_bg, font=lbl_font).place(x=75, y=265)
dd = OptionMenu(left_frame, bk_status, *['Available', 'Issued'])
dd.configure(font=entry_font, width=12)
dd.place(x=75, y=300)

submit = Button(left_frame, text='Add new record', font=btn_font, bg=btn_hlb_bg, width=20, command=add_record)
submit.place(x=50, y=375)

clear = Button(left_frame, text='Clear fields', font=btn_font, bg=btn_hlb_bg, width=20, command=clear_fields)
clear.place(x=50, y=435)

# Right Top Frame
Button(RT_frame, text='Delete book record', font=btn_font, bg=btn_hlb_bg, width=17, command=remove_record).place(x=8, y=30)
Button(RT_frame, text='Delete full inventory', font=btn_font, bg=btn_hlb_bg, width=17, command=delete_inventory).place(x=178, y=30)
Button(RT_frame, text='Update book details', font=btn_font, bg=btn_hlb_bg, width=17, command=update_record).place(x=348, y=30)
Button(RT_frame, text='Change Book Availability', font=btn_font, bg=btn_hlb_bg, width=19, command=change_availability).place(x=518, y=30)

# Right Bottom Frame
Label(RB_frame, text='BOOK INVENTORY', bg=rbf_bg, font=("Noto Sans CJK TC", 15, 'bold')).pack(side=TOP, fill=X)
tree = ttk.Treeview(RB_frame, columns=('Book Name', 'Book ID', 'Author Name', 'Status of Book', 'Card ID'))
tree['show'] = 'headings'
tree.heading('Book Name', text='Book Name', anchor='w')
tree.heading('Book ID', text='Book ID', anchor='w')
tree.heading('Author Name', text='Author Name', anchor='w')
tree.heading('Status of Book', text='Status of Book', anchor='w')
tree.heading('Card ID', text='Card ID', anchor='w')
tree.column('Book Name', anchor='w', width=250)
tree.column('Book ID', anchor='center', width=100)
tree.column('Author Name', anchor='w', width=200)
tree.column('Status of Book', anchor='center', width=150)
tree.column('Card ID', anchor='center', width=100)

tree.pack(fill=BOTH, expand=True)

# Displaying Records
display_records()

root.mainloop()

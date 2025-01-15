from os import curdir
from tkinter import*
from tkinter.font import BOLD
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
class categoryclass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1076x459+193+129")
        self.root.title("Inventory Management System | PROJECT ")
        self.root.config(bg="white")
        self.root.focus_force()
        #=====variables===========
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        #==================title===
        lbl_title=Label(self.root,text="Manage Product Category",font=("BELL MT",25),bg="purple",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=7.5,pady=15)
        lbl_name=Label(self.root,text="Enter Category Name",font=("BELL MT",25),bg="white").place(x=50,y=100)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("BELL MT",15),bg="lightyellow").place(x=50,y=170,width=300)

        btn_add=Button(self.root,text="ADD",command=self.add,font=("BELL MT",12),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("BELL MT",12),bg="red",fg="white",cursor="hand2").place(x=520,y=170,width=150,height=30)

         #===Category Details===

        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=90,width=380,height=300)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.category_table=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.category_table.xview)
        scrolly.config(command=self.category_table.yview)

        self.category_table.heading("cid",text="Category ID")
        self.category_table.heading("name",text="Name")
        self.category_table["show"]="headings"
        self.category_table.column("cid",width=90)
        self.category_table.column("name",width=90)
        self.category_table.pack(fill=BOTH,expand=1)
        self.category_table.bind("<ButtonRelease-1>",self.get_data)

        #===Images#=======
        self.im1=Image.open("images/cat.jpg")
        self.im1=self.im1.resize((600,200),Image.ANTIALIAS)
        self.im1=ImageTk.PhotoImage(self.im1)

        self.lbl_im1=Label(self.root,image=self.im1,bd=4,relief=RAISED)
        self.lbl_im1.place(x=50,y=220)

        self.show()
#===functions==================================
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        
        try:
          if self.var_name.get()=="":
            messagebox.showerror("Error","Category name should be required",parent=self.root)
          else:
            cur.execute("Select * from category where name=?",(self.var_name.get(),))
            row=cur.fetchone()
            if row!=None:
              messagebox.showerror("Error","Category already exist, try different",parent=self.root)
            else:
              cur.execute("Insert into category (name) values(?)",(  self.var_name.get(),))
              con.commit()
              messagebox.showinfo("Sucess","Category Added Successfully",parent=self.root)
              self.show()
        
        except Exception as ex:
          messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
      con=sqlite3.connect(database=r'ims.db')
      cur=con.cursor()
      try:
        cur.execute("select * from category")
        rows=cur.fetchall()
        self.category_table.delete(*self.category_table.get_children())
        for row in rows:
           self.category_table.insert('',END,values=row)

      
      except Exception as ex:
          messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
      f=self.category_table.focus()
      content=(self.category_table.item(f))
      row=content['values']
      #print(row)
      self.var_cat_id.set(row[0])
      self.var_name.set(row[1])
    
    def delete(self):
      con=sqlite3.connect(database=r'ims.db')
      cur=con.cursor()
      try:
          if self.var_cat_id.get()=="":
            messagebox.showerror("Error","please select category from list",parent=self.root)
          else:
            cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
            row=cur.fetchone()
            if row==None:
              messagebox.showerror("Error","please try again",parent=self.root)
            else:
               op=messagebox.askyesno("Confirm","Do you want to delete?",parent=self.root)
               if op==True:
                  cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                  con.commit()
                  messagebox.showinfo("Delete","category Deleted Successfully",parent=self.root)
                  self.show()
                  self.var_cat_id.set("")
                  self.var_name.set("")


      
      except Exception as ex:
          messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
      
       


if __name__=="__main__":
     root=Tk()
     obj=categoryclass(root)
     root.mainloop()   
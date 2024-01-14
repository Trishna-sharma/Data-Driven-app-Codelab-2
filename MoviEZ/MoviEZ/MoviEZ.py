import tkinter as tk
import requests
from PIL import Image, ImageTk
import io

api = '624b4a8fe48b3308b7c1ffdfdad2ab74'
tmdb = 'https://api.themoviedb.org/3'
   
root = tk.Tk()
root.iconbitmap('Vector.ico')
root.title("Moviez")
root.geometry("600x400")


result2 = None #variable initialized globally so can be used freely
image_label = None

def search_movies(entry, resultBox): #function to search the movies 
    user = entry.get()
    search_i = f'{tmdb}/search/movie'
    params = {
        'api_key': api,
        'query': user
    }

    response = requests.get(search_i, params=params)
    if response.status_code == 200:
        results= response.json().get('results', [])
        display(results, resultBox)
    else:
        resultBox.config(text="No results found")

def display(movies, resultBox):#function to display the searched result by the user 
    resultBox.config(state=tk.NORMAL)

    if movies:
        for i, movie in enumerate(movies[:15]):
          
            title = movie['title']
            resultBox.insert(tk.END, title + '\n', f"tag_{i}")
            resultBox.tag_configure(f"tag_{i}", foreground='white')
            resultBox.tag_bind(f"tag_{i}", "<Button-1>", lambda event, movie=movie: (show_poster(movie), movie_details(movie)))
            resultBox.insert(tk.END, '\n\n')

    else:
        resultBox.insert(tk.END, 'Oops! NOT FOUND\n')

    resultBox.config(state=tk.DISABLED) 
        

def clear_results(resultBox):  #To clear the previous result from the resultBox text widget
    resultBox.config(state=tk.NORMAL)
    resultBox.delete(1.0, tk.END)
    resultBox.config(state=tk.DISABLED)


def show_poster(movie): #function to successfully call up the poster image 
    
    global image_label

    result4 = tk.Text(root, font=("Arial", 12), fg='white')
    result4.place(relx=0.56, rely=0.46)
    
    if image_label is not None:
        
        image_label.destroy()

    
    id = movie['id']
    url = f"{tmdb}/movie/{id}"
    params = {
        'api_key':api,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        movie_info = response.json()
        posterurl = f"https://image.tmdb.org/t/p/w500/{movie_info['poster_path']}"
        response = requests.get(posterurl)

        if response.status_code == 200:
            with Image.open(io.BytesIO(response.content)) as img:
               
                img = img.resize((190, 260), Image.ANTIALIAS)
                poster = ImageTk.PhotoImage(img)

                imgposter = tk.Label(result4, image=poster)
                imgposter.image = poster  
                imgposter.pack()

        
    



def movie_details(movie): #function to call up the other informations from the API and to display them
    global result2

    if result2 is None:
     #to create the result2 when there is none
        result2 = tk.Text(root, font=("Arial", 12), fg='white', bg='#212121', width=45,height=20,highlightthickness=0, bd=0)
        result2.place(relx=0.70, rely=0.46)
        result2.lower()

        
    else:
        
        result2.config(state=tk.NORMAL)
        result2.delete(1.0, tk.END) #clear previous contents in result2

   
    id = movie['id']
    url = f"{tmdb}/movie/{id}"
    params = {
        'api_key': api,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        info = response.json()

       
        result2.insert( tk.END,f"{info['title']}\n", "title\n")  # To display the movie elements 
        result2.tag_configure("title", font=("Arial", 18, "bold"))
        result2.insert( tk.END,f"\nPlot: {info['overview']}\n","plot\n")
        result2.tag_configure("plot",font=("Arial",12))
        result2.insert( tk.END,f"\nRelease Year: {info['release_date'][:4]}\n")
        result2.insert(tk.END, f"\nLanguage: {info['original_language']}\n")
    else:
        result2.insert(tk.END, 'Oops!!NOT FOUND')
        


def exit(event): #function to enable esc key to decrease full screen
    if root.attributes('-fullscreen'):
        root.attributes('-fullscreen', False)

def instructions_window():  #to open the instruction window
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg='#212121')

    instruction = tk.Label(root, text="Thanks for downloading MoviEZ app !!\nInstructions:\n1. Search any movie name you want to in the search bar\n2. you can get all the details, click continue to proceed", font=("Helvetica", 16), bg='#212121',fg='white')
    instruction.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    continue_btn = tk.Button(root, text="Continue", command=third_window, font=("Helvetica", 14), bg='#912F4C', fg='white')
    continue_btn.place(relx=0.5, rely=0.6, anchor=tk.CENTER)




def third_window():     #to open a new window
    for widget in root.winfo_children(): #to destroy previous contents
        widget.destroy() 

    root.configure(bg='#212121')

    movietitle = tk.Label(root, text="MoVIEZ", font=("Helvetica", 30), bg="#212121", fg="white") #To display the movie title 
    movietitle.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    searchBox = tk.Frame(root, bg="#212121")  #the frame to keep all the search contents in it
    searchBox.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    refreshbtn = tk.Button(searchBox, font=( 18), bg='#212121', fg='#ffffff', text="🔁",bd=0, command=third_window)
    refreshbtn.grid(row=0, column=0)  #button to refresh and search again


    searchlabel = tk.Label(searchBox, text="Search a movie name or actor:", font=("Helvetica", 14), bg='#212121', fg='white') #label to search a movie
    searchlabel.grid(row=0, column=1) 

    entry = tk.Entry(searchBox, font=("Arial", 14), width=30) # to take an input
    entry.grid(row=0, column=2, padx=10)

    searchbtn = tk.Button(searchBox, text="⌕", command=lambda: [clear_results(resultBox), search_movies(entry, resultBox)], font=("Helvetica", 20), bg='#C45275', fg='white') #the search button
    searchbtn.grid(row=0, column=3)


    resultBox = tk.Text( font=("Helvetica", 12), fg='white', bg='#912F4C',width=50,height=20) #The result Display box
    resultBox.place(relx=0.2, rely=0.46)

    

    
root.attributes('-fullscreen', True)
root.bind('<Escape>', exit)

imgpath = "Untitled design 1.png"
image = tk.PhotoImage(file=imgpath)
start_img = tk.Label(root, image=image)
start_img.place(x=0, y=0, relwidth=1, relheight=1)

start_btn = tk.Button(root, text="Get started", command=instructions_window, bg="#3E8ACC", fg="white", font=("Helvetica", 18)) #button to move to the next window 
start_btn.pack(side=tk.BOTTOM, pady=40) 

app_title = tk.Label(root, text="MoVIEZ", font=("Helvetica", 22), bg="#E58B87", fg="white") #for the title
app_title.pack(side=tk.BOTTOM, pady=30)

root.configure(bg='#212121')

root.mainloop()

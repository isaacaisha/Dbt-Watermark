import io
from tkinter import *
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle

BACKGROUND_COLOR = 'black'


class WatermarkInterface:

    def __init__(self):
        self.window = Tk()
        self.window.title('WAT€RMARK')
        self.window.config(padx=19, pady=19, bg=BACKGROUND_COLOR)
        # self.window.geometry("1400x805")

        # Set the theme using ttkthemes
        self.style = ThemedStyle(self.window)
        self.style.set_theme('arc')  # You can choose a theme from the available ones

        self.logo_image = None
        self.logo_text = None

        self.canvas = Canvas(height=433, width=379, highlightbackground='#B4CDE6', bg='black')
        self.canvas.grid(column=1, row=2, pady=19)

        true_img = PhotoImage(file='static/images/true.png')

        # Store the chosen image as an attribute of the class
        self.chosen_image = None

        self.add_watermark_text_label = Label(fg='green', bg=BACKGROUND_COLOR, font=('Times', 27, 'italic'))
        self.add_watermark_text_label.config(text=f"Add Watermark Text\n👇🏿👇🏿👇🏿")
        self.add_watermark_text_label.grid(column=0, row=0)
        self.true_btn_text = Button(image=true_img, highlightbackground='#B4CDE6', highlightthickness=0,
                                    command=self.add_watermark_text)
        self.true_btn_text.grid(column=0, row=1)

        self.choose_img_label = Label(fg='yellow', bg=BACKGROUND_COLOR, font=('Times', 27, 'italic'))
        self.choose_img_label.config(text=f"Click to choose a picture\n👇🏿👇🏿👇🏿")
        self.choose_img_label.grid(column=1, row=0)
        self.true_btn_img = Button(image=true_img, highlightbackground='#B4CDE6', highlightthickness=0,
                                   command=self.choose_image)
        self.true_btn_img.grid(column=1, row=1)

        self.add_watermark_logo_label = Label(fg='red', bg=BACKGROUND_COLOR, font=('Times', 27, 'italic'))
        self.add_watermark_logo_label.config(text=f"Add Watermark Logo\n👇🏿👇🏿👇🏿")
        self.add_watermark_logo_label.grid(column=2, row=0)
        self.true_btn_logo = Button(image=true_img, highlightbackground='#B4CDE6', highlightthickness=0,
                                    command=self.add_watermark_logo)
        self.true_btn_logo.grid(column=2, row=1)

        self.save_btn = Button(text='Save ¡!¡', fg='green', highlightbackground=BACKGROUND_COLOR, command=self.save)
        self.save_btn.grid(column=2, row=2)

        self.be_good_label = Label(fg='#33FFD8', bg=BACKGROUND_COLOR, font=('Times', 27, 'bold'))
        self.be_good_label.config(text=f'be good,\ndoing good,\nby acting good ¡!¡')
        self.be_good_label.grid(column=0, row=2, padx=9)

        self.window.mainloop()

    def choose_image(self):
        self.canvas.delete("watermark")
        file_path = filedialog.askopenfilename(
            title='Choose an image file',
            filetypes=[('Image files', '*.png *.jpg *.jpeg *.gif *.bmp *.ico *.webp'),
                       ('All files', '*.*')]
        )
        if file_path:
            # Use PIL to open the image
            pil_image = Image.open(file_path)

            # Convert the PIL image to a PhotoImage
            self.chosen_image = ImageTk.PhotoImage(pil_image)

            # Place the PhotoImage on the canvas
            self.canvas.create_image(self.canvas.winfo_reqwidth() / 2,
                                     self.canvas.winfo_reqheight() / 2,
                                     anchor="center", image=self.chosen_image)

    def add_watermark_text(self):
        if self.chosen_image:
            # Remove any existing watermark from the canvas
            self.canvas.delete("watermark")

            # Get user input for the logo
            self.logo_text = simpledialog.askstring("Enter Watermark Text", "Enter the Watermark text:")

            # Place the watermark text at the right bottom corner of the chosen image
            text_x = self.canvas.winfo_reqwidth() - 10
            text_y = self.canvas.winfo_reqheight() - 10

            # Add the new watermark text
            self.canvas.create_text(text_x, text_y, anchor="se",
                                    text=self.logo_text, fill='#9633FF',
                                    font=('Arial', 19, 'bold'), tags="watermark")

    def add_watermark_logo(self):
        if self.chosen_image:
            # Ask the user to choose a logo image
            file_path = filedialog.askopenfilename(
                title='Choose a logo image',
                filetypes=[('Image files', '*.png *.jpg *.jpeg *.gif *.bmp *.ico *.webp'),
                           ('All files', '*.*')]
            )

            if file_path:
                # Use PIL to open the logo image
                pil_logo = Image.open(file_path)

                # Resize the logo image to a specific size (e.g., 100x100)
                logo_size = (37, 37)
                pil_logo = pil_logo.resize(logo_size)

                # Convert the PIL image to a PhotoImage
                self.logo_image = ImageTk.PhotoImage(pil_logo)

                # Place the logo image in the top left corner of the chosen image
                logo_x = 10
                logo_y = 10

                # Add the new watermark logo
                self.canvas.create_image(logo_x, logo_y, anchor="nw", image=self.logo_image, tags="watermark")

    def save(self):
        if self.chosen_image:
            # Convert the canvas content to an image with watermarks
            modified_image = Image.open(io.BytesIO(self.canvas.postscript(colormode='color').encode('utf-8')))
            # Convert to RGB mode if needed
            modified_image = modified_image.convert('RGB')

            # Ask the user to choose a save location
            file_path = filedialog.asksaveasfilename(
                defaultextension='.png',
                filetypes=[('PNG files', '*.png'), ('JPEG files', '*.jpg *.jpeg'), ('All files', '*.*')]
            )

            if file_path:
                # Save the modified image with watermarks as PNG with maximum quality
                modified_image.save(file_path, compress_level=0)


# Create an instance of the WatermarkInterface class and start the main loop
watermark = WatermarkInterface()

import requests
from PIL import Image
from io import BytesIO
import streamlit as st
import zipfile
import os

# 1. Fungsi untuk menghasilkan gambar menggunakan Stable Diffusion
def generate_image(prompt, api_key, endpoint='https://api.stablediffusionapi.com/v3/text2image', width=512, height=512):
    """
    Menghasilkan gambar berdasarkan prompt menggunakan API Stable Diffusion.
    :param prompt: Teks prompt untuk menghasilkan gambar.
    :param api_key: API key untuk Stable Diffusion.
    :param endpoint: Endpoint API (default menggunakan Stable Diffusion).
    :param width: Lebar gambar.
    :param height: Tinggi gambar.
    :return: Objek PIL gambar.
    """
    payload = {
        "key": api_key,
        "prompt": prompt,
        "width": width,
        "height": height
    }

    response = requests.post(endpoint, data=payload)
    if response.status_code == 200:
        image_data = response.json()
        image_url = image_data['image_url']
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))
        return image
    else:
        print("Error generating image:", response.status_code)
        return None


# 2. Fungsi untuk menambahkan watermark ke gambar
def add_watermark(image, watermark_path, position=(10, 10)):
    """
    Menambahkan watermark ke gambar yang diberikan.
    :param image: Objek gambar PIL yang akan diberi watermark.
    :param watermark_path: Path ke gambar watermark.
    :param position: Posisi watermark (default di pojok kiri atas).
    :return: Gambar dengan watermark.
    """
    # Membuka gambar watermark dan memastikan menggunakan mode RGBA untuk transparansi
    watermark = Image.open(watermark_path).convert("RGBA")
    
    # Ukuran watermark (opsional)
    watermark = watermark.resize((100, 100))
    
    # Menempelkan watermark ke gambar asli (dengan transparansi)
    image.paste(watermark, position, watermark)  # Posisi bisa disesuaikan
    
    return image


# 3. Fungsi untuk membuat file zip dari gambar dan kode
def create_zip_file(zip_filename='image_package.zip', files=None):
    """
    Membuat file zip berisi gambar yang dihasilkan dan watermark.
    :param zip_filename: Nama file zip.
    :param files: Daftar file yang akan dimasukkan ke dalam zip.
    """
    if files is None:
        files = ['generated_image.png', 'watermarked_image.png', 'app.py']  # Sesuaikan dengan file yang ada
    
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files:
            if os.path.exists(file):
                zipf.write(file)
            else:
                print(f"File {file} tidak ditemukan.")
    print(f"File zip telah dibuat: {zip_filename}")


# 4. Fungsi untuk menampilkan gambar menggunakan Streamlit
def display_image(image_path):
    """
    Menampilkan gambar pada aplikasi web menggunakan Streamlit.
    :param image_path: Path ke gambar yang akan ditampilkan.
    """
    st.title("Gambar yang Dihasilkan dan Diberi Watermark")
    st.image(image_path, caption="Tas/Suitcase dengan Watermark", use_column_width=True)


# Fungsi utama untuk menjalankan semua langkah
def main():
    # Konfigurasi
    api_key = "your_stable_diffusion_api_key"  # Ganti dengan API key Stable Diffusion Anda
    prompt = "A modern leather suitcase on a clean white background"
    watermark_path = "twibbon_logo.png"  # Ganti dengan path gambar watermark Anda
    
    # Menghasilkan gambar
    generated_image = generate_image(prompt, api_key)
    
    if generated_image:
        # Menyimpan gambar yang dihasilkan secara lokal
        generated_image.save('generated_image.png')

        # Menambahkan watermark ke gambar
        watermarked_image = add_watermark(generated_image, watermark_path)
        watermarked_image.save('watermarked_image.png')

        # Membuat file zip berisi gambar dan kode
        create_zip_file(zip_filename='image_package.zip', files=['generated_image.png', 'watermarked_image.png', 'app.py'])
        
        # Menampilkan gambar dengan Streamlit
        display_image('watermarked_image.png')  # Menampilkan gambar yang sudah di-watermark


if __name__ == "__main__":
    main()
